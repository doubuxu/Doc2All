import requests
import os
from urllib.parse import urlparse
def download_logo_simple(logo_url: str, name: str, output_dir: str = "logos"):
    """简单下载Logo"""
    if not logo_url:
        print(f"  ✗ {name}: 没有Logo URL")
        return None
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        response = requests.get(logo_url, timeout=10)
        if response.status_code == 200:
            # 确定扩展名
            parsed = urlparse(logo_url)
            ext = parsed.path.split('.')[-1].split('?')[0]
            if ext not in ['png', 'jpg', 'jpeg', 'svg', 'webp']:
                ext = 'png'
            
            # 清理文件名
            safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in name)
            filename = f"{output_dir}/{safe_name}.{ext}"
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"  ✓ 已下载: {filename} ({len(response.content)} bytes)")
            return filename
            
    except Exception as e:
        print(f"  ✗ {name} 下载失败: {e}")
    
    return None