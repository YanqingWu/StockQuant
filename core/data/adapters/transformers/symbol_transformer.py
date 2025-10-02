"""
股票代码转换器
"""

import re
from typing import Any, Dict, Optional
from .base import BaseTransformer
from ..base import TransformContext
from ..stock_symbol import StockSymbol
from ..constants import SYMBOL_KEYS


class SymbolTransformer(BaseTransformer):
    """股票代码转换器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.supported_formats = self._get_config_value('supported_formats', ['dot', 'prefix', 'code'])
    
    def can_transform(self, context: TransformContext) -> bool:
        """检查是否有股票代码需要转换"""
        return any(key in context.source_params for key in SYMBOL_KEYS)
    
    def transform(self, context: TransformContext) -> TransformContext:
        """执行股票代码转换"""
        for key in SYMBOL_KEYS:
            if context.has_source_key(key):
                value = context.source_params[key]
                if value is not None:
                    target_format = self._detect_target_format(context, key)
                    converted_value = self._convert_symbol(value, target_format, context)
                    context.set_target_value(key, converted_value)
        
        return context
    
    def _convert_symbol(self, value: Any, target_format: str, context: TransformContext) -> Any:
        """转换股票代码格式"""
        def convert_one(v: Any) -> Any:
            sym = StockSymbol.parse(v)
            if not sym:
                if isinstance(v, str) and target_format == "code":
                    m = re.search(r"(\d{6})", v)
                    if m:
                        return m.group(1)
                return v
            
            if target_format == "dot":
                m = sym.market.upper() if sym.market else ""
                return f"{sym.code}.{m}" if re.fullmatch(r"[A-Za-z]{2}", m or "") else sym.code
            elif target_format == "prefix":
                m = sym.market.upper() if sym.market else ""
                return f"{m}{sym.code}" if re.fullmatch(r"[A-Za-z]{2}", m or "") else sym.code
            elif target_format == "code":
                return sym.to_code()
            elif target_format == "lowercase_prefix":
                m = sym.market.lower() if sym.market else ""
                return f"{m}{sym.code}" if re.fullmatch(r"[A-Za-z]{2}", m or "") else sym.code
            elif target_format == "us_prefix":
                return f"105.{sym.code}"
            else:
                return v
        
        return self._apply_to_value(value, convert_one)
    
    def _detect_target_format(self, context: TransformContext, field: str) -> str:
        """检测目标格式 - 基于示例参数智能检测，避免硬编码"""
        # 优先分析示例参数
        if context.metadata and hasattr(context.metadata, 'example_params'):
            example = context.metadata.example_params
            if field in example:
                analyzed_format = self._analyze_format(example[field])
                
                # 智能处理：如果示例是小写前缀格式，强制使用lowercase_prefix
                if isinstance(example[field], str):
                    example_val = example[field].strip()
                    if example_val.startswith(('sh', 'sz', 'bj', 'hk', 'us')):
                        return "lowercase_prefix"
                    elif example_val.startswith(('SH', 'SZ', 'BJ', 'HK', 'US')):
                        return "prefix"
                    elif re.fullmatch(r'\d{6}', example_val):
                        return "code"
                    elif re.fullmatch(r'\d+\.\w+', example_val):
                        return "us_prefix"
                
                return analyzed_format
        
        # 如果示例参数分析失败，使用默认格式
        return "dot"
    
    def _analyze_format(self, example_symbol: str) -> str:
        """分析示例符号的格式"""
        if not isinstance(example_symbol, str):
            return "unknown"
        
        s = example_symbol.strip().upper()
        
        # A股格式：6位数字
        if re.fullmatch(r"\d{6}\.(SZ|SH|BJ)", s):
            return "dot"
        if re.fullmatch(r"(SZ|SH|BJ)\d{6}", s):
            return "prefix"
        if re.fullmatch(r"\d{6}", example_symbol):
            return "code"
        # 纯数字代码：5-6位（A股6位，港股5位）
        if re.fullmatch(r"\d{5,6}", example_symbol):
            return "code"
        # 美股格式：纯字母代码（如AAPL, FB）
        if re.fullmatch(r"[A-Z]{1,5}", s):
            return "code"
        # 美股历史格式：数字.字母（如105.MSFT）
        if re.fullmatch(r"\d+\.[A-Z]{1,5}", s):
            return "code"
        # B股格式：小写市场前缀+代码（如sh900901）
        if re.fullmatch(r"(sh|sz)\d{6}", example_symbol.lower()):
            return "lowercase_prefix"
        
        return "unknown"
    
    def _detect_symbol_style(self, s: str) -> str:
        """检测股票代码风格"""
        if not isinstance(s, str):
            return "unknown"
        
        s = s.strip()
        if "." in s:
            return "dot"
        elif s.startswith(("SH", "SZ", "BJ", "HK", "US")):
            return "prefix"
        elif s.isdigit():
            return "code"
        else:
            return "unknown"
    
    def _detect_target_key_style_case(self, example: Dict[str, Any], accepted: set) -> tuple:
        """检测目标键的风格"""
        # 查找symbol相关的键
        symbol_keys = ["symbol", "stock", "code", "ts_code"]
        for key in symbol_keys:
            if key in accepted and key in example:
                value = example[key]
                if isinstance(value, str):
                    style = self._detect_symbol_style(value)
                    if style != "unknown":
                        return (key, style, "upper" if value.isupper() else "lower")
        return None
