"""
日期转换器
"""

import re
from typing import Any, Dict, Optional
from .base import BaseTransformer
from ..base import TransformContext


class DateTransformer(BaseTransformer):
    """日期转换器"""
    
    # 日期键名列表
    DATE_KEYS = ["date", "trade_date", "start_date", "from_date", "begin_date", 
                 "end_date", "to_date", "start_year", "end_year"]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.supported_formats = self._get_config_value('supported_formats', ['y-m-d', 'ymd', 'year'])
    
    def can_transform(self, context: TransformContext) -> bool:
        """检查是否有日期需要转换"""
        return any(key in context.source_params for key in self.DATE_KEYS)
    
    def transform(self, context: TransformContext) -> TransformContext:
        """执行日期转换"""
        for key in self.DATE_KEYS:
            if context.has_source_key(key):
                value = context.source_params[key]
                if value is not None:
                    target_format = self._detect_target_format(context, key)
                    converted_value = self._convert_date(value, target_format)
                    context.set_target_value(key, converted_value)
        
        return context
    
    def _convert_date(self, value: Any, target_format: str) -> Any:
        """转换日期格式"""
        def convert_one(v: Any) -> Any:
            if not isinstance(v, str):
                return v
            
            s = v.strip()
            if not s:
                return v
            
            # 解析日期
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
                y, m, d = s.split("-")
            elif re.fullmatch(r"\d{8}", s):
                y, m, d = s[0:4], s[4:6], s[6:8]
            else:
                return v
            
            # 如果是年份参数，只返回年份
            if target_format == "year":
                return y
            elif target_format == "y-m-d":
                return f"{y}-{m}-{d}"
            elif target_format == "compact":
                return f"{y}{m}{d}"
            else:  # ymd
                return f"{y}{m}{d}"
        
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
        """检测目标格式 - 基于示例参数智能检测，避免硬编码接口名称"""
        # 优先分析示例参数
        if context.metadata and hasattr(context.metadata, 'example_params'):
            example = context.metadata.example_params
            if field in example:
                analyzed_format = self._analyze_format(example[field])
                if analyzed_format != "unknown":
                    return analyzed_format
        
        # 基于字段名称智能推断格式
        if field in ["start_year", "end_year"]:
            return "year"
        
        # 基于示例参数特征智能检测日期格式
        if context.metadata and hasattr(context.metadata, 'example_params'):
            example = context.metadata.example_params
            # 检查示例中是否有紧凑格式的日期
            for key, value in example.items():
                if isinstance(value, str) and re.fullmatch(r"\d{8}", value.strip()):
                    return "compact"
        
        # 默认使用标准格式
        return "y-m-d"
    
    def _analyze_format(self, example_date: str) -> str:
        """分析示例日期的格式"""
        if not isinstance(example_date, str):
            return "unknown"
        
        s = example_date.strip()
        if re.fullmatch(r"\d{4}", s):
            return "year"
        if re.fullmatch(r"\d{8}", s):
            return "ymd"
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
            return "y-m-d"
        
        return "unknown"
