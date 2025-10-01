"""
自定义日志处理器

提供文件轮转、缓冲等高级日志处理功能。
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional
from .formatters import create_formatter, create_console_formatter


def create_console_handler(config) -> logging.StreamHandler:
    """
    创建控制台处理器
    
    Args:
        config: 日志配置
        
    Returns:
        logging.StreamHandler: 控制台处理器
    """
    handler = logging.StreamHandler()
    handler.setLevel(config.get_console_level())
    
    # 设置格式化器
    formatter = create_console_formatter(config)
    handler.setFormatter(formatter)
    
    return handler


def create_file_handler(config) -> Optional[logging.Handler]:
    """
    创建文件处理器
    
    Args:
        config: 日志配置
        
    Returns:
        Optional[logging.Handler]: 文件处理器，如果未配置文件路径则返回None
    """
    file_path = config.get_file_path()
    if not file_path:
        return None
    
    # 创建轮转文件处理器
    handler = logging.handlers.RotatingFileHandler(
        filename=file_path,
        maxBytes=config.max_file_size,
        backupCount=config.backup_count,
        encoding=config.encoding
    )
    
    handler.setLevel(config.get_level())
    
    # 设置格式化器
    formatter = create_formatter(config)
    handler.setFormatter(formatter)
    
    return handler


def create_timed_file_handler(config) -> Optional[logging.Handler]:
    """
    创建按时间轮转的文件处理器
    
    Args:
        config: 日志配置
        
    Returns:
        Optional[logging.Handler]: 时间轮转文件处理器
    """
    file_path = config.get_file_path()
    if not file_path:
        return None
    
    # 创建按时间轮转的文件处理器
    handler = logging.handlers.TimedRotatingFileHandler(
        filename=file_path,
        when='midnight',
        interval=1,
        backupCount=config.backup_count,
        encoding=config.encoding
    )
    
    handler.setLevel(config.get_level())
    
    # 设置格式化器
    formatter = create_formatter(config)
    handler.setFormatter(formatter)
    
    return handler


def create_buffered_handler(config) -> Optional[logging.Handler]:
    """
    创建缓冲文件处理器
    
    适用于高频日志场景，减少I/O操作。
    
    Args:
        config: 日志配置
        
    Returns:
        Optional[logging.Handler]: 缓冲文件处理器
    """
    file_path = config.get_file_path()
    if not file_path:
        return None
    
    # 创建缓冲文件处理器
    handler = logging.handlers.BufferingHandler(capacity=1000)
    
    # 设置实际的文件处理器
    file_handler = create_file_handler(config)
    if file_handler:
        handler.addHandler(file_handler)
    
    handler.setLevel(config.get_level())
    
    return handler


def create_memory_handler(config) -> logging.Handler:
    """
    创建内存处理器
    
    将日志存储在内存中，适用于调试和测试场景。
    
    Args:
        config: 日志配置
        
    Returns:
        logging.Handler: 内存处理器
    """
    handler = logging.handlers.MemoryHandler(
        capacity=1000,
        flushLevel=logging.ERROR
    )
    
    handler.setLevel(config.get_level())
    
    # 设置格式化器
    formatter = create_formatter(config)
    handler.setFormatter(formatter)
    
    return handler


def setup_handlers(logger: logging.Logger, config) -> None:
    """
    为logger设置处理器
    
    Args:
        logger: 要设置的logger
        config: 日志配置
    """
    # 清除现有处理器
    logger.handlers.clear()
    
    # 添加控制台处理器
    if config.console_enabled:
        console_handler = create_console_handler(config)
        logger.addHandler(console_handler)
    
    # 添加文件处理器
    file_handler = create_file_handler(config)
    if file_handler:
        logger.addHandler(file_handler)
    
    # 设置传播（不传播到父logger，避免重复输出）
    logger.propagate = False
