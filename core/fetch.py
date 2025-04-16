from utils.network import AsyncFetcher
from utils.parser import ChannelParser
import utils.file_ops as file_ops

class DataFetcher:
    """数据获取核心类"""
    def __init__(self):
        self.fetcher = AsyncFetcher()
        self.parser = ChannelParser()
    
    async def fetch_subscribe_sources(self):
        """获取自定义订阅源"""
        urls = file_ops.read_lines('config/subscribe.txt')
        contents = await self.fetcher.batch_fetch(urls)
        return [self.parser.parse_m3u(content) for content in contents if content]
    
    async def fetch_epg_sources(self):
        """获取EPG源"""
        urls = file_ops.read_lines('config/epg_sources.txt')
        contents = await self.fetcher.batch_fetch(urls)
        return {url: self.parser.parse_epg(content) for url, content in zip(urls, contents) if content}
    
    def close(self):
        """释放资源"""
        self.fetcher.close()
