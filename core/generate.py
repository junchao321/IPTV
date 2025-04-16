from utils.file_ops import write_file

class ResultGenerator:
    """结果生成器"""
    def generate_m3u(self, channels, output_path):
        """生成M3U格式文件"""
        content = '#EXTM3U\n'
        for channel in channels:
            content += (
                f'#EXTINF:-1 tvg-id="{channel["id"]}" tvg-name="{channel["name"]}" tvg-logo="{channel["icon"]}" group-title="{channel["group"]}",{channel["name"]}\n'
                f'{channel["url"]}\n'
            )
        write_file(output_path, content)
    
    def generate_txt(self, channels, output_path):
        """生成TXT格式文件"""
        content = '\n'.join([
            f"{channel['name']}|{channel['url']}|{channel['group']}|{channel['icon']}"
            for channel in channels
        ])
        write_file(output_path, content)
    
    def generate_epg_m3u(self, channels, epg_data, output_path):
        """生成含EPG的M3U"""
        # 关联EPG数据
        for channel in channels:
            channel['epg'] = epg_data.get(channel['id'], {})
        # 生成带EPG标签的M3U
        self.generate_m3u(channels, output_path)
