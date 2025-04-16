from bs4 import BeautifulSoup
import re

class ChannelParser:
    """频道数据解析器"""
    def parse_m3u(self, content):
        """解析M3U格式内容"""
        channels = []
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('#EXTINF:'):
                # 解析EXTINF标签
                info = re.match(r'#EXTINF:-1,([^,]+),([^)]+)\(([^)]+)\)', line)
                if info:
                    channel = {
                        'name': info.group(1),
                        'icon': info.group(2),
                        'group': info.group(3)
                    }
                    channels.append(channel)
        return channels
    
    def parse_epg(self, xml_content):
        """解析EPG XML内容"""
        soup = BeautifulSoup(xml_content, 'lxml')
        channels = {
            channel.get('id'): channel.get_text(strip=True)
            for channel in soup.find_all('channel')
        }
        return channels
