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
        # 如果没有配置规则，跳过验证
        if not self.format_rules:
            return True
            
        for field, rules in self.format_rules.items():
            if field in context.target_params:
                value = context.target_params[field]
                if not self._validate_field_format(field, value, rules, context):
                    # 对于日期格式，尝试更宽松的验证
                    if field in ['date', 'trade_date', 'start_date', 'end_date']:
                        if self._is_valid_date_format(value):
                            continue  # 日期格式可以接受，跳过严格验证
                    raise ValueError(f"参数 {field} 格式不正确: {value}")
        
        return True
    
    def _validate_field_format(self, field: str, value: Any, rules: Dict[str, Any], context: TransformContext = None) -> bool:
        """验证单个字段的格式"""
        if value is None:
            return True  # None值由必填验证器处理
        
        # 检查类型
        expected_type = rules.get('type')
        if expected_type and not isinstance(value, expected_type):
            return False
        
        # 检查正则表达式
        pattern = rules.get('pattern')
        if pattern and isinstance(value, str):
            if not re.match(pattern, value):
                return False
        
        # 检查长度
        min_length = rules.get('min_length')
        if min_length and isinstance(value, str) and len(value) < min_length:
            return False
        
        max_length = rules.get('max_length')
        if max_length and isinstance(value, str) and len(value) > max_length:
            return False
        
        # 检查枚举值
        valid_values = rules.get('valid_values')
        if valid_values and value not in valid_values:
            return False
        
        return True
    
    def _is_valid_date_format(self, value: Any) -> bool:
        """检查是否为有效的日期格式（宽松验证）"""
        if not isinstance(value, str):
            return False
        
        # 支持多种日期格式
        date_patterns = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{8}$',              # YYYYMMDD
            r'^\d{4}/\d{2}/\d{2}$',  # YYYY/MM/DD
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, value.strip()):
                return True
        
        return False
