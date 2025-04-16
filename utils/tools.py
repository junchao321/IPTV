import os
import re
from urllib.parse import urljoin

def join_url(base_url, url):
    return urljoin(base_url, url)

def convert_to_m3u(path=None, first_channel_name=None, data=None):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            m3u_output = f'#EXTM3U x-tvg-url="{join_url(config.cdn_url, "https://raw.githubusercontent.com/fanmingming/live/main/e.xml")}"\n'
            current_group = None
            for line in file:
                trimmed_line = line.strip()
                if trimmed_line != "":
                    if "#genre#" in trimmed_line:
                        current_group = trimmed_line.replace(",#genre#", "").strip()
                    else:
                        try:
                            original_channel_name, _, channel_link = map(
                                str.strip, trimmed_line.partition(",")
                            )
                        except:
                            continue
                        processed_channel_name = re.sub(
                            r"(CCTV|CETV)-(\d+)(\+.*)?",
                            lambda m: f"{m.group(1)}{m.group(2)}" + ("+" if m.group(3) else ""),
                            first_channel_name if current_group == "🕘️更新时间" else original_channel_name,
                        )
                        m3u_output += f'#EXTINF:-1 tvg-name="{processed_channel_name}" tvg-logo="{join_url(config.cdn_url, f"https://raw.githubusercontent.com/fanmingming/live/main/tv/{processed_channel_name}.png")}"'
                        if current_group:
                            m3u_output += f' group-title="{current_group}"'
                        m3u_output += f",{original_channel_name}\n"
                        if data:
                            item_list = data.get(original_channel_name, [])
                            for item in item_list:
                                if item["url"] == channel_link:
                                    headers = item.get("headers")
                                    if headers:
                                        for key, value in headers.items():
                                            m3u_output += f"#EXTVLCOPT:http-{key.lower()}={value}\n"
                                    break
                        m3u_output += f"{channel_link}\n"
            m3u_file_path = os.path.splitext(path)[0] + ".m3u"
            with open(m3u_file_path, "w", encoding="utf-8") as m3u_file:
                m3u_file.write(m3u_output)
