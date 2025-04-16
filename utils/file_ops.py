import os
import configparser
from typing import List, Dict

class FileOps:
    """文件操作工具类"""
    
    @staticmethod
    def read_text_file(file_path: str) -> List[str]:
        """读取文本文件，忽略空行和注释行（#开头）"""
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
            return [line for line in lines if line and not line.startswith('#')]
    
    @staticmethod
    def create_directory(dir_path: str):
        """创建目录（递归创建）"""
        os.makedirs(dir_path, exist_ok=True)
    
    @staticmethod
    def write_text_file(file_path: str, content: str):
        """写入文本文件，自动创建父目录"""
        FileOps.create_directory(os.path.dirname(file_path))
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    @staticmethod
    def read_config(file_path: str) -> configparser.ConfigParser:
        """读取配置文件"""
        config = configparser.ConfigParser()
        config.read(file_path, encoding='utf-8')
        return config
