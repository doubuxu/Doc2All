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
    "poster": """
你是一个严格的 HTML 海报布局设计者，而不是内容生成器。

你的任务是将提供的 JSON 格式论文元数据设计为高分辨率学术海报（HTML/CSS 实现）。

这是一个“结构映射 + 布局规划任务”，而不是创作任务。你必须严格遵守以下所有规则：

【强约束规则】

1. 内容真实性（禁止捏造）
- 只能使用 JSON 中提供的信息。
- 严禁添加任何 JSON 中不存在的内容（包括：作者单位、额外说明、参考文献、图片等）。
- 如果 JSON 中没有提供某信息，则不得自行补充。

2. 结构一致性（禁止新增或修改结构）
- 海报中的 section 必须与 JSON 完全一致。
- section 的 id 和标题必须保持不变。
- 严禁新增或删除 section。

3. 图像与表格位置（严格绑定）
- 每个 figure/table 必须且只能出现一次。
- 必须放置在其所属的 section 中。
- 严禁跨 section 移动或重复使用。

4. 文本完整性（极其重要）
- 所有文本内容必须逐字从 JSON 拷贝。
- 严禁改写、总结或扩展文本内容。
- caption 必须与 JSON 完全一致。

5. 信息覆盖（禁止遗漏）
- JSON 中的所有元素必须完整出现在海报中。
- 不允许遗漏任何 figure、table 或段落。

6. 布局设计要求（海报特有）
- 使用 HTML/CSS 实现清晰的多栏布局（如 grid 或 flex）。
- 保证视觉层次清晰（标题、正文、图像分区明确）。
- 适用于高分辨率展示（避免内容重叠或排版混乱）。
- 但布局设计不能改变内容结构和归属关系。

7. HTML 合法性
- 生成完整且合法的 HTML 代码。
- 所有标签必须正确闭合。
- 严禁重复生成或出现死循环。

8. 图片渲染
- 必须使用 JSON 中提供的 img_path。
- 严禁伪造或修改路径。

【输出要求】

- 仅输出最终 HTML 代码。
- 不要输出解释。
- 所有内容必须严格对应 JSON，不得有任何新增或修改。""",
    "web":"""
        你是一个严格的网页布局设计者，而不是内容生成器。

你的任务是根据提供的 JSON 格式论文元数据设计为 基于HTML/CSS 的网页布局。

这是一个“结构映射任务”，而不是创作任务。你必须严格遵守以下所有规则：

【强约束规则】

1. 内容真实性（禁止捏造）
- 只能使用 JSON 中提供的信息。
- 严禁添加任何 JSON 中不存在的内容（包括：作者单位、参考文献、额外章节、图片等）。
- 如果 JSON 中没有提供某信息，则不得自行补充。

2. 结构一致性（禁止新增或修改结构）
- HTML 中的 section 数量必须与 JSON 完全一致。
- 每个 section 的 id 和标题必须与 JSON 完全一致。
- 严禁新增 section（例如 section5、section6 等）。

3. 图像与表格位置（严格绑定）
- 每个 figure/table 必须且只能出现一次。
- 每个 figure/table 必须放在其所属的 section 中。
- 严禁跨 section 放置、重复或遗漏。

4. 文本完整性（极其重要）
- 所有文本内容（标题、段落、caption）必须逐字从 JSON 拷贝。
- 严禁改写、总结、扩写或缩写。
- 必须保持与 JSON 完全一致。

5. 信息覆盖（禁止遗漏）
- JSON 中的所有内容元素（section、段落、figure、table）必须全部出现在 HTML 中。
- 任何缺失都视为错误。

6. HTML 合法性
- 生成完整且合法的 HTML 代码。
- 所有标签必须正确闭合。
- 严禁重复生成内容或进入循环生成。

7. 图片渲染
- 必须使用 JSON 中提供的 img_path。
- 严禁伪造或修改图片路径。

【输出要求】

- 仅输出最终 HTML 代码。
- 不要输出解释或额外文本。
- HTML 必须严格对应 JSON 内容，不得有任何偏差。
    """    ,
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
        
        model_path = "../finetune/LLaMA-Factory/models/poster_data_filtered"
        #model_path = "../finetune/LLaMA-Factory/models/poster_data_compare"
        #model_path = "../finetune/LLaMA-Factory/models/web_data_compare"
        
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
            max_new_tokens=4096*2,
            do_sample=False,    # 保持你要求的确定性输出
        )

    # 4. 解码输出：只截取新生成的 token，去掉输入部分
    input_len = model_inputs["input_ids"].shape[1]
    new_ids = generated_ids[:, input_len:]
    response = tokenizer.decode(new_ids[0], skip_special_tokens=True)

    return response

BASELINE_INSTRUCTIONS = {
    "poster": 
    """你是一个专业的前端工程师。请根据提供的 JSON 格式的海报元数据，
    使用 HTML/CSS 代码编写来进行学术海报布局设计，并根据json信息正确渲染图片占位符。你的任务是基于输入的海报元数据进行布局规划，不得捏造或省略海报元数据中的信息。
    生成的HTML/CSS代码风格要求：
    1. **样式框架**: 必须使用 Tailwind CSS (通过 CDN 引入)。
    2. **数学公式**: 使用 MathJax 解析 LaTeX 公式，确保公式包含在 `$` (行内) 或 `$$` (块级) 中。
    3. **字体**: 默认使用 'Inter' 字体或无衬线字体。
    4. **整体设计**: 响应式设计，在大尺寸屏幕上呈现为多栏布局，在小尺寸屏幕上自动调整为单栏布局。
    5. **图片处理**: 图片占位符应使用 `<img>` 标签，`src` 属性指向 JSON 中的img_path，并添加适当的 `alt` 文本。
    6. **输出要求**: 仅输出以<!DOCTYPE html>开头的 HTML/CSS 代码，不要包含任何解释性文本或额外信息。确保生成的代码可以直接用于渲染海报，并且在视觉上具有专业水平的设计感和清晰的信息层次结构。
    """,

    "web":    """
    你是一个专业的前端工程师。请根据提供的 JSON 格式的海报元数据，
    使用 HTML/CSS 代码编写来进行学术网页布局设计，并根据json信息正确渲染图片占位符。你的任务是基于输入的海报元数据进行布局规划，不得捏造或省略海报元数据中的信息。
    生成的HTML/CSS代码风格要求：
    1. **样式框架**: 必须使用 Tailwind CSS (通过 CDN 引入)。
    2. **数学公式**: 使用 MathJax 解析 LaTeX 公式，确保公式包含在 `$` (行内) 或 `$$` (块级) 中。
    3. **字体**: 默认使用 'Inter' 字体或无衬线字体。
    4. **整体设计**: 响应式设计，整体布局适应不同屏幕尺寸，确保在桌面和移动设备上都具有良好的可读性和用户体验。
    5. **图片处理**: 图片占位符应使用 `<img>` 标签，`src` 属性指向 JSON 中的img_path，并添加适当的 `alt` 文本。
    6. **输出要求**: 仅输出以<!DOCTYPE html>开头的 HTML/CSS 代码，不要包含任何解释性文本或额外信息。确保生成的代码可以直接用于渲染海报，并且在视觉上具有专业水平的设计感和清晰的信息层次结构。
""",
}

def htmlGenerateBaseline(content_plan, data_type):
    """
    加载未微调的 Qwen2.5 原始模型生成 HTML 字符串，用于 Baseline 对比。
    """
    # 使用独立的缓存 Key，避免覆盖微调模型的实例
    if _MODEL_CACHE.get("baseline_model") is None:
        print("基础模型首次调用，正在加载原始 Qwen2.5 权重...")
        
        # 建议：如果显存足够，可以不设置 CUDA_VISIBLE_DEVICES，
        # 或者确保此处的逻辑不会导致显存溢出。
        # os.environ["CUDA_VISIBLE_DEVICES"] = "0" 

        # 这里的路径改为你本地存放原始 Qwen2.5-7B-Instruct 的路径
        baseline_path = "/home/huangyc/.cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots/a09a35458c702b33eeacc393d103063234e8bc28"

        _MODEL_CACHE["baseline_tokenizer"] = AutoTokenizer.from_pretrained(
            baseline_path, 
            trust_remote_code=True
        )
        
        _MODEL_CACHE["baseline_model"] = AutoModelForCausalLM.from_pretrained(
            baseline_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            trust_remote_code=True
        )
        print("✅ 原始模型（Baseline）加载成功。")

    # 获取缓存
    tokenizer = _MODEL_CACHE["baseline_tokenizer"]
    model = _MODEL_CACHE["baseline_model"]

    # --- 逻辑处理 ---
    # 使用你自定义的指令集（假设你已经定义了 _INSTRUCTIONS_BASELINE）
    # 或者沿用原有的 _INSTRUCTIONS
    instruction = BASELINE_INSTRUCTIONS[data_type] 

    if isinstance(content_plan, dict):
        content_str = json.dumps(content_plan, ensure_ascii=False, indent=2)
    else:
        content_str = str(content_plan)

    messages = [
        {"role": "system", "content": instruction},
        {"role": "user",   "content": content_str},
    ]

    # 构建 Prompt
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    # 推理
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    with torch.no_grad():
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=4096*2,
            do_sample=False, # 保持确定性，方便对比
        )

    # 截取新生成的 Token 并解码
    input_len = model_inputs["input_ids"].shape[1]
    response = tokenizer.decode(generated_ids[0][input_len:], skip_special_tokens=True)

    return response

if __name__=="__main__":
    content_plan_json_path="/data/huangyc/Document2All/data/output/20260322_173105_sceneGraph_web/contentPlan/final_content_plan.json"
    content_plan = load_json(content_plan_json_path)
    data_type="poster"
    html_code = htmlGenerate(content_plan,data_type)
    save_path="/data/huangyc/Document2All/data/output/20260322_173105_sceneGraph_web/web1.html"
    save_html(save_path,html_code)