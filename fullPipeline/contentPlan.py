from openai import OpenAI   # v1.x 新写法
from jinja2 import Environment
from jinja2 import Template
from pathlib import Path
import re
import json
from typing import Any, Dict, Union
"""
client = OpenAI(
    api_key="sk-606d0363b5b84ae49603caa5a32e04ed",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"   # 若用中转/本地，可改
)

#test=Template(open('prompts/paper_content_plan.txt').read())

response = client.chat.completions.create(
    model="qwen3-14b",
    messages=[{"role": "user", "content": "用一句话解释量子纠缠"}],
    stream=False,
    extra_body={"enable_thinking": False}
)

print(response.choices[0].message.content)
"""

def save_json(content:str,path):
    raw=content.strip()
    m = re.search(r'(?s)^```(?:json)?\s*\r?\n(.*?)```$', raw)
    if m:
        raw = m.group(1).strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError("agent 返回的不是合法 JSON") from e

    # 4. 落盘
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return file_path


def content_plan(prompt,path):
    client = OpenAI(
    api_key="sk-606d0363b5b84ae49603caa5a32e04ed",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"   # 若用中转/本地，可改
    )

    #test=Template(open('prompts/paper_content_plan.txt').read())

    response = client.chat.completions.create(
        model="qwen3-max",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        extra_body={"enable_thinking": False}
    )
    print(response.choices[0].message.content)
    save_json(response.choices[0].message.content,path)
    return response.choices[0].message.content



if __name__=="__main__":
    prompt=Template(open('prompts/paper_content_plan.txt').read())
    #prompt=Path('prompts/paper_content_plan.txt').read_text(encoding='utf-8')
    markdown_document=Path("../data/output2/demo1/demo1.md").read_text(encoding='utf-8')
    print(markdown_document)
    prompt=prompt.render(summary=markdown_document)
    path='../data/contentPlanTest/test.json'
    content_plan(prompt,path)