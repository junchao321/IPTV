import asyncio
import os
from utils.config import config
from utils.channel import get_channel_items, append_total_data, write_channel_to_file
from utils.tools import convert_to_m3u
from updates.fofa import get_channels_by_fofa
from updates.hotel import get_channels_by_hotel
from updates.multicast import get_channels_by_multicast
from updates.online_search import get_channels_by_online_search
from updates.subscribe import get_channels_by_subscribe_urls


class UpdateSource:
    def __init__(self):
        self.channel_items = {}
        self.hotel_fofa_result = {}
        self.hotel_foodie_result = {}
        self.multicast_result = {}
        self.subscribe_result = {}
        self.online_search_result = {}
        self.channel_data = {}

    async def visit_page(self, channel_names):
        tasks_config = [
            ("hotel_fofa", get_channels_by_fofa, "hotel_fofa_result"),
            ("multicast", get_channels_by_multicast, "multicast_result"),
            ("hotel_foodie", get_channels_by_hotel, "hotel_foodie_result"),
            ("subscribe", get_channels_by_subscribe_urls, "subscribe_result"),
            ("online_search", get_channels_by_online_search, "online_search_result"),
        ]

        for setting, task_func, result_attr in tasks_config:
            if (setting == "hotel_foodie" or setting == "hotel_fofa") and not config.open_hotel:
                continue
            if config.open_method[setting]:
                task = asyncio.create_task(task_func(channel_names))
                setattr(self, result_attr, await task)

    async def main(self):
        if config.open_update:
            self.channel_items = get_channel_items()
            channel_names = [name for channel_obj in self.channel_items.values() for name in channel_obj.keys()]
            if not channel_names:
                print(f"❌ No channel names found! Please check the {config.source_file}!")
                return
            await self.visit_page(channel_names)
            append_total_data(
                self.channel_items.items(),
                channel_names,
                self.channel_data,
                self.hotel_fofa_result,
                self.multicast_result,
                self.hotel_foodie_result,
                self.subscribe_result,
                self.online_search_result,
            )
            write_channel_to_file(
                self.channel_data,
                first_channel_name=channel_names[0]
            )
            txt_path = os.path.join(config.output_dir, config.final_file)
            convert_to_m3u(path=txt_path, first_channel_name=channel_names[0], data=self.channel_data)
            print(f"🥳 Update completed! Please check the {config.final_file} file!")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    update_source = UpdateSource()
    loop.run_until_complete(update_source.main())
    loop.close()
