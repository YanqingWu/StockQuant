"""
日志配置管理模块

提供日志配置类和环境变量支持。
"""

import os
import logging
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class LoggingConfig:
    """
    日志配置类
    
    支持从环境变量读取配置，提供默认值。
    """
    
    # 基本配置
    level: str = "INFO"
    file_path: Optional[str] = None
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 文件配置
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    encoding: str = "utf-8"
    
    # 控制台配置
    console_enabled: bool = True
    console_level: Optional[str] = None  # 如果为None，使用level
    
    # 高级配置
    use_json_format: bool = False
    include_module_info: bool = True
    
    @classmethod
    def from_env(cls) -> 'LoggingConfig':
        """
        从环境变量创建配置
        
        支持的环境变量：
        - STOCKQUANT_LOG_LEVEL: 日志级别 (DEBUG/INFO/WARNING/ERROR/CRITICAL)
        - STOCKQUANT_LOG_FILE: 日志文件路径
        - STOCKQUANT_LOG_FORMAT: 日志格式 (standard/json)
        - STOCKQUANT_LOG_CONSOLE: 是否启用控制台输出 (true/false)
        - STOCKQUANT_LOG_MAX_SIZE: 最大文件大小 (MB)
        - STOCKQUANT_LOG_BACKUP_COUNT: 备份文件数量
        
        Returns:
            LoggingConfig: 配置实例
        """
        # 读取日志级别
        log_level = os.getenv('STOCKQUANT_LOG_LEVEL', 'INFO').upper()
        if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            log_level = 'INFO'
        
        # 读取日志文件路径
        log_file = os.getenv('STOCKQUANT_LOG_FILE')
        
        # 读取日志格式
        log_format = os.getenv('STOCKQUANT_LOG_FORMAT', 'standard').lower()
        use_json = log_format == 'json'
        
        # 读取控制台配置
        console_enabled = os.getenv('STOCKQUANT_LOG_CONSOLE', 'true').lower() == 'true'
        
        # 读取文件大小配置
        try:
            max_size_mb = int(os.getenv('STOCKQUANT_LOG_MAX_SIZE', '10'))
            max_file_size = max_size_mb * 1024 * 1024
        except (ValueError, TypeError):
            max_file_size = 10 * 1024 * 1024
        
        # 读取备份数量配置
        try:
            backup_count = int(os.getenv('STOCKQUANT_LOG_BACKUP_COUNT', '5'))
            backup_count = max(0, backup_count)
        except (ValueError, TypeError):
            backup_count = 5
        
        # 根据格式选择默认格式字符串
        if use_json:
            default_format = 'json'
        else:
            default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        return cls(
            level=log_level,
            file_path=log_file,
            format=default_format,
            max_file_size=max_file_size,
            backup_count=backup_count,
            console_enabled=console_enabled,
            use_json_format=use_json,
            include_module_info=True
        )
    
    def get_level(self) -> int:
        """
        获取日志级别数值
        
        Returns:
            int: logging模块的级别常量
        """
        return getattr(logging, self.level, logging.INFO)
    
    def get_console_level(self) -> int:
        """
        获取控制台日志级别数值
        
        Returns:
            int: logging模块的级别常量
        """
        if self.console_level:
            return getattr(logging, self.console_level, logging.INFO)
        return self.get_level()
    
    def get_file_path(self) -> Optional[Path]:
        """
        获取日志文件路径
        
        Returns:
            Optional[Path]: 日志文件路径，如果未配置则返回None
        """
        if not self.file_path:
            return None
        
        file_path = Path(self.file_path)
        # 确保目录存在
        file_path.parent.mkdir(parents=True, exist_ok=True)
        return file_path
    
    def is_valid(self) -> bool:
        """
        验证配置是否有效
        
        Returns:
            bool: 配置是否有效
        """
        try:
            # 验证日志级别
            level = self.get_level()
            if level not in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]:
                return False
            
            # 验证文件路径（如果提供）
            if self.file_path:
                file_path = self.get_file_path()
                if not file_path:
                    return False
                # 检查父目录是否可写
                try:
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                except Exception:
                    return False
            
            # 验证文件大小
            if self.max_file_size <= 0:
                return False
            
            # 验证备份数量
            if self.backup_count < 0:
                return False
            
            return True
            
        except Exception:
            return False
    
    def to_dict(self) -> dict:
        """
        转换为字典格式
        
        Returns:
            dict: 配置字典
        """
        return {
            'level': self.level,
            'file_path': self.file_path,
            'format': self.format,
            'max_file_size': self.max_file_size,
            'backup_count': self.backup_count,
            'encoding': self.encoding,
            'console_enabled': self.console_enabled,
            'console_level': self.console_level,
            'use_json_format': self.use_json_format,
            'include_module_info': self.include_module_info
        }
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"LoggingConfig(level={self.level}, file={self.file_path}, format={self.format})"
