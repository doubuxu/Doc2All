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
        print(f"[INFO] 正在加载页面: {url}")
        await page.goto(url, wait_until="networkidle", timeout=60000)

        # 1. 处理动态加载与滚动
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(3)
        await page.evaluate("window.scrollTo(0, 0)")

        # 3. 获取网页真实高度
        metrics = await page.evaluate("""
            () => {
                return {
                    width: Math.max(document.body.scrollWidth, document.documentElement.scrollWidth),
                    height: Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)
                }
            }
        """)

        # 4. 导出 PDF
        filename = safe_title(title) + ".pdf"
        pdf_path = output_dir / filename
        
        print(f"[INFO] 正在导出单页 PDF ({metrics['width']}x{metrics['height']})...")

        await page.pdf(
            path=str(pdf_path),
            width=f"{metrics['width']}px",
            height=f"{metrics['height'] + 100}px",
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