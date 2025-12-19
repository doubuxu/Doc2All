

def save_html(save_path:str,code:str):
    with open(save_path,'w',encoding='utf-8') as f:
        f.write(code)

def load_html(html_path):
    with open(html_path,'r',encoding='utf-8') as f:
        data=f.read()
    return data