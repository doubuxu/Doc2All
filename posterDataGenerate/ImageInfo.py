"""
enrich_content_plan.py
----------------------
补全 content_plan.json 中所有子图的尺寸信息（figure_width/height、table_width/height）
和语义描述（description），并将结果原地写回 JSON 文件。

图片路径直接来自 JSON 条目的 img_path 字段（如 "./fig_1.jpg"），
相对路径以 JSON 文件所在目录为基准解析为绝对路径，无需额外传入图片目录。

对外接口：
    enrich_content_plan(json_path) -> None
    enrich_content_plan2(json_path) -> None
        json_path : content_plan.json 的完整路径，处理后原地写回

环境变量：
    API_KEY      : 模型 API Key
    BASE_URL     : 模型 API Base URL
    VISUAL_MODEL : 视觉模型名称（默认 qwen-vl-max）

依赖：
    pip install openai pillow
"""

import os
import json
import base64
import copy
from pathlib import Path
from PIL import Image
from openai import OpenAI


# ─────────────────────────────────────────────────────────────────────────────
# 模型客户端（懒初始化，只初始化一次）
# ─────────────────────────────────────────────────────────────────────────────

_client: OpenAI | None = None
_model_name: str = ""


def _get_client() -> tuple[OpenAI, str]:
    global _client, _model_name
    if _client is None:
        api_key     = os.getenv("API_KEY", "")
        base_url    = os.getenv("BASE_URL", "")
        _model_name = os.getenv("SEMANTIC_MODEL", "qwen-vl-max")
        _client = OpenAI(api_key=api_key, base_url=base_url)
    return _client, _model_name


# ─────────────────────────────────────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────────────────────────────────────

def _resolve_img_path(img_path: str, json_dir: str) -> str:
    """
    将 JSON 中的 img_path 解析为绝对路径。
    - 已是绝对路径则直接返回
    - 相对路径（如 ./fig_1.jpg）以 JSON 文件所在目录为基准拼接
    """
    p = Path(img_path)
    if p.is_absolute():
        return str(p)
    return str(Path(json_dir) / p)


def _get_image_size(abs_path: str) -> tuple[int, int]:
    """返回 (width, height)，失败则返回 (0, 0)。"""
    try:
        with Image.open(abs_path) as img:
            return img.size
    except Exception as e:
        print(f"  [WARN] 无法读取尺寸 {abs_path}: {e}")
        return 0, 0


def _infer_media_type(abs_path: str) -> str:
    return {
        ".jpg":  "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png":  "image/png",
        ".gif":  "image/gif",
        ".webp": "image/webp",
    }.get(Path(abs_path).suffix.lower(), "image/jpeg")


def _describe_image(abs_path: str, context: str = "") -> str:
    """
    调用视觉大模型，返回图片的简洁语义描述（英文，一句话，≤30词）。
    context : 所属 section 标题，帮助模型理解图片用途。
    """
    client, model_name = _get_client()

    system_prompt = (
        "You are an assistant that writes concise, accurate descriptions for figures "
        "in academic posters. Respond with ONE sentence  in English, "
        "describing what the image shows."
    )

    user_text = (
        f"This image appears in a poster section titled: '{context}'. "
        "Describe what the image shows."
        if context else
        "Describe what this image shows."
        "if image content is an equation,use latex code to describe it"
    )

    with open(abs_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    media_type = _infer_media_type(abs_path)

    message = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{media_type};base64,{b64}"},
                },
                {"type": "text", "text": user_text},
            ],
        },
    ]

    resp = client.chat.completions.create(
        model=model_name,
        messages=message,
        temperature=0,
    )
    return resp.choices[0].message.content.strip()


# ─────────────────────────────────────────────────────────────────────────────
# 核心：补全单个条目
# ─────────────────────────────────────────────────────────────────────────────

def _enrich_entry(entry: dict, json_dir: str, context: str,
                  width_key: str, height_key: str) -> None:
    """
    原地修改单个 figure 或 table 条目：
      - img_path 字段直接给出图片路径，以 json_dir 为基准解析
      - width_key / height_key 为 0 时补全尺寸
      - description 为空时调用模型补全语义描述
    """
    img_path = entry.get("img_path", "")
    if not img_path:
        return

    abs_path = _resolve_img_path(img_path, json_dir)
    if not os.path.isfile(abs_path):
        print(f"  [SKIP] 文件不存在: {abs_path}")
        return

    label = entry.get("fig_id") or entry.get("table_id") or img_path

    # 补全尺寸
    if entry.get(width_key, 0) == 0 or entry.get(height_key, 0) == 0:
        w, h = _get_image_size(abs_path)
        entry[width_key]  = w
        entry[height_key] = h
        print(f"  [SIZE] {label}: {w}×{h}")

    # 补全描述
    desc = _describe_image(abs_path, context=context)
    entry["description"] = desc
    print(f"  [DESC] {label}: {desc}")


def _enrich_entry_size_only(entry: dict, json_dir: str,
                            width_key: str, height_key: str) -> None:
    """
    原地修改单个 figure 或 table 条目，仅补全尺寸信息：
      - 若本地找不到对应文件，直接跳过，不做任何操作。
      - width_key / height_key 为 0 时补全尺寸
      - 不修改 description 等其他字段
    """
    img_path = entry.get("img_path", "")
    if not img_path:
        return

    abs_path = _resolve_img_path(img_path, json_dir)
    
    # 【修改点】：如果文件不存在，直接 return，不修改 entry 中的任何字段（包括保留原本的 0）
    if not os.path.isfile(abs_path):
        print(f"  [SKIP] 文件不存在: {abs_path}")
        return

    label = entry.get("fig_id") or entry.get("table_id") or img_path

    if entry.get(width_key, 0) == 0 or entry.get(height_key, 0) == 0:
        w, h = _get_image_size(abs_path)
        entry[width_key] = w
        entry[height_key] = h
        print(f"  [SIZE] {label}: {w}×{h}")


# ─────────────────────────────────────────────────────────────────────────────
# 对外接口
# ─────────────────────────────────────────────────────────────────────────────

def enrich_content_plan(json_path: str) -> None:
    """
    补全 content_plan.json 中所有子图的尺寸与语义描述，原地写回。

    图片路径直接取自 JSON 条目的 img_path 字段，
    相对路径以 JSON 文件所在目录为基准解析。

    参数
    ----
    json_path : content_plan.json 的完整路径
    """
    json_dir = str(Path(json_path).parent)

    with open(json_path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    plan = copy.deepcopy(plan)

    # metadata 中的 logo 等图片
    poster_title = plan.get("metadata", {}).get("title", "")
    for entry in plan.get("metadata", {}).get("figures", []):
        _enrich_entry(entry, json_dir,
                      context=f"poster header — {poster_title}",
                      width_key="figure_width", height_key="figure_height")

    # 各 section 中的 figures 和 tables
    for section in plan.get("sections", []):
        sec_title = section.get("title", "")
        print(f"\n[SECTION] {section.get('id', '')} — {sec_title}")

        for entry in section.get("figures", []):
            _enrich_entry(entry, json_dir,
                          context=sec_title,
                          width_key="figure_width", height_key="figure_height")

        for entry in section.get("tables", []):
            _enrich_entry(entry, json_dir,
                          context=sec_title,
                          width_key="table_width", height_key="table_height")

    # 写回
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    print(f"\n✅  已写回: {json_path}")


def enrich_content_plan2(json_path: str) -> None:
    """
    仅补全 content_plan.json 中所有子图的尺寸信息，原地写回。
    遇到无法在本地找到对应文件的图片，不做任何操作，直接跳过。

    图片路径直接取自 JSON 条目的 img_path 字段，
    相对路径以 JSON 文件所在目录为基准解析。

    参数
    ----
    json_path : content_plan.json 的完整路径
    """
    json_dir = str(Path(json_path).parent)

    with open(json_path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    plan = copy.deepcopy(plan)

    for entry in plan.get("metadata", {}).get("figures", []):
        _enrich_entry_size_only(
            entry,
            json_dir,
            width_key="figure_width",
            height_key="figure_height",
        )

    for section in plan.get("sections", []):
        sec_title = section.get("title", "")
        print(f"\n[SECTION] {section.get('id', '')} — {sec_title}")

        for entry in section.get("figures", []):
            _enrich_entry_size_only(
                entry,
                json_dir,
                width_key="figure_width",
                height_key="figure_height",
            )

        for entry in section.get("tables", []):
            _enrich_entry_size_only(
                entry,
                json_dir,
                width_key="table_width",
                height_key="table_height",
            )

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    print(f"\n✅  已写回: {json_path}")


# ─────────────────────────────────────────────────────────────────────────────
# 命令行入口（可选）
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    load_dotenv()

    if len(sys.argv) < 2:
        print("用法: python enrich_content_plan.py <content_plan.json>")
        sys.exit(1)

    enrich_content_plan(json_path=sys.argv[1])
