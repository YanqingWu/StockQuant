"""
验证器基类
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..base import TransformContext, ParameterValidator


class BaseValidator(ParameterValidator):
    """验证器基类，提供通用功能"""
    
    def __init__(self):
        pass
    
    def _is_empty_value(self, value: Any) -> bool:
        """检查值是否为空"""
        if value is None:
            return True
        if isinstance(value, str) and value.strip() == "":
            return True
        if isinstance(value, list) and len(value) == 0:
            return True
        return False
