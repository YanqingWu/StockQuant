"""
提取器常量定义
避免硬编码和魔法数字
"""

from pathlib import Path
from typing import Union, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExtractorConstants:
    """提取器常量定义"""
    # 配置文件相关
    DEFAULT_CONFIG_FILE = "extraction_config.yaml"
    CONFIG_FILE_ENV_VAR = "EXTRACTION_CONFIG_PATH"
    
    # 数据验证相关
    MIN_SYMBOL_LENGTH = 6
    MAX_MEMORY_MB = 500
    MAX_RETRY_ATTEMPTS = 3
    
    # 超时和重试相关
    DEFAULT_TIMEOUT = 30
    DEFAULT_RETRY_COUNT = 3
    
    # 日期格式相关
    SUPPORTED_DATE_FORMATS = [
        '%Y%m%d',      # 20230922
        '%Y-%m-%d',    # 2023-09-22
        '%Y/%m/%d',    # 2023/09/22
        '%Y.%m.%d',    # 2023.09.22
        '%m/%d/%Y',    # 09/22/2023
        '%d/%m/%Y',    # 22/09/2023
    ]
    
    # 股票代码前缀
    STOCK_CODE_PREFIXES = ('sz', 'sh', 'bj')
    
    # 市场代码
    MARKET_CODES = {
        'sz': 'SZ',
        'sh': 'SH', 
        'bj': 'BJ'
    }


class ExtractionContext:
    """提取上下文管理器，避免实例变量污染"""
    
    def __init__(self, params: Union[Dict[str, Any], Any]):
        self.params = params
        self.start_time = datetime.now()
        self.interface_name = None
        self.category = None
        self.data_type = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 清理资源
        self.params = None
        self.interface_name = None
        self.category = None
        self.data_type = None
    
    def set_extraction_info(self, category: str, data_type: str, interface_name: str = None):
        """设置提取信息"""
        self.category = category
        self.data_type = data_type
        self.interface_name = interface_name
    
    def get_elapsed_time(self) -> float:
        """获取已用时间（秒）"""
        return (datetime.now() - self.start_time).total_seconds()


def get_default_config_path() -> Path:
    """获取默认配置文件路径"""
    import os
    
    # 优先从环境变量获取
    env_path = os.getenv(ExtractorConstants.CONFIG_FILE_ENV_VAR)
    if env_path:
        return Path(env_path)
    
    # 使用默认路径
    current_dir = Path(__file__).parent
    return current_dir / ExtractorConstants.DEFAULT_CONFIG_FILE
