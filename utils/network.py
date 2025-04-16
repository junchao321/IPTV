import aiohttp
import asyncio

class AsyncFetcher:
    """异步网络请求工具"""
    def __init__(self):
        self.session = aiohttp.ClientSession()
    
    async def fetch(self, url: str, timeout: int = 10) -> str:
        """获取单个URL内容"""
        try:
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                return await response.text()
        except Exception as e:
            print(f"请求失败: {url}, 错误: {str(e)}")
            return ""
    
    async def batch_fetch(self, urls: List[str]) -> List[str]:
        """批量异步获取URL列表"""
        tasks = [self.fetch(url) for url in urls]
        return await asyncio.gather(*tasks)
    
    async def close(self):
        """关闭会话"""
        await self.session.close()
