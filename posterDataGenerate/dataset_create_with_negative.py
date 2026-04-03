"""
create_dataset.py
-----------------
将海报（poster）和/或网页（web）数据整合为微调数据集 JSON 文件（支持负样本纠错）。

新增功能：
1. 若存在 negative_poster.html，则自动生成纠错任务
2. 自动读取 negative_reason.txt 并注入 instruction
3. 最终数据集全局随机打乱

对外接口：
    create_dataset(poster_path, web_path, output_path)
"""

import json
import random
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# Instruction 模板
# ─────────────────────────────────────────────────────────────────────────────

_INSTRUCTION = {
    "poster": """
你是一个严格的 HTML 海报布局设计者，而不是内容生成器。

你的任务是将提供的 JSON 格式论文元数据设计为高分辨率学术海报（HTML/CSS 实现）。

这是一个“结构映射 + 布局规划任务”，而不是创作任务。你必须严格遵守以下所有规则：

【强约束规则】

1. 内容真实性（禁止捏造）
- 只能使用 JSON 中提供的信息。
- 严禁添加任何 JSON 中不存在的内容（包括：作者单位、额外说明、参考文献、图片等）。
- 如果 JSON 中没有提供某信息，则不得自行补充。

2. 结构一致性（禁止新增或修改结构）
- 海报中的 section 必须与 JSON 完全一致。
- section 的 id 和标题必须保持不变。
- 严禁新增或删除 section。

3. 图像与表格位置（严格绑定）
- 每个 figure/table 必须且只能出现一次。
- 必须放置在其所属的 section 中。
- 严禁跨 section 移动或重复使用。

4. 文本完整性（极其重要）
- 所有文本内容必须逐字从 JSON 拷贝。
- 严禁改写、总结或扩展文本内容。
- caption 必须与 JSON 完全一致。

5. 信息覆盖（禁止遗漏）
- JSON 中的所有元素必须完整出现在海报中。
- 不允许遗漏任何 figure、table 或段落。

6. 布局设计要求（海报特有）
- 使用 HTML/CSS 实现清晰的多栏布局（如 grid 或 flex）。
- 保证视觉层次清晰（标题、正文、图像分区明确）。
- 适用于高分辨率展示（避免内容重叠或排版混乱）。
- 但布局设计不能改变内容结构和归属关系。

7. HTML 合法性
- 生成完整且合法的 HTML 代码。
- 所有标签必须正确闭合。
- 严禁重复生成或出现死循环。

8. 图片渲染
- 必须使用 JSON 中提供的 img_path。
- 严禁伪造或修改路径。

【输出要求】

- 仅输出最终 HTML 代码。
- 不要输出解释。
- 所有内容必须严格对应 JSON，不得有任何新增或修改。""",

    "web": """
        你是一个严格的网页布局设计者，而不是内容生成器。

你的任务是根据提供的 JSON 格式论文元数据设计为 基于HTML/CSS 的网页布局。

这是一个“结构映射任务”，而不是创作任务。你必须严格遵守以下所有规则：

【强约束规则】

1. 内容真实性（禁止捏造）
- 只能使用 JSON 中提供的信息。
- 严禁添加任何 JSON 中不存在的内容（包括：作者单位、参考文献、额外章节、图片等）。
- 如果 JSON 中没有提供某信息，则不得自行补充。

2. 结构一致性（禁止新增或修改结构）
- HTML 中的 section 数量必须与 JSON 完全一致。
- 每个 section 的 id 和标题必须与 JSON 完全一致。
- 严禁新增 section（例如 section5、section6 等）。

3. 图像与表格位置（严格绑定）
- 每个 figure/table 必须且只能出现一次。
- 每个 figure/table 必须放在其所属的 section 中。
- 严禁跨 section 放置、重复或遗漏。

4. 文本完整性（极其重要）
- 所有文本内容（标题、段落、caption）必须逐字从 JSON 拷贝。
- 严禁改写、总结、扩写或缩写。
- 必须保持与 JSON 完全一致。

5. 信息覆盖（禁止遗漏）
- JSON 中的所有内容元素（section、段落、figure、table）必须全部出现在 HTML 中。
- 任何缺失都视为错误。

6. HTML 合法性
- 生成完整且合法的 HTML 代码。
- 所有标签必须正确闭合。
- 严禁重复生成内容或进入循环生成。

7. 图片渲染
- 必须使用 JSON 中提供的 img_path。
- 严禁伪造或修改图片路径。

【输出要求】

- 仅输出最终 HTML 代码。
- 不要输出解释或额外文本。
- HTML 必须严格对应 JSON 内容，不得有任何偏差。
    """,
}


# ✅ 新增：纠错 instruction 模板（支持错误注入）
def build_correction_instruction(reasons: list[str]) -> str:
    reason_text = "\n".join([f"- {r}" for r in reasons]) if reasons else "- 未知错误"

    return f"""
你是一个严格的 HTML 纠错与对齐专家。

你的任务是：
根据 JSON 数据修复输入的错误 HTML，使其完全正确。

该 HTML 存在以下问题：
{reason_text}

【任务要求】

1. 所有内容必须严格来自 JSON（禁止捏造）
2. 所有文本必须逐字一致（禁止改写）
3. 所有 figure/table：
   - 必须出现且仅出现一次
   - 必须位于正确的 section
4. 不允许新增或删除 section
5. 修复所有：
   - 内容缺失
   - 图像错位
   - 文本修改
   - 重复内容
6. 保证 HTML 结构完整、标签闭合
7. 尽量保留原有布局，仅修正错误

【输出要求】

- 仅输出修复后的 HTML
- 不要输出解释
"""


# ─────────────────────────────────────────────────────────────────────────────
# 工具函数（核心修改在这里）
# ─────────────────────────────────────────────────────────────────────────────

def _load_samples_from_dir(root: str, data_type: str) -> list[dict]:
    root_p = Path(root)
    if not root_p.is_dir():
        raise ValueError(f"路径不存在或不是文件夹: {root}")

    instruction = _INSTRUCTION[data_type]
    samples = []

    for sub in sorted(root_p.iterdir()):
        if not sub.is_dir():
            continue

        json_files = list(sub.glob("*.json"))
        html_files = list(sub.glob("*.html"))

        if len(json_files) != 1:
            print(f"[SKIP] {sub.name}: JSON 文件数量异常")
            continue
        if len(html_files) < 1:
            print(f"[SKIP] {sub.name}: 没有 HTML 文件")
            continue

        json_path = json_files[0]

        # 找正确 HTML
        html_path = None
        for f in html_files:
            if f.name in ["poster.html", "web.html"]:
                html_path = f
                break
        if html_path is None:
            html_path = html_files[0]

        negative_html_path = sub / "negative_poster.html"
        reason_path = sub / "negative_reason.txt"

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                json_content = json.load(f)

            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()

        except Exception as e:
            print(f"[SKIP] {sub.name}: 读取失败 {e}")
            continue

        # ───── 正样本（保持不变） ─────
        samples.append({
            "instruction": instruction,
            "input": json.dumps(json_content, ensure_ascii=False),
            "output": html_content,
        })

        # ───── 负样本纠错（新增） ─────
        if negative_html_path.exists():
            try:
                with open(negative_html_path, "r", encoding="utf-8") as f:
                    negative_html = f.read()

                # 读取错误原因
                reasons = []
                if reason_path.exists():
                    with open(reason_path, "r", encoding="utf-8") as f:
                        reasons = [line.strip() for line in f if line.strip()]

                correction_instruction = build_correction_instruction(reasons)

                correction_input = (
                    "【JSON】\n"
                    + json.dumps(json_content, ensure_ascii=False)
                    + "\n\n【错误HTML】\n"
                    + negative_html
                )

                samples.append({
                    "instruction": correction_instruction,
                    "input": correction_input,
                    "output": html_content,
                })

            except Exception as e:
                print(f"[WARN] {sub.name}: 负样本读取失败 {e}")

    print(f"[{data_type}] 加载 {len(samples)} 条（含纠错）")
    return samples


def _interleave(a: list, b: list) -> list:
    result = []
    for pair in zip(a, b):
        result.extend(pair)
    longer = a if len(a) > len(b) else b
    result.extend(longer[min(len(a), len(b)):])
    return result


# ─────────────────────────────────────────────────────────────────────────────
# 主函数（仅增加最后 shuffle）
# ─────────────────────────────────────────────────────────────────────────────

def create_dataset(poster_path: str | None,
                   web_path: str | None,
                   output_path: str) -> None:

    has_poster = bool(poster_path and poster_path.strip())
    has_web = bool(web_path and web_path.strip())

    if not has_poster and not has_web:
        raise ValueError("poster_path 和 web_path 不能同时为空")

    poster_samples = []
    web_samples = []

    if has_poster:
        poster_samples = _load_samples_from_dir(poster_path, "poster")
    if has_web:
        web_samples = _load_samples_from_dir(web_path, "web")

    if has_poster and has_web:
        random.shuffle(poster_samples)
        random.shuffle(web_samples)
        all_samples = _interleave(poster_samples, web_samples)
        print(f"[merge] 混合 {len(all_samples)} 条")
    elif has_poster:
        all_samples = poster_samples
    else:
        all_samples = web_samples

    # ✅ 新增：全局打乱
    random.shuffle(all_samples)

    # 保存
    output_p = Path(output_path)
    output_p.parent.mkdir(parents=True, exist_ok=True)

    with open(output_p, "w", encoding="utf-8") as f:
        for sample in all_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")

    print(f"\n✅ 数据集已保存: {output_path} ({len(all_samples)} 条)")


# ─────────────────────────────────────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    create_dataset(
        poster_path="../finetuneData/poster/batchData1",
        web_path="../finetuneData/web/pair_data2",
        output_path="../finetune/LLaMA-Factory/data/mix_data_with_neg_and_longPrompt.jsonl"
    )