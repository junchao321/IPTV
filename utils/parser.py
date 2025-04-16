from bs4 import BeautifulSoup
import re
from typing import Dict, List

class ChannelParser:
    """频道数据解析器"""
    
    def parse_m3u_channels(self, content: str) -> List[Dict]:
        """解析M3U格式内容，提取频道信息"""
        channels = []
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('#EXTINF:'):
                # 解析EXTINF标签格式：#EXTINF:-1,tvg-id="xxx",tvg-name="xxx",tvg-logo="xxx",group-title="xxx"
                match = re.match(
                    r'#EXTINF:-1,.*?tvg-id="(.*?)".*?tvg-name="(.*?)".*?tvg-logo="(.*?)".*?group-title="(.*?)"',
                    line,
                    re.DOTALL
                )
                if match:
                    channels.append({
                        'id': match.group(1),
                        'name': match.group(2),
                        'icon': match.group(3),
                        'group': match.group(4)
                    })
            elif line.startswith('http'):  # 提取频道URL
                if channels:
                    channels[-1]['url'] = line
        return [c for c in channels if 'url' in c]  # 过滤无效频道
    
    def parse_epg_data(self, xml_content: str) -> Dict[str, str]:
        """解析XMLTV格式的EPG数据"""
        soup = BeautifulSoup(xml_content, 'lxml')
        return {
            channel.get('id'): channel.find('display-name').get_text(strip=True)
            for channel in soup.find_all('channel')
            if channel.get('id') and channel.find('display-name')
        }
