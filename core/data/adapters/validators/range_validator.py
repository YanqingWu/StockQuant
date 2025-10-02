"""
范围验证器
"""

from typing import Any, Dict, Optional
from .base import BaseValidator
from ..base import TransformContext


class RangeValidator(BaseValidator):
    """范围验证器"""
    
    def __init__(self):
        super().__init__()
        self.range_rules = {}
    
    def can_validate(self, context: TransformContext) -> bool:
        """检查是否可以验证"""
        return bool(self.range_rules)
    
    def validate(self, context: TransformContext) -> bool:
        """执行范围验证"""
        for field, rules in self.range_rules.items():
            if field in context.target_params:
                value = context.target_params[field]
                if not self._validate_field_range(field, value, rules):
                    raise ValueError(f"参数 {field} 超出有效范围: {value}")
        
        return True
    
    def _validate_field_range(self, field: str, value: Any, rules: Dict[str, Any]) -> bool:
        """验证单个字段的范围"""
        if value is None:
            return True  # None值由必填验证器处理
        
        # 检查最小值
        min_value = rules.get('min_value')
        if min_value is not None and isinstance(value, (int, float)):
            if value < min_value:
                return False
        
        # 检查最大值
        max_value = rules.get('max_value')
        if max_value is not None and isinstance(value, (int, float)):
            if value > max_value:
                return False
        
        # 检查字符串长度范围
        min_length = rules.get('min_length')
        if min_length is not None and isinstance(value, str):
            if len(value) < min_length:
                return False
        
        max_length = rules.get('max_length')
        if max_length is not None and isinstance(value, str):
            if len(value) > max_length:
                return False
        
        return True
