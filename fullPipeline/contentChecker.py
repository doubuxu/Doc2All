from openai import OpenAI
from jinja2 import Environment
from jinja2 import Template
import json
from pathlib import Path
from utils.JsonTools import extract_llm_json,load_json,save_json
import os
#输入应该是md文件和plan


def ContentCheck_test(content_plan,raw_content_path,max_try):
    content_plan_check_prompt_template=Template(open('./prompts/contentPlanCheck.txt').read())
    raw_content=Path(raw_content_path).read_text(encoding='utf-8')
    content_plan_check_prompt=content_plan_check_prompt_template.render(contentPlan=content_plan,docContent=raw_content)

    times=0 
    is_pass=False
    while times<max_try and  not is_pass:
        client = OpenAI(
        api_key="sk-606d0363b5b84ae49603caa5a32e04ed",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"   # 若用中转/本地，可改
        )

        #test=Template(open('prompts/paper_content_plan.txt').read())

        response = client.chat.completions.create(
            model="qwen-long",
            messages=[{"role": "user", "content": content_plan_check_prompt}],
            stream=False,
            extra_body={"enable_thinking": False}
        )
        json_data=extract_llm_json(response.choices[0].message.content)
        save_json(json_data,'./test.json')
        is_pass=json_data["exact"]
        print(json_data["improvementSuggestions"])
        break

def content_check(prompt,save_path):
    api=os.getenv("API_KEY")
    url=os.getenv("BASE_URL")
    model_name=os.getenv("TEXT_GENERATION_MODEL","qwen3-max")
    client = OpenAI(
        api_key=api,
        base_url=url   # 若用中转/本地，可改
    )

        #test=Template(open('prompts/paper_content_plan.txt').read())
    response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            extra_body={"enable_thinking": False}
        )
    json_data=extract_llm_json(response.choices[0].message.content)
    save_json(json_data,save_path)
    return json_data,response
        

if __name__=="__main__":
    content_plan=load_json('../data/output/docsam/docsam_content_plan.json')
    #doc_content=Path('../data/output/docsam/docsam.md').read_text(encoding='utf-8')
    doc_path='../data/output/docsam/docsam.md'
    ContentCheck_test(content_plan,doc_path,1)


