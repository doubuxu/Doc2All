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
    print(f"[INFO] Starting batch test with input: {input_dir} and output: {output_dir}")
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    batch_results = []
    pdf_files = list(input_dir.glob("*.pdf"))
    
    print(f"[INFO] 开始批量测试，共计 {len(pdf_files)} 个文件")

    # 定义评估维度名称
    evaluate_aspect = [
        "contentComplete", "contentLogic", "layoutRobustness", 
        "spaceEfficiency", "visualFlow", "visualHierarchy", "visualAlign"
    ]

    for input_path in pdf_files:
        file_name = input_path.stem
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. 准备输出路径
        log = get_logger(str(output_dir), file_name, __name__)
        mode = "poster"
        
        try:
            print(f"--- 正在处理: {file_name} ---")
            # 2. 调用生成逻辑
            presentation_generate(str(input_path), str(output_dir), mode, log)
            
            # 3. 移动并重命名结果文件夹以防止冲突
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
            
            # --- 核心修改：将分数与维度名称一一对应 ---
            vlm_scores_raw = result[3:]
            scores_map = {}
            for i, aspect in enumerate(evaluate_aspect):
                val = vlm_scores_raw[i]
                # 容错处理：提取字典中的"分数"字段，若非字典则取原值
                score = val.get("分数", 0) if isinstance(val, dict) else (val if isinstance(val, (int, float)) else 0)
                scores_map[aspect] = score

            # 记录当前文件的信息
            record = {
                "file_name": file_name,
                "html_valid": result[0],
                "css_valid": result[1],
                "img_path_acc": result[2],
                "scores": scores_map  # 存储字典格式方便后续按名称调用
            }
            batch_results.append(record)
            
        except Exception as e:
            print(f"[ERROR] 处理 {file_name} 时崩溃: {e}")

    # ================== 统计与保存 ==================
    if not batch_results:
        print("没有成功处理任何文件。")
        return

    total = len(batch_results)
    
    # 写入报告
    report_path = output_dir / f"batch_test_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("================ BATCH TEST REPORT ================\n")
        f.write(f"测试时间: {datetime.datetime.now()}\n")
        f.write(f"样本总量: {total}\n\n")
        
        f.write("--- 汇总统计 (Summary) ---\n")
        f.write(f"HTML 语法正确率: {sum(1 for r in batch_results if r['html_valid'])/total*100:.2f}%\n")
        f.write(f"CSS  语法正确率: {sum(1 for r in batch_results if r['css_valid'])/total*100:.2f}%\n")
        f.write(f"图片路径平均准确率: {sum(r['img_path_acc'] for r in batch_results)/total:.4f}\n")
        
        # --- 修改处：带名字的平均分统计 ---
        for aspect in evaluate_aspect:
            avg_score = sum(r["scores"][aspect] for r in batch_results) / total
            f.write(f"{aspect:<20} 平均得分: {avg_score:.4f}\n")
        
        f.write("\n--- 详细记录 (Details) ---\n")
        # 动态生成表头，包含所有指标名称
        aspect_headers = " | ".join([f"{asp[:10]:<10}" for asp in evaluate_aspect])
        header = f"{'FileName':<30} | {'HTML':<5} | {'CSS':<5} | {'ImgAcc':<7} | {aspect_headers}"
        f.write(header + "\n")
        f.write("-" * len(header) + "\n")
        
        for r in batch_results:
            # 动态生成每一行的分数数据
            scores_line = " | ".join([f"{r['scores'][asp]:<10.2f}" for asp in evaluate_aspect])
            f.write(f"{r['file_name'][:30]:<30} | {str(r['html_valid']):<5} | {str(r['css_valid']):<5} | {r['img_path_acc']:.4f} | {scores_line}\n")

    print(f"[SUCCESS] 批量测试完成，报告已保存至: {report_path}")

if __name__ == "__main__":
    # 使用示例
    batch_test("../data/testFiles", "../data/baselineModel_output2")