"""
SQLite存储后端

提供基于SQLite的持久化存储实现
"""

import sqlite3
import pickle
import time
import threading
import os
from typing import Any, Optional, List, Tuple
from contextlib import contextmanager


class SQLiteStorage:
    """SQLite存储后端"""
    
    def __init__(self, db_path: str):
        """初始化SQLite存储"""
        self.db_path = db_path
        self._lock = threading.RLock()
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表 - 永久存储版本"""
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cache_entries (
                    key TEXT PRIMARY KEY,
                    value BLOB NOT NULL,
                    created_at REAL NOT NULL,
                    access_count INTEGER DEFAULT 0,
                    last_access REAL NOT NULL
                )
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_last_access 
                ON cache_entries(last_access)
            ''')
            
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """获取数据库连接的上下文管理器"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        try:
            conn.execute('PRAGMA journal_mode=WAL')
            conn.execute('PRAGMA synchronous=NORMAL')
            conn.execute('PRAGMA cache_size=10000')
            yield conn
        finally:
            conn.close()
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值 - 永久存储，无过期检查"""
        with self._lock:
            with self._get_connection() as conn:
                cursor = conn.execute('''
                    SELECT value, access_count 
                    FROM cache_entries 
                    WHERE key = ?
                ''', (key,))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                value_blob, access_count = row
                current_time = time.time()
                
                # 更新访问统计
                conn.execute('''
                    UPDATE cache_entries 
                    SET access_count = ?, last_access = ?
                    WHERE key = ?
                ''', (access_count + 1, current_time, key))
                conn.commit()
                
                # 反序列化值
                try:
                    return pickle.loads(value_blob)
                except (pickle.PickleError, EOFError):
                    conn.execute('DELETE FROM cache_entries WHERE key = ?', (key,))
                    conn.commit()
                    return None
    
    def set(self, key: str, value: Any) -> None:
        """设置缓存值 - 永久存储"""
        with self._lock:
            try:
                value_blob = pickle.dumps(value)
                current_time = time.time()
                
                with self._get_connection() as conn:
                    conn.execute('''
                        INSERT OR REPLACE INTO cache_entries 
                        (key, value, created_at, access_count, last_access)
                        VALUES (?, ?, ?, 0, ?)
                    ''', (key, value_blob, current_time, current_time))
                    conn.commit()
                    
            except pickle.PickleError:
                pass
    
    def delete(self, key: str) -> bool:
        """删除缓存条目"""
        with self._lock:
            with self._get_connection() as conn:
                cursor = conn.execute('DELETE FROM cache_entries WHERE key = ?', (key,))
                conn.commit()
                return cursor.rowcount > 0
    
    def clear(self) -> None:
        """清空所有缓存"""
        with self._lock:
            with self._get_connection() as conn:
                conn.execute('DELETE FROM cache_entries')
                conn.commit()
    
    def cleanup_expired(self) -> int:
        """清理过期条目 - 由于不再使用TTL，返回0"""
        # 不再需要清理过期缓存，因为缓存是永久的
        return 0
    
    def get_stats(self) -> dict:
        """获取存储统计信息 - 永久存储版本"""
        with self._lock:
            with self._get_connection() as conn:
                cursor = conn.execute('SELECT COUNT(*) FROM cache_entries')
                total_entries = cursor.fetchone()[0]
                
                current_time = time.time()
                
                db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
                
                cursor = conn.execute('''
                    SELECT AVG(access_count), MAX(access_count), MIN(last_access), MAX(last_access)
                    FROM cache_entries
                ''')
                stats_row = cursor.fetchone()
                avg_access = stats_row[0] or 0
                max_access = stats_row[1] or 0
                min_last_access = stats_row[2] or current_time
                max_last_access = stats_row[3] or current_time
                
                return {
                    'total_entries': total_entries,
                    'expired_entries': 0,  # 不再有过期条目
                    'valid_entries': total_entries,
                    'db_size_bytes': db_size,
                    'db_size_mb': db_size / (1024 * 1024),
                    'avg_access_count': round(avg_access, 2),
                    'max_access_count': max_access,
                    'oldest_access_age': current_time - min_last_access,
                    'newest_access_age': current_time - max_last_access
                }
    
    def get_all_keys(self) -> List[str]:
        """获取所有缓存键"""
        with self._lock:
            with self._get_connection() as conn:
                cursor = conn.execute('SELECT key FROM cache_entries')
                return [row[0] for row in cursor.fetchall()]
    
    def get_entries_by_pattern(self, pattern: str) -> List[Tuple[str, Any]]:
        """根据模式获取缓存条目"""
        with self._lock:
            current_time = time.time()
            with self._get_connection() as conn:
                cursor = conn.execute('''
                    SELECT key, value FROM cache_entries 
                    WHERE key LIKE ? AND expires_at > ?
                ''', (pattern, current_time))
                
                results = []
                for key, value_blob in cursor.fetchall():
                    try:
                        value = pickle.loads(value_blob)
                        results.append((key, value))
                    except (pickle.PickleError, EOFError):
                        continue
                
                return results
    
    def vacuum(self) -> None:
        """压缩数据库以回收空间"""
        with self._lock:
            with self._get_connection() as conn:
                conn.execute('VACUUM')
                conn.commit()
    
    def close(self) -> None:
        """关闭数据库连接"""
        pass