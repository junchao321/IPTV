import aiohttp
import asyncio
from datetime import datetime

class SpeedTester:
    """网络测速工具"""
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = aiohttp.ClientSession()
    
    async def test_latency(self, url: str) -> int:
        """测试延迟（毫秒）"""
        start = datetime.now()
        try:
            async with self.session.head(url, timeout=aiohttp.ClientTimeout(total=self.timeout)):
                return (datetime.now() - start).microseconds // 1000
        except:
            return -1  # 表示超时或失败
    
    async def batch_test_channels(self, channels: List[Dict]) -> List[Dict]:
        """批量测试频道延迟"""
        tasks = [self.test_latency(channel['url']) for channel in channels]
        latencies = await asyncio.gather(*tasks)
        for i, channel in enumerate(channels):
            channel['latency'] = latencies[i]
        return channels
    
    async def close(self):
        """关闭会话"""
        await self.session.close()
