"""
统一日志管理器

提供单例模式的日志管理，支持动态配置更新。
"""

import logging
import threading
from typing import Optional, Dict, Any
from .config import LoggingConfig
from .handlers import setup_handlers


class LoggingManager:
    """
    统一日志管理器 - 单例模式
    
    负责管理整个应用的日志配置和logger实例。
    支持环境变量配置和动态配置更新。
    """
    
    _instance: Optional['LoggingManager'] = None
    _initialized: bool = False
    _lock = threading.Lock()
    
    def __new__(cls) -> 'LoggingManager':
        """单例模式实现"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化日志管理器"""
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self.config = LoggingConfig.from_env()
                    self._loggers: Dict[str, logging.Logger] = {}
                    self._setup_root_logger()
                    LoggingManager._initialized = True
    
    def _setup_root_logger(self) -> None:
        """设置根logger"""
        root_logger = logging.getLogger()
        root_logger.setLevel(self.config.get_level())
        
        # 清除现有处理器
        root_logger.handlers.clear()
        
        # 设置处理器
        setup_handlers(root_logger, self.config)
        
        # 设置传播（根logger需要传播）
        root_logger.propagate = True
    
    def get_logger(self, name: str) -> logging.Logger:
        """
        获取指定名称的logger
        
        Args:
            name: logger名称，通常使用 __name__
            
        Returns:
            logging.Logger: 配置好的logger实例
        """
        if name not in self._loggers:
            with self._lock:
                if name not in self._loggers:
                    logger = logging.getLogger(name)
                    logger.setLevel(self.config.get_level())
                    
                    # 为特定logger设置处理器（如果与根logger不同）
                    if name != 'root':
                        setup_handlers(logger, self.config)
                    
                    self._loggers[name] = logger
        
        return self._loggers[name]
    
    def update_config(self, new_config: LoggingConfig) -> None:
        """
        动态更新日志配置
        
        Args:
            new_config: 新的日志配置
        """
        if not new_config.is_valid():
            raise ValueError("Invalid logging configuration")
        
        with self._lock:
            self.config = new_config
            
            # 更新根logger
            self._setup_root_logger()
            
            # 更新所有已创建的logger
            for logger in self._loggers.values():
                logger.setLevel(self.config.get_level())
                setup_handlers(logger, self.config)
    
    def get_logger_info(self, name: str) -> Dict[str, Any]:
        """
        获取logger的详细信息
        
        Args:
            name: logger名称
            
        Returns:
            Dict[str, Any]: logger信息字典
        """
        logger = self.get_logger(name)
        
        return {
            'name': logger.name,
            'level': logging.getLevelName(logger.level),
            'handlers': [str(h) for h in logger.handlers],
            'propagate': logger.propagate,
            'parent': logger.parent.name if logger.parent else None,
            'disabled': logger.disabled
        }
    
    def get_all_loggers(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有logger的信息
        
        Returns:
            Dict[str, Dict[str, Any]]: 所有logger的信息
        """
        return {name: self.get_logger_info(name) for name in self._loggers.keys()}
    
    def clear_loggers(self) -> None:
        """清除所有logger缓存"""
        with self._lock:
            self._loggers.clear()
    
    def reset(self) -> None:
        """重置日志管理器"""
        with self._lock:
            self.config = LoggingConfig.from_env()
            self._loggers.clear()
            self._setup_root_logger()
    
    def get_config(self) -> LoggingConfig:
        """
        获取当前配置
        
        Returns:
            LoggingConfig: 当前配置实例
        """
        return self.config
    
    def is_configured(self) -> bool:
        """
        检查是否已配置
        
        Returns:
            bool: 是否已配置
        """
        return self._initialized and self.config.is_valid()
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"LoggingManager(config={self.config}, loggers={len(self._loggers)})"
    
    def __repr__(self) -> str:
        """详细字符串表示"""
        return (f"LoggingManager(config={self.config}, "
                f"loggers={list(self._loggers.keys())}, "
                f"initialized={self._initialized})")
