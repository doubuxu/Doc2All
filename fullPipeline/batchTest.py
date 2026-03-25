import os
import sys
import shutil
import datetime
import pandas as pd
from pathlib import Path

# 将当前文件所在文件夹的父文件夹加入系统变量
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pipeline import presentation_generate
from evaluate.evaluate import Evaluate
from logger import get_logger

def batch_test(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    batch_results = []
    pdf_files = list(input_dir.glob("*.pdf"))
    
    print(f"[INFO] 开始批量测试，共计 {len(pdf_files)} 个文件")

    for input_path in pdf_files:
        file_name = input_path.stem
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. 准备输出路径
        # 假设 presentation_generate 会在 output_dir 下创建一个以 file_name 命名的子文件夹
        log = get_logger(str(output_dir), file_name, __name__)
        mode = "poster"
        
        try:
            print(f"--- 正在处理: {file_name} ---")
            # 2. 调用生成逻辑
            presentation_generate(str(input_path), str(output_dir), mode, log)
            
            # 3. 移动并重命名结果文件夹以防止冲突
            # 假设原始生成路径是 output_dir / file_name
            original_gen_path = output_dir / file_name
            new_path = output_dir / f"{timestamp}_{file_name}_{mode}"
            
            if original_gen_path.exists():
                shutil.move(str(original_gen_path), str(new_path))
            else:
                print(f"[WARN] 未找到生成目录: {original_gen_path}")
                continue

            # 4. 执行评估
            eva = Evaluate(str(new_path), file_name)
            result = eva.evaluate()  # 预期格式: [bool, bool, float, json1, ..., json7]
            
            # 记录当前文件的信息，方便后续统计
            record = {
                "file_name": file_name,
                "html_valid": result[0],
                "css_valid": result[1],
                "img_path_acc": result[2],
                "json_scores": [j.get("分数", 0) if isinstance(j, dict) else 0 for j in result[3:]]
            }
            batch_results.append(record)
            
        except Exception as e:
            print(f"[ERROR] 处理 {file_name} 时崩溃: {e}")

    # ================== 统计与保存 ==================
    if not batch_results:
        print("没有成功处理任何文件。")
        return

    # 统计数据
    total = len(batch_results)
    avg_html = sum(1 for r in batch_results if r["html_valid"]) / total * 100
    avg_css = sum(1 for r in batch_results if r["css_valid"]) / total * 100
    avg_img = sum(r["img_path_acc"] for r in batch_results) / total
    
    # 七个 JSON 的平均分
    json_avg_scores = []
    for i in range(7):
        avg_score = sum(r["json_scores"][i] for r in batch_results) / total
        json_avg_scores.append(avg_score)

    # 写入报告
    report_path = output_dir / f"batch_test_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("================ BATCH TEST REPORT ================\n")
        f.write(f"测试时间: {datetime.datetime.now()}\n")
        f.write(f"样本总量: {total}\n\n")
        
        f.write("--- 汇总统计 (Summary) ---\n")
        f.write(f"HTML 语法正确率: {avg_html:.2f}%\n")
        f.write(f"CSS  语法正确率: {avg_css:.2f}%\n")
        f.write(f"图片路径平均准确率: {avg_img:.4f}\n")
        for i, score in enumerate(json_avg_scores, 1):
            f.write(f"JSON_{i} 平均得分: {score:.4f}\n")
        
        f.write("\n--- 详细记录 (Details) ---\n")
        f.write(f"{'FileName':<30} | {'HTML':<5} | {'CSS':<5} | {'ImgAcc':<7} | {'JSON_Scores'}\n")
        f.write("-" * 80 + "\n")
        for r in batch_results:
            scores_str = ", ".join([f"{s:.2f}" for s in r["json_scores"]])
            f.write(f"{r['file_name'][:30]:<30} | {str(r['html_valid']):<5} | {str(r['css_valid']):<5} | {r['img_path_acc']:.4f} | [{scores_str}]\n")

    print(f"[SUCCESS] 批量测试完成，报告已保存至: {report_path}")

# 使用示例
# batch_test("./test_pdfs", "./test_outputs")