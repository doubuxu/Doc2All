from openai import OpenAI   # v1.x 新写法
from jinja2 import Environment
from jinja2 import Template
from pathlib import Path
import re
import json
from typing import Any, Dict, Union
from utils.JsonTools import load_json,save_json,extract_llm_json
from contentChecker import content_check
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
"""

def load_original_contentPlan_prompt(raw_content_dir,file_name):

    prompt_template=Template(open(Path('./prompts/content_plan.txt')).read())
    
    md_path=Path(raw_content_dir)/file_name/f"{file_name}.md"
    #images_dict_path=Path(raw_content_dir)/file_name/"dict"/"images.json"
    #tables_dict_path=Path(raw_content_dir)/file_name/"dict"/"tables.json"
    md_content=Path(md_path).read_text(encoding='utf-8')
    #images_dict=load_json(images_dict_path)
    #tables_dict=load_json(tables_dict_path)
    content_plan_prompt=prompt_template.render(document=md_content)
    return content_plan_prompt

def load_contentReplan_prompt(raw_content_dir,file_name,content_plan,suggestions):
    prompt_template=Template(open(Path('./prompts/Recontent_plan.txt')).read())
    md_path=Path(raw_content_dir)/file_name/f"{file_name}.md"
    #images_dict_path=Path(raw_content_dir)/file_name/"dict"/"images.json"
    #tables_dict_path=Path(raw_content_dir)/file_name/"dict"/"tables.json"
    md_content=Path(md_path).read_text(encoding='utf-8')
    #images_dict=load_json(images_dict_path)
    #tables_dict=load_json(tables_dict_path)
    prompt=prompt_template.render(document=md_content,originContentPLan=content_plan,improvementSuggestions=suggestions)
    return prompt



def load_content_check_prompt(raw_content_dir,file_name,contentPlan):
    prompt_template=Template(open(Path('./prompts/contentPlanCheck.txt')).read())
    md_path=Path(raw_content_dir)/file_name/f"{file_name}.md"
    #images_dict_path=Path(raw_content_dir)/file_name/"dict"/"images.json"
    #tables_dict_path=Path(raw_content_dir)/file_name/"dict"/"tables.json"
    md_content=Path(md_path).read_text(encoding='utf-8')
    #images_dict=load_json(images_dict_path)
    #tables_dict=load_json(tables_dict_path)
    prompt=prompt_template.render(contentPlan=contentPlan,docContent=md_content)
    return prompt  

def content_plan(prompt,path):
    client = OpenAI(
    api_key="sk-606d0363b5b84ae49603caa5a32e04ed",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"   # 若用中转/本地，可改
    )

    #test=Template(open('prompts/paper_content_plan.txt').read())

    response = client.chat.completions.create(
        model="qwen-plus-2025-12-01",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        extra_body={"enable_thinking": False}
    )
    json_data=extract_llm_json(response.choices[0].message.content)
    #print(response.choices[0].message.content)
    save_json(json_data,path)
    return json_data


def content_replan(prompt,save_path):
    client = OpenAI(
    api_key="sk-606d0363b5b84ae49603caa5a32e04ed",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"   # 若用中转/本地，可改
    )

    #test=Template(open('prompts/paper_content_plan.txt').read())

    response = client.chat.completions.create(
        model="qwen-plus-2025-12-01",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        extra_body={"enable_thinking": False}
    )
    json_data=extract_llm_json(response.choices[0].message.content)
    #print(response.choices[0].message.content)
    save_json(json_data,save_path)
    return json_data

def content_plan_with_check(raw_content_dir,file_name,save_path,max_try=3):
    #搭建提示词

    original_contentPlan_prompt=load_original_contentPlan_prompt(raw_content_dir,file_name)
    #content_replan_prompt=load_contentReplan_prompt()
    #content_plan_check_prompt=load_content_check_prompt()

    try_index=0
    is_pass=False
    while try_index<max_try and not is_pass:
        if try_index==0:#第一次内容规划
            contentPlanPath=Path(raw_content_dir)/file_name/"contentPlan"/f"contentPlan_{try_index+1}.json"
            contentPlan=content_plan(original_contentPlan_prompt,contentPlanPath)#生成规划内容
            content_plan_check_prompt=load_content_check_prompt(raw_content_dir,file_name,contentPlan)
            suggestions_path=Path(raw_content_dir)/file_name/"contentPlan"/f"suggestions_{try_index+1}.json"
            suggenstions=content_check(content_plan_check_prompt,suggestions_path)
            is_pass=suggenstions["exact"]#是否通过
        else:
            contentPlanPath=Path(raw_content_dir)/file_name/"contentPlan"/f"contentPlan_{try_index+1}.json"

            originalContentPlan=load_json(Path(raw_content_dir)/file_name/"contentPlan"/f"contentPlan_{try_index}.json")
            originalSuggenstions=load_json(Path(raw_content_dir)/file_name/"contentPlan"/f"suggestions_{try_index}.json")
            prompt=load_contentReplan_prompt(raw_content_dir,file_name,originalContentPlan,originalSuggenstions)

            contentPlan=content_replan(prompt,contentPlanPath)#生成规划内容

            content_plan_check_prompt=load_content_check_prompt(raw_content_dir,file_name,contentPlan)
            suggestions_path=Path(raw_content_dir)/file_name/"contentPlan"/f"suggestions_{try_index+1}.json"
            suggenstions=content_check(content_plan_check_prompt,suggestions_path)
            is_pass=suggenstions["exact"]#是否通过
    return contentPlan
    



if __name__=="__main__":
    """
    prompt=Template(open('prompts/paper_content_plan.txt').read())
    #prompt=Path('prompts/paper_content_plan.txt').read_text(encoding='utf-8')
    markdown_document=Path("../data/output2/demo1/demo1.md").read_text(encoding='utf-8')
    print(markdown_document)
    prompt=prompt.render(summary=markdown_document)
    path='../data/contentPlanTest/test.json'
    content_plan(prompt,path)
    """
    print(content_plan_with_check("../data/output","docsam","..",3))