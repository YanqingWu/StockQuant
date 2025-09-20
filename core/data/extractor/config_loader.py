"""
配置文件加载器
负责加载、解析、验证和保存数据提取配置文件
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class InterfaceConfig:
    """接口配置"""
    name: str
    enabled: bool = True
    priority: int = 1


@dataclass
class DataTypeConfig:
    """数据类型配置"""
    description: str = ""
    enabled: bool = True
    interfaces: List[InterfaceConfig] = field(default_factory=list)
    
    def get_enabled_interfaces(self) -> List[InterfaceConfig]:
        """获取启用的接口，按优先级排序"""
        if not self.enabled:
            return []
        enabled = [iface for iface in self.interfaces if iface.enabled]
        return sorted(enabled, key=lambda x: x.priority, reverse=False)
    
    def get_interface_by_name(self, name: str) -> Optional[InterfaceConfig]:
        """根据名称获取接口配置"""
        for iface in self.interfaces:
            if iface.name == name:
                return iface
        return None


@dataclass
class DataCategoryConfig:
    """数据分类配置"""
    description: str = ""
    cache_duration: int = 300
    retry_strategy: str = "standard"
    priority: int = 1
    enabled: bool = True
    data_types: Dict[str, DataTypeConfig] = field(default_factory=dict)
    
    def get_enabled_data_types(self) -> Dict[str, DataTypeConfig]:
        """获取启用的数据类型"""
        if not self.enabled:
            return {}
        return {name: config for name, config in self.data_types.items() if config.enabled}


@dataclass
class GlobalConfig:
    """全局配置"""
    timeout: int = 30
    retry_count: int = 3
    enable_cache: bool = True
    default_cache_duration: int = 300
    log_level: str = "INFO"


@dataclass
class ExtractionConfig:
    """数据提取配置"""
    version: str = "1.0"
    description: str = ""
    global_config: GlobalConfig = field(default_factory=GlobalConfig)
    standard_fields: Dict[str, Dict[str, List[str]]] = field(default_factory=dict)
    data_categories: Dict[str, DataCategoryConfig] = field(default_factory=dict)
    field_mappings: Dict[str, str] = field(default_factory=dict)
    
    def get_category_config(self, category: str) -> Optional[DataCategoryConfig]:
        """获取数据分类配置"""
        return self.data_categories.get(category)
    
    def get_data_type_config(self, category: str, data_type: str) -> Optional[DataTypeConfig]:
        """获取数据类型配置"""
        category_config = self.get_category_config(category)
        if category_config:
            return category_config.data_types.get(data_type)
        return None
    
    def get_enabled_interfaces(self, category: str, data_type: str) -> List[InterfaceConfig]:
        """获取指定数据类型的启用接口"""
        config = self.get_data_type_config(category, data_type)
        if config:
            return config.get_enabled_interfaces()
        return []
    
    def get_standard_fields(self, category: str, data_type: str) -> List[str]:
        """获取标准字段列表"""
        if category in self.standard_fields and data_type in self.standard_fields[category]:
            return self.standard_fields[category][data_type]
        return []
    
    def get_field_mapping(self, field_name: str) -> str:
        """获取字段映射"""
        return self.field_mappings.get(field_name, field_name)
    
    def has_field_mapping(self, field_name: str) -> bool:
        """检查是否存在字段映射"""
        return field_name in self.field_mappings


class ConfigLoader:
    """配置文件加载器"""
    
    def __init__(self):
        self._config: Optional[ExtractionConfig] = None
        self._config_path: Optional[Path] = None
    
    def load_from_file(self, config_path: str) -> ExtractionConfig:
        """从文件加载配置"""
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            config = self._parse_config(config_data)
            self._validate_config(config)
            
            self._config = config
            self._config_path = path
            
            logger.info(f"成功加载配置文件: {config_path}")
            return config
            
        except yaml.YAMLError as e:
            raise ValueError(f"配置文件格式错误: {e}")
        except Exception as e:
            raise ValueError(f"加载配置文件失败: {e}")
    
    def load_from_dict(self, config_data: Dict[str, Any]) -> ExtractionConfig:
        """从字典加载配置"""
        config = self._parse_config(config_data)
        self._validate_config(config)
        self._config = config
        return config
    
    def get_config(self) -> Optional[ExtractionConfig]:
        """获取当前配置"""
        return self._config
    
    def reload(self) -> ExtractionConfig:
        """重新加载配置文件"""
        if not self._config_path:
            raise ValueError("没有配置文件路径，无法重新加载")
        return self.load_from_file(str(self._config_path))
    
    def save_to_file(self, config_path: str, config: Optional[ExtractionConfig] = None) -> None:
        """保存配置到文件"""
        if config is None:
            config = self._config
        
        if config is None:
            raise ValueError("没有配置可以保存")
        
        config_data = self._config_to_dict(config)
        
        path = Path(config_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        logger.info(f"配置已保存到: {config_path}")
    
    def _parse_config(self, config_data: Dict[str, Any]) -> ExtractionConfig:
        """解析配置数据"""
        # 解析全局配置
        global_data = config_data.get('global_config', {})
        global_config = GlobalConfig(
            timeout=global_data.get('timeout', 30),
            retry_count=global_data.get('retry_count', 3),
            enable_cache=global_data.get('enable_cache', True),
            default_cache_duration=global_data.get('default_cache_duration', 300),
            log_level=global_data.get('log_level', 'INFO')
        )
        
        # 解析标准字段
        standard_fields = config_data.get('standard_fields', {})
        
        # 解析数据分类配置
        data_categories = {}
        categories_data = config_data.get('data_categories', {})
        
        for category_name, category_data in categories_data.items():
            # 解析数据类型
            data_types = {}
            data_types_data = category_data.get('data_types', {})
            
            for data_type_name, type_data in data_types_data.items():
                # 解析接口配置
                interfaces = []
                interfaces_data = type_data.get('interfaces', [])
                
                for iface_data in interfaces_data:
                    interface = InterfaceConfig(
                        name=iface_data['name'],
                        enabled=iface_data.get('enabled', True),
                        priority=iface_data.get('priority', 1)
                    )
                    interfaces.append(interface)
                
                data_type_config = DataTypeConfig(
                    description=type_data.get('description', ''),
                    enabled=type_data.get('enabled', True),
                    interfaces=interfaces
                )
                data_types[data_type_name] = data_type_config
            
            category_config = DataCategoryConfig(
                description=category_data.get('description', ''),
                cache_duration=category_data.get('cache_duration', 300),
                retry_strategy=category_data.get('retry_strategy', 'standard'),
                priority=category_data.get('priority', 1),
                enabled=category_data.get('enabled', True),
                data_types=data_types
            )
            data_categories[category_name] = category_config
        
        # 解析字段映射
        field_mappings = config_data.get('field_mappings', {})
        
        return ExtractionConfig(
            version=config_data.get('version', '1.0'),
            description=config_data.get('description', ''),
            global_config=global_config,
            standard_fields=standard_fields,
            data_categories=data_categories,
            field_mappings=field_mappings
        )
    
    def _validate_config(self, config: ExtractionConfig) -> None:
        """验证配置"""
        # 验证数据分类不为空
        if not config.data_categories:
            raise ValueError("配置中必须包含至少一个数据分类")
        
        # 验证每个数据分类
        for category_name, category_config in config.data_categories.items():
            if not category_config.data_types:
                logger.warning(f"数据分类 '{category_name}' 没有包含数据类型")
                continue
            
            # 验证每个数据类型至少有一个接口
            for data_type_name, type_config in category_config.data_types.items():
                if not type_config.interfaces:
                    logger.warning(f"数据类型 '{category_name}.{data_type_name}' 没有包含接口")
                    continue
                
                # 验证接口名称不重复
                interface_names = [iface.name for iface in type_config.interfaces]
                if len(interface_names) != len(set(interface_names)):
                    raise ValueError(f"数据类型 '{category_name}.{data_type_name}' 中存在重复的接口名称")
                
                # 验证优先级为非负整数
                for iface in type_config.interfaces:
                    if iface.priority < 0:
                        raise ValueError(f"接口 '{iface.name}' 的优先级不能小于0")
        
        # 验证全局配置
        if config.global_config.retry_count < 0:
            raise ValueError("重试次数不能为负数")
        
        if config.global_config.timeout <= 0:
            raise ValueError("超时时间必须大于0")
        
        if config.global_config.default_cache_duration < 0:
            raise ValueError("默认缓存时间不能为负数")
        
        # 验证字段映射
        if config.field_mappings:
            for chinese_field, english_field in config.field_mappings.items():
                if not chinese_field or not english_field:
                    raise ValueError(f"字段映射不能为空: '{chinese_field}' -> '{english_field}'")
    
    def _config_to_dict(self, config: ExtractionConfig) -> Dict[str, Any]:
        """将配置转换为字典"""
        # 转换数据分类
        data_categories = {}
        for category_name, category_config in config.data_categories.items():
            data_types = {}
            for data_type_name, type_config in category_config.data_types.items():
                interfaces = []
                for iface in type_config.interfaces:
                    interfaces.append({
                        'name': iface.name,
                        'enabled': iface.enabled,
                        'priority': iface.priority
                    })
                data_types[data_type_name] = {
                    'description': type_config.description,
                    'enabled': type_config.enabled,
                    'priority': type_config.priority,
                    'interfaces': interfaces
                }
            
            data_categories[category_name] = {
                'description': category_config.description,
                'cache_duration': category_config.cache_duration,
                'retry_strategy': category_config.retry_strategy,
                'priority': category_config.priority,
                'enabled': category_config.enabled,
                'data_types': data_types
            }
        
        return {
            'version': config.version,
            'description': config.description,
            'global_config': {
                'timeout': config.global_config.timeout,
                'retry_count': config.global_config.retry_count,
                'enable_cache': config.global_config.enable_cache,
                'default_cache_duration': config.global_config.default_cache_duration,
                'log_level': config.global_config.log_level
            },
            'standard_fields': config.standard_fields,
            'data_categories': data_categories,
            'field_mappings': config.field_mappings
        }