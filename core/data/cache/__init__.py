"""
缓存模块 - 提供持久化缓存功能

提供完整的缓存解决方案，包括持久化缓存实现和管理工具
"""

from .cache_config import CacheConfig, PersistentCacheConfig
from .persistent_cache import PersistentCache
from .cache_manager import CacheManager, CacheStats
from .storage import SQLiteStorage

# 导入日志系统
from core.logging import get_logger

# 模块级logger
logger = get_logger(__name__)

__all__ = [
    'CacheConfig',
    'PersistentCacheConfig', 
    'PersistentCache',
    'CacheManager',
    'CacheStats',
    'SQLiteStorage'
]