import os
import json
import base64
import re
import dotenv
from openai import OpenAI
from jinja2 import Template

dotenv.load_dotenv()

def JudgeByVLM(target_path, file_name, evaluate_aspect):
    # ── 1. 加载提示词模板 ──────────────────────────────────────────
    prompt_path = f"./prompts/{evaluate_aspect}.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # ── 2. 按角度选择性加载文本文件并渲染占位符 ───────────────────
    template_vars = {}

    if evaluate_aspect == "contentComplete":
        # 加载 md
        md_path = os.path.join(target_path, f"{file_name}.md")
        with open(md_path, "r", encoding="utf-8") as f:
            template_vars["original_document_text"] = f.read()
        # 加载 json
        html_path = os.path.join(target_path, f"{file_name}.html")
        with open(html_path, "r", encoding="utf-8") as f:
            template_vars["html_code"] = f.read()

    elif evaluate_aspect == "contentLogic":
        # 加载 json
        html_path = os.path.join(target_path, f"{file_name}.html")
        with open(html_path, "r", encoding="utf-8") as f:
            template_vars["html_code"] = f.read()

    # 其余三种角度不需要文本文件，template_vars 保持空字典

    # 用 Jinja2 渲染提示词
    rendered_prompt = Template(prompt_template).render(**template_vars)

    # ── 3. 加载图片并 base64 编码 ─────────────────────────────────
    img_path = os.path.join(target_path, "evaluate_view.png")
    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    # ── 4. 构建完整 message ────────────────────────────────────────
    message = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": rendered_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{img_b64}",
                        "detail": "high"   # 尽可能高分辨率
                    }
                }
            ]
        }
    ]

    # ── 5. 调用 VLM ────────────────────────────────────────────────
    api        = os.getenv("API_KEY")
    url        = os.getenv("BASE_URL")
    model_name = os.getenv("VISUAL_MODEL", "qwen3-max")

    client = OpenAI(api_key=api, base_url=url)
    resp = client.chat.completions.create(
        model=model_name,
        messages=message,
        temperature=0
    )

    # ── 6. 解析并返回 JSON ─────────────────────────────────────────
    raw = resp.choices[0].message.content.strip()

    # 兼容模型可能在 json 外包裹 markdown 代码块的情况
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

    return json.loads(raw)