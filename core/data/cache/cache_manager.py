"""
缓存管理工具

提供缓存统计、监控、清理等管理功能
"""

import time
import threading
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from .persistent_cache import PersistentCache


@dataclass
class CacheStats:
    """缓存统计信息"""
    timestamp: float = field(default_factory=time.time)
    total_requests: int = 0
    hits: int = 0
    misses: int = 0
    hit_rate: float = 0.0
    sets: int = 0
    deletes: int = 0
    memory_hits: int = 0
    storage_hits: int = 0
    evictions: int = 0
    memory_cache_size: int = 0
    storage_entries: int = 0
    storage_size_mb: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'timestamp': self.timestamp,
            'datetime': datetime.fromtimestamp(self.timestamp).isoformat(),
            'total_requests': self.total_requests,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': self.hit_rate,
            'sets': self.sets,
            'deletes': self.deletes,
            'memory_hits': self.memory_hits,
            'storage_hits': self.storage_hits,
            'evictions': self.evictions,
            'memory_cache_size': self.memory_cache_size,
            'storage_entries': self.storage_entries,
            'storage_size_mb': self.storage_size_mb
        }


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache: PersistentCache):
        """初始化缓存管理器"""
        self.cache = cache
        self._lock = threading.RLock()
        self._stats_history: List[CacheStats] = []
        self._max_history_size = 1000
        self._monitoring_enabled = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._monitor_interval = 60
    
    def get_current_stats(self) -> CacheStats:
        """获取当前缓存统计信息"""
        raw_stats = self.cache.get_stats()
        storage_stats = raw_stats.get('storage_stats', {})
        
        return CacheStats(
            timestamp=time.time(),
            total_requests=raw_stats.get('total_requests', 0),
            hits=raw_stats.get('hits', 0),
            misses=raw_stats.get('misses', 0),
            hit_rate=raw_stats.get('hit_rate', 0.0),
            sets=raw_stats.get('sets', 0),
            deletes=raw_stats.get('deletes', 0),
            memory_hits=raw_stats.get('memory_hits', 0),
            storage_hits=raw_stats.get('storage_hits', 0),
            evictions=raw_stats.get('evictions', 0),
            memory_cache_size=raw_stats.get('memory_cache_size', 0),
            storage_entries=storage_stats.get('valid_entries', 0),
            storage_size_mb=storage_stats.get('db_size_mb', 0.0)
        )
    
    def get_detailed_stats(self) -> Dict[str, Any]:
        """获取详细的缓存统计信息"""
        current_stats = self.get_current_stats()
        raw_stats = self.cache.get_stats()
        history_stats = self._calculate_history_stats()
        
        return {
            'current': current_stats.to_dict(),
            'detailed': raw_stats,
            'history': history_stats,
            'health': self.get_health_status(),
            'recommendations': self.get_recommendations()
        }
    
    def _calculate_history_stats(self) -> Dict[str, Any]:
        """计算历史统计信息"""
        with self._lock:
            if len(self._stats_history) < 2:
                return {'available': False, 'reason': 'Insufficient history data'}
            
            current_time = time.time()
            hour_ago = current_time - 3600
            recent_stats = [s for s in self._stats_history if s.timestamp >= hour_ago]
            
            if len(recent_stats) < 2:
                return {'available': False, 'reason': 'Insufficient recent data'}
            
            first_stat = recent_stats[0]
            last_stat = recent_stats[-1]
            time_diff = last_stat.timestamp - first_stat.timestamp
            
            if time_diff <= 0:
                return {'available': False, 'reason': 'Invalid time range'}
            
            requests_per_min = (last_stat.total_requests - first_stat.total_requests) / (time_diff / 60)
            hits_per_min = (last_stat.hits - first_stat.hits) / (time_diff / 60)
            sets_per_min = (last_stat.sets - first_stat.sets) / (time_diff / 60)
            avg_hit_rate = sum(s.hit_rate for s in recent_stats) / len(recent_stats)
            
            return {
                'available': True,
                'time_range_minutes': time_diff / 60,
                'data_points': len(recent_stats),
                'requests_per_minute': round(requests_per_min, 2),
                'hits_per_minute': round(hits_per_min, 2),
                'sets_per_minute': round(sets_per_min, 2),
                'average_hit_rate': round(avg_hit_rate, 4),
                'hit_rate_trend': 'improving' if last_stat.hit_rate > first_stat.hit_rate else 'declining',
                'storage_growth_mb': round(last_stat.storage_size_mb - first_stat.storage_size_mb, 2)
            }
    
    def get_health_status(self) -> Dict[str, Any]:
        """获取缓存健康状态"""
        stats = self.get_current_stats()
        config = self.cache.config
        
        health_issues = []
        health_score = 100
        
        # 检查命中率
        if stats.hit_rate < 0.5:
            health_issues.append("Low hit rate (< 50%)")
            health_score -= 20
        elif stats.hit_rate < 0.7:
            health_issues.append("Moderate hit rate (< 70%)")
            health_score -= 10
        
        # 检查内存缓存使用率
        memory_usage = stats.memory_cache_size / config.memory_cache_size if config.memory_cache_size > 0 else 0
        if memory_usage > 0.9:
            health_issues.append("High memory cache usage (> 90%)")
            health_score -= 15
        
        # 检查驱逐率
        if stats.evictions > stats.sets * 0.1:
            health_issues.append("High eviction rate (> 10% of sets)")
            health_score -= 10
        
        # 确定健康等级
        if health_score >= 90:
            health_level = "excellent"
        elif health_score >= 75:
            health_level = "good"
        elif health_score >= 60:
            health_level = "fair"
        elif health_score >= 40:
            health_level = "poor"
        else:
            health_level = "critical"
        
        return {
            'score': max(0, health_score),
            'level': health_level,
            'issues': health_issues,
            'metrics': {
                'hit_rate': stats.hit_rate,
                'memory_usage_ratio': memory_usage,
                'storage_size_mb': stats.storage_size_mb,
                'eviction_ratio': stats.evictions / max(1, stats.sets)
            }
        }
    
    def get_recommendations(self) -> List[str]:
        """获取优化建议"""
        stats = self.get_current_stats()
        config = self.cache.config
        recommendations = []
        
        if stats.hit_rate < 0.5:
            recommendations.append("Review caching strategy - ensure frequently accessed data is cached")
        
        memory_usage = stats.memory_cache_size / config.memory_cache_size if config.memory_cache_size > 0 else 0
        if memory_usage > 0.8:
            recommendations.append("Consider increasing memory_cache_size for better performance")
        
        if stats.evictions > stats.sets * 0.05:
            recommendations.append("High eviction rate detected - consider increasing cache size")
        
        if stats.storage_hits > stats.memory_hits * 2:
            recommendations.append("Most hits are from storage - consider increasing memory cache size")
        
        return recommendations
    
    def cleanup_cache(self, max_age_hours: Optional[float] = None) -> Dict[str, int]:
        """清理缓存"""
        expired_count = self.cache.cleanup_expired()
        
        result = {
            'expired_entries_removed': expired_count,
            'old_entries_removed': 0
        }
        
        return result
    
    def start_monitoring(self, interval_seconds: int = 60) -> None:
        """启动监控"""
        if self._monitoring_enabled:
            return
        
        self._monitor_interval = interval_seconds
        self._monitoring_enabled = True
        
        def monitor_worker():
            while self._monitoring_enabled:
                try:
                    stats = self.get_current_stats()
                    
                    with self._lock:
                        self._stats_history.append(stats)
                        
                        if len(self._stats_history) > self._max_history_size:
                            self._stats_history = self._stats_history[-self._max_history_size:]
                    
                    time.sleep(self._monitor_interval)
                    
                except Exception:
                    time.sleep(self._monitor_interval)
        
        self._monitor_thread = threading.Thread(target=monitor_worker, daemon=True)
        self._monitor_thread.start()
    
    def stop_monitoring(self) -> None:
        """停止监控"""
        self._monitoring_enabled = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
            self._monitor_thread = None
    
    def export_stats_report(self, include_history: bool = True) -> Dict[str, Any]:
        """导出统计报告"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'cache_config': {
                'enabled': self.cache.config.enabled,
                'max_size': self.cache.config.max_size,
                'persistent': self.cache.config.persistent,
                'memory_cache_size': self.cache.config.memory_cache_size,
                'cleanup_interval': self.cache.config.cleanup_interval
            },
            'current_stats': self.get_current_stats().to_dict(),
            'health_status': self.get_health_status(),
            'recommendations': self.get_recommendations()
        }
        
        if include_history:
            with self._lock:
                report['history'] = [stats.to_dict() for stats in self._stats_history]
                report['history_summary'] = self._calculate_history_stats()
        
        return report
    
    def reset_stats(self) -> None:
        """重置所有统计信息"""
        self.cache.reset_stats()
        with self._lock:
            self._stats_history.clear()