"""
配置加载器
"""

from typing import Dict, Any, Optional
from .adapter_config import AdapterConfig


class AdapterConfigLoader:
    """适配器配置加载器"""
    
    def __init__(self, config: Optional[AdapterConfig] = None):
        self.config = config or AdapterConfig.get_default_config()
    
    def get_config(self) -> AdapterConfig:
        """获取配置"""
        return self.config
    
    def get_interface_config(self, interface_name: str) -> Dict[str, Any]:
        """获取接口配置"""
        if interface_name in self.config.interface_configs:
            interface_config = self.config.interface_configs[interface_name]
            return {
                'transformers': [rule.config for rule in interface_config.transformers],
                'mappers': [rule.config for rule in interface_config.mappers],
                'validators': [rule.config for rule in interface_config.validators],
                'special_handlers': interface_config.special_handlers
            }
        else:
            # 返回默认配置
            return {
                'name_mappings': self.config.global_rules.get('name_mappings', {}),
                'value_mappings': self.config.global_rules.get('value_mappings', {}),
                'symbol_config': self.config.global_rules.get('symbol_config', {}),
                'date_config': self.config.global_rules.get('date_config', {}),
                'time_config': self.config.global_rules.get('time_config', {}),
                'period_config': self.config.global_rules.get('period_config', {}),
                'adjust_config': self.config.global_rules.get('adjust_config', {}),
                'market_config': self.config.global_rules.get('market_config', {}),
                'keyword_config': self.config.global_rules.get('keyword_config', {}),
                'special_rules': self.config.global_rules.get('special_rules', {}),
                'format_rules': self.config.global_rules.get('format_rules', {}),
                'range_rules': self.config.global_rules.get('range_rules', {}),
            }
    
    def get_name_mapping_config(self) -> Dict[str, Any]:
        """获取参数名映射配置"""
        return {
            'name_mappings': self.config.global_rules.get('name_mappings', {})
        }
    
    def get_value_mapping_config(self) -> Dict[str, Any]:
        """获取参数值映射配置"""
        return {
            'value_mappings': self.config.global_rules.get('value_mappings', {})
        }
    
    def get_symbol_config(self) -> Dict[str, Any]:
        """获取股票代码转换配置"""
        return self.config.global_rules.get('symbol_config', {})
    
    def get_date_config(self) -> Dict[str, Any]:
        """获取日期转换配置"""
        return self.config.global_rules.get('date_config', {})
    
    def get_time_config(self) -> Dict[str, Any]:
        """获取时间转换配置"""
        return self.config.global_rules.get('time_config', {})
    
    def get_period_config(self) -> Dict[str, Any]:
        """获取周期转换配置"""
        return self.config.global_rules.get('period_config', {})
    
    def get_adjust_config(self) -> Dict[str, Any]:
        """获取复权转换配置"""
        return self.config.global_rules.get('adjust_config', {})
    
    def get_market_config(self) -> Dict[str, Any]:
        """获取市场转换配置"""
        return self.config.global_rules.get('market_config', {})
    
    def get_keyword_config(self) -> Dict[str, Any]:
        """获取关键词转换配置"""
        return self.config.global_rules.get('keyword_config', {})
    
    def get_special_config(self) -> Dict[str, Any]:
        """获取特殊处理配置"""
        return {
            'special_rules': self.config.global_rules.get('special_rules', {})
        }
    
    def get_required_config(self) -> Dict[str, Any]:
        """获取必填参数配置"""
        return {
            'required_fields': []
        }
    
    def get_format_config(self) -> Dict[str, Any]:
        """获取格式验证配置"""
        # 不返回严格的格式验证规则，让验证器使用宽松验证
        return {
            'format_rules': {}
        }
    
    def get_range_config(self) -> Dict[str, Any]:
        """获取范围验证配置"""
        return {
            'range_rules': self.config.global_rules.get('range_rules', {})
        }
