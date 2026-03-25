import asyncio
import hashlib
import base64
import subprocess
import re
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

# ================== 配置 ==================
OUT_DIR = Path("output_academic")
PDF_DIR = OUT_DIR / "pdf"
MEDIA_DIR = OUT_DIR / "media"
TMP_DIR = OUT_DIR / "tmp"

for d in (PDF_DIR, MEDIA_DIR, TMP_DIR):
    d.mkdir(parents=True, exist_ok=True)

# ---------- 工具函数 ----------

def sha1(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()

def get_base64_image(img_path: Path) -> str:
    """将图片转为 base64 字符串"""
    with open(img_path, "rb") as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return f"data:image/png;base64,{data}"

def extract_cover_frame(src_path: Path, out_img: Path) -> bool:
    """使用 ffmpeg 抽取视频或动图的第一帧"""
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src_path), "-vf", "select=eq(n\\,0)", "-vframes", "1", str(out_img)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    try:
        Image.open(out_img).verify()
        return True
    except:
        out_img.unlink(missing_ok=True)
        return False

# ---------- 核心渲染逻辑 ----------

async def process_page_to_pdf(url: str, title: str):
    async with async_playwright() as p:
        # 使用较高的 device_scale_factor 以确保长图放大后依然清晰
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(device_scale_factor=2)
        page = await context.new_page()

        print(f"[INFO] 正在加载页面: {url}")
        await page.goto(url, wait_until="networkidle", timeout=60000)

        # 1. 处理动态加载与滚动
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(3) 
        await page.evaluate("window.scrollTo(0, 0)")

        # 2. 媒体处理逻辑 (保持之前 Base64 替换的代码不变)
        # ... [此处省略之前的 media_elements 提取和替换逻辑] ...

        # 3. 获取网页真实高度
        # 有些网页可能有绝对定位的元素，scrollHeight 是最可靠的指标
        metrics = await page.evaluate("""
            () => {
                return {
                    width: Math.max(document.body.scrollWidth, document.documentElement.scrollWidth),
                    height: Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)
                }
            }
        """)

        # 4. 导出 PDF
        safe_title = re.sub(r'[\\/:*?"<>|]', "_", title)[:100]
        pdf_path = PDF_DIR / f"{safe_title}.pdf"
        
        print(f"[INFO] 正在导出单页 PDF ({metrics['width']}x{metrics['height']})...")
        
        await page.pdf(
            path=str(pdf_path),
            width=f"{metrics['width']}px",
            height=f"{metrics['height'] + 100}px", # 额外加 100 像素防止底部被截断
            print_background=True,
            margin={"top": "0px", "bottom": "0px", "left": "0px", "right": "0px"}
        )
        
        await browser.close()
        print(f"[SUCCESS] 单页 PDF 已保存")

if __name__ == "__main__":
    # 填入你想要处理的网页信息
    target_url = "https://byte-edit.github.io" 
    target_title = "ByteEdit_Generative_Image_Editing"
    
    asyncio.run(process_page_to_pdf(target_url, target_title))