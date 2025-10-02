"""
转换规则配置
提取硬编码的转换逻辑为配置化规则
"""

from typing import Any, Dict, List, Optional, Union
import re


class ConversionRules:
    """转换规则配置类"""
    
    # 周期映射规则
    PERIOD_MAPPING = {
        "daily": "daily", "day": "daily", "d": "daily",
        "1min": "1min", "5min": "5min", "15min": "15min",
        "30min": "30min", "60min": "60min"
    }
    
    # 复权映射规则
    ADJUST_MAPPING = {
        "none": "none", "no": "none", "null": "none", 
        "na": "none", "n": "none", "": "none",
        "qfq": "qfq", "hfq": "hfq"
    }
    
    # 市场别名映射
    MARKET_ALIASES = {
        "sz": "SZ", "sh": "SH", "bj": "BJ", "hk": "HK", "us": "US",
        "szse": "SZ", "sse": "SH", "bse": "BJ", "hkex": "HK",
        "nasdaq": "US", "nyse": "US", "港股": "HK", "美股": "US",
    }
    
    # 市场到交易所映射
    MARKET_TO_EXCHANGE = {
        "SZ": "SZSE", "SH": "SSE", "BJ": "BSE", "HK": "HKEX", "US": "US"
    }
    
    # 日期格式检测规则
    DATE_FORMAT_PATTERNS = {
        "year": re.compile(r"^\d{4}$"),
        "ymd": re.compile(r"^\d{8}$"),
        "y-m-d": re.compile(r"^\d{4}-\d{2}-\d{2}$"),
        "y/m/d": re.compile(r"^\d{4}/\d{2}/\d{2}$"),
    }
    
    # 股票代码格式检测规则
    SYMBOL_FORMAT_PATTERNS = {
        "dot": re.compile(r"^\d{5,6}\.(SZ|SH|BJ|HK|US)$"),
        "prefix": re.compile(r"^(SZ|SH|BJ|HK|US)\d{5,6}$"),
        "code": re.compile(r"^\d{5,6}$"),
        "us_code": re.compile(r"^[A-Z]{1,5}$"),
        "lowercase_prefix": re.compile(r"^(sh|sz|bj|hk|us)\d{5,6}$"),
    }
    
    @classmethod
    def convert_period(cls, value: Any) -> Any:
        """转换周期参数"""
        if not isinstance(value, (str, int)):
            return value
        
        s = str(value).strip().lower()
        
        # 直接映射
        if s in cls.PERIOD_MAPPING:
            return cls.PERIOD_MAPPING[s]
        
        # 分钟格式匹配
        m = re.fullmatch(r"(\d+)\s*(m|min|minute)$", s)
        if m:
            return f"{m.group(1)}min"
        
        # 不可识别时返回原值
        return value
    
    @classmethod
    def convert_adjust(cls, value: Any) -> Any:
        """转换复权参数"""
        if not isinstance(value, str):
            return value
        
        s = value.strip().lower()
        return cls.ADJUST_MAPPING.get(s, value)
    
    @classmethod
    def detect_date_format(cls, value: str) -> str:
        """检测日期格式"""
        if not isinstance(value, str):
            return "unknown"
        
        s = value.strip()
        for format_name, pattern in cls.DATE_FORMAT_PATTERNS.items():
            if pattern.match(s):
                return format_name
        
        return "unknown"
    
    @classmethod
    def detect_symbol_format(cls, value: str) -> str:
        """检测股票代码格式"""
        if not isinstance(value, str):
            return "unknown"
        
        s = value.strip().upper()
        for format_name, pattern in cls.SYMBOL_FORMAT_PATTERNS.items():
            if pattern.match(s):
                return format_name
        
        return "unknown"
    
    @classmethod
    def canon_market(cls, market: Optional[str]) -> str:
        """标准化市场代码"""
        if not market:
            return ""
        key = str(market).strip().lower()
        return cls.MARKET_ALIASES.get(key, key.upper())
    
    @classmethod
    def get_exchange_from_market(cls, market: str) -> str:
        """从市场代码获取交易所代码"""
        return cls.MARKET_TO_EXCHANGE.get(market, market)
