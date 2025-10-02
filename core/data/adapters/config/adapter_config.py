"""
适配器配置类
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional


@dataclass
class TransformRule:
    """转换规则"""
    name: str
    transformer: str
    conditions: Dict[str, Any]
    config: Dict[str, Any]


@dataclass
class MapRule:
    """映射规则"""
    name: str
    mapper: str
    source_key: str
    target_key: str
    conditions: Dict[str, Any]


@dataclass
class ValidationRule:
    """验证规则"""
    name: str
    validator: str
    field: str
    config: Dict[str, Any]


@dataclass
class InterfaceAdapterConfig:
    """接口适配器配置"""
    interface_name: str
    transformers: List[TransformRule]
    mappers: List[MapRule]
    validators: List[ValidationRule]
    special_handlers: Dict[str, Any]


@dataclass
class AdapterConfig:
    """适配器总配置"""
    version: str
    default_transformers: List[str]
    default_mappers: List[str]
    default_validators: List[str]
    interface_configs: Dict[str, InterfaceAdapterConfig]
    global_rules: Dict[str, Any]
    
    @classmethod
    def get_default_config(cls) -> 'AdapterConfig':
        """获取默认配置"""
        return cls(
            version="2.0",
            default_transformers=["value_mapper", "symbol", "date", "time", "period", "adjust", "market", "keyword", "special"],
            default_mappers=["value_mapper"],
            default_validators=["required", "format", "range"],
            interface_configs={},
            global_rules={
                'value_mappings': {
                    'adjust': {
                        'none': '',
                        'no': '',
                        'na': '',
                        'n': '',
                        'null': '',
                        'qfq': 'qfq',
                        'hfq': 'hfq',
                    }
                },
                'symbol_config': {
                    'supported_formats': ['dot', 'prefix', 'code', 'lowercase_prefix', 'us_prefix']
                },
                'date_config': {
                    'supported_formats': ['y-m-d', 'ymd', 'year', 'compact']
                },
                'time_config': {
                    'supported_formats': ['h:m:s', 'hms']
                },
                'period_config': {
                    'supported_periods': ['daily', '1min', '5min', '15min', '30min', '60min']
                },
                'adjust_config': {
                    'supported_values': ['none', 'qfq', 'hfq'],
                    'default_value': ''
                },
                'market_config': {
                    'supported_markets': ['SH', 'SZ', 'BJ', 'HK', 'US'],
                    'market_to_exchange': {
                        "SZ": "SZSE", 
                        "SH": "SSE", 
                        "BJ": "BSE",
                        "HK": "HKEX",
                        "US": "US"
                    }
                },
                'keyword_config': {
                    'max_length': 100,
                    'strip_whitespace': True
                },
                'special_rules': {
                    # 基于参数特征的特殊规则，避免硬编码接口名称
                    'year_dependency': {
                        'type': 'year_dependency',
                        'description': '年份参数需要成对出现'
                    },
                    'remove_unsupported_params': {
                        'type': 'remove_unsupported_params',
                        'description': '移除不支持的参数'
                    }
                },
                'format_rules': {
                    'symbol': {
                        'type': str,
                        'pattern': r'^[A-Za-z0-9\.]+$'
                    },
                    'date': {
                        'type': str,
                        'pattern': r'^\d{4}-\d{2}-\d{2}$'
                    }
                },
                'range_rules': {
                    'page': {
                        'min_value': 1
                    },
                    'page_size': {
                        'min_value': 1
                    }
                }
            }
        )
