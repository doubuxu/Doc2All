
import re
import requests
import time
import os
from urllib.parse import urljoin
from pathlib import Path

class F1000PosterDownloader:
    def __init__(self, output_dir="f1000_posters", delay=2):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.base_url = "https://f1000research.com"
        self.delay = delay
        self.stats = {'total': 0, 'success': 0, 'failed': 0}
    
    def get_list_page(self, page_num):
        """获取列表页并提取海报ID"""
        url = f"{self.base_url}/browse/posters?show=20&page={page_num}"
        print(f"\n📄 获取列表页 {page_num}: {url}")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
        except Exception as e:
            print(f"❌ 获取列表页失败: {e}")
            return []
        
        # 从JavaScript代码中提取海报链接
        # 模式: href="/posters/15-101"
        pattern = r'href="(/posters/\d+-\d+)"'
        matches = re.findall(pattern, response.text)
        
        # 去重并保持顺序
        seen = set()
        unique_ids = []
        for match in matches:
            if match not in seen:
                seen.add(match)
                unique_ids.append(match)
        
        print(f"✅ 找到 {len(unique_ids)} 个海报")
        return unique_ids
    
    def get_poster_details(self, poster_path):
        """获取海报详情页，提取标题和PDF链接"""
        url = f"{self.base_url}{poster_path}"
        poster_id = poster_path.split('/')[-1]
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            html = response.text
        except Exception as e:
            print(f"  ❌ 获取详情页失败: {e}")
            return None
        
        # 提取标题 (从<h1>标签或<title>)
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1))  # 去除HTML标签
            title = re.sub(r'\s+', ' ', title).strip()  # 清理空白
        else:
            title = f"poster_{poster_id}"
        
        # 提取PDF链接 (data-url属性)
        pdf_pattern = r'data-url="(https://f1000research-files\.f1000\.com/posters/[^"]+\.pdf)"'
        pdf_match = re.search(pdf_pattern, html)
        
        if not pdf_match:
            print(f"  ⚠️ 未找到PDF链接: {poster_id}")
            return None
        
        pdf_url = pdf_match.group(1)
        
        return {
            'id': poster_id,
            'title': title,
            'pdf_url': pdf_url,
            'detail_url': url
        }
    
    def download_pdf(self, poster_info):
        """下载PDF文件"""
        # 清理标题作为文件名
        safe_title = re.sub(r'[\\/:*?"<>|]', '', poster_info['title'])
        safe_title = safe_title[:100]  # 限制长度
        filename = f"{safe_title}.pdf"
        filepath = self.output_dir / filename
        
        # 检查是否已存在
        if filepath.exists():
            print(f"  ⏭️  已存在，跳过: {filename}")
            return True
        
        print(f"  ⬇️  下载: {filename[:60]}...")
        print(f"     URL: {poster_info['pdf_url'][:80]}...")
        
        try:
            response = self.session.get(poster_info['pdf_url'], stream=True, timeout=60)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"     进度: {percent:.1f}%", end='\r')
            
            file_size = filepath.stat().st_size / 1024 / 1024
            print(f"  ✅ 完成: {file_size:.2f} MB")
            return True
            
        except Exception as e:
            print(f"  ❌ 下载失败: {e}")
            if filepath.exists():
                filepath.unlink()
            return False
    
    def run(self, start_page=1, end_page=None):
        """
        运行批量下载
        start_page: 起始页码
        end_page: 结束页码（None表示直到最后一页）
        """
        page = start_page
        
        while True:
            if end_page and page > end_page:
                break
            
            # 获取列表页
            poster_paths = self.get_list_page(page)
            
            if not poster_paths:
                print(f"\n⚠️ 第 {page} 页无数据，停止")
                break
            
            # 处理每个海报
            for i, path in enumerate(poster_paths, 1):
                print(f"\n[{i}/{len(poster_paths)}] 处理海报: {path}")
                
                # 获取详情
                info = self.get_poster_details(path)
                if not info:
                    self.stats['failed'] += 1
                    continue
                
                print(f"  标题: {info['title'][:70]}...")
                
                # 下载
                if self.download_pdf(info):
                    self.stats['success'] += 1
                else:
                    self.stats['failed'] += 1
                
                self.stats['total'] += 1
                
                # 延迟
                if i < len(poster_paths):
                    time.sleep(self.delay)
            
            page += 1
            time.sleep(self.delay)
        
        # 统计
        print("\n" + "="*60)
        print("📊 下载统计")
        print("="*60)
        print(f"总计处理: {self.stats['total']}")
        print(f"成功: {self.stats['success']} ✅")
        print(f"失败: {self.stats['failed']} ❌")
        print(f"保存位置: {self.output_dir.absolute()}")
        print("="*60)

# 运行示例
if __name__ == "__main__":
    downloader = F1000PosterDownloader(output_dir="../f1000_posters", delay=2)
    
    # 下载第1-3页作为测试
    # 总共13053张海报，每页20张，约653页
    # 建议分批下载，避免长时间运行中断
    downloader.run(start_page=2, end_page=50)
