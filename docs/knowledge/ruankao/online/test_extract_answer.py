from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import extract_answer


class ExtractAnswerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.index_path = CURRENT_DIR / "index.html"
        cls.answer_path = CURRENT_DIR / "answer.md"
        cls.index_html = cls.index_path.read_text(encoding="utf-8")
        cls.expected_markdown = cls.answer_path.read_text(encoding="utf-8")

    def test_parse_exam_html_extracts_expected_counts(self) -> None:
        parsed = extract_answer.parse_exam_html(self.index_html)
        self.assertEqual(parsed.title, "2025年5月信息系统项目管理师选择题（第2批次回忆版）")
        self.assertEqual(len(parsed.questions), 75)
        self.assertEqual(parsed.summary.score, "45")
        self.assertEqual(parsed.summary.correct_count, "45道")
        self.assertEqual(parsed.summary.wrong_count, "30道")

    def test_build_markdown_matches_current_answer_md(self) -> None:
        generated = extract_answer.build_markdown(self.index_html)
        self.assertEqual(generated, self.expected_markdown)

    def test_convert_file_cli_writes_expected_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "generated_answer.md"
            exit_code = extract_answer.main([str(self.index_path), str(output_path)])
            self.assertEqual(exit_code, 0)
            self.assertTrue(output_path.exists())
            self.assertEqual(output_path.read_text(encoding="utf-8"), self.expected_markdown)


if __name__ == "__main__":
    unittest.main()