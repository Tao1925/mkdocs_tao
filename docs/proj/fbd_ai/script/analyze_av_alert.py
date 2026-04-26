#!/usr/bin/env python3
import argparse
import json
import sys
import textwrap
import time
import urllib.error
import urllib.request


DEFAULT_MODEL = "qwen3.5:4b"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.5
DEFAULT_HEALTH_TIMEOUT = 10
ALLOWED_JUDGEMENTS = {
    "likely_false_positive",
    "likely_true_positive",
    "needs_review",
}

TRUSTED_SIGNERS = {
    "microsoft",
    "vmware",
    "citrix",
    "huawei",
    "h3c",
    "sangfor",
    "360",
    "kingsoft",
    "tencent",
}

LOW_RISK_PATH_KEYWORDS = (
    "\\program files\\",
    "\\program files (x86)\\",
    "\\vendor\\",
    "\\update\\",
    "\\patch\\",
)

HIGH_RISK_PARENT_PROCESSES = {
    "powershell.exe",
    "cmd.exe",
    "wscript.exe",
    "cscript.exe",
    "mshta.exe",
    "rundll32.exe",
    "regsvr32.exe",
}

HIGH_RISK_BEHAVIORS = {
    "persistence",
    "lateral_movement",
    "network_beacon",
    "credential_access",
    "registry_autorun",
    "scheduled_task",
}

JSON_EXAMPLE = {
    "host": "pc-001",
    "engine_name": "ExampleAV",
    "detection_name": "Trojan.GenericKD",
    "file_path": "C:\\Program Files\\Vendor\\agent\\agent_updater.exe",
    "file_hash": "sha256:demo",
    "signed": True,
    "signer": "Microsoft Windows",
    "parent_process": "services.exe",
    "prevalence": "high",
    "distribution": "software_update",
    "behavior_flags": [],
    "raw_log": "ExampleAV detected Trojan.GenericKD in C:\\Program Files\\Vendor\\agent\\agent_updater.exe on host pc-001"
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze one antivirus alert with local CPU LLM and rule fallback."
    )
    parser.add_argument(
        "--input",
        help="Path to a JSON file describing one antivirus alert.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Local Ollama model name. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--ollama-url",
        default=OLLAMA_URL,
        help=f"Local Ollama generate API URL. Default: {OLLAMA_URL}",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=DEFAULT_MAX_RETRIES,
        help=f"Max retries for Ollama health check and generate requests. Default: {DEFAULT_MAX_RETRIES}",
    )
    parser.add_argument(
        "--retry-delay",
        type=float,
        default=DEFAULT_RETRY_DELAY,
        help=f"Base retry delay in seconds. Default: {DEFAULT_RETRY_DELAY}",
    )
    parser.add_argument(
        "--rule-only",
        action="store_true",
        help="Skip LLM and only use the built-in heuristic rules.",
    )
    parser.add_argument(
        "--show-example",
        action="store_true",
        help="Print the expected input JSON example and exit.",
    )
    return parser.parse_args()


def load_alert(path: str) -> dict:
    with open(path, "r", encoding="utf-8-sig") as handle:
        data = json.load(handle)

    required_fields = ["detection_name", "file_path", "signed", "behavior_flags"]
    missing = [field for field in required_fields if field not in data]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    return data


def normalize_text(value: str) -> str:
    return value.strip().lower() if isinstance(value, str) else ""


def configure_console_output() -> None:
    if sys.platform == "win32":
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleOutputCP(65001)
            kernel32.SetConsoleCP(65001)
        except Exception:
            pass

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except ValueError:
                pass


def write_json_output(payload: dict) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if hasattr(sys.stdout, "buffer"):
        sys.stdout.buffer.write(text.encode("utf-8", errors="replace"))
        sys.stdout.buffer.write(b"\n")
        sys.stdout.flush()
        return

    print(text)


def write_error(message: str) -> None:
    if hasattr(sys.stderr, "buffer"):
        sys.stderr.buffer.write((message + "\n").encode("utf-8", errors="replace"))
        sys.stderr.flush()
        return

    print(message, file=sys.stderr)


def sanitize_text(value: object, fallback: str = "") -> str:
    if value is None:
        candidate = ""
    elif isinstance(value, str):
        candidate = value
    else:
        candidate = json.dumps(value, ensure_ascii=False)

    candidate = candidate.replace("\x00", "")
    candidate = candidate.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not candidate:
        return fallback

    suspicious_markers = ("Ã", "Â", "Ð", "Ñ", "â", "€", "™")
    if any(marker in candidate for marker in suspicious_markers):
        try:
            repaired = candidate.encode("latin1").decode("utf-8")
            if repaired.count("�") <= candidate.count("�"):
                candidate = repaired
        except UnicodeError:
            pass

    latin_noise_count = sum(1 for char in candidate if 0x00A0 <= ord(char) <= 0x017F)
    if latin_noise_count >= 2:
        try:
            repaired = candidate.encode("latin1").decode("utf-8")
            if repaired.count("�") <= candidate.count("�"):
                candidate = repaired
        except UnicodeError:
            if fallback:
                return fallback

    lines = [line.strip() for line in candidate.splitlines() if line.strip()]
    candidate = "\n".join(lines).strip()
    return candidate or fallback


def build_ollama_tags_url(ollama_url: str) -> str:
    base_url = ollama_url.rsplit("/", 1)[0]
    return f"{base_url}/tags"


def request_json(url: str, payload: dict | None = None, timeout: int = 30) -> dict:
    request_data = None
    headers = {}
    method = "GET"
    if payload is not None:
        request_data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
        method = "POST"

    request = urllib.request.Request(
        url,
        data=request_data,
        headers=headers,
        method=method,
    )

    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def check_ollama_health(model: str, ollama_url: str) -> None:
    tags_url = build_ollama_tags_url(ollama_url)
    body = request_json(tags_url, timeout=DEFAULT_HEALTH_TIMEOUT)
    model_names = {
        item.get("name")
        for item in body.get("models", [])
        if isinstance(item, dict) and item.get("name")
    }
    if model not in model_names:
        raise ValueError(
            f"本地 Ollama 服务可达，但未找到模型 {model}。当前可用模型: {sorted(model_names)}"
        )


def evaluate_rules(alert: dict) -> dict:
    false_positive_signals = []
    suspicious_signals = []

    file_path = normalize_text(alert.get("file_path", ""))
    signer = normalize_text(alert.get("signer", ""))
    parent_process = normalize_text(alert.get("parent_process", ""))
    prevalence = normalize_text(alert.get("prevalence", "unknown"))
    distribution = normalize_text(alert.get("distribution", "unknown"))
    behavior_flags = {
        normalize_text(item) for item in alert.get("behavior_flags", []) if item
    }

    if alert.get("signed") is True:
        false_positive_signals.append("文件存在数字签名")
    else:
        suspicious_signals.append("文件缺少可信数字签名")

    if any(keyword in file_path for keyword in LOW_RISK_PATH_KEYWORDS):
        false_positive_signals.append("文件路径更像软件安装或升级目录")

    if any(vendor in signer for vendor in TRUSTED_SIGNERS):
        false_positive_signals.append("签名发布者命中常见可信厂商")

    if prevalence in {"high", "very_high"}:
        false_positive_signals.append("同类样本出现频率较高")
    elif prevalence in {"low", "rare"}:
        suspicious_signals.append("同类样本出现频率很低")

    if distribution in {"software_update", "patch", "sccm", "publish_platform"}:
        false_positive_signals.append("告警与软件分发或补丁发布场景一致")

    if parent_process in HIGH_RISK_PARENT_PROCESSES:
        suspicious_signals.append(f"父进程为高风险解释器或系统工具: {parent_process}")

    matched_behaviors = sorted(flag for flag in behavior_flags if flag in HIGH_RISK_BEHAVIORS)
    if matched_behaviors:
        suspicious_signals.append(
            "出现高风险行为标记: " + ", ".join(matched_behaviors)
        )

    if "\\users\\" in file_path or "\\temp\\" in file_path or "\\appdata\\" in file_path:
        suspicious_signals.append("文件位于用户目录、临时目录或 AppData 目录")

    fp_score = len(false_positive_signals)
    mal_score = len(suspicious_signals)
    gap = fp_score - mal_score

    if gap >= 2:
        judgement = "likely_false_positive"
        confidence = min(0.55 + gap * 0.1, 0.9)
        summary = "规则层面更像误报，但仍建议保留人工抽样复核。"
        need_human_review = confidence < 0.8
    elif gap <= -2:
        judgement = "likely_true_positive"
        confidence = min(0.55 + abs(gap) * 0.1, 0.9)
        summary = "规则层面存在较多可疑特征，建议按真实威胁优先处理。"
        need_human_review = True
    else:
        judgement = "needs_review"
        confidence = 0.5
        summary = "规则信号冲突或不足，需要模型补充分析或人工复核。"
        need_human_review = True

    return {
        "judgement": judgement,
        "confidence": round(confidence, 2),
        "summary": summary,
        "false_positive_signals": false_positive_signals,
        "suspicious_signals": suspicious_signals,
        "need_human_review": need_human_review,
    }


def build_prompt(alert: dict, rule_result: dict) -> str:
    compact_alert = {
        "host": alert.get("host"),
        "engine_name": alert.get("engine_name"),
        "detection_name": alert.get("detection_name"),
        "file_path": alert.get("file_path"),
        "file_hash": alert.get("file_hash"),
        "signed": alert.get("signed"),
        "signer": alert.get("signer"),
        "parent_process": alert.get("parent_process"),
        "prevalence": alert.get("prevalence"),
        "distribution": alert.get("distribution"),
        "behavior_flags": alert.get("behavior_flags"),
        "raw_log": alert.get("raw_log"),
    }

    prompt = f"""
你是一名内网防病毒告警分析助手。你的任务是根据一条病毒告警，判断它更像误报还是真实威胁。

请遵守以下原则：
1. 输出必须是一个 JSON 对象，不能输出任何额外文字。
2. judgement 只能取以下三个值之一：likely_false_positive、likely_true_positive、needs_review。
3. confidence 是 0 到 1 之间的小数。
4. analysis 必须是 2 到 4 句简短中文说明。
5. key_evidence 必须是 2 到 5 条中文短句数组。
6. recommended_action 必须是一句中文建议。
7. 在证据不足或规则冲突时，优先输出 needs_review。
8. 你必须参考规则层结果，但不能盲从；如果你推翻规则结果，必须在 analysis 中说明原因。

当前告警如下：
{json.dumps(compact_alert, ensure_ascii=False, indent=2)}

规则层结果如下：
{json.dumps(rule_result, ensure_ascii=False, indent=2)}

请只返回 JSON，例如：
{{
  "judgement": "likely_false_positive",
  "confidence": 0.78,
  "analysis": "该样本位于合法安装目录且有可信签名，更像升级组件触发的误报。当前未见持久化或外联等高风险行为，但仍建议抽查一次。",
  "key_evidence": [
    "路径位于合法软件安装目录",
    "文件存在可信签名",
    "未出现持久化行为"
  ],
  "recommended_action": "加入人工抽查队列，暂不执行隔离。"
}}
"""
    return textwrap.dedent(prompt).strip()


def parse_llm_json_text(raw_text: str) -> dict:
    candidate = sanitize_text(raw_text)
    if not candidate:
        raise ValueError("模型返回空内容")

    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if len(lines) >= 3:
            candidate = "\n".join(lines[1:-1]).strip()

    start = candidate.find("{")
    end = candidate.rfind("}")
    if start != -1 and end != -1 and start < end:
        candidate = candidate[start : end + 1]

    return json.loads(candidate)


def extract_llm_json(body: dict) -> dict:
    llm_json = None
    parse_errors = []

    for field_name in ("response", "thinking"):
        raw_text = body.get(field_name, "")
        if not isinstance(raw_text, str) or not raw_text.strip():
            continue
        try:
            llm_json = parse_llm_json_text(raw_text)
            break
        except (json.JSONDecodeError, ValueError) as exc:
            parse_errors.append(f"{field_name}: {exc}")

    if llm_json is None:
        response_length = len(body.get("response", "") or "")
        thinking_length = len(body.get("thinking", "") or "")
        details = "; ".join(parse_errors) if parse_errors else "未返回可解析 JSON"
        raise ValueError(
            "Ollama 返回内容无法解析为 JSON "
            f"(response_len={response_length}, thinking_len={thinking_length}): {details}"
        )

    return llm_json


def validate_llm_result(llm_json: dict) -> dict:
    if not isinstance(llm_json, dict):
        raise ValueError("模型返回的根对象不是 JSON 对象")

    judgement = sanitize_text(llm_json.get("judgement"), "needs_review")
    if judgement not in ALLOWED_JUDGEMENTS:
        judgement = "needs_review"

    try:
        confidence = float(llm_json.get("confidence", 0.5))
    except (TypeError, ValueError):
        confidence = 0.5
    confidence = round(min(max(confidence, 0.0), 1.0), 2)

    analysis = sanitize_text(
        llm_json.get("analysis"),
        "模型未返回有效分析，建议人工复核。",
    )

    raw_key_evidence = llm_json.get("key_evidence", [])
    if isinstance(raw_key_evidence, str):
        raw_key_evidence = [raw_key_evidence]
    elif not isinstance(raw_key_evidence, list):
        raw_key_evidence = []

    key_evidence = []
    for item in raw_key_evidence:
        evidence = sanitize_text(item)
        if evidence and evidence not in key_evidence:
            key_evidence.append(evidence)
        if len(key_evidence) >= 5:
            break
    if not key_evidence:
        key_evidence = ["模型未返回稳定证据，建议人工复核。"]

    recommended_action = sanitize_text(
        llm_json.get("recommended_action"),
        "建议转人工复核队列。",
    )

    return {
        "judgement": judgement,
        "confidence": confidence,
        "analysis": analysis,
        "key_evidence": key_evidence,
        "recommended_action": recommended_action,
    }


def call_ollama(
    alert: dict,
    rule_result: dict,
    model: str,
    ollama_url: str,
    max_retries: int,
    retry_delay: float,
) -> dict:
    payload = {
        "model": model,
        "prompt": build_prompt(alert, rule_result),
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.1,
            "num_ctx": 2048,
        },
    }

    attempt_errors = []
    total_attempts = max(1, max_retries)
    base_delay = max(0.0, retry_delay)

    for attempt in range(1, total_attempts + 1):
        try:
            check_ollama_health(model, ollama_url)
            body = request_json(ollama_url, payload=payload, timeout=120)
            llm_json = extract_llm_json(body)
            return validate_llm_result(llm_json)
        except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError, ValueError) as exc:
            attempt_errors.append(f"第{attempt}次尝试失败: {exc}")
            if attempt >= total_attempts:
                break
            if isinstance(exc, ValueError) and "未找到模型" in str(exc):
                break
            time.sleep(base_delay * attempt)

    raise ValueError("; ".join(attempt_errors))


def merge_results(rule_result: dict, llm_result: dict | None, mode: str) -> dict:
    if llm_result is None:
        return {
            "mode": mode,
            "judgement": rule_result["judgement"],
            "confidence": rule_result["confidence"],
            "analysis": rule_result["summary"],
            "key_evidence": rule_result["false_positive_signals"]
            + rule_result["suspicious_signals"],
            "recommended_action": "建议人工复核后再决定是否隔离或加入白名单。",
            "rule_result": rule_result,
        }

    return {
        "mode": mode,
        "judgement": llm_result["judgement"],
        "confidence": llm_result["confidence"],
        "analysis": llm_result["analysis"],
        "key_evidence": llm_result["key_evidence"],
        "recommended_action": llm_result["recommended_action"],
        "rule_result": rule_result,
    }


def main() -> int:
    configure_console_output()
    args = parse_args()

    if args.show_example:
        write_json_output(JSON_EXAMPLE)
        return 0

    if not args.input:
        write_error("[ERROR] --input is required unless --show-example is used.")
        return 1

    try:
        alert = load_alert(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        write_error(f"[ERROR] Failed to load input: {exc}")
        return 1

    rule_result = evaluate_rules(alert)

    if args.rule_only:
        output = merge_results(rule_result, None, mode="rule_only")
        write_json_output(output)
        return 0

    try:
        llm_result = call_ollama(
            alert,
            rule_result,
            args.model,
            args.ollama_url,
            args.max_retries,
            args.retry_delay,
        )
        output = merge_results(rule_result, llm_result, mode="llm_plus_rules")
    except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError, ValueError) as exc:
        output = merge_results(rule_result, None, mode="rule_fallback")
        output["warning"] = f"本地模型调用失败，已回退到规则模式: {exc}"

    write_json_output(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())