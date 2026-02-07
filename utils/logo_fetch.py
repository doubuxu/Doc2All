import requests
import json
from urllib.parse import urlparse

class LogoFetcher:
    def __init__(self):
        self.clearbit_base = "https://logo.clearbit.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWeb/537.36'
        }
    
    def get_logo_by_domain(self, domain: str, size: str = "256") -> str:
        """
        通过域名获取Logo
        size可选: 16, 24, 32, 48, 64, 128, 256, 512
        """
        # 清理域名
        domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
        logo_url = f"{self.clearbit_base}/{domain}?size={size}"
        return logo_url
    
    def search_institution_domain(self, institution_name: str) -> str:
        """
        通过机构名搜索域名（使用Brandfetch搜索API）
        """
        search_url = "https://api.brandfetch.io/v2/search"
        params = {"query": institution_name}
        
        try:
            response = requests.get(search_url, params=params, headers=self.headers, timeout=10)
            if response.status_code == 200:
                results = response.json()
                if results and len(results) > 0:
                    # 返回第一个结果的域名
                    return results[0].get('domain', '')
        except:
            pass
        return ''
    
    def fetch_logo(self, institution_name: str, institution_type: str = 'unknown') -> dict:
        """
        主函数：获取机构Logo
        """
        result = {
            'name': institution_name,
            'type': institution_type,
            'logo_url': None,
            'source': None
        }
        
        # 1. 尝试直接匹配知名机构
        known_domains = self._get_known_domains(institution_name)
        if known_domains:
            result['logo_url'] = self.get_logo_by_domain(known_domains)
            result['source'] = 'known_mapping'
            return result
        
        # 2. 搜索域名
        domain = self.search_institution_domain(institution_name)
        if domain:
            result['logo_url'] = self.get_logo_by_domain(domain)
            result['source'] = 'brandfetch_search'
            return result
        
        return result
    
    def _get_known_domains(self, name: str) -> str:
        """知名机构域名映射"""
        name_lower = name.lower()
        mappings = {
            'mit': 'mit.edu',
            'massachusetts institute': 'mit.edu',
            'stanford': 'stanford.edu',
            'harvard': 'harvard.edu',
            'google': 'google.com',
            'deepmind': 'deepmind.com',
            'openai': 'openai.com',
            'microsoft': 'microsoft.com',
            'facebook': 'meta.com',
            'meta': 'meta.com',
            'amazon': 'amazon.com',
            'apple': 'apple.com',
            'nvidia': 'nvidia.com',
            'tsinghua': 'tsinghua.edu.cn',
            'peking': 'pku.edu.cn',
            'peking university': 'pku.edu.cn',
            'beijing': 'pku.edu.cn',  # 可能需要更精确匹配
            'cmu': 'cmu.edu',
            'carnegie mellon': 'cmu.edu',
            'berkeley': 'berkeley.edu',
            'uc berkeley': 'berkeley.edu',
        }
        
        for key, domain in mappings.items():
            if key in name_lower:
                return domain
        return ''

# 使用示例
fetcher = LogoFetcher()

institutions = [
    "Massachusetts Institute of Technology",
    "Google DeepMind",
    "Tsinghua University",
    "OpenAI",
    "Stanford University"
]

for inst in institutions:
    result = fetcher.fetch_logo(inst)
    print(f"{result['name']}: {result['logo_url']}")