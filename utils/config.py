import os

class Config:
    def __init__(self):
        self.open_update = True
        self.open_hotel = True
        self.open_method = {
            "hotel_fofa": True,
            "multicast": True,
            "hotel_foodie": True,
            "subscribe": True,
            "online_search": True
        }
        self.source_file = "config/source.txt"
        self.final_file = "result.txt"
        self.output_dir = "output"
        self.cdn_url = ""
        self.ipv6_support = False
        self.open_sort = True
        self.open_history = True
        self.open_service = False
        self.open_local = True
        self.open_rtmp = True


config = Config()
