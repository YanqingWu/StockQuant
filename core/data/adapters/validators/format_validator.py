"""
格式验证器
"""

import re
from typing import Any, Dict, Optional, List
from .base import BaseValidator
from ..base import TransformContext
from ..exceptions import ParameterValidationError


class FormatValidator(BaseValidator):
    """格式验证器"""
    
    def __init__(self):
        super().__init__()
        # 只验证股票代码和日期格式，其他参数不限制
    
    def can_validate(self, context: TransformContext) -> bool:
        """检查是否可以验证"""
        return bool(context.target_params)
    
    def validate(self, context: TransformContext) -> bool:
        """执行格式验证"""
        # 验证股票代码格式
        if 'symbol' in context.target_params:
            value = context.target_params['symbol']
            if not self._validate_symbol_format(value):
                raise ParameterValidationError('symbol', value, "股票代码格式错误")
        
        # 验证日期格式
        for field in ['date', 'trade_date', 'start_date', 'end_date']:
            if field in context.target_params:
                value = context.target_params[field]
                if not self._validate_date_format(value):
                    raise ParameterValidationError(field, value, "日期格式错误")
        
        return True
    
    
    def _validate_symbol_format(self, value: Any) -> bool:
        """使用 StockSymbol 验证股票代码格式"""
        if not value:
            return True
        
        try:
            from ..stock_symbol import StockSymbol
            StockSymbol.parse(value)
            return True
        except Exception:
            return False
    
    def _validate_date_format(self, value: Any) -> bool:
        """验证日期格式"""
        if not value:
            return True
        
        if not isinstance(value, str):
            return False
        
        date_patterns = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{8}$',              # YYYYMMDD
            r'^\d{4}/\d{2}/\d{2}$',  # YYYY/MM/DD
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, value.strip()):
                return True
        
        return False
