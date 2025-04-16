import os
import configparser
from typing import List

def read_lines(file_path: str) -> List[str]:
    """读取文本文件每行内容，忽略空行和注释行"""
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
        return [line for line in lines if line and not line.startswith('#')]

def create_dir(dir_path: str):
    """创建目录（递归创建）"""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

def write_file(file_path: str, content: str):
    """写入文件（自动创建父目录）"""
    create_dir(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def read_config(config_path: str) -> configparser.ConfigParser:
    """读取配置文件"""
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config
