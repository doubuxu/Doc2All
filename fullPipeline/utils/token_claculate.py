from openai import OpenAI
import os
from pathlib import Path
def token_calculate(response) -> int:
    
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens
    return [input_tokens, output_tokens, total_tokens]
        
def token_logger(response, output_path: str, file_name: str, stage_name:str):#根据response记录各个阶段的token使用情况，写入log文件
    tokens = token_calculate(response)
    log_path = Path(output_path) / file_name / "log" / "token_usage.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"{stage_name}: Input Tokens: {tokens[0]}, Output Tokens: {tokens[1]}, Total Tokens: {tokens[2]}\n")

def token_sum(output_path: str, file_name: str) -> int:#计算总的token使用情况
    log_path = Path(output_path) / file_name / "log" / "token_usage.log"
    inp_tot = out_tot = total_tot = 0

    for line in log_path.read_text(encoding="utf8").splitlines():
        # 每行格式：xxx: Input Tokens: 123, Output Tokens: 45, Total Tokens: 168
        parts = line.split(",")        # 3 段
        inp_tot  += int(parts[0].split(":")[-1])
        out_tot  += int(parts[1].split(":")[-1])
        total_tot+= int(parts[2].split(":")[-1])
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"Total: Input Tokens: {inp_tot}, Output Tokens: {out_tot}, Total Tokens: {total_tot}\n")