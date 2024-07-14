import re

from crawlers.base import BaseCrawler


class CrawlerDispatcher:
    def __init__(self) -> None:
        """初始化一個名為 _crawlers 的字典，這個字典用來儲存已註冊的爬蟲"""
        self._crawlers = {}

    def register(self, domain: str, crawler: type[BaseCrawler]) -> None:
        """註冊一個新的爬蟲"""
        self._crawlers[r"https://(www\.)?{}.com/*".format(re.escape(domain))] = crawler

    def get_crawler(self, url: str) -> BaseCrawler:
        """ 遍歷 _crawlers 字典，並檢查每個爬蟲的正規表達式是否與給定的 URL(domain) 匹配，以獲取適當的爬蟲"""
        for pattern, crawler in self._crawlers.items():
            if re.match(pattern, url):
                return crawler()
        else:
            raise ValueError("No crawler found for the provided link")