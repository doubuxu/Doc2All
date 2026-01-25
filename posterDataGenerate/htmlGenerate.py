# 1. 安装依赖（仅需一次）
# pip install openai

import os
from openai import OpenAI
import base64
"""
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

"""
def singele_poster_process(img_path)->str:

    def image_encode(img_path):
        with open(img_path, "rb") as f:
            img_data = f.read()
        encoded_str = base64.b64encode(img_data).decode("utf-8")
        return encoded_str
    
    b64=image_encode(img_path)
    messges=[
        {"role": "system", "content": "你是一个海报布局信息提取专家，能够根据海报内容生成海报的精准html代码表示。"},
        {"role": "user", "content":[
            {"type":"text","text":"请根据输入的学术海报生成一个html代码来表示这份海报的布局信息。要求：1.对于图中的文本和公式信息，要一字不差的在html中展示出来，并遵循原图中的换行。2.对于图片和表格，生成与原图对应图片或表格大小相同的矩形框来表示。3.要严格遵循原图的布局信息，例如原图中的若干张图片是横向排列，那html中就必须是横向排列。4.对于组图，要分别用小矩形框来表示子图，不能用一个大矩形框来表示，这样会造成布局信息的丢失。5.对于图片和表格的caption，一字不差的生成文本内容，并保持与图片或表格的相对位置。6.你只需要输出完整的html代码，不要输出任何多余的信息7. 不要遗漏任何文本、公式、图片或表格信息"},
            {
                "type":"image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{b64}"
                }
            }
        ]

        }
    ]
    resp = client.chat.completions.create(
        model="liquid/lfm-2.5-1.2b-thinking:free",  # 或任意你想试的 Gemini 模型
        messages=messges,
        temperature=0.7
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    img_path="../posterData/[Re] Graph Edit Networks_poster.jpg"
    html_code=singele_poster_process(img_path)
    print(html_code)