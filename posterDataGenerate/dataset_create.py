"""
create_dataset.py
-----------------
将海报（poster）和/或网页（web）数据整合为微调数据集 JSON 文件。

对外接口：
    create_dataset(poster_path, web_path, output_path)
        poster_path : 海报数据根目录（可为 None 或空字符串）
        web_path    : 网页数据根目录（可为 None 或空字符串）
        output_path : 输出 JSON 文件路径（每行一条 JSON，即 JSONL 格式）
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


# ─────────────────────────────────────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────────────────────────────────────

def _load_samples_from_dir(root: str, data_type: str) -> list[dict]:
    """
    遍历 root 下所有子文件夹，每个子文件夹中：
      - 找到唯一的 .json 文件作为 input
      - 找到唯一的 .html 文件作为 output
    返回样本列表，每条样本为微调格式的 dict。

    data_type : "poster" 或 "web"，决定使用哪条 instruction。
    """
    root_p = Path(root)
    if not root_p.is_dir():
        raise ValueError(f"路径不存在或不是文件夹: {root}")

    instruction = _INSTRUCTION[data_type]
    samples = []

    for sub in sorted(root_p.iterdir()):
        if not sub.is_dir():
            continue

        # 找唯一 json 和 html
        json_files = list(sub.glob("*.json"))
        html_files = list(sub.glob("*.html"))

        if len(json_files) != 1:
            print(f"  [SKIP] {sub.name}: 找到 {len(json_files)} 个 JSON 文件，跳过")
            continue
        if len(html_files) != 1:
            print(f"  [SKIP] {sub.name}: 找到 {len(html_files)} 个 HTML 文件，跳过")
            continue

        json_path = json_files[0]
        html_path = html_files[0]

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                json_content = json.load(f)
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
        except Exception as e:
            print(f"  [SKIP] {sub.name}: 读取失败 — {e}")
            continue

        samples.append({
            "instruction": instruction,
            "input":       json.dumps(json_content, ensure_ascii=False),
            "output":      html_content,
        })

    print(f"  [{data_type}] 共加载 {len(samples)} 条样本，来源: {root}")
    return samples


def _interleave(a: list, b: list) -> list:
    """
    将两个列表交错合并，确保 a、b 的数据穿插出现。
    若长度不等，剩余部分追加在末尾。
    示例：[a1,a2,a3] + [b1,b2] → [a1,b1,a2,b2,a3]
    """
    result = []
    for pair in zip(a, b):
        result.extend(pair)
    longer = a if len(a) > len(b) else b
    result.extend(longer[min(len(a), len(b)):])
    return result


# ─────────────────────────────────────────────────────────────────────────────
# 对外接口
# ─────────────────────────────────────────────────────────────────────────────

def create_dataset(poster_path: str | None,
                   web_path: str | None,
                   output_path: str) -> None:
    """
    构建微调数据集并保存为 JSONL 文件（每行一条 JSON）。

    参数
    ----
    poster_path : 海报数据根目录，为空则不加载海报数据
    web_path    : 网页数据根目录，为空则不加载网页数据
    output_path : 输出 JSONL 文件路径
    """
    has_poster = bool(poster_path and poster_path.strip())
    has_web    = bool(web_path    and web_path.strip())

    if not has_poster and not has_web:
        raise ValueError("poster_path 和 web_path 不能同时为空")

    # ── 加载数据 ──────────────────────────────────────────────────────────────
    poster_samples: list[dict] = []
    web_samples:    list[dict] = []

    if has_poster:
        poster_samples = _load_samples_from_dir(poster_path, "poster")
    if has_web:
        web_samples = _load_samples_from_dir(web_path, "web")

    # ── 组合数据 ──────────────────────────────────────────────────────────────
    if has_poster and has_web:
        # 混合数据集：各自内部先打乱，再交错合并
        random.shuffle(poster_samples)
        random.shuffle(web_samples)
        all_samples = _interleave(poster_samples, web_samples)
        print(f"  [merge] 混合后共 {len(all_samples)} 条，poster/web 交错排列")
    elif has_poster:
        all_samples = poster_samples
        print(f"  [merge] 单一 poster 数据集，共 {len(all_samples)} 条，不打乱")
    else:
        all_samples = web_samples
        print(f"  [merge] 单一 web 数据集，共 {len(all_samples)} 条，不打乱")

    # ── 写出 JSONL ────────────────────────────────────────────────────────────
    output_p = Path(output_path)
    output_p.parent.mkdir(parents=True, exist_ok=True)

    with open(output_p, "w", encoding="utf-8") as f:
        for sample in all_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")

    print(f"\n✅  数据集已保存: {output_path}  ({len(all_samples)} 条)")


# ─────────────────────────────────────────────────────────────────────────────
# 命令行入口（可选）
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    # 用法: python create_dataset.py <poster_path|""> <web_path|""> <output.jsonl>
    poster_path="../finetuneData/poster/batchData3_filtered"
    web_path="../finetuneData/web/pair_data2_filtered"
    output_path="../finetune/LLaMA-Factory/data/mix_data_filtered.jsonl"
    create_dataset(
        poster_path,
        web_path=None,
        output_path=output_path
    )