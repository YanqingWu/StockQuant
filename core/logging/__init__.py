"""
StockQuant 统一日志系统

提供统一的日志管理功能，支持环境变量配置和文件输出。
"""

import logging
from .manager import LoggingManager
from .config import LoggingConfig

# 全局日志管理器实例
_logging_manager = LoggingManager()

def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的logger
    
    Args:
        name: logger名称，通常使用 __name__
        
    Returns:
        logging.Logger: 配置好的logger实例
        
    Example:
        >>> from core.logging import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("这是一条日志消息")
    """
    return _logging_manager.get_logger(name)

def update_logging_config(config: LoggingConfig):
    """
    动态更新日志配置
    
    Args:
        config: 新的日志配置
        
    Example:
        >>> from core.logging import update_logging_config, LoggingConfig
        >>> new_config = LoggingConfig(level="DEBUG", file_path="debug.log")
        >>> update_logging_config(new_config)
    """
    _logging_manager.update_config(config)

def get_current_config() -> LoggingConfig:
    """
    获取当前日志配置
    
    Returns:
        LoggingConfig: 当前配置实例
    """
    return _logging_manager.config

# 导出主要接口
__all__ = [
    'get_logger', 
    'update_logging_config', 
    'get_current_config',
    'LoggingConfig',
    'LoggingManager'
]
