"""
持久化缓存实现

提供完全兼容SimpleCache接口的持久化缓存，支持双层缓存架构
"""

import time
import threading
from typing import Any, Optional, Union
from collections import OrderedDict

from .cache_config import CacheConfig, PersistentCacheConfig
from .storage import SQLiteStorage


class PersistentCache:
    """持久化缓存类 - 完全兼容SimpleCache接口"""
    
    def __init__(self, config: Union[CacheConfig, PersistentCacheConfig]):
        """初始化持久化缓存"""
        # 处理配置兼容性
        if isinstance(config, CacheConfig) and not isinstance(config, PersistentCacheConfig):
            self.config = PersistentCacheConfig.from_cache_config(config, persistent=True)
        else:
            self.config = config
        
        # 强制启用持久化
        self.config.persistent = True
        
        # 线程锁
        self._lock = threading.RLock()
        
        # 初始化存储后端
        self._storage = SQLiteStorage(self.config.db_path)
        
        # 内存LRU缓存
        self._memory_cache: OrderedDict[str, dict] = OrderedDict()
        
        # 统计信息
        self._stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'deletes': 0,
            'memory_hits': 0,
            'storage_hits': 0,
            'evictions': 0
        }
        
        # 启动后台清理线程
        if self.config.cleanup_interval > 0:
            self._start_cleanup_thread()
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值 - 永久存储，无过期检查"""
        if not self.config.enabled:
            return None
        
        with self._lock:
            self._stats['hits'] += 1
            
            # 检查内存缓存
            if key in self._memory_cache:
                entry = self._memory_cache[key]
                self._memory_cache.move_to_end(key)  # LRU更新
                self._stats['memory_hits'] += 1
                return entry['value']
            
            # 检查持久化存储
            value = self._storage.get(key)
            if value is not None:
                self._add_to_memory_cache(key, value)
                self._stats['storage_hits'] += 1
                return value
            
            # 未找到
            self._stats['misses'] += 1
            self._stats['hits'] -= 1
            return None
    
    def set(self, key: str, value: Any) -> None:
        """设置缓存值 - 永久存储"""
        if not self.config.enabled:
            return
        
        with self._lock:
            self._stats['sets'] += 1
            
            # 添加到内存缓存和持久化存储（永久存储）
            self._add_to_memory_cache(key, value)
            self._storage.set(key, value)
    
    def clear(self) -> None:
        """清空缓存"""
        with self._lock:
            self._memory_cache.clear()
            self._storage.clear()
    
    def _add_to_memory_cache(self, key: str, value: Any) -> None:
        """添加条目到内存缓存 - LRU策略，无过期时间"""
        if key in self._memory_cache:
            del self._memory_cache[key]
        
        # 检查内存缓存大小限制
        while len(self._memory_cache) >= self.config.memory_cache_size:
            oldest_key = next(iter(self._memory_cache))
            del self._memory_cache[oldest_key]
            self._stats['evictions'] += 1
        
        # 添加新条目（永久存储）
        self._memory_cache[key] = {
            'value': value
        }
    
    def _start_cleanup_thread(self) -> None:
        """启动后台清理线程 - 由于不再使用TTL，此方法保留但不执行清理"""
        # 不再需要清理过期缓存，因为缓存是永久的
        pass
    
    def _cleanup_expired(self) -> None:
        """清理过期条目 - 由于不再使用TTL，此方法保留但不执行清理"""
        # 不再需要清理过期缓存，因为缓存是永久的
        pass
    
    def delete(self, key: str) -> bool:
        """删除指定缓存条目"""
        with self._lock:
            self._stats['deletes'] += 1
            
            memory_deleted = key in self._memory_cache
            if memory_deleted:
                del self._memory_cache[key]
            
            storage_deleted = self._storage.delete(key)
            
            return memory_deleted or storage_deleted
    
    def get_stats(self) -> dict:
        """获取缓存统计信息"""
        with self._lock:
            storage_stats = self._storage.get_stats()
            
            current_time = time.time()
            memory_expired = sum(
                1 for entry in self._memory_cache.values()
                if current_time > entry['expires_at']
            )
            
            total_requests = self._stats['hits'] + self._stats['misses']
            hit_rate = self._stats['hits'] / total_requests if total_requests > 0 else 0
            
            return {
                'enabled': self.config.enabled,
                'total_requests': total_requests,
                'hits': self._stats['hits'],
                'misses': self._stats['misses'],
                'hit_rate': round(hit_rate, 4),
                'sets': self._stats['sets'],
                'deletes': self._stats['deletes'],
                'memory_hits': self._stats['memory_hits'],
                'storage_hits': self._stats['storage_hits'],
                'evictions': self._stats['evictions'],
                'memory_cache_size': len(self._memory_cache),
                'memory_cache_max_size': self.config.memory_cache_size,
                'memory_cache_expired': memory_expired,
                'memory_cache_valid': len(self._memory_cache) - memory_expired,
                'storage_stats': storage_stats,
                'config': {
                    'ttl': self.config.ttl,
                    'max_size': self.config.max_size,
                    'persistent': self.config.persistent,
                    'cleanup_interval': self.config.cleanup_interval
                }
            }
    
    def get_all_keys(self) -> list:
        """获取所有缓存键"""
        with self._lock:
            memory_keys = set(self._memory_cache.keys())
            storage_keys = set(self._storage.get_all_keys())
            return list(memory_keys | storage_keys)
    
    def cleanup_expired(self) -> int:
        """手动清理过期条目 - 由于不再使用TTL，返回0"""
        # 不再需要清理过期缓存，因为缓存是永久的
        return 0
    
    def reset_stats(self) -> None:
        """重置统计信息"""
        with self._lock:
            self._stats = {
                'hits': 0,
                'misses': 0,
                'sets': 0,
                'deletes': 0,
                'memory_hits': 0,
                'storage_hits': 0,
                'evictions': 0
            }
            
            if hasattr(self._storage, 'reset_stats'):
                self._storage.reset_stats()
    
    def __len__(self) -> int:
        """返回缓存中的条目数量"""
        return len(self.get_all_keys())
    
    def __contains__(self, key: str) -> bool:
        """检查键是否存在于缓存中"""
        return self.get(key) is not None