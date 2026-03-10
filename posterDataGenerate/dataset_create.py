import os
import json

def create_poster_dataset(json_dir, html_dir, output_file):
    dataset = []
    # 获取json文件夹下所有的文件名（不含后缀）
    json_files = {os.path.splitext(f)[0]: f for f in os.listdir(json_dir) if f.endswith('.json')}
    
    # 定义统一的任务指令
    instruction = (
        "你是一个专业的前端工程师。请根据提供的 JSON 格式的论文元数据，"
        "生成一个采用 HTML/CSS 编写的高分辨率学术海报。"
        "并根据 JSON 内容正确渲染图片占位符。"
    )

    matched_count = 0
    
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for file_id, json_name in json_files.items():
            html_name = f"{file_id[:-13]}.html"
            html_path = os.path.join(html_dir, html_name)
            json_path = os.path.join(json_dir, json_name)

            # 检查是否有对应的 HTML 文件
            if os.path.exists(html_path):
                # 读取 JSON 内容
                with open(json_path, 'r', encoding='utf-8') as f_json:
                    json_content = json.load(f_json)
                
                # 读取 HTML 内容
                with open(html_path, 'r', encoding='utf-8') as f_html:
                    html_content = f_html.read()

                # 构建训练数据条目
                data_entry = {
                    "instruction": instruction,
                    "input": json.dumps(json_content, ensure_ascii=False),
                    "output": html_content
                }

                # 写入一行 JSONL
                f_out.write(json.dumps(data_entry, ensure_ascii=False) + '\n')
                matched_count += 1
            else:
                print(f"Warning: 找不到对应的 HTML 文件: {html_name}")

    print(f"--- 转换完成 ---")
    print(f"成功匹配并写入: {matched_count} 条数据")
    print(f"输出文件路径: {output_file}")

# --- 使用示例 ---
if __name__ == "__main__":
    # 请根据你的实际路径修改以下三个变量
    JSON_FOLDER = "../poster_pair_data_2/json_data"
    HTML_FOLDER = "../poster_pair_data_2/html_data"
    OUTPUT_JSONL = "../poster_pair_data_2/train_dataset.jsonl"

    create_poster_dataset(JSON_FOLDER, HTML_FOLDER, OUTPUT_JSONL)