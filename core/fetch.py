from utils import FileOps, AsyncFetcher, ChannelParser
import asyncio

class DataFetcher:
    """数据获取与解析核心类"""
    def __init__(self, config: configparser.ConfigParser):
        self.config = config
        self.file_ops = FileOps()
        self.fetcher = AsyncFetcher()
        self.parser = ChannelParser()
    
    async def get_subscribe_channels(self) -> List[Dict]:
        """获取并解析订阅源频道"""
        subscribe_urls = self.file_ops.read_text_file(
            self.config['PATHS']['subscribe_file']
        )
        contents = await self.fetcher.batch_fetch(subscribe_urls)
        all_channels = []
        for content in contents:
            if content:
                all_channels.extend(self.parser.parse_m3u_channels(content))
        return all_channels
    
    async def get_epg_data(self) -> Dict[str, str]:
        """获取并解析EPG数据"""
        epg_urls = self.file_ops.read_text_file(
            self.config['PATHS']['epg_source_file']
        )
        contents = await self.fetcher.batch_fetch(epg_urls)
        epg_data = {}
        for content in contents:
            if content:
                epg_data.update(self.parser.parse_epg_data(content))
        return epg_data
    
    async def close(self):
        """释放资源"""
        await self.fetcher.close()
