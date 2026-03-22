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
    "poster": (
        "你是一个专业的前端工程师。请根据提供的 JSON 格式的论文元数据，"
        "生成一个采用 HTML/CSS 编写的高分辨率学术海报。"
        "并根据 JSON 内容正确渲染图片占位符。"
    ),
    "web": (
        "你是一个专业的前端工程师。请根据提供的 JSON 格式的论文元数据，"
        "生成一个采用 HTML/CSS 编写的高分辨率网页。"
        "并根据 JSON 内容正确渲染图片占位符。"
    ),
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
    poster_path="../pair_data3"
    web_path="../webData/pair_data2"
    output_path="../finetune/LLaMA-Factory/data/poster_data_original.jsonl"
    create_dataset(
        poster_path,
        None,
        output_path
    )