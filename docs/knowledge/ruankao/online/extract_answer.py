from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError as exc:  # pragma: no cover - import guard for direct CLI usage
    raise SystemExit(
        "Missing dependency: beautifulsoup4. Install it with `pip install beautifulsoup4`."
    ) from exc


@dataclass(frozen=True)
class ExamQuestion:
    number: str
    question_type: str
    score_text: str
    question: str
    options: list[str]
    user_answer: str
    correct_answer: str
    result: str
    analysis: str


@dataclass(frozen=True)
class ExamSummary:
    score: str
    pass_status: str
    correct_count: str
    wrong_count: str
    accuracy: str
    duration: str


@dataclass(frozen=True)
class ParsedExam:
    title: str
    summary: ExamSummary
    questions: list[ExamQuestion]


def normalize_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def render_node(node: NavigableString | Tag) -> str:
    if isinstance(node, NavigableString):
        return str(node)
    if not isinstance(node, Tag):
        return ""

    name = node.name.lower()
    if name == "br":
        return "\n"
    if name == "img":
        source = (node.get("src") or "").strip()
        if not source:
            return ""
        alt = (node.get("alt") or node.get("title") or "image").strip() or "image"
        return f"\n![{alt}]({source})\n"

    parts = "".join(render_node(child) for child in node.children)
    if name in {"p", "div", "li"}:
        return parts + "\n"
    return parts


def extract_block(element: Tag | None) -> str:
    if not element:
        return ""
    return normalize_text("".join(render_node(child) for child in element.children))


def extract_text(element: Tag | None, default: str = "") -> str:
    if not element:
        return default
    return normalize_text(element.get_text(" ", strip=True)) or default


def parse_exam_html(html: str) -> ParsedExam:
    soup = BeautifulSoup(html, "html.parser")

    title = extract_text(soup.select_one("p.exam-header-title"), "答题记录")
    score = extract_text(soup.select_one("span.exam-result-score-num"))
    pass_status = extract_text(soup.select_one("span.exam-result-pass-status"))

    result_items = [
        extract_text(item.select_one(".exam-result-info-item-num"))
        + extract_text(item.select_one(".exam-result-info-item-unit"))
        for item in soup.select(".exam-result-info-item")
    ]
    correct_count, wrong_count, accuracy, duration = (result_items + [""] * 4)[:4]

    questions: list[ExamQuestion] = []
    for index, card in enumerate(soup.select("div.exam-item-card.select-none"), start=1):
        result_text = extract_text(card.select_one("div.exam-item-answer-result"), "未知")
        if "正确" in result_text:
            result = "正确"
        elif "错误" in result_text:
            result = "错误"
        else:
            result = result_text

        questions.append(
            ExamQuestion(
                number=extract_text(card.select_one("span.serial-number"), str(index)).rstrip("."),
                question_type=extract_text(card.select_one("span.card-title"), "题目"),
                score_text=extract_text(card.select_one("span.card-score")),
                question=extract_block(card.select_one("div.exam-item-title")),
                options=[extract_text(label) for label in card.select("div.el-radio-group > label")],
                user_answer=extract_text(card.select_one("div.exam-item-answer-user span"), "未作答"),
                correct_answer=extract_text(card.select_one("div.exam-item-answer-right span"), "未提取到"),
                result=result,
                analysis=extract_block(card.select_one("div.exam-item-analyze-content")) or "无",
            )
        )

    return ParsedExam(
        title=title,
        summary=ExamSummary(
            score=score,
            pass_status=pass_status,
            correct_count=correct_count,
            wrong_count=wrong_count,
            accuracy=accuracy,
            duration=duration,
        ),
        questions=questions,
    )


def render_markdown(parsed_exam: ParsedExam) -> str:
    lines = [f"# {parsed_exam.title}答题提取", ""]

    summary_lines = build_summary_lines(parsed_exam.summary)
    if summary_lines:
        lines.extend(summary_lines)
        lines.append("")

    for question in parsed_exam.questions:
        heading = f"## {question.number}. {question.question_type}"
        if question.score_text:
            heading += f"（{question.score_text}）"

        lines.extend(
            [
                heading,
                "",
                "题目：",
                question.question,
                "",
                "选项：",
            ]
        )
        lines.extend(f"- {option}" for option in question.options)
        lines.extend(
            [
                "",
                f"你的答案：{question.user_answer}",
                f"正确答案：{question.correct_answer}",
                f"结果：{question.result}",
                "",
                "解析：",
                question.analysis,
                "",
                "---",
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def build_summary_lines(summary: ExamSummary) -> list[str]:
    items: list[str] = []
    if summary.score:
        items.append(f"- 得分：{summary.score}分")
    if summary.pass_status:
        items.append(f"- 结果：{summary.pass_status}")
    if summary.correct_count:
        items.append(f"- 正确：{summary.correct_count}")
    if summary.wrong_count:
        items.append(f"- 错误：{summary.wrong_count}")
    if summary.accuracy:
        items.append(f"- 正确率：{summary.accuracy}")
    if summary.duration:
        items.append(f"- 用时：{summary.duration}")
    return items


def build_markdown(html: str) -> str:
    return render_markdown(parse_exam_html(html))


def convert_file(input_path: Path, output_path: Path) -> str:
    markdown = build_markdown(input_path.read_text(encoding="utf-8"))
    output_path.write_text(markdown, encoding="utf-8")
    return markdown


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract exam answers from 51CTO result HTML.")
    parser.add_argument(
        "input_html",
        nargs="?",
        default="index.html",
        help="Path to the source index.html file.",
    )
    parser.add_argument(
        "output_markdown",
        nargs="?",
        default="answer.md",
        help="Path to the generated answer.md file.",
    )
    return parser.parse_args(list(argv) if argv is not None else None)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    input_path = Path(args.input_html)
    output_path = Path(args.output_markdown)
    convert_file(input_path, output_path)
    print(f"Generated {output_path} from {input_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())