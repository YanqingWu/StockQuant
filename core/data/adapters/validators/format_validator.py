"""
格式验证器
"""

import re
from typing import Any, Dict, Optional, List
from .base import BaseValidator
from ..base import TransformContext


class FormatValidator(BaseValidator):
    """格式验证器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.format_rules = self._get_config_value('format_rules', {})
    
    def can_validate(self, context: TransformContext) -> bool:
        """检查是否可以验证"""
        return bool(self.format_rules)
    
    def validate(self, context: TransformContext) -> bool:
        """执行格式验证"""
        if not self.format_rules:
            return True
            
        for field, rules in self.format_rules.items():
            if field in context.target_params:
                value = context.target_params[field]
                if not self._validate_field_format(field, value, rules, context):
                    if field in ['date', 'trade_date', 'start_date', 'end_date']:
                        if self._is_valid_date_format(value):
                            continue
                    raise ValueError(f"参数 {field} 格式不正确: {value}")
        
        return True
    
    def _validate_field_format(self, field: str, value: Any, rules: Dict[str, Any], context: TransformContext = None) -> bool:
        """验证单个字段的格式"""
        if value is None:
            return True
        
        expected_type = rules.get('type')
        if expected_type and not isinstance(value, expected_type):
            return False
        
        pattern = rules.get('pattern')
        if pattern and isinstance(value, str):
            if not re.match(pattern, value):
                return False
        
        min_length = rules.get('min_length')
        if min_length and isinstance(value, str) and len(value) < min_length:
            return False
        
        max_length = rules.get('max_length')
        if max_length and isinstance(value, str) and len(value) > max_length:
            return False
        
        valid_values = rules.get('valid_values')
        if valid_values and value not in valid_values:
            return False
        
        return True
    
    def _is_valid_date_format(self, value: Any) -> bool:
        """检查是否为有效的日期格式"""
        if not isinstance(value, str):
            return False
        
        date_patterns = [
            r'^\d{4}-\d{2}-\d{2}$',
            r'^\d{8}$',
            r'^\d{4}/\d{2}/\d{2}$',
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, value.strip()):
                return True
        
        return False
