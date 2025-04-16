import asyncio
import configparser
from core import DataFetcher, SpeedTester, ResultGenerator
from utils import FileOps

def main():
    # 加载配置
    config = FileOps.read_config('config/config.ini')
    
    # 初始化模块
    fetcher = DataFetcher(config)
    tester = SpeedTester(int(config['SPEED_TEST']['timeout']))
    generator = ResultGenerator(config)
    
    # 1. 获取原始数据
    print("开始获取订阅源...")
    channels = asyncio.run(fetcher.get_subscribe_channels())
    print(f"获取到 {len(channels)} 个有效频道")
    
    print("开始获取EPG数据...")
    epg_data = asyncio.run(fetcher.get_epg_data())
    print(f"获取到 {len(epg_data)} 个EPG频道映射")
    
    # 2. 测速筛选
    print("开始执行测速...")
    tested_channels = asyncio.run(tester.batch_test_channels(channels))
    
    # 过滤无效频道（延迟超过阈值）
    valid_channels = [
        c for c in tested_channels
        if c['latency'] != -1 and c['latency'] <= int(config['SPEED_TEST']['min_latency'])
    ]
    print(f"筛选出 {len(valid_channels)} 个符合条件的频道")
    
    # 3. 生成输出文件
    output_dir = config['SETTINGS']['output_dir']
    m3u_path = f"{output_dir}/iptv.m3u"
    txt_path = f"{output_dir}/iptv_report.txt"
    
    print("生成M3U直播列表...")
    generator.generate_m3u(valid_channels, m3u_path)
    
    print("生成TXT统计报告...")
    generator.generate_txt_report(valid_channels, txt_path)
    
    # 清理资源
    asyncio.run(fetcher.close())
    asyncio.run(tester.close())

if __name__ == "__main__":
    main()
