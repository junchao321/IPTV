import aiohttp
import asyncio
from typing import List

class AsyncFetcher:
    """增强型异步网络请求工具（带连接池和UA伪装）"""
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
        }
        self.session = aiohttp.ClientSession(headers=self.headers)
        self.semaphore = asyncio.Semaphore(200)  # 并发控制（推荐值≤200）

    async def fetch(self, url: str, timeout: int = 15) -> str:
        """带重试机制的GET请求"""
        for _ in range(3):  # 最多重试3次
            try:
                async with self.semaphore, \
                      self.session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                    return await response.text()
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print(f"请求重试中: {url}, 错误: {str(e)}")
        return ""

    async def batch_fetch(self, urls: List[str]) -> List[str]:
        """批量异步请求（带异常处理）"""
        tasks = [self.fetch(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def close(self):
        """资源释放（带优雅关闭）"""
        await self.session.close()
        await asyncio.sleep(0.1)  # 等待资源释放完成
