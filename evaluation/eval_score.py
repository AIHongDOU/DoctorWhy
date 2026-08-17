"""DoctorWhy 纵向评测打分脚本。

读 evaluation/cases.md 的用例,人工(或 agent)逐条评测后,
把每个决策点的"是否问到"标记填入,本脚本算出分数。

用法:
  python eval_score.py               # 读取脚本旁的默认 cases.md
  python eval_score.py <score.md>    # 读取指定的评测结果文件

评分维度(每用例 0-5,共 3 维,总分 15):
  覆盖（coverage） = 问到的决策点 / 期望决策点
  收敛（converge） = 数据流清晰时是否及时停止（人工评）
  深度（depth）    = 是否引用暗规则、点破矛盾或触发红线（人工评）
"""
import re
import sys
from pathlib import Path

CASES = Path(__file__).with_name("cases.md")
CASE_HEADING = re.compile(
    r"(?m)^(?=###\s*C\d+\b|##\s*用例\s*\d+\s*[：:])"
)

def count_checked(text: str) -> tuple[int, int]:
    """统计 [x] 打勾数 / [ ] 未勾数。"""
    checked = len(re.findall(r"\[x\]", text))
    unchecked = len(re.findall(r"\[ \]", text))
    return checked, checked + unchecked

def score_case(text: str) -> tuple[str, float, float, float]:
    """提取用例标题,算三个维度分。"""
    title = re.search(r"^###\s*(C\d+)\s*[·:]\s*(.*)$", text, re.MULTILINE)
    if title:
        name = " ".join(title.groups()).strip()
    else:
        legacy_title = re.search(
            r"^##\s*用例\s*\d+\s*[：:]\s*(.*)$", text, re.MULTILINE
        )
        name = legacy_title.group(1).strip() if legacy_title else "?"
    checked, total = count_checked(text)
    coverage = round(checked / total * 5, 1) if total else 0.0
    # 收敛与深度无法自动判断,要求评测者在用例末尾标注 "收敛:x/5 深度:x/5"
    converge = float(re.search(r"收敛:(\d(?:\.\d)?)/5", text).group(1)) if re.search(r"收敛:(\d(?:\.\d)?)/5", text) else 0.0
    depth = float(re.search(r"深度:(\d(?:\.\d)?)/5", text).group(1)) if re.search(r"深度:(\d(?:\.\d)?)/5", text) else 0.0
    return name, coverage, converge, depth

def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else CASES
    with path.open(encoding="utf-8") as f:
        content = f.read()

    # 按当前 C1/C2... 标题或旧版“## 用例 1：...”标题分块。
    blocks = [
        block
        for block in CASE_HEADING.split(content)
        if re.search(r"(?m)^###\s*C\d+\b|^##\s*用例\s*\d+\s*[：:]", block)
    ]
    if not blocks:
        raise SystemExit(f"未找到有效用例标题: {path}")
    print(f"{'用例':<14}{'覆盖':>6}{'收敛':>6}{'深度':>6}{'总分':>6}")
    print("-" * 40)
    total = 0.0
    for b in blocks:
        name, cov, con, dep = score_case(b)
        s = cov + con + dep
        total += s
        print(f"{name[:12]:<14}{cov:>6}{con:>6}{dep:>6}{s:>6.1f}")
    n = len(blocks)
    print("-" * 40)
    print(f"平均总分 /15: {total / n:.1f}" if n else "无用例")

if __name__ == "__main__":
    main()
