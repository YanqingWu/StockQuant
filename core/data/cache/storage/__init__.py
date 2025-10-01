"""
存储后端模块

提供不同的存储后端实现：
- SQLiteStorage: SQLite数据库存储
"""

from .sqlite_storage import SQLiteStorage

__all__ = ['SQLiteStorage']