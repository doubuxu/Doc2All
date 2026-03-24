import asyncio
from pathlib import Path

from html2image import SimpleRenderer,my_eval_task
from contentExtract import parse_html_to_content_plan
from CodeRightness import is_html_syntax_valid
from ImgPathCheck import calculate_image_path_ratio
from CSSCheck import is_css_valid
from VLMEvaluate import JudgeByVLM
class Evaluate:
    def __init__(self,target_path,file_name):
        self.target_path=target_path
        self.file_name=file_name
        #生成view_img
        self.html_path = Path(target_path)/f"{file_name}.html"
        self.view_img_path = Path(target_path)/"evaluate_view.png"
        asyncio.run(my_eval_task(self.html_path,self.view_img_path))

        #生成html提取内容
        self.content_extract_path = Path(target_path)/"htmlContentExtract.json"
        parse_html_to_content_plan(self.html_path,self.target_path)

        self.evaluate_aspect=["contentComplete","contentLogic","layoutRobustness","spaceEfficiency","visualFlow"]

    def evaluate(self):
        result=[]
        #objective指标计算
        codeRight = is_html_syntax_valid(self.html_path)
        result.append(codeRight)
        css_right = is_css_valid(self.html_path)
        result.append(css_right)
        path_rightness = calculate_image_path_ratio(self.html_path)
        result.append(path_rightness)
        #subjective指标计算
        for aspect in self.evaluate_aspect:
            evaluate_result = JudgeByVLM(self.target_path,self.file_name,aspect)
            result.append(evaluate_result)

        return result
    
if __name__=="__main__":
    evaluate = Evaluate("../data/output/20260323_154516_layoutTransformer_poster/","layoutTransformer")
    print(evaluate.evaluate())
