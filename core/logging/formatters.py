"""
自定义日志格式化器

提供多种日志格式支持，包括标准格式和JSON格式。
"""

import logging
import json
from datetime import datetime
from typing import Any, Dict, Optional


class StockQuantFormatter(logging.Formatter):
    """
    StockQuant专用日志格式化器
    
    支持标准格式和JSON格式两种输出模式。
    """
    
    def __init__(self, 
                 use_json: bool = False,
                 include_module_info: bool = True,
                 date_format: Optional[str] = None):
        """
        初始化格式化器
        
        Args:
            use_json: 是否使用JSON格式
            include_module_info: 是否包含模块信息
            date_format: 日期格式，如果为None则使用默认格式
        """
        self.use_json = use_json
        self.include_module_info = include_module_info
        
        if use_json:
            # JSON格式不需要设置fmt和datefmt
            super().__init__()
        else:
            # 标准格式
            if date_format is None:
                date_format = "%Y-%m-%d %H:%M:%S"
            
            fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            if include_module_info:
                fmt = "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s"
            
            super().__init__(fmt=fmt, datefmt=date_format)
    
    def format(self, record: logging.LogRecord) -> str:
        """
        格式化日志记录
        
        Args:
            record: 日志记录
            
        Returns:
            str: 格式化后的日志字符串
        """
        if self.use_json:
            return self._format_json(record)
        else:
            return super().format(record)
    
    def _format_json(self, record: logging.LogRecord) -> str:
        """
        JSON格式日志
        
        Args:
            record: 日志记录
            
        Returns:
            str: JSON格式的日志字符串
        """
        # 基础日志数据
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "logger": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
        }
        
        # 添加模块信息
        if self.include_module_info:
            log_data.update({
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
                "pathname": record.pathname,
            })
        
        # 添加线程信息
        if record.thread:
            log_data["thread"] = record.thread
        if record.threadName:
            log_data["thread_name"] = record.threadName
        
        # 添加进程信息
        if record.process:
            log_data["process"] = record.process
        if record.processName:
            log_data["process_name"] = record.processName
        
        # 添加异常信息
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # 添加额外字段
        if hasattr(record, 'extra_fields') and record.extra_fields:
            log_data.update(record.extra_fields)
        
        return json.dumps(log_data, ensure_ascii=False, separators=(',', ':'))
    
    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
        """
        格式化时间
        
        Args:
            record: 日志记录
            datefmt: 日期格式
            
        Returns:
            str: 格式化后的时间字符串
        """
        if self.use_json:
            # JSON格式使用ISO格式时间
            return datetime.fromtimestamp(record.created).isoformat()
        else:
            # 标准格式使用父类方法
            return super().formatTime(record, datefmt)


class ColoredFormatter(StockQuantFormatter):
    """
    彩色控制台格式化器
    
    在控制台输出时使用颜色区分不同级别的日志。
    """
    
    # ANSI颜色代码
    COLORS = {
        'DEBUG': '\033[36m',      # 青色
        'INFO': '\033[32m',       # 绿色
        'WARNING': '\033[33m',    # 黄色
        'ERROR': '\033[31m',      # 红色
        'CRITICAL': '\033[35m',   # 紫色
        'RESET': '\033[0m'        # 重置
    }
    
    def __init__(self, *args, use_colors=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_colors = use_colors
    
    def format(self, record: logging.LogRecord) -> str:
        """
        格式化日志记录并添加颜色
        
        Args:
            record: 日志记录
            
        Returns:
            str: 带颜色的格式化日志字符串
        """
        if not self.use_colors or self.use_json:
            return super().format(record)
        
        # 获取基础格式
        formatted = super().format(record)
        
        # 添加颜色
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        return f"{color}{formatted}{reset}"


def create_formatter(config) -> logging.Formatter:
    """
    根据配置创建格式化器
    
    Args:
        config: 日志配置
        
    Returns:
        logging.Formatter: 格式化器实例
    """
    if config.use_json_format:
        return StockQuantFormatter(
            use_json=True,
            include_module_info=config.include_module_info
        )
    else:
        return StockQuantFormatter(
            use_json=False,
            include_module_info=config.include_module_info
        )


def create_console_formatter(config) -> logging.Formatter:
    """
    根据配置创建控制台格式化器
    
    Args:
        config: 日志配置
        
    Returns:
        logging.Formatter: 控制台格式化器实例
    """
    if config.use_json_format:
        return StockQuantFormatter(
            use_json=True,
            include_module_info=config.include_module_info
        )
    else:
        return ColoredFormatter(
            use_json=False,
            include_module_info=config.include_module_info,
            use_colors=True
        )
