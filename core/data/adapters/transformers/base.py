"""
转换器基类
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from ..base import TransformContext, ParameterTransformer


class BaseTransformer(ParameterTransformer):
    """转换器基类，提供通用功能"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
    
    def _get_config_value(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self.config.get(key, default)
    
    def _apply_to_value(self, value: Any, fn) -> Any:
        """支持列表与逗号分隔字符串的转换"""
        if isinstance(value, list):
            return [fn(v) for v in value]
        if isinstance(value, str) and "," in value:
            parts = [p.strip() for p in value.split(",") if p.strip()]
            if all(p for p in parts):
                return ",".join(str(fn(p)) for p in parts)
        return fn(value)
    
    def _detect_target_format(self, context: TransformContext, field: str) -> str:
        """检测目标格式"""
        if context.metadata and hasattr(context.metadata, 'example_params'):
            example = context.metadata.example_params
            if field in example:
                return self._analyze_format(example[field])
        return self._get_config_value('default_format', 'dot')
    
    def _analyze_format(self, example_value: str) -> str:
        """分析示例值的格式"""
        # 子类可以重写此方法
        return 'unknown'
