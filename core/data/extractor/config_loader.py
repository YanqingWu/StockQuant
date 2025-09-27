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
    markets: List[str] = field(default_factory=list)  # 新增：适用市场列表
    
    def is_market_supported(self, market: str) -> bool:
        """检查是否支持指定市场"""
        return not self.markets or market in self.markets


@dataclass
class DataTypeConfig:
    """数据类型配置"""
    description: str = ""
    interfaces: List[InterfaceConfig] = field(default_factory=list)
    
    def get_enabled_interfaces(self, market: Optional[str] = None) -> List[InterfaceConfig]:
        """获取启用的接口，按优先级排序，可按市场过滤"""
        enabled = [iface for iface in self.interfaces if iface.enabled]
        
        # 如果指定了市场，进行过滤
        if market:
            enabled = [iface for iface in enabled if iface.is_market_supported(market)]
        
        return sorted(enabled, key=lambda x: x.priority, reverse=False)
    
    def get_interface_by_name(self, name: str) -> Optional[InterfaceConfig]:
        """根据名称获取接口配置"""
        for iface in self.interfaces:
            if iface.name == name:
                return iface
        return None


@dataclass
class CategoryConfig:
    """数据分类配置"""
    description: str = ""
    cache_duration: int = 300
    retry_strategy: str = "standard"
    data_types: Dict[str, DataTypeConfig] = field(default_factory=dict)
    
    def get_enabled_data_types(self) -> Dict[str, DataTypeConfig]:
        """获取启用的数据类型"""
        return self.data_types
    
    def get_data_type_config(self, data_type: str) -> Optional[DataTypeConfig]:
        """获取数据类型配置"""
        return self.data_types.get(data_type)


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
    interfaces_config: Dict[str, CategoryConfig] = field(default_factory=dict)  # 重命名
    field_mappings: Dict[str, str] = field(default_factory=dict)
    
    def get_category_config(self, category: str) -> Optional[CategoryConfig]:
        """获取数据分类配置"""
        return self.interfaces_config.get(category)
    
    def get_data_type_config(self, category: str, data_type: str) -> Optional[DataTypeConfig]:
        """获取数据类型配置"""
        category_config = self.get_category_config(category)
        if category_config:
            return category_config.get_data_type_config(data_type)
        return None
    
    def get_enabled_interfaces(self, category: str, data_type: str, market: Optional[str] = None) -> List[InterfaceConfig]:
        """获取指定数据类型的启用接口"""
        config = self.get_data_type_config(category, data_type)
        if config:
            return config.get_enabled_interfaces(market)
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
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        初始化配置加载器
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认路径
        """
        if config_path is None:
            # 默认配置文件路径
            current_dir = Path(__file__).parent
            config_path = current_dir / "extraction_config.yaml"
        
        self.config_path = Path(config_path)
        self._config: Optional[ExtractionConfig] = None
        self._last_modified: Optional[float] = None
    
    def load_config(self, force_reload: bool = False) -> ExtractionConfig:
        """
        加载配置文件
        
        Args:
            force_reload: 是否强制重新加载
            
        Returns:
            ExtractionConfig: 配置对象
            
        Raises:
            FileNotFoundError: 配置文件不存在
            yaml.YAMLError: YAML解析错误
            ValueError: 配置验证失败
        """
        # 检查文件是否存在
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        
        # 检查是否需要重新加载
        current_modified = self.config_path.stat().st_mtime
        if not force_reload and self._config is not None and self._last_modified == current_modified:
            return self._config
        
        try:
            # 读取YAML文件
            with open(self.config_path, 'r', encoding='utf-8') as f:
                raw_config = yaml.safe_load(f)
            
            # 解析配置
            config = self._parse_config(raw_config)
            
            # 验证配置
            self._validate_config(config)
            
            # 缓存配置
            self._config = config
            self._last_modified = current_modified
            
            logger.info(f"成功加载配置文件: {self.config_path}")
            return config
            
        except yaml.YAMLError as e:
            logger.error(f"YAML解析错误: {e}")
            raise
        except Exception as e:
            logger.error(f"配置加载失败: {e}")
            raise
    
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
        
        # 解析接口配置 - 支持多层嵌套结构
        interfaces_config = {}
        interfaces_data = config_data.get('interfaces_config', {})
        
        def parse_interfaces_recursive(data: Dict[str, Any]) -> List[InterfaceConfig]:
            """递归解析接口配置"""
            interfaces = []
            interfaces_list = data.get('interfaces', [])
            
            for interface_data in interfaces_list:
                interface = InterfaceConfig(
                    name=interface_data['name'],
                    enabled=interface_data.get('enabled', True),
                    priority=interface_data.get('priority', 1),
                    markets=interface_data.get('markets', [])
                )
                interfaces.append(interface)
            
            return interfaces
        
        def parse_data_type_recursive(data: Dict[str, Any], path: str = "") -> Dict[str, DataTypeConfig]:
            """递归解析数据类型配置"""
            data_types = {}
            
            for key, value in data.items():
                # 跳过分类级别的配置字段
                if key in ['description', 'cache_duration', 'retry_strategy']:
                    continue
                
                if isinstance(value, dict):
                    # 检查是否直接包含interfaces
                    if 'interfaces' in value:
                        # 直接包含接口的数据类型
                        interfaces = parse_interfaces_recursive(value)
                        data_type = DataTypeConfig(
                            description=value.get('description', ''),
                            interfaces=interfaces
                        )
                        data_types[key] = data_type
                    else:
                        # 可能是嵌套的数据类型结构，需要进一步解析
                        nested_data_types = parse_data_type_recursive(value, f"{path}.{key}" if path else key)
                        # 将嵌套的数据类型展平，使用点号分隔
                        for nested_key, nested_data_type in nested_data_types.items():
                            full_key = f"{key}.{nested_key}"
                            data_types[full_key] = nested_data_type
            
            return data_types
        
        for category_name, category_data in interfaces_data.items():
            # 递归解析数据类型配置
            data_types = parse_data_type_recursive(category_data)
            
            category = CategoryConfig(
                description=category_data.get('description', ''),
                cache_duration=category_data.get('cache_duration', 300),
                retry_strategy=category_data.get('retry_strategy', 'standard'),
                data_types=data_types
            )
            interfaces_config[category_name] = category
        
        # 解析字段映射
        field_mappings = config_data.get('field_mappings', {})
        
        return ExtractionConfig(
            version=config_data.get('version', '1.0'),
            description=config_data.get('description', ''),
            global_config=global_config,
            standard_fields=standard_fields,
            interfaces_config=interfaces_config,  # 使用新的字段名
            field_mappings=field_mappings
        )
    
    def _validate_config(self, config: ExtractionConfig) -> None:
        """验证配置"""
        # 验证接口配置不为空
        if not config.interfaces_config:
            raise ValueError("配置中必须包含至少一个接口分类")
        
        # 验证每个接口分类
        for category_name, category_config in config.interfaces_config.items():
            if not category_config.data_types:
                logger.warning(f"接口分类 '{category_name}' 没有包含数据类型")
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
        # 转换接口配置
        interfaces_config = {}
        for category_name, category_config in config.interfaces_config.items():
            category_dict = {
                'description': category_config.description,
                'cache_duration': category_config.cache_duration,
                'retry_strategy': category_config.retry_strategy
            }
            
            # 处理数据类型，支持多层嵌套结构
            nested_structure = {}
            for data_type_name, type_config in category_config.data_types.items():
                # 处理点号分隔的嵌套结构
                if '.' in data_type_name:
                    parts = data_type_name.split('.')
                    current = nested_structure
                    
                    # 构建嵌套结构
                    for i, part in enumerate(parts[:-1]):
                        if part not in current:
                            current[part] = {}
                        current = current[part]
                    
                    # 设置最终的接口配置
                    interfaces = []
                    for iface in type_config.interfaces:
                        interface_dict = {
                            'name': iface.name,
                            'enabled': iface.enabled,
                            'priority': iface.priority
                        }
                        # 只有当markets不为空时才添加到字典中
                        if iface.markets:
                            interface_dict['markets'] = iface.markets
                        interfaces.append(interface_dict)
                    
                    current[parts[-1]] = {
                        'description': type_config.description,
                        'interfaces': interfaces
                    }
                else:
                    # 直接的数据类型
                    interfaces = []
                    for iface in type_config.interfaces:
                        interface_dict = {
                            'name': iface.name,
                            'enabled': iface.enabled,
                            'priority': iface.priority
                        }
                        # 只有当markets不为空时才添加到字典中
                        if iface.markets:
                            interface_dict['markets'] = iface.markets
                        interfaces.append(interface_dict)
                    
                    nested_structure[data_type_name] = {
                        'description': type_config.description,
                        'interfaces': interfaces
                    }
            
            # 合并嵌套结构到分类字典
            category_dict.update(nested_structure)
            interfaces_config[category_name] = category_dict
        
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
            'interfaces_config': interfaces_config,  # 使用新的字段名
            'field_mappings': config.field_mappings
        }