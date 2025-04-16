import os
import pickle
from collections import defaultdict

def get_name_uri_from_dir(dir_path):
    result = {}
    if os.path.exists(dir_path):
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    for line in file:
                        name, _, uri = line.strip().partition(",")
                        result[name] = uri
    return result

def get_name_urls_from_file(file_path, format_name_flag=False):
    result = defaultdict(list)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                name, _, url = line.strip().partition(",")
                result[name].append({"url": url})
    return result

def get_channel_data_from_file(channels, file, whitelist, open_local, local_data, live_data, hls_data):
    for line in file:
        trimmed_line = line.strip()
        if trimmed_line != "":
            if "#genre#" in trimmed_line:
                current_group = trimmed_line.replace(",#genre#", "").strip()
            else:
                try:
                    original_channel_name, _, channel_link = map(str.strip, trimmed_line.partition(","))
                except:
                    continue
                if original_channel_name in whitelist:
                    channels[current_group][original_channel_name].extend(whitelist[original_channel_name])
                if open_local and original_channel_name in local_data:
                    channels[current_group][original_channel_name].extend(local_data[original_channel_name])
                if live_data and original_channel_name in live_data:
                    channels[current_group][original_channel_name].append({"url": live_data[original_channel_name]})
                if hls_data and original_channel_name in hls_data:
                    channels[current_group][original_channel_name].append({"url": hls_data[original_channel_name]})
                channels[current_group][original_channel_name].append({"url": channel_link})
    return channels

def get_channel_items():
    user_source_file = os.path.join(os.getcwd(), config.source_file)
    channels = defaultdict(lambda: defaultdict(list))
    live_data = None
    hls_data = None
    if config.open_rtmp:
        live_data = get_name_uri_from_dir("config/live")
        hls_data = get_name_uri_from_dir("config/hls")
    local_data = get_name_urls_from_file("config/local.txt", format_name_flag=True)
    whitelist = get_name_urls_from_file("config/whitelist.txt")

    if os.path.exists(user_source_file):
        with open(user_source_file, "r", encoding="utf-8") as file:
            channels = get_channel_data_from_file(
                channels, file, whitelist, config.open_local, local_data, live_data, hls_data
            )

    if config.open_history:
        cache_path = os.path.join(os.getcwd(), "output/cache.pkl")
        if os.path.exists(cache_path):
            with open(cache_path, "rb") as file:
                old_result = pickle.load(file)
                for cate, data in channels.items():
                    if cate in old_result:
                        for name, info_list in data.items():
                            urls = [url.partition("$")[0] for item in info_list if (url := item["url"])]
                            if name in old_result[cate]:
                                for info in old_result[cate][name]:
                                    if info:
                                        pure_url = info["url"].partition("$")[0]
                                        if pure_url not in urls:
                                            channels[cate][name].append(info)
    return channels

def append_total_data(channel_items, channel_names, channel_data, *results):
    for group, channels in channel_items:
        for channel_name in channels:
            if channel_name not in channel_data:
                channel_data[channel_name] = []
            for result in results:
                if channel_name in result:
                    channel_data[channel_name].extend(result[channel_name])

def write_channel_to_file(channel_data, ipv6=False, first_channel_name=None, callback=None):
    output_path = os.path.join(config.output_dir, config.final_file)
    with open(output_path, "w", encoding="utf-8") as file:
        for channel_name, url_info_list in channel_data.items():
            for url_info in url_info_list:
                file.write(f"{channel_name},{url_info['url']}\n")
