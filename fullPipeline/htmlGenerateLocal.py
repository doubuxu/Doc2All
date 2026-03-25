import os
import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import argparse
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from utils.JsonTools import load_json,save_json
from utils.htmlTools import load_html,save_html
# --- 1. 核心：全局缓存对象，确保模型只加载一次且在函数调用时才加载 ---
_MODEL_CACHE = {
    "model": None,
    "tokenizer": None
}

# 保持你原有的指令设计
_INSTRUCTIONS = {
    "poster": "你是一个专业的前端工程师。请根据提供的 JSON 格式的论文元数据，生成一个采用 HTML/CSS 编写的高分辨率学术海报。并根据 JSON 内容正确渲染图片占位符。",
    "web":    "你是一个专业的前端工程师。请根据提供的 JSON 格式的论文元数据，生成一个采用 HTML/CSS 编写的高分辨率网页。并根据 JSON 内容正确渲染图片占位符。",
}

def htmlGenerate(content_plan, data_type):
    """
    根据 content_plan（dict 或 str）和 data_type（'poster'/'web'）
    调用本地 Qwen2.5 模型生成 HTML 字符串。
    """
    
    # --- 2. 延迟加载逻辑：仅在第一次调用此函数时初始化模型 ---
    if _MODEL_CACHE["model"] is None:
        print("🚀 检测到首次生成任务，正在加载本地 Qwen2.5 模型...")
        
        # 强制指定显卡，确保与 MinerU 逻辑隔离（或在同一张卡顺序接力）
        os.environ["CUDA_VISIBLE_DEVICES"] = "0" 
        
        model_path = "../finetune/LLaMA-Factory/models/qwen2.5_7b_merged"
        
        #与微调前的baseline对比模型
        #model_path = "/home/huangyc/.cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots/a09a35458c702b33eeacc393d103063234e8bc28"
        # 加载分词器
        _MODEL_CACHE["tokenizer"] = AutoTokenizer.from_pretrained(
            model_path, 
            trust_remote_code=True
        )
        
        # 加载模型
        _MODEL_CACHE["model"] = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16, # 4090/4080 硬件特性支持
            device_map="auto",          # 自动平衡显存分配
            trust_remote_code=True
        )
        print("✅ 模型加载成功，开始生成 HTML。")

    # 获取缓存中的模型和分词器
    tokenizer = _MODEL_CACHE["tokenizer"]
    model = _MODEL_CACHE["model"]

    # --- 3. 保持原有的处理逻辑 ---
    instruction = _INSTRUCTIONS[data_type]

    # content_plan 统一转为 JSON 字符串作为用户输入
    if isinstance(content_plan, dict):
        content_str = json.dumps(content_plan, ensure_ascii=False, indent=2)
    else:
        content_str = str(content_plan)

    messages = [
        {"role": "system", "content": instruction},
        {"role": "user",   "content": content_str},
    ]

    # 使用 apply_chat_template 处理 Prompt 模板
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    # 准备模型输入并移动到模型所在设备
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    # 生成回答
    with torch.no_grad():  # 显式使用 no_grad 进一步节省生成时的显存开销
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=4096,
            do_sample=False,    # 保持你要求的确定性输出
        )

    # 4. 解码输出：只截取新生成的 token，去掉输入部分
    input_len = model_inputs["input_ids"].shape[1]
    new_ids = generated_ids[:, input_len:]
    response = tokenizer.decode(new_ids[0], skip_special_tokens=True)

    return response

if __name__=="__main__":
    content_plan_json_path="/data/huangyc/Document2All/data/output/20260322_173105_sceneGraph_web/contentPlan/final_content_plan.json"
    content_plan = load_json(content_plan_json_path)
    data_type="poster"
    html_code = htmlGenerate(content_plan,data_type)
    save_path="/data/huangyc/Document2All/data/output/20260322_173105_sceneGraph_web/web1.html"
    save_html(save_path,html_code)