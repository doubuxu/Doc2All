import json
from pathlib import Path
import re
def save_json(data,path):

    with open(path,'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

def load_json(path):
    with open(path,'r',encoding='utf-8') as f:
        data=json.load(f)
    return data

def extract_llm_json(content:str):
    raw=content.strip()
    m = re.search(r'(?s)^```(?:json)?\s*\r?\n(.*?)```$', raw)
    if m:
        raw = m.group(1).strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError("agent 返回的不是合法 JSON") from e


    return data
