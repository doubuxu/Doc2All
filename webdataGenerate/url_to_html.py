import pandas as pd
import asyncio
import os
import sys
import subprocess
import re
import csv
import time
from urllib.parse import quote
from playwright.async_api import async_playwright, Error as PlaywrightError
import fitz  # PyMuPDF

# ================= 配置区 =================
CHROMIUM_PATH = "/home/huangyc/.cache/ms-playwright/chromium-1161/chrome-linux/chrome" 
SINGLE_FILE_BIN = os.path.abspath("./node_modules/.bin/single-file")
# ==========================================

def get_safe_filename(text):
    clean_text = re.sub(r'[^\w\-]', '_', str(text))
    return re.sub(r'_+', '_', clean_text).strip('_')

def log_to_csv(file_path, data_dict):
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data_dict.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data_dict)

def run_singlefile_cli(url, output_html):
    try:
        subprocess.run(["pkill", "-f", "single-file-node.js"], capture_output=True)
    except:
        pass
    # 增加 --browser-wait-delay 规避 unsettled top-level await 警告
    cmd = [
        SINGLE_FILE_BIN,
        url,
        output_html,
        "--browser-executable-path", CHROMIUM_PATH,
        "--browser-wait-until", "load",
        "--browser-wait-delay", "2000", 
        "--browser-headless", "true",
        "--browser-args", '["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu"]'
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=180)
        if os.path.exists(output_html) and os.path.getsize(output_html) > 0:
            return True, "HTML generated"
        return False, "File empty"
    except Exception as e:
        return False, f"SingleFile Error: {str(e)[:100]}"

async def convert_html_to_assets(browser, html_path, pdf_path, png_path):
    # 增加物理文件检查延迟，规避 ERR_FAILED
    for _ in range(5):
        if os.path.exists(html_path): break
        await asyncio.sleep(1)

    page = None
    context = None
    try:
        # 允许跨文件访问，解决 file:///data/... 的权限问题
        context = await browser.new_context(java_script_enabled=True)
        page = await context.new_page()
        await page.set_viewport_size({"width": 1920, "height": 1080})
        await page.emulate_media(media="screen")

        abs_path = os.path.abspath(html_path)
        file_url = f"file://{abs_path}" # 有时不需要 quote 路径，视系统而定

        await page.goto(file_url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(1)
        
        height = await page.evaluate('document.documentElement.scrollHeight || 2000')
        await page.pdf(path=pdf_path, width="1920px", height=f"{height}px", print_background=True)
        
        doc = fitz.open(pdf_path)
        pix = doc[0].get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
        pix.save(png_path)
        doc.close()
        return True, f"Success ({height}px)"
    except Exception as e:
        return False, str(e)
    finally:
        if page: await page.close()
        if context: await context.close()

async def get_browser(p):
    """封装浏览器启动，添加权限参数"""
    return await p.chromium.launch(
        executable_path=CHROMIUM_PATH,
        args=[
            "--no-sandbox", 
            "--disable-setuid-sandbox",
            "--allow-file-access-from-files", # 解决本地文件 ERR_FAILED
            "--disable-web-security"          # 进一步放开本地访问限制
        ]
    )

async def main(csv_path, output_root, start_idx, end_idx):
    output_root = os.path.abspath(output_root)
    html_dir, assets_dir, log_dir = [os.path.join(output_root, d) for d in ["html", "assets", "logs"]]
    for d in [html_dir, assets_dir, log_dir]: os.makedirs(d, exist_ok=True)

    success_log, failed_log = os.path.join(log_dir, "success.csv"), os.path.join(log_dir, "failed.csv")
    df = pd.read_csv(csv_path).iloc[start_idx:end_idx]

    async with async_playwright() as p:
        browser = await get_browser(p)
        
        for index, row in df.iterrows():
            url, title = row['url'], row.get('title', 'untitled')
            base_name = f"{index:05d}_{get_safe_filename(title)[:80]}"
            t_html, t_pdf, t_png = os.path.join(html_dir, f"{base_name}.html"), os.path.join(assets_dir, f"{base_name}.pdf"), os.path.join(assets_dir, f"{base_name}.png")

            print(f"\n任务 [{index}]: {url}")
            
            h_ok, h_msg = run_singlefile_cli(url, t_html)
            if h_ok:
                # 尝试转换，如果浏览器崩溃则重启
                try:
                    a_ok, a_msg = await convert_html_to_assets(browser, t_html, t_pdf, t_png)
                except PlaywrightError as e:
                    if "closed" in str(e).lower():
                        print("   [严重] 浏览器已关闭，正在尝试重启...")
                        browser = await get_browser(p)
                        a_ok, a_msg = await convert_html_to_assets(browser, t_html, t_pdf, t_png)
                    else:
                        a_ok, a_msg = False, str(e)

                if a_ok:
                    print(f"   [成功] {a_msg}"); log_to_csv(success_log, {"index": index, "url": url, "info": a_msg})
                else:
                    print(f"   [失败] 资产转换: {a_msg}"); log_to_csv(failed_log, {"index": index, "url": url, "reason": a_msg, "stage": "Asset"})
            else:
                print(f"   [跳过] SingleFile: {h_msg}"); log_to_csv(failed_log, {"index": index, "url": url, "reason": h_msg, "stage": "SingleFile"})

        await browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 5: print("Usage: python script.py <csv> <out> <start> <end>")
    else: asyncio.run(main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])))