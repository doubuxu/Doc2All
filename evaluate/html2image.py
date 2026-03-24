import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
from http.server import SimpleHTTPRequestHandler
import socketserver
import threading

class SimpleRenderer:
    @staticmethod
    async def html_to_desktop_image(html_path: str, output_path: str):
        """
        极简调用接口：仅需输入路径，自动处理大屏渲染与相对资源
        """
        html_file = Path(html_path).resolve()
        output_file = Path(output_path).resolve()
        
        # 1. 在 HTML 所在目录启动临时服务器 (解决 ./visuals/ 路径问题)
        handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(*args, directory=str(html_file.parent), **kwargs)
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", 8888), handler) as httpd:
            # 后台运行服务器
            thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            thread.start()

            async with async_playwright() as p:
                # 2. 启动浏览器并设置大屏视口
                browser = await p.chromium.launch(headless=True)
                # 强制 1920 宽度防止挤压，不设置高度限制
                context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
                page = await context.new_page()

                # 3. 加载并渲染
                try:
                    await page.goto(f"http://localhost:8888/{html_file.name}", wait_until="networkidle")
                    
                    # 注入你的“防挤压”样式
                    await page.add_style_tag(content="body { min-width: 1440px !important; background: white; }")
                    
                    # 4. 截图 (full_page=True 确保不被 1080 高度截断)
                    await page.screenshot(path=str(output_file), full_page=True)
                    print(f"成功渲染图片: {output_file}")
                finally:
                    await browser.close()
                    httpd.shutdown()


# 导入你刚刚写的类
async def my_eval_task(html_path,image_output):
    #html_input = "../data/output/20260323_154516_layoutTransformer_poster/layoutTransformer.html"
    #image_output = "../data/output/20260323_154516_layoutTransformer_poster/evaluate_view.png"
    
    # 只需要这一行调用
    await SimpleRenderer.html_to_desktop_image(html_path, image_output)

# 运行
if __name__=="__main__":
    asyncio.run(my_eval_task())