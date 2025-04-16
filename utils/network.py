import aiohttp
import asyncio

class AsyncFetcher:
    """异步网络请求工具"""
    def __init__(self):
        self.session = aiohttp.ClientSession()
    
    async def fetch_url(self, url, timeout=10):
        """获取单个URL内容"""
        try:
            async with self.session.get(url, timeout=timeout) as response:
                return await response.text()
        except Exception as e:
            print(f"请求失败: {url}, 错误: {str(e)}")
            return None
    
    async def batch_fetch(self, urls):
        """批量异步获取URL列表"""
        tasks = [self.fetch_url(url) for url in urls]
        return await asyncio.gather(*tasks)
    
    def close(self):
        """关闭会话"""
        self.session.close()
