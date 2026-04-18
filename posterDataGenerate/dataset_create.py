"""
create_dataset.py
-----------------
将多个路径下的海报（poster）和/或网页（web）数据整合为微调数据集 JSON 文件。

对外接口：
    create_dataset(poster_paths, web_paths, output_path)
        poster_paths : 海报数据根目录列表（可为 None, [], 或单个 str）
        web_paths    : 网页数据根目录列表（可为 None, [], 或单个 str）
        output_path  : 输出 JSON 文件路径（JSONL 格式）
"""

import json
import random
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Instruction 模板
# ─────────────────────────────────────────────────────────────────────────────

_INSTRUCTION = {
    "poster": """你是一个严格的 HTML 海报布局设计者，而不是内容生成器...""", # 此处省略了你原文中详细的 prompt 以保持代码简洁，实际使用请保留完整
    "web": """你是一个严格的网页布局设计者，而不是内容生成器...""",      # 此处同上
}

# 补充完整 Instruction（如需直接运行请确保内容完整）
_INSTRUCTION["poster"] = """你是一个严格的 HTML 海报布局设计者，而不是内容生成器。你的任务是将提供的 JSON 格式论文元数据设计为高分辨率学术海报（HTML/CSS 实现）。...（此处省略后续规则）"""
_INSTRUCTION["web"] = """你是一个严格的网页布局设计者，而不是内容生成器。你的任务是根据提供的 JSON 格式论文元数据设计为 基于HTML/CSS 的网页布局。...（此处省略后续规则）"""


# ─────────────────────────────────────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────────────────────────────────────

def _load_samples_from_dir(root: str, data_type: str) -> list[dict]:
    """
    遍历单个 root 下所有子文件夹构建样本。
    """
    root_p = Path(root)
    if not root_p.is_dir():
        print(f"  [WARN] 路径不存在或不是文件夹: {root}")
        return []

    instruction = _INSTRUCTION[data_type]
    samples = []

    for sub in sorted(root_p.iterdir()):
        if not sub.is_dir():
            continue

        json_files = list(sub.glob("*.json"))
        html_files = list(sub.glob("*.html"))

        if len(json_files) != 1 or len(html_files) != 1:
            continue

        try:
            with open(json_files[0], "r", encoding="utf-8") as f:
                json_content = json.load(f)
            with open(html_files[0], "r", encoding="utf-8") as f:
                html_content = f.read()
            
            samples.append({
                "instruction": instruction,
                "input":       json.dumps(json_content, ensure_ascii=False),
                "output":      html_content,
            })
        except Exception as e:
            print(f"  [SKIP] {sub.name}: 读取失败 — {e}")
            continue

    return samples


def _interleave(a: list, b: list) -> list:
    result = []
    for pair in zip(a, b):
        result.extend(pair)
    longer = a if len(a) > len(b) else b
    result.extend(longer[min(len(a), len(b)):])
    return result


# ─────────────────────────────────────────────────────────────────────────────
# 对外接口
# ─────────────────────────────────────────────────────────────────────────────

def create_dataset(poster_paths: list[str] | str | None,
                   web_paths: list[str] | str | None,
                   output_path: str) -> None:
    """
    构建微调数据集并保存为 JSONL 文件。
    """
    # 统一转换为列表处理
    if isinstance(poster_paths, str): poster_paths = [poster_paths]
    if isinstance(web_paths, str): web_paths = [web_paths]
    
    poster_paths = [p for p in (poster_paths or []) if p and p.strip()]
    web_paths = [p for p in (web_paths or []) if p and p.strip()]

    if not poster_paths and not web_paths:
        raise ValueError("poster_paths 和 web_paths 不能同时为空")

    # ── 加载数据 ──────────────────────────────────────────────────────────────
    poster_samples: list[dict] = []
    web_samples:    list[dict] = []

    if poster_paths:
        print(f"开始加载 Poster 数据，共 {len(poster_paths)} 个路径...")
        for path in poster_paths:
            poster_samples.extend(_load_samples_from_dir(path, "poster"))
        print(f"  -> [poster] 总计加载 {len(poster_samples)} 条样本")

    if web_paths:
        print(f"开始加载 Web 数据，共 {len(web_paths)} 个路径...")
        for path in web_paths:
            web_samples.extend(_load_samples_from_dir(path, "web"))
        print(f"  -> [web] 总计加载 {len(web_samples)} 条样本")

    # ── 组合数据 ──────────────────────────────────────────────────────────────
    if poster_samples and web_samples:
        random.shuffle(poster_samples)
        random.shuffle(web_samples)
        all_samples = _interleave(poster_samples, web_samples)
        print(f"  [merge] 混合后共 {len(all_samples)} 条，poster/web 交错排列")
    elif poster_samples:
        all_samples = poster_samples
        print(f"  [merge] 仅含有 poster 数据，共 {len(all_samples)} 条")
    else:
        all_samples = web_samples
        print(f"  [merge] 仅含有 web 数据，共 {len(all_samples)} 条")

    # ── 写出 JSONL ────────────────────────────────────────────────────────────
    output_p = Path(output_path)
    output_p.parent.mkdir(parents=True, exist_ok=True)

    with open(output_p, "w", encoding="utf-8") as f:
        for sample in all_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")

    print(f"\n✅ 数据集已保存: {output_path} (共 {len(all_samples)} 条)")


# ─────────────────────────────────────────────────────────────────────────────
# 示例用法
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # 示例：传入路径列表
    p_paths = [
        "../finetuneData/poster/batchData1_filtered",
        "../finetuneData/poster/batchData2_filtered",
        "../finetuneData/poster/batchData3_filtered"
    ]
    w_paths = [
        "../finetuneData/web/pair_data1",
        "../finetuneData/web/pair_data2_filtered"
    ]
    out = "../finetune/LLaMA-Factory/data/poster_data_filtered.jsonl"

    create_dataset(
        poster_paths=p_paths,
        web_paths=None,
        output_path=out
    )