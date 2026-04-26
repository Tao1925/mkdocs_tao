# 防病毒误报研判最小化方案

## 一、方案目标

基于 [docs/proj/fbd_ai/plan.md](docs/proj/fbd_ai/plan.md) 的思路，先做一个最小可运行版本，只解决下面两件事。

1. 在本地离线环境中，用 CPU 跑一个通用小模型。
2. 写一个 Python 脚本，输入一条病毒告警日志，输出“更像误报还是更像真实威胁”的结果，并给出简短分析。

这个版本不追求完整平台化，也不追求高准确率，重点是先把最小闭环跑通。

---

## 二、最小化技术路线

最小方案采用下面这条路线。

- 本地模型引擎：Ollama
- 模型类型：通用中文小模型，建议 `Qwen2.5 3B Instruct` 的量化版本
- 运行方式：全程本机 CPU 推理
- 输入形式：一条 JSON 格式的病毒告警
- 输出形式：一条 JSON 格式的研判结果
- 研判逻辑：先做轻量规则判断，再调用本地小模型补充分析

这么设计的原因是。

- 符合离线要求，不依赖外部 API。
- 对 CPU 更友好，适合先做 PoC。
- 比纯大模型直推更稳，因为脚本带了规则兜底。

---

## 三、目录与脚本

本次最小实现的脚本在这里。

- [docs/proj/fbd_ai/script/analyze_av_alert.py](docs/proj/fbd_ai/script/analyze_av_alert.py)

这个脚本默认调用本机 `http://127.0.0.1:11434` 的 Ollama 服务，并默认使用模型 `qwen2.5:3b`。

如果本地模型暂时不可用，脚本会自动退回到规则模式，仍然给出一个保守的初步结果。

---

## 四、推荐的小模型选择

### 1. 默认建议

建议优先选择下面这个级别的模型。

- `Qwen2.5 3B Instruct` 量化版

理由很简单。

- 中文理解能力相对稳定。
- 参数规模不大，适合 CPU 跑最小 PoC。
- 用来做“简短分析 + 结构化输出”已经够用。

### 2. 如果 CPU 更弱

如果内网机器 CPU 较弱或者内存偏小，可以退一步改用。

- `Qwen2.5 1.5B Instruct` 量化版

此时只需要在运行脚本时改一下模型名即可。

---

## 五、输入输出格式

### 1. 输入格式

输入采用 JSON 文件。当前脚本至少要求下面几个字段。

- `detection_name`：病毒名或检测名
- `file_path`：告警文件路径
- `signed`：是否有数字签名，值为 `true` 或 `false`
- `behavior_flags`：行为标记数组，例如 `[]`、`["persistence"]`

建议同时补充下面这些字段，模型分析会更稳。

- `host`
- `engine_name`
- `file_hash`
- `signer`
- `parent_process`
- `prevalence`
- `distribution`
- `raw_log`

可以直接用下面这条命令生成示例输入。

```powershell
python docs/proj/fbd_ai/script/analyze_av_alert.py --show-example > sample_alert.json
```

生成后的示例内容大致如下。

```json
{
	"host": "pc-001",
	"engine_name": "ExampleAV",
	"detection_name": "Trojan.GenericKD",
	"file_path": "C:\\Program Files\\Vendor\\agent\\agent_updater.exe",
	"file_hash": "sha256:demo",
	"signed": true,
	"signer": "Microsoft Windows",
	"parent_process": "services.exe",
	"prevalence": "high",
	"distribution": "software_update",
	"behavior_flags": [],
	"raw_log": "ExampleAV detected Trojan.GenericKD in C:\\Program Files\\Vendor\\agent\\agent_updater.exe on host pc-001"
}
```

### 2. 输出格式

脚本输出 JSON，核心字段如下。

- `judgement`：`likely_false_positive`、`likely_true_positive`、`needs_review`
- `confidence`：0 到 1 之间的小数
- `analysis`：简短中文分析
- `key_evidence`：关键证据数组
- `recommended_action`：建议动作
- `rule_result`：规则层的原始结果

如果本地模型不可用，还会额外输出一个 `warning` 字段，提示当前结果来自规则回退。

---

## 六、实施步骤

### 步骤 1：在内网机器安装并启动 Ollama

最小方案默认使用 Ollama 作为本地推理引擎。

如果你的内网不能联网，建议采用“外网审批下载 + 离线介质导入”的方式，把 Ollama 安装包和模型文件导入内网。

安装完成后，先启动服务。

```powershell
ollama serve
```

如果本机已经注册成后台服务，也可以直接检查服务是否可用。

```powershell
ollama list
```

### 步骤 2：准备一个本地 CPU 小模型

推荐优先准备 `Qwen2.5 3B Instruct` 的量化版本。

因为内网环境通常不能直接在线拉取模型，所以这里推荐两种做法。

第一种，内网已经有现成模型。

- 直接使用已有模型名，例如 `qwen2.5:3b`

第二种，离线导入 GGUF 模型。

- 先把批准后的 GGUF 模型文件拷入内网
- 编写 `Modelfile`
- 使用 `ollama create` 生成本地模型

如果你已经有一个名字为 `qwen2.5:3b` 的本地模型，可以直接跳过这一步。

### 步骤 3：准备一条病毒告警输入

先生成示例文件。

```powershell
python docs/proj/fbd_ai/script/analyze_av_alert.py --show-example > sample_alert.json
```

然后根据你真实的病毒告警，把 `sample_alert.json` 里的字段替换掉。

最小 PoC 阶段，建议优先把下面这些字段填准确。

- 检测名
- 文件路径
- 是否签名
- 签名发布者
- 父进程
- 是否有持久化、外联、计划任务等行为标记

### 步骤 4：运行分析脚本

在仓库根目录执行。

```powershell
python docs/proj/fbd_ai/script/analyze_av_alert.py --input sample_alert.json --model qwen3.5:4b
```

如果你想先不接模型，只验证规则流程，可以执行。

```powershell
python docs/proj/fbd_ai/script/analyze_av_alert.py --input sample_alert.json --rule-only
```

如果你改用了更小的模型，比如 `qwen2.5:1.5b`，则命令如下。

```powershell
python docs/proj/fbd_ai/script/analyze_av_alert.py --input sample_alert.json --model qwen2.5:1.5b
```

### 步骤 5：查看结果

输出会是标准 JSON，例如。

```json
{
	"mode": "llm_plus_rules",
	"judgement": "likely_false_positive",
	"confidence": 0.78,
	"analysis": "该样本位于合法软件安装目录，且签名发布者可信，更像升级组件触发的误报。当前未见持久化或外联等高风险行为，但仍建议人工抽样复核一次。",
	"key_evidence": [
		"路径位于合法软件安装目录",
		"签名发布者可信",
		"未见高风险行为标记"
	],
	"recommended_action": "加入人工抽查队列，暂不执行主机隔离。",
	"rule_result": {
		"judgement": "likely_false_positive",
		"confidence": 0.75,
		"summary": "规则层面更像误报，但仍建议保留人工抽样复核。",
		"false_positive_signals": [
			"文件存在数字签名",
			"文件路径更像软件安装或升级目录"
		],
		"suspicious_signals": [],
		"need_human_review": true
	}
}
```

这里最关键的是 `judgement` 和 `analysis`。

- `likely_false_positive`：更像误报
- `likely_true_positive`：更像真实威胁
- `needs_review`：证据不足或信号冲突，建议人工复核

---

## 七、这个最小方案的边界

这个版本只是 PoC，不是生产方案。

它的边界主要有四点。

1. 没有接入真实工单系统、资产系统和历史案例库。
2. 规则还是通用启发式规则，不是你单位的专有规则。
3. 小模型只是做初步解释，不具备真正的安全专家能力。
4. 输出结果只能作为辅助判断，不能直接替代人工处置。

---

## 八、下一步建议

如果这个最小版本跑通，下一步建议按下面顺序扩展。

1. 固化你们单位常见误报模式，补进规则层。
2. 把真实历史告警整理成案例库，做本地检索增强。
3. 统一输入字段，沉淀一批高质量标注样本。
4. 再考虑用 LoRA 做轻量微调，而不是一开始就训大模型。
