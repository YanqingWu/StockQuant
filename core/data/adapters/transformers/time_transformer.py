"""
时间转换器
"""

import re
from typing import Any, Dict, Optional
from .base import BaseTransformer
from ..base import TransformContext
from ..conversion_rules import ConversionRules


class TimeTransformer(BaseTransformer):
    """时间转换器"""
    
    TIME_KEYS = ["start_time", "end_time"]
    START_TIME_KEYS = ["start_time"]
    END_TIME_KEYS = ["end_time"]
    
    def __init__(self):
        super().__init__()
    
    def can_transform(self, context: TransformContext) -> bool:
        """检查是否有时间需要转换"""
        return any(key in context.source_params for key in self.TIME_KEYS)
    
    def transform(self, context: TransformContext) -> TransformContext:
        """执行时间转换"""
        for key in self.TIME_KEYS:
            if context.has_source_key(key):
                value = context.source_params[key]
                if value is not None:
                    target_format = self._detect_target_format(context, key)
                    converted_value = self._convert_time(value, target_format)
                    context.set_target_value(key, converted_value)
        
        return context
    
    def _convert_time(self, value: Any, target_format: str) -> Any:
        """转换时间格式"""
        def convert_one(v: Any) -> Any:
            # 使用ConversionRules统一转换
            converted = ConversionRules.convert_time(v, target_format)
            if converted != v:  # 如果转换成功
                return converted
            
            # 如果ConversionRules无法处理，使用原有逻辑作为后备
            if not isinstance(v, str):
                return v
            
            s = v.strip()
            if not s:
                return v
            
            if re.fullmatch(r"\d{2}:\d{2}:\d{2}", s):
                hh, mm, ss = s.split(":")
            elif re.fullmatch(r"\d{6}", s):
                hh, mm, ss = s[0:2], s[2:4], s[4:6]
            else:
                return v
            
            if target_format == "hms":
                return f"{hh}{mm}{ss}"
            else:  # h:m:s
                return f"{hh}:{mm}:{ss}"
        
        return self._apply_to_value(value, convert_one)
    
    def _detect_target_format(self, context: TransformContext, field: str) -> str:
        """检测目标格式"""
        if context.metadata and context.metadata.example_params:
            example = context.metadata.example_params
            if field in example:
                return self._analyze_format(example[field])
        
        return "h:m:s"
    
    def _analyze_format(self, example_time: str) -> str:
        """分析示例时间的格式"""
        return ConversionRules.detect_time_format(example_time)
