import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from evaluation import eval_score


SCRIPT = Path(eval_score.__file__).resolve()


class EvalScoreTests(unittest.TestCase):
    """验证评测脚本的标题解析、路径处理和异常提示。"""

    def test_current_c_case_format(self):
        """当前 C1/C2 标题格式应被分别识别。"""
        content = "### C1 · 当前用例\n输入\n\n### C2 · 第二个用例\n输入\n"
        blocks = [
            block
            for block in eval_score.CASE_HEADING.split(content)
            if block.strip()
        ]

        self.assertEqual(len(blocks), 2)
        self.assertEqual(eval_score.score_case(blocks[0])[0], "C1 当前用例")
        self.assertEqual(eval_score.score_case(blocks[1])[0], "C2 第二个用例")

    def test_legacy_case_format(self):
        """旧版“## 用例 1：...”格式应继续兼容。"""
        content = "## 用例 1：旧版用例\n输入\n\n## 用例 2: 第二个旧版用例\n输入\n"
        blocks = [
            block
            for block in eval_score.CASE_HEADING.split(content)
            if block.strip()
        ]

        self.assertEqual(len(blocks), 2)
        self.assertEqual(eval_score.score_case(blocks[0])[0], "旧版用例")
        self.assertEqual(eval_score.score_case(blocks[1])[0], "第二个旧版用例")

    def test_default_path_works_from_another_directory(self):
        """从其他目录启动时，应自动读取脚本旁的 cases.md。"""
        with tempfile.TemporaryDirectory() as directory:
            environment = os.environ.copy()
            environment["PYTHONIOENCODING"] = "utf-8"
            result = subprocess.run(
                [sys.executable, str(SCRIPT)],
                cwd=directory,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=environment,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("C1", result.stdout)
        self.assertIn("C6", result.stdout)

    def test_empty_input_fails_with_actionable_message(self):
        """没有有效标题时，应返回失败并给出可操作的错误提示。"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.md"
            path.write_text("没有用例标题\n", encoding="utf-8")
            environment = os.environ.copy()
            environment["PYTHONIOENCODING"] = "utf-8"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=environment,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("未找到有效用例标题", result.stderr)


if __name__ == "__main__":
    unittest.main()
