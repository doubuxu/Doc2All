import asyncio
import csv
import re
import sys
import random
import fitz  # PyMuPDF
import pandas as pd
from pathlib import Path
from playwright.async_api import async_playwright
from pdf2image import convert_from_path

# ================== 工具函数 ==================

def safe_title(title: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', "_", title)[:100]

# 用于并发环境下安全写入 CSV 的锁
csv_lock = asyncio.Lock()

def update_csv_status(csv_path: Path, title: str):
    """同步更新 CSV 中对应 title 的 used 状态为 True"""
    df = pd.read_csv(csv_path)
    df.loc[df['title'] == title, 'used'] = 'True'
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

def merge_pdf_to_one_page(input_pdf_path: Path, output_pdf_path: Path):
    """将多页 PDF 合并为一页超长 PDF"""
    doc = fitz.open(input_pdf_path)
    if len(doc) == 0:
        return False
    
    # 计算总高度和最大宽度
    total_height = 0
    max_width = 0
    page_rects = []
    
    for page in doc:
        rect = page.rect
        page_rects.append(rect)
        total_height += rect.height
        max_width = max(max_width, rect.width)
    
    # 创建新文档和超长页面
    new_doc = fitz.open()
    new_page = new_doc.new_page(width=max_width, height=total_height)
    
    current_y = 0
    for i, rect in enumerate(page_rects):
        # 将每一页放置在累加的高度位置
        target_rect = fitz.Rect(0, current_y, rect.width, current_y + rect.height)
        new_page.show_pdf_page(target_rect, doc, i)
        current_y += rect.height
        
    new_doc.save(output_pdf_path)
    new_doc.close()
    doc.close()
    return True

def generate_img_from_pdf(pdf_path: Path, output_dir: Path):
    """从 PDF 生成 JPG 图片"""
    file_name = pdf_path.stem
    target_path = Path(output_dir) / f"{file_name}.jpg"
    try:
        # 网页长图转 PDF 后通常只有一页（合并后）
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        if images:
            images[0].save(target_path, "JPEG", quality=95)
            return True
    except Exception as e:
        print(f"[ERROR] PDF转图片失败 {file_name}: {e}")
    return False

# ================== 核心处理逻辑 ==================

async def process_page_to_pdf(context, url: str, title: str, output_dir: Path, csv_path: Path):
    page = await context.new_page()
    temp_pdf = Path(output_dir) / f"temp_{safe_title(title)}.pdf"
    final_pdf = Path(output_dir) / f"{safe_title(title)}.pdf"

    try:
        await page.emulate_media(media="screen")
        await page.set_viewport_size({"width": 1280, "height": 800})
        
        print(f"[INFO] 正在加载: {title}")
        await page.goto(url, wait_until="networkidle", timeout=60000)

        # 注入 CSS 优化布局
        await page.add_style_tag(content="""
            html, body { height: auto !important; min-height: 0 !important; }
            header, nav, .navbar, .fixed { position: relative !important; }
            *, *::before, *::after { transition: none !important; animation: none !important; }
        """)

        # 滚动触发渲染
        await page.evaluate("""
            async () => {
                for (let i = 0; i < document.body.scrollHeight; i += 800) {
                    window.scrollTo(0, i);
                    await new Promise(r => setTimeout(r, 100));
                }
                window.scrollTo(0, 0);
            }
        """)
        await asyncio.sleep(2)

        full_height = await page.evaluate("Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")

        # 1. 生成原始 PDF
        await page.pdf(
            path=str(temp_pdf),
            width="1280px",
            height=f"{full_height}px",
            print_background=True,
            margin={"top":"0px","bottom":"0px","left":"0px","right":"0px"}
        )

        # 2. 合并为单页 PDF
        if merge_pdf_to_one_page(temp_pdf, final_pdf):
            # 3. 生成图片
            if generate_img_from_pdf(final_pdf, output_dir):
                print(f"[SUCCESS] 已完成: {title}")
                # 4. 更新 CSV 状态
                async with csv_lock:
                    update_csv_status(csv_path, title)
            
            # 5. 删除临时和最终 PDF 文件
            if temp_pdf.exists(): temp_pdf.unlink()
            if final_pdf.exists(): final_pdf.unlink()

    except Exception as e:
        print(f"[ERROR] 处理失败 {title}: {e}")
    finally:
        await page.close()

async def worker(semaphore, context, title, url, output_dir, csv_path):
    async with semaphore:
        await process_page_to_pdf(context, url, title, output_dir, csv_path)

async def process_csv(csv_path: Path, output_dir: Path, count: int, concurrency: int = 5):
    # 读取并过滤未处理的数据
    df = pd.read_csv(csv_path)
    # 确保 used 列存在
    if 'used' not in df.columns:
        df['used'] = 'False'
        df.to_csv(csv_path, index=False)

    # 过滤未使用的行
    pending_df = df[df['used'].astype(str).str.lower() != 'true']
    rows = pending_df[['title', 'url']].values.tolist()

    if not rows:
        print("[INFO] 没有待处理的任务。")
        return

    # 随机挑选指定数量
    process_rows = random.sample(rows, min(len(rows), count))
    print(f"[INFO] 本次计划处理 {len(process_rows)} 条记录")

    semaphore = asyncio.Semaphore(concurrency)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(device_scale_factor=2)

        tasks = [
            worker(semaphore, context, row[0], row[1], output_dir, csv_path)
            for row in process_rows
        ]

        await asyncio.gather(*tasks)
        await browser.close()

if __name__ == "__main__":
    #url2image端到到批量生成
    # 用法：python script.py data.csv ./output 10

    csv_path = "./url.csv"
    out_dir = "../webData/batchData2"
    num_to_process = 100

    Path(out_dir).mkdir(parents=True, exist_ok=True)

    asyncio.run(process_csv(csv_path, out_dir, num_to_process, concurrency=3))