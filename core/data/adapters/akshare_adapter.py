"""
Akshare适配器实现
重构后的主适配器类，保持对外接口不变
"""

from typing import Any, Dict, Optional
from core.data.extractor.config_loader import ConfigLoader
from .base import TransformContext, TransformChain, ValidationChain
from .transformers import (
    ValueMapper, SymbolTransformer, DateTransformer, 
    TimeTransformer, PeriodTransformer, AdjustTransformer, 
    MarketTransformer, KeywordTransformer, SpecialHandler,
    ParameterMapper
)
from .validators import RequiredValidator, FormatValidator, RangeValidator
from .exceptions import InterfaceMappingError, RequiredParameterError
from core.logging import get_logger

logger = get_logger(__name__)


class AkshareStockParamAdapter:
    """
    Akshare 参数适配器
    """
    
    def __init__(self, config_loader: Optional['ConfigLoader'] = None) -> None:
        """初始化适配器，可选传入配置加载器"""
        self.config_loader = config_loader
        
        # 初始化参数映射器
        if config_loader:
            interface_mappings = config_loader.get_parameter_mappings()
            self.parameter_mapper = ParameterMapper(interface_mappings)
        else:
            self.parameter_mapper = ParameterMapper()
        
        # 预初始化所有transformer，避免延迟导入
        self._init_transformers()
        
        # 初始化转换链和验证链
        self._init_transform_chain()
        self._init_validation_chain()
    
    def _init_transform_chain(self) -> None:
        """初始化转换链"""
        self.transform_chain = TransformChain([
            ValueMapper(),
            SymbolTransformer(),
            DateTransformer(),
            TimeTransformer(),
            PeriodTransformer(),
            AdjustTransformer(),
            MarketTransformer(),
            KeywordTransformer(),
            SpecialHandler(),
        ])
    
    def _init_validation_chain(self) -> None:
        """初始化验证链"""
        self.validation_chain = ValidationChain([
            RequiredValidator(),
            FormatValidator(),
            RangeValidator(),
        ])
    
    def _init_transformers(self) -> None:
        """预初始化所有transformer实例"""
        self._market_transformer = MarketTransformer()
        self._date_transformer = DateTransformer()
        self._time_transformer = TimeTransformer()
        self._symbol_transformer = SymbolTransformer()
    
    def adapt(self, interface_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """适配参数（保持对外接口不变）"""
        # 1. 检查是否为映射接口
        if self.config_loader and self.parameter_mapper.is_mapping_interface(interface_name):
            return self._handle_mapping_interface(interface_name, params)
        
        # 2. 使用基础适配逻辑处理
        return self._adapt_base(interface_name, params)
    
    def _handle_mapping_interface(self, interface_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理映射接口"""
        try:
            # 映射到目标接口
            target_interface, mapped_params = self.parameter_mapper.map_parameters(interface_name, params)
            logger.debug(f"映射接口 {interface_name} -> {target_interface}, 映射后参数: {mapped_params}")
            
            # 使用基础适配器处理映射后的参数
            return self._adapt_base(target_interface, mapped_params)
        
        except Exception as e:
            logger.error(f"接口映射失败: {interface_name}, 错误: {e}")
            raise InterfaceMappingError(interface_name, str(e))
    
    def _adapt_base(self, interface_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """基础适配逻辑（重构版）"""
        from core.data.interfaces.base import get_interface_metadata
        
        # 1. 获取接口元数据
        metadata = get_interface_metadata(interface_name)
        if not metadata:
            return params
        
        # 2. 创建转换上下文
        context = TransformContext(
            interface_name=interface_name,
            source_params=params,
            target_params={},
            accepted_keys=set((metadata.required_params or []) + (metadata.optional_params or [])),
            metadata=metadata
        )
        
        # 3. 执行参数转换
        context = self.transform_chain.transform(context)
        
        # 4. 执行参数验证
        if not self.validation_chain.validate(context):
            # 验证失败时会抛出具体的异常，这里不需要额外处理
            pass
        
        return context.target_params
