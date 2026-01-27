import base64
from pathlib import Path

def imgEncoder(image_path:str, encoding: str = 'utf-8') -> str:
    ext = image_path.split('.')[-1].lower()
    mime_map = {'jpg': 'jpeg', 'jpeg': 'jpeg', 'png': 'png',
                'gif': 'gif', 'bmp': 'bmp', 'webp': 'webp'}
    mime = mime_map.get(ext, 'octet-stream')

    with open(image_path, 'rb') as f:
        binary_data = f.read()

    base64_data = base64.b64encode(binary_data).decode(encoding)
    return f'data:image/{mime};base64,{base64_data}'

if __name__=="__main__":
    code=imgEncoder('./fig_1.jpg')
    with open('./test.txt','w',encoding='utf-8') as f:
        f.write(code)