"""
时间转换器
"""

import re
from typing import Any, Dict, Optional
from .base import BaseTransformer
from ..base import TransformContext


class TimeTransformer(BaseTransformer):
    """时间转换器"""
    
    # 时间键名列表
    TIME_KEYS = ["start_time", "end_time"]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.supported_formats = self._get_config_value('supported_formats', ['h:m:s', 'hms'])
    
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
    
    def _apply_to_value(self, value: Any, fn) -> Any:
        """支持列表与逗号分隔字符串的转换"""
        if isinstance(value, list):
            return [fn(v) for v in value]
        if isinstance(value, str) and "," in value:
            parts = [p.strip() for p in value.split(",")]
            if all(p for p in parts):
                return ",".join(str(fn(p)) for p in parts)
        return fn(value)
    
    def _detect_target_format(self, context: TransformContext, field: str) -> str:
        """检测目标格式"""
        if context.metadata and hasattr(context.metadata, 'example_params'):
            example = context.metadata.example_params
            if field in example:
                return self._analyze_format(example[field])
        
        return "h:m:s"  # 默认格式
    
    def _analyze_format(self, example_time: str) -> str:
        """分析示例时间的格式"""
        if not isinstance(example_time, str):
            return "unknown"
        
        s = example_time.strip()
        if re.fullmatch(r"\d{2}:\d{2}:\d{2}", s):
            return "h:m:s"
        if re.fullmatch(r"\d{6}", s):
            return "hms"
        
        return "unknown"
