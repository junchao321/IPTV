import aiohttp
import asyncio
from datetime import datetime

class SpeedTester:
    """测速系统"""
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.session = aiohttp.ClientSession()
    
    async def test_latency(self, url):
        """测试延迟（毫秒）"""
        start = datetime.now()
        try:
            async with self.session.head(url, timeout=self.timeout):
                return (datetime.now() - start).microseconds // 1000
        except:
            return None
    
    async def test_resolution(self, url):
        """测试分辨率（通过头部信息或FFmpeg解析）"""
        # 简化逻辑，实际需解析视频流信息
        headers = await self.session.head(url).headers
        return headers.get('Resolution', 'unknown')
    
    async def batch_test(self, channels):
        """批量测速"""
        results = []
        for channel in channels:
            latency = await self.test_latency(channel['url'])
            resolution = await self.test_resolution(channel['url'])
            results.append({
                **channel,
                'latency': latency,
                'resolution': resolution,
                'timestamp': datetime.now()
            })
        return results
    
    def close(self):
        self.session.close()
