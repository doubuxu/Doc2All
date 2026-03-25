import asyncio
import csv
import re
import sys
from pathlib import Path
from playwright.async_api import async_playwright

# ================== 工具函数 ==================

def safe_title(title: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', "_", title)[:100]


# ================== 你的核心逻辑（完全未修改） ==================

async def process_page_to_pdf(context, url: str, title: str, output_dir: Path):
    page = await context.new_page()

    try:
        # 强制使用屏幕媒体类型，避开干扰布局的打印样式
        await page.emulate_media(media="screen")
        await page.set_viewport_size({"width": 1280, "height": 800})

        print(f"[INFO] 正在加载页面: {url}")
        await page.goto(url, wait_until="networkidle", timeout=60000)

        # 【核心改进 1】: 强制清除 100vh 和 绝对定位产生的间距
        await page.add_style_tag(content="""
            /* 1. 强制所有元素高度自适应，禁止 100vh 撑开间距 */
            html, body, section, div, [class*='container'] { 
                height: auto !important; 
                min-height: 0 !important;
            }
            /* 2. 隐藏或设为静态布局：避免悬浮导航栏干扰高度计算 */
            header, nav, .navbar, #header, .fixed { 
                position: relative !important; 
            }
            /* 3. 移除动画，防止内容在滚动时才渐显导致的布局空洞 */
            *, *::before, *::after {
                transition: none !important;
                animation: none !important;
            }
        """)

        # 【核心改进 2】: 彻底触发懒加载和公式渲染
        # 慢速滚动比直接跳到页尾更能触发 MathJax 和延迟加载图
        await page.evaluate("""
            async () => {
                const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
                for (let i = 0; i < document.body.scrollHeight; i += 800) {
                    window.scrollTo(0, i);
                    await delay(100);
                }
                window.scrollTo(0, 0);
            }
        """)
        await asyncio.sleep(2) # 留给公式渲染最后的窗口期

        # 重新获取高度
        full_height = await page.evaluate("Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")

        filename = safe_title(title) + ".pdf"
        pdf_path = output_dir / filename
        
        print(f"[INFO] 正在导出 PDF (高度: {full_height})...")

        await page.pdf(
            path=str(pdf_path),
            width="1280px",
            height=f"{full_height}px",
            print_background=True,
            margin={"top": "0px", "bottom": "0px", "left": "0px", "right": "0px"}
        )

        print(f"[SUCCESS] 已保存: {filename}")

    except Exception as e:
        print(f"[ERROR] 处理失败: {title} | {url} | 错误: {e}")
    finally:
        await page.close()


# ================== 新增：CSV + 并发控制 ==================

async def worker(semaphore, context, title, url, output_dir):
    async with semaphore:
        await process_page_to_pdf(context, url, title, output_dir)


async def process_csv(csv_path: Path, output_dir: Path, concurrency: int = 5):
    rows = []

    # 读取 CSV
    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get("title", "").strip()
            url = row.get("url", "").strip()
            if title and url:
                rows.append((title, url))
    import random

    sample_size = 100  # 想跑多少条改这里

    if len(rows) > sample_size:
        rows = random.sample(rows, sample_size)
        
    print(f"[INFO] 共读取 {len(rows)} 条记录")
    print(f"[INFO] 并发数: {concurrency}")

    semaphore = asyncio.Semaphore(concurrency)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(device_scale_factor=2)

        tasks = [
            worker(semaphore, context, title, url, output_dir)
            for title, url in rows
        ]

        await asyncio.gather(*tasks)

        await browser.close()


# ================== 主程序 ==================

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python batch_csv_to_pdf.py <csv路径> <输出pdf目录>")
        sys.exit(1)

    csv_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    if not csv_file.exists():
        print("CSV 文件不存在")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    asyncio.run(process_csv(csv_file, output_dir, concurrency=5))

# 在此函数的基础上进行修改，目前csv结构为title、url和used，其中used为true表示该文件已经被使用过，遍历到这条数据时直接跳过
# 在批量url转pdf的函数中加入处理文件数量的参数，每次从csvfile中随机挑选指定数量的url进行处理，处理后将used改为true，以后不再处理
# 不要修改pdf生成逻辑
# 在当前的pdf生成逻辑后加入下面的代码，将pdf合并为一页
"""
import fitz  # PyMuPDF

# 打开原始 PDF
doc = fitz.open("../webData/web_pdf/Can LLMs Solve Molecule Puzzles_ A Multimodal Benchmark for Molecular Structure Elucidation.pdf")

page1 = doc[0]
page2 = doc[1]

# 获取页面尺寸
rect1 = page1.rect
rect2 = page2.rect

# 新建 PDF
new_doc = fitz.open()

# 创建一个新页面（高度为两页之和）
new_page = new_doc.new_page(
    width=max(rect1.width, rect2.width),
    height=rect1.height + rect2.height
)

# 将第一页插入
new_page.show_pdf_page(
    fitz.Rect(0, 0, rect1.width, rect1.height),
    doc, 0
)

# 将第二页插入（放在第一页下面）
new_page.show_pdf_page(
    fitz.Rect(0, rect1.height, rect2.width, rect1.height + rect2.height),
    doc, 1
)

# 保存
new_doc.save("merged_one_page.pdf")
new_doc.close()
doc.close()
"""

#基于合并为一页的pdf生成图片，图片名与csv的title名保持一致
#前两个pdf和图片都输出到函数参数的输出路径中
#最后将两个pdf文件从本地删除
#生成图片的代码如下：
"""
import pandas as pd
import random
from pathlib import Path
from pdf2image import convert_from_path

def generateIMG(pdf_path, output_path):
    pdf_path = Path(pdf_path)
    file_name = pdf_path.stem
    target_path = Path(output_path) / f"{file_name}.jpg"
    
    try:
        # 将 PDF 转换为图片列表（默认取第一页）
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        if images:
            images[0].save(target_path, "JPEG")
            return True
    except Exception as e:
        print(f"转换文件 {file_name} 时出错: {e}")
        return False
    return False
"""