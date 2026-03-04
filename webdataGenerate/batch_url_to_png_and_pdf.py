import asyncio
import random
import os
import re
from io import BytesIO

import pandas as pd
from PIL import Image
from playwright.async_api import async_playwright


CSV_PATH = "url.csv"
OUTPUT_DIR = "../webData/pdf_and_png"
SAMPLE_SIZE = 100
CONCURRENCY = 2
SEGMENT_HEIGHT = 3000


def safe_filename(text):
    text = re.sub(r'[\\/*?:"<>|]', "_", text)
    return text[:150]


async def freeze_page(page):
    await page.evaluate("""
    () => {
        const style = document.createElement('style');
        style.innerHTML = `
            * {
                animation-play-state: paused !important;
                transition: none !important;
            }
        `;
        document.head.appendChild(style);

        document.querySelectorAll('video').forEach(v => {
            try { v.pause(); v.currentTime = 0; } catch(e){}
        });

        window.requestAnimationFrame = () => {};
        document.body.style.transform = "none";
    }
    """)


async def segmented_capture(page, output_png):

    total_height = await page.evaluate("document.documentElement.scrollHeight")
    total_width = await page.evaluate("document.documentElement.scrollWidth")

    images = []

    for y in range(0, total_height, SEGMENT_HEIGHT):

        await page.set_viewport_size({
            "width": total_width,
            "height": SEGMENT_HEIGHT
        })

        await page.evaluate(f"window.scrollTo(0, {y})")
        await page.wait_for_timeout(800)

        img_bytes = await page.screenshot()
        images.append(Image.open(BytesIO(img_bytes)))

    # 拼接
    final_image = Image.new("RGB", (total_width, total_height))

    current_y = 0
    for img in images:
        final_image.paste(img, (0, current_y))
        current_y += img.height

    final_image.save(output_png)
    final_image.save(output_png.replace(".png", ".pdf"), "PDF")


async def process_url(row, semaphore):

    async with semaphore:

        url = row["url"]
        title = safe_filename(row.get("title", "page"))

        print(f"[INFO] 处理: {title}")

        try:
            async with async_playwright() as p:

                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-gpu",
                        "--disable-dev-shm-usage",
                        "--no-sandbox",
                        "--disable-webgl"
                    ]
                )

                context = await browser.new_context()
                page = await context.new_page()

                await page.goto(url, timeout=60000, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)

                await freeze_page(page)

                output_png = os.path.join(OUTPUT_DIR, f"{title}.png")

                await segmented_capture(page, output_png)

                await browser.close()

                print(f"[SUCCESS] 完成: {title}")

        except Exception as e:
            print(f"[ERROR] 失败: {title} | {url} | {e}")


async def main():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(CSV_PATH)

    print(f"[INFO] 原始记录数: {len(df)}")

    if len(df) > SAMPLE_SIZE:
        df = df.sample(SAMPLE_SIZE, random_state=42)

    print(f"[INFO] 实际运行记录数: {len(df)}")
    print(f"[INFO] 并发数: {CONCURRENCY}")

    semaphore = asyncio.Semaphore(CONCURRENCY)

    tasks = [
        process_url(row, semaphore)
        for _, row in df.iterrows()
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())