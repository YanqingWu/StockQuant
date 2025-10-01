"""
缓存配置模块

提供缓存系统的配置类，包括基础配置和持久化配置
"""

from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class CacheConfig:
    """基础缓存配置"""
    enabled: bool = True
    ttl: int = 300  # 缓存时间（秒）
    max_size: int = 1000  # 最大缓存条目数


@dataclass 
class PersistentCacheConfig(CacheConfig):
    """持久化缓存配置"""
    
    # 持久化配置
    persistent: bool = True
    db_path: str = "cache.db"
    
    # 内存缓存配置
    memory_cache_size: int = 1000
    
    # 清理配置
    cleanup_interval: int = 3600
    
    def __post_init__(self):
        """初始化后处理"""
        # 确保数据库路径是绝对路径
        if not os.path.isabs(self.db_path):
            self.db_path = os.path.abspath(self.db_path)
            
        # 确保数据库目录存在
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    
    @classmethod
    def from_cache_config(cls, cache_config: CacheConfig, **kwargs) -> 'PersistentCacheConfig':
        """从基础配置创建持久化配置"""
        # 默认启用持久化
        kwargs.setdefault('persistent', True)
        
        return cls(
            enabled=cache_config.enabled,
            ttl=cache_config.ttl,
            max_size=cache_config.max_size,
            **kwargs
        )
    
    def to_cache_config(self) -> CacheConfig:
        """转换为基础CacheConfig（向后兼容）"""
        return CacheConfig(
            enabled=self.enabled,
            ttl=self.ttl,
            max_size=self.max_size
        )