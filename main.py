import asyncio
from core.fetch import DataFetcher
from core.speed_test import SpeedTester
from core.generate import ResultGenerator
import utils.file_ops as file_ops

async def main():
    # 初始化模块
    fetcher = DataFetcher()
    tester = SpeedTester()
    generator = ResultGenerator()
    
    # 1. 获取数据
    print("开始获取订阅源...")
    channels = await fetcher.fetch_subscribe_sources()
    print(f"获取到 {len(channels)} 个频道")
    
    print("开始获取EPG数据...")
    epg_data = await fetcher.fetch_epg_sources()
    print(f"获取到 {len(epg_data)} 个EPG源")
    
    # 2. 测速筛选
    print("开始测速...")
    tested_channels = await tester.batch_test(channels)
    # 过滤无效数据
    valid_channels = [c for c in tested_channels if c['latency'] <= config.max_latency]
    
    # 3. 生成结果
    output_dir = config.output_dir
    file_ops.create_dir(output_dir)
    
    print("生成M3U文件...")
    generator.generate_m3u(valid_channels, f"{output_dir}/m3u/iptv.m3u")
    generator.generate_epg_m3u(valid_channels, epg_data, f"{output_dir}/m3u/iptv_epg.m3u")
    
    print("生成TXT文件...")
    generator.generate_txt(valid_channels, f"{output_dir}/txt/iptv.txt")
    
    # 清理资源
    fetcher.close()
    tester.close()

if __name__ == "__main__":
    asyncio.run(main())
