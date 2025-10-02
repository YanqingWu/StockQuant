"""
转换规则类
集中管理所有参数转换规则和格式检测

这个类是整个适配器系统的核心，包含了：
- 各种参数格式的检测规则（日期、时间、股票代码等）
- 参数值的转换逻辑（周期、复权、市场等）
- 市场代码的标准化和映射

设计原则：
1. 集中管理：所有转换规则都在这里定义
2. 统一接口：提供一致的检测和转换方法
3. 易于扩展：新增规则只需在这里添加
4. 避免重复：消除各transformer中的硬编码逻辑
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
    
    # 时间格式检测规则
    TIME_FORMAT_PATTERNS = {
        "hms": re.compile(r"^\d{6}$"),
        "h:m:s": re.compile(r"^\d{2}:\d{2}:\d{2}$"),
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
    
    @classmethod
    def convert_symbol_format(cls, value: Any, target_format: str) -> Any:
        """转换股票代码格式"""
        if not isinstance(value, str):
            return value
        
        # 对于美股，需要特殊处理
        if target_format == "us_code":
            # 如果是105.XXX格式，提取XXX部分
            if value.startswith("105."):
                return value[4:]  # 去掉"105."前缀
            # 如果是其他格式，直接返回
            return value
        elif target_format == "us_prefix":
            # 转换为105.XXX格式
            if not value.startswith("105."):
                return f"105.{value}"
            return value
        
        # 其他格式暂时返回原值，让原有逻辑处理
        return value
    
    @classmethod
    def detect_time_format(cls, value: str) -> str:
        """检测时间格式"""
        if not isinstance(value, str):
            return "unknown"
        
        s = value.strip()
        for format_name, pattern in cls.TIME_FORMAT_PATTERNS.items():
            if pattern.match(s):
                return format_name
        
        return "unknown"
    
    @classmethod
    def convert_time(cls, value: Any, target_format: str) -> Any:
        """转换时间格式"""
        if not isinstance(value, str):
            return value
        
        s = value.strip()
        if not s:
            return value
        
        # 检测当前格式
        current_format = cls.detect_time_format(s)
        if current_format == "unknown":
            return value
        
        # 如果已经是目标格式，直接返回
        if current_format == target_format:
            return value
        
        # 转换格式
        if current_format == "h:m:s" and target_format == "hms":
            return s.replace(":", "")
        elif current_format == "hms" and target_format == "h:m:s":
            if len(s) == 6:
                return f"{s[0:2]}:{s[2:4]}:{s[4:6]}"
        
        return value
