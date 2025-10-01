"""API接口注册相关的基类

这个模块专注于接口的注册、管理和元数据定义，
不涉及具体的调用逻辑。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import logging


class ParameterPatternGenerator:
    """动态参数模式生成器"""
    
    @staticmethod
    def generate_pattern(params: List[str]) -> str:
        """根据参数列表生成唯一的模式标识符
        
        Args:
            params: 参数名称列表
            
        Returns:
            str: 唯一的参数模式标识符
        """
        if not params:
            return "no_params"
        
        pattern_id = "_".join(params)
        
        return pattern_id


class ParameterPattern:
    """参数模式类，支持动态生成"""
    
    def __init__(self, pattern: str):
        self.pattern = pattern
    
    def __str__(self) -> str:
        return self.pattern
    
    def __repr__(self) -> str:
        return f"ParameterPattern('{self.pattern}')"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, ParameterPattern):
            return self.pattern == other.pattern
        elif isinstance(other, str):
            return self.pattern == other
        return False
    
    def __hash__(self) -> int:
        return hash(self.pattern)
    
    @classmethod
    def from_params(cls, params: List[str]) -> 'ParameterPattern':
        """从参数列表创建参数模式
        
        Args:
            params: 参数名称列表
            
        Returns:
            ParameterPattern: 参数模式实例
        """
        pattern = ParameterPatternGenerator.generate_pattern(params)
        return cls(pattern)


class DataSource(Enum):
    """数据源枚举"""
    AKSHARE = "akshare"


class FunctionCategory(Enum):
    """功能分类枚举"""
    # 股票相关
    STOCK_BASIC = "stock_basic"  # 股票基础信息
    STOCK_QUOTE = "stock_quote"  # 股票行情
    STOCK_FINANCIAL = "stock_financial"  # 财务数据
    STOCK_TECHNICAL = "stock_technical"  # 技术指标
    
    # 市场相关
    MARKET_INDEX = "market_index"  # 市场指数
    MARKET_OVERVIEW = "market_overview"  # 市场概览
    
    # 宏观经济
    MACRO_ECONOMY = "macro_economy"  # 宏观经济
    
    # 行业相关
    INDUSTRY_DATA = "industry_data"  # 行业数据
    
    # 基金相关
    FUND_DATA = "fund_data"  # 基金数据
    
    # 债券相关
    BOND_DATA = "bond_data"  # 债券数据
    
    # 外汇相关
    FOREX_DATA = "forex_data"  # 外汇数据
    
    # 期货相关
    FUTURES_DATA = "futures_data"  # 期货数据
    
    # 其他
    OTHER = "other"  # 其他


@dataclass
class InterfaceMetadata:
    """接口元数据"""
    name: str  # 接口名称
    description: str  # 接口描述
    parameter_pattern: ParameterPattern  # 参数模式
    data_source: DataSource  # 数据源
    function_category: FunctionCategory  # 功能分类
    required_params: List[str]  # 必需参数列表
    optional_params: List[str]  # 可选参数列表
    return_type: str  # 返回类型描述
    example_params: Optional[Dict[str, Any]] = None  # 示例参数
    keywords: Optional[List[str]] = None  # 关键词（用于搜索）
    frequency_limit: Optional[int] = None  # 频率限制（每分钟调用次数）
    is_deprecated: bool = False  # 是否已废弃
    version: str = "1.0"  # 版本号

logger = logging.getLogger(__name__)


class APIRegistry:
    """API接口注册表 - 专门管理接口的注册和查询"""
    
    def __init__(self):
        self._interfaces: Dict[str, InterfaceMetadata] = {}
        self._pattern_index: Dict[ParameterPattern, Set[str]] = {}
        self._source_index: Dict[DataSource, Set[str]] = {}
        self._category_index: Dict[FunctionCategory, Set[str]] = {}
        self._keyword_index: Dict[str, Set[str]] = {}  # 关键词索引
    
    def register_interface(self, metadata: InterfaceMetadata) -> None:
        """注册单个接口"""
        interface_name = metadata.name
        
        # 存储接口元数据
        self._interfaces[interface_name] = metadata
        
        # 更新索引
        self._update_pattern_index(interface_name, metadata.parameter_pattern)
        self._update_source_index(interface_name, metadata.data_source)
        self._update_category_index(interface_name, metadata.function_category)
        self._update_keyword_index(interface_name, metadata)
        
        logger.debug(f"注册接口: {interface_name}")
    
    def register_interfaces(self, interfaces: List[InterfaceMetadata]) -> None:
        """批量注册接口"""
        for metadata in interfaces:
            self.register_interface(metadata)
        logger.info(f"批量注册 {len(interfaces)} 个接口")
    
    def get_interface_metadata(self, interface_name: str) -> Optional[InterfaceMetadata]:
        """获取接口元数据"""
        return self._interfaces.get(interface_name)
    
    def list_all_interfaces(self) -> List[str]:
        """列出所有接口名称"""
        return list(self._interfaces.keys())
    
    def get_interfaces_by_pattern(self, pattern: ParameterPattern) -> List[str]:
        """按参数模式获取接口列表"""
        return list(self._pattern_index.get(pattern, set()))
    
    def get_interfaces_by_source(self, source: DataSource) -> List[str]:
        """按数据源获取接口列表"""
        return list(self._source_index.get(source, set()))
    
    def get_interfaces_by_category(self, category: FunctionCategory) -> List[str]:
        """按功能分类获取接口列表"""
        return list(self._category_index.get(category, set()))
    
    def search_interfaces(self, keyword: str) -> List[str]:
        """搜索接口"""
        keyword_lower = keyword.lower()
        matching_interfaces = set()
        
        # 在关键词索引中搜索
        for indexed_keyword, interfaces in self._keyword_index.items():
            if keyword_lower in indexed_keyword:
                matching_interfaces.update(interfaces)
        
        return list(matching_interfaces)
    
    def get_interface_by_source_and_name(self, source: DataSource, interface_name: str) -> Optional[InterfaceMetadata]:
        """根据数据源和接口名称查找接口"""
        metadata = self.get_interface_metadata(interface_name)
        if metadata and metadata.data_source == source:
            return metadata
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取注册统计信息"""
        return {
            'total_interfaces': len(self._interfaces),
            'by_pattern': {pattern.pattern: len(interfaces) for pattern, interfaces in self._pattern_index.items()},
            'by_source': {source.value: len(interfaces) for source, interfaces in self._source_index.items()},
            'by_category': {category.value: len(interfaces) for category, interfaces in self._category_index.items()}
        }
    
    def _update_pattern_index(self, interface_name: str, pattern: ParameterPattern) -> None:
        """更新参数模式索引"""
        if pattern not in self._pattern_index:
            self._pattern_index[pattern] = set()
        self._pattern_index[pattern].add(interface_name)
    
    def _update_source_index(self, interface_name: str, source: DataSource) -> None:
        """更新数据源索引"""
        if source not in self._source_index:
            self._source_index[source] = set()
        self._source_index[source].add(interface_name)
    
    def _update_category_index(self, interface_name: str, category: FunctionCategory) -> None:
        """更新功能分类索引"""
        if category not in self._category_index:
            self._category_index[category] = set()
        self._category_index[category].add(interface_name)
    
    def _update_keyword_index(self, interface_name: str, metadata: InterfaceMetadata) -> None:
        """更新关键词索引"""
        # 从接口名称、描述、关键词中提取关键词
        keywords = []
        
        # 接口名称
        keywords.append(interface_name.lower())
        
        # 描述
        if metadata.description:
            keywords.append(metadata.description.lower())
        
        # 关键词
        if metadata.keywords:
            keywords.extend([keyword.lower() for keyword in metadata.keywords])
        
        # 更新索引
        for keyword in keywords:
            if keyword not in self._keyword_index:
                self._keyword_index[keyword] = set()
            self._keyword_index[keyword].add(interface_name)


class BaseAPIProvider(ABC):
    """API提供者基类 - 专注于接口注册"""
    
    def __init__(self, name: str, source_type: DataSource):
        self.name = name
        self.source_type = source_type
        self.registry = APIRegistry()
        self._initialized = False
    
    @abstractmethod
    def register_interfaces(self) -> None:
        """注册接口 - 子类需要在此方法中注册所有支持的接口"""
        pass
    
    def get_registry(self) -> APIRegistry:
        """获取接口注册表"""
        if not self._initialized:
            self.register_interfaces()
            self._initialized = True
        return self.registry
    
    def get_supported_interfaces(self) -> List[str]:
        """获取支持的接口列表"""
        return self.get_registry().list_all_interfaces()
    
    def get_interface_metadata(self, interface_name: str) -> Optional[InterfaceMetadata]:
        """获取接口元数据"""
        return self.get_registry().get_interface_metadata(interface_name)
    
    def is_interface_supported(self, interface_name: str) -> bool:
        """检查是否支持指定接口"""
        return interface_name in self.get_supported_interfaces()
    
    def get_interfaces_by_pattern(self, pattern: ParameterPattern) -> List[str]:
        """按参数模式获取接口列表"""
        return self.get_registry().get_interfaces_by_pattern(pattern)
    
    def get_interfaces_by_category(self, category: FunctionCategory) -> List[str]:
        """按功能分类获取接口列表"""
        return self.get_registry().get_interfaces_by_category(category)
    
    def search_interfaces(self, keyword: str) -> List[str]:
        """搜索接口"""
        return self.get_registry().search_interfaces(keyword)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = self.get_registry().get_statistics()
        stats['provider_name'] = self.name
        stats['source_type'] = self.source_type.value
        return stats


class APIProviderManager:
    """API提供者管理器 - 管理多个API提供者"""
    
    def __init__(self):
        self._providers: Dict[str, BaseAPIProvider] = {}
        self._global_registry = APIRegistry()
    
    def register_provider(self, provider: BaseAPIProvider) -> None:
        """注册API提供者"""
        self._providers[provider.name] = provider
        
        # 将提供者的接口注册到全局注册表
        provider_registry = provider.get_registry()
        for interface_name in provider_registry.list_all_interfaces():
            metadata = provider_registry.get_interface_metadata(interface_name)
            if metadata:
                self._global_registry.register_interface(metadata)
        
        logger.info(f"注册API提供者: {provider.name}, 接口数量: {len(provider.get_supported_interfaces())}")
    
    def get_provider(self, provider_name: str) -> Optional[BaseAPIProvider]:
        """获取API提供者"""
        return self._providers.get(provider_name)
    
    def find_provider_for_interface(self, interface_name: str) -> Optional[BaseAPIProvider]:
        """查找支持指定接口的提供者"""
        for provider in self._providers.values():
            if provider.is_interface_supported(interface_name):
                return provider
        return None
    
    def get_all_interfaces(self) -> List[str]:
        """获取所有接口列表"""
        return self._global_registry.list_all_interfaces()
    
    def get_interface_metadata(self, interface_name: str) -> Optional[InterfaceMetadata]:
        """获取接口元数据"""
        return self._global_registry.get_interface_metadata(interface_name)
    
    def get_interfaces_by_pattern(self, pattern: ParameterPattern) -> List[str]:
        """按参数模式获取接口列表"""
        return self._global_registry.get_interfaces_by_pattern(pattern)
    
    def get_interfaces_by_source(self, source: DataSource) -> List[str]:
        """按数据源获取接口列表"""
        return self._global_registry.get_interfaces_by_source(source)
    
    def get_interfaces_by_category(self, category: FunctionCategory) -> List[str]:
        """按功能分类获取接口列表"""
        return self._global_registry.get_interfaces_by_category(category)
    
    def search_interfaces(self, keyword: str) -> List[str]:
        """搜索接口"""
        return self._global_registry.search_interfaces(keyword)
    
    def get_providers_by_source(self, source: DataSource) -> List[BaseAPIProvider]:
        """按数据源获取提供者列表"""
        return [provider for provider in self._providers.values() if provider.source_type == source]
    
    def find_interface_by_source_and_name(self, source: DataSource, interface_name: str) -> Optional[InterfaceMetadata]:
        """根据数据源和接口名称查找接口"""
        return self._global_registry.get_interface_by_source_and_name(source, interface_name)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取全局统计信息"""
        stats = self._global_registry.get_statistics()
        stats['total_providers'] = len(self._providers)
        stats['providers'] = {name: provider.get_statistics() for name, provider in self._providers.items()}
        return stats


class InterfaceBuilder:
    """接口构建器 - 帮助构建接口元数据"""
    
    def __init__(self, name: str):
        self.metadata = InterfaceMetadata(
            name=name,
            description="",
            parameter_pattern=ParameterPattern.from_params([]),  # 默认无参数模式
            data_source=DataSource.AKSHARE,
            function_category=FunctionCategory.OTHER,
            required_params=[],
            optional_params=[],
            return_type="DataFrame"
        )

    def with_pattern(self, pattern: ParameterPattern) -> 'InterfaceBuilder':
        """设置参数模式（手动设置，会覆盖自动生成的模式）"""
        self.metadata.parameter_pattern = pattern
        return self

    def with_source(self, source: DataSource) -> 'InterfaceBuilder':
        """设置数据源"""
        self.metadata.data_source = source
        return self

    def with_category(self, category: FunctionCategory) -> 'InterfaceBuilder':
        """设置功能分类"""
        self.metadata.function_category = category
        return self

    def with_description(self, description: str) -> 'InterfaceBuilder':
        """设置描述"""
        self.metadata.description = description
        return self

    def with_required_params(self, *params: str) -> 'InterfaceBuilder':
        """设置必需参数并自动生成参数模式"""
        self.metadata.required_params = list(params)
        # 自动生成参数模式
        self.metadata.parameter_pattern = ParameterPattern.from_params(list(params))
        return self
    
    def with_optional_params(self, *params: str) -> 'InterfaceBuilder':
        """设置可选参数"""
        self.metadata.optional_params = list(params)
        return self
    
    def with_keywords(self, *keywords: str) -> 'InterfaceBuilder':
        """设置关键词"""
        self.metadata.keywords = list(keywords)
        return self
    
    def with_frequency_limit(self, frequency_limit: int) -> 'InterfaceBuilder':
        """设置频率限制"""
        self.metadata.frequency_limit = frequency_limit
        return self
    
    def with_return_type(self, return_type: str) -> 'InterfaceBuilder':
        """设置返回类型"""
        self.metadata.return_type = return_type
        return self
    
    def with_example_params(self, example_params: Dict[str, Any]) -> 'InterfaceBuilder':
        """设置示例参数"""
        self.metadata.example_params = example_params
        return self
    
    def with_deprecated(self, is_deprecated: bool = True) -> 'InterfaceBuilder':
        """设置是否已废弃"""
        self.metadata.is_deprecated = is_deprecated
        return self
    
    def with_version(self, version: str) -> 'InterfaceBuilder':
        """设置版本号"""
        self.metadata.version = version
        return self
    
    def build(self) -> InterfaceMetadata:
        """构建接口元数据"""
        return self.metadata


# 全局API提供者管理器实例
api_provider_manager = APIProviderManager()


def register_provider(provider: BaseAPIProvider) -> None:
    """注册API提供者的便捷函数"""
    api_provider_manager.register_provider(provider)


def get_interface_metadata(interface_name: str) -> Optional[InterfaceMetadata]:
    """获取接口元数据的便捷函数"""
    return api_provider_manager.get_interface_metadata(interface_name)


def search_interfaces(keyword: str) -> List[str]:
    """搜索接口的便捷函数"""
    return api_provider_manager.search_interfaces(keyword)


def find_interface_by_source_and_name(source: DataSource, interface_name: str) -> Optional[InterfaceMetadata]:
    """根据数据源和接口名称查找接口的便捷函数"""
    return api_provider_manager.find_interface_by_source_and_name(source, interface_name)


def create_interface(name: str) -> InterfaceBuilder:
    """创建接口构建器的便捷函数"""
    return InterfaceBuilder(name)