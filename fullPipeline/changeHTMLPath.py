import re

def changeHTML(html_code):
    def replace_path(match):
        quote = match.group(1)
        path = match.group(2)
        
        # 提取文件名
        filename = path.lstrip('./')
        
        if re.match(r'fig_\d+\.\w+', filename):
            new_path = f'./visuals/images/{filename}'
        elif re.match(r'table_\d+\.\w+', filename):
            new_path = f'./visuals/tables/{filename}'
        elif re.match(r'equations_\d+\.\w+', filename):
            new_path = f'./visuals/equations/{filename}'
        else:
            return match.group(0)  # 保持不变
        
        return f'src={quote}{new_path}{quote}'
    
    result = re.sub(r'src=(["\'])(\.\/[^"\']+)\1', replace_path, html_code)
    return result