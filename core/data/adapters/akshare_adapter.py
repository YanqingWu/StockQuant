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
            raise RequiredParameterError(["参数验证失败"])
        
        return context.target_params
    
    def _get_market_hint(self, params: Dict[str, Any], example: Dict[str, Any]) -> str:
        """获取市场提示"""
        return self._market_transformer._get_market_hint(params, example)
    
    def _pick_from_aliases(self, src: Dict[str, Any], aliases: list) -> Any:
        """从别名中选取值"""
        from .utils import pick_from_aliases
        return pick_from_aliases(src, aliases)
    
    def _apply_to_value(self, value: Any, fn) -> Any:
        """支持列表与逗号分隔字符串的转换"""
        from .utils import apply_to_value
        return apply_to_value(value, fn)
    
    def _convert_date(self, v: str, target_style: str) -> str:
        """转换日期格式"""
        return self._date_transformer._convert_date(v, target_style)
    
    def _convert_time(self, v: str, target_style: str) -> str:
        """转换时间格式"""
        return self._time_transformer._convert_time(v, target_style)
    
    def _detect_symbol_style(self, s: str) -> str:
        """检测股票代码风格"""
        return self._symbol_transformer._detect_symbol_style(s)
    
    def _detect_target_key_style_case(self, example: Dict[str, Any], accepted: set) -> tuple:
        """检测目标键的风格"""
        return self._symbol_transformer._detect_target_key_style_case(example, accepted)
