"""
复权转换器
"""

from typing import Any, Dict, Optional
from .base import BaseTransformer
from ..base import TransformContext
from ..conversion_rules import ConversionRules


class AdjustTransformer(BaseTransformer):
    """复权转换器"""
    
    ADJUST_KEYS = ["adjust", "fq", "adj"]
    
    def __init__(self):
        super().__init__()
        self.supported_values = ['none', 'qfq', 'hfq']
        self.default_value = ''
    
    def can_transform(self, context: TransformContext) -> bool:
        """检查是否有复权需要转换"""
        return any(key in context.source_params for key in self.ADJUST_KEYS)
    
    def transform(self, context: TransformContext) -> TransformContext:
        """执行复权转换"""
        for key in self.ADJUST_KEYS:
            if context.has_source_key(key):
                value = context.source_params[key]
                if value is not None:
                    converted_value = self._convert_adjust(value)
                    context.set_target_value(key, converted_value)
            else:
                if key in context.accepted_keys:
                    context.set_target_value(key, self.default_value)
        
        return context
    
    def _convert_adjust(self, value: Any) -> Any:
        """转换复权格式"""
        def convert_one(v: Any) -> Any:
            if v is None or (isinstance(v, str) and v.strip() == ""):
                return self.default_value
            
            # 使用ConversionRules统一转换
            converted = ConversionRules.convert_adjust(v)
            if converted == v:  # 如果没有转换，返回原值
                return v
            
            # 如果转换为"none"，返回空字符串
            if converted == "none":
                return ""
            
            return converted
        
        return self._apply_to_value(value, convert_one)
