"""
周期转换器
"""

import re
from typing import Any, Dict, Optional
from .base import BaseTransformer
from ..base import TransformContext


class PeriodTransformer(BaseTransformer):
    """周期转换器"""
    
    # 周期键名列表
    PERIOD_KEYS = ["period", "freq", "frequency"]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.supported_periods = self._get_config_value('supported_periods', 
                                                       ['daily', '1min', '5min', '15min', '30min', '60min'])
    
    def can_transform(self, context: TransformContext) -> bool:
        """检查是否有周期需要转换"""
        return any(key in context.source_params for key in self.PERIOD_KEYS)
    
    def transform(self, context: TransformContext) -> TransformContext:
        """执行周期转换"""
        for key in self.PERIOD_KEYS:
            if context.has_source_key(key):
                value = context.source_params[key]
                if value is not None:
                    target_format = self._detect_target_format(context, key)
                    converted_value = self._convert_period(value, target_format)
                    context.set_target_value(key, converted_value)
        
        return context
    
    def _convert_period(self, value: Any, target_format: str) -> Any:
        """转换周期格式"""
        def convert_one(v: Any) -> Any:
            if not isinstance(v, (str, int)):
                return v
            
            s = str(v).strip().lower()
            
            # 常见输入：'5m' -> '5'
            m = re.fullmatch(r"(\d+)(m|min|minute)?", s)
            if m:
                if target_format == "numeric":
                    return m.group(1)
                else:
                    return s if s in self.supported_periods else "daily"
            
            if s in {"daily", "day", "d"}:
                return "daily" if target_format != "numeric" else s
            
            # 检查是否在支持的周期列表中
            if s in self.supported_periods:
                return s
            
            return v
        
        return self._apply_to_value(value, convert_one)
    
    def _detect_target_format(self, context: TransformContext, field: str) -> str:
        """检测目标格式"""
        if context.metadata and hasattr(context.metadata, 'example_params'):
            example = context.metadata.example_params
            if field in example:
                return self._analyze_format(example[field])
        
        return "standard"  # 默认格式
    
    def _analyze_format(self, example_period: str) -> str:
        """分析示例周期的格式"""
        if not isinstance(example_period, str):
            return "unknown"
        
        s = example_period.strip()
        if re.fullmatch(r"\d+", s):
            return "numeric"
        else:
            return "standard"
