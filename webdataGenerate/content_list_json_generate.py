import sys
import os
from pathlib import Path
father_path = os.path.dirname(os.path.abspath(__file__))
grandfather_path = os.path.dirname(father_path)
sys.path.append(grandfather_path)
sys.path.append(father_path)
from posterDataGenerate.mineru_batch import mineru_process
import json


if __name__ == "__main__":
    # 这里直接调用 mineru_process，传入 PDF 路径和输出目录
    pdf_path = "../webData/web_pdf_final"
    output_dir = "../webData/mineru_output"
    #input_pdf = "/mnt/data/2e0cf08b-f831-420b-8686-dd07866092d8.pdf"
    #output_dir = "./output_mineru"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for filename in os.listdir(pdf_path):
        if filename.lower().endswith(".pdf"):
            input_pdf = os.path.join(pdf_path, filename)
            mineru_process(input_pdf, output_dir)