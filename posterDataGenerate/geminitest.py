# 1. 安装依赖（仅需一次）
# pip install openai

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),  # 也可以直接写字符串
    base_url="https://openrouter.ai/api/v1"
)

resp = client.chat.completions.create(
    model="liquid/lfm-2.5-1.2b-thinking:free",  # 或任意你想试的 Gemini 模型
    messages=[{"role": "user", "content": "用中文介绍一下你自己"}],
    temperature=0.7
)

print(resp.choices[0].message.content)