"""
数据提取器类型定义
"""

from dataclasses import dataclass
from typing import Any, Optional, List


@dataclass
class ExtractionResult:
    """提取结果"""
    success: bool
    data: Any
    error: Optional[str] = None
    interface_name: Optional[str] = None
    source_interface: Optional[str] = None
    extracted_fields: Optional[List[str]] = None
