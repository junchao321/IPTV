import aiohttp
import asyncio

class AsyncFetcher:
    """纯Python实现的异步网络请求工具（避免C扩展依赖）"""
    def __init__(self):
        self.session = aiohttp.ClientSession()
    
    async def fetch(self, url: str, timeout: int = 10) -> str:
        """带错误处理的GET请求"""
        try:
            async with self.session.get(
                url, 
                timeout=aiohttp.ClientTimeout(total=timeout),
                headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
            ) as response:
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"客户端错误: {url}, 错误: {str(e)}")
            return ""
        except asyncio.TimeoutError:
            print(f"请求超时: {url}")
            return ""
        except Exception as e:
            print(f"未知错误: {url}, 错误: {str(e)}")
            return ""
    
    async def batch_fetch(self, urls: List[str]) -> List[str]:
        """批量异步请求（带并发控制）"""
        semaphore = asyncio.Semaphore(100)  # 控制并发数防止过载
        async def fetch_with_semaphore(url):
            async with semaphore:
                return await self.fetch(url)
        tasks = [fetch_with_semaphore(url) for url in urls]
        return await asyncio.gather(*tasks)
    
    async def close(self):
        """安全关闭会话"""
        await self.session.close()
