"""
Akshare适配器实现
重构后的主适配器类，保持对外接口不变
"""

from typing import Any, Dict, Optional
from .base import TransformContext, TransformChain, ValidationChain
from .transformers import (
    NameMapper, ValueMapper, SymbolTransformer, DateTransformer, 
    TimeTransformer, PeriodTransformer, AdjustTransformer, 
    MarketTransformer, KeywordTransformer, SpecialHandler
)
from .validators import RequiredValidator, FormatValidator, RangeValidator
from .config import AdapterConfigLoader
from .mappers import InterfaceMapper
from core.logging import get_logger

logger = get_logger(__name__)


class AkshareStockParamAdapter:
    """
    Akshare 参数适配器（重构版）
    保持对外接口不变，内部使用新的转换器架构
    """
    
    def __init__(self, config_loader=None):
        """初始化适配器，可选传入配置加载器"""
        self.config_loader = config_loader
        self.config_loader_adapter = AdapterConfigLoader()
        self.interface_mapper = InterfaceMapper()
        
        # 初始化转换链和验证链
        self._init_transform_chain()
        self._init_validation_chain()
        
        # 初始化委托用的transformer实例（避免重复创建）
        self._init_delegate_transformers()
    
    def _init_transform_chain(self):
        """初始化转换链"""
        self.transform_chain = TransformChain([
            NameMapper(self.config_loader_adapter.get_name_mapping_config()),
            ValueMapper(self.config_loader_adapter.get_value_mapping_config()),
            SymbolTransformer(self.config_loader_adapter.get_symbol_config()),
            DateTransformer(self.config_loader_adapter.get_date_config()),
            TimeTransformer(self.config_loader_adapter.get_time_config()),
            PeriodTransformer(self.config_loader_adapter.get_period_config()),
            AdjustTransformer(self.config_loader_adapter.get_adjust_config()),
            MarketTransformer(self.config_loader_adapter.get_market_config()),
            KeywordTransformer(self.config_loader_adapter.get_keyword_config()),
            SpecialHandler(self.config_loader_adapter.get_special_config()),
        ])
    
    def _init_validation_chain(self):
        """初始化验证链"""
        self.validation_chain = ValidationChain([
            RequiredValidator(self.config_loader_adapter.get_required_config()),
            FormatValidator(self.config_loader_adapter.get_format_config()),
            RangeValidator(self.config_loader_adapter.get_range_config()),
        ])
    
    def _init_delegate_transformers(self):
        """初始化委托用的transformer实例"""
        self._market_transformer = None
        self._date_transformer = None
        self._time_transformer = None
        self._symbol_transformer = None
    
    def adapt(self, interface_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """适配参数（保持对外接口不变）"""
        # 1. 检查是否为映射接口
        if self.config_loader and self.interface_mapper.is_mapping_interface(interface_name):
            return self._handle_mapping_interface(interface_name, params)
        
        # 2. 使用基础适配逻辑处理
        return self._adapt_base(interface_name, params)
    
    def _handle_mapping_interface(self, interface_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理映射接口"""
        try:
            # 映射到目标接口
            target_interface, mapped_params = self.interface_mapper.map_parameters(interface_name, params)
            logger.debug(f"映射接口 {interface_name} -> {target_interface}, 映射后参数: {mapped_params}")
            
            # 使用基础适配器处理映射后的参数
            return self._adapt_base(target_interface, mapped_params)
        
        except Exception as e:
            logger.error(f"接口映射失败: {interface_name}, 错误: {e}")
            raise
    
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
            metadata=metadata,
            config=self.config_loader_adapter.get_interface_config(interface_name)
        )
        
        # 3. 执行参数转换
        context = self.transform_chain.transform(context)
        
        # 4. 执行参数验证
        if not self.validation_chain.validate(context):
            raise ValueError("参数验证失败")
        
        return context.target_params
    
    def _get_market_hint(self, params: Dict[str, Any], example: Dict[str, Any]) -> str:
        """获取市场提示"""
        if self._market_transformer is None:
            from .transformers.market_transformer import MarketTransformer
            self._market_transformer = MarketTransformer()
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
        if self._date_transformer is None:
            from .transformers.date_transformer import DateTransformer
            self._date_transformer = DateTransformer()
        return self._date_transformer._convert_date(v, target_style)
    
    def _convert_time(self, v: str, target_style: str) -> str:
        """转换时间格式"""
        if self._time_transformer is None:
            from .transformers.time_transformer import TimeTransformer
            self._time_transformer = TimeTransformer()
        return self._time_transformer._convert_time(v, target_style)
    
    def _detect_symbol_style(self, s: str) -> str:
        """检测股票代码风格"""
        if self._symbol_transformer is None:
            from .transformers.symbol_transformer import SymbolTransformer
            self._symbol_transformer = SymbolTransformer()
        return self._symbol_transformer._detect_symbol_style(s)
    
    def _detect_target_key_style_case(self, example: Dict[str, Any], accepted: set) -> tuple:
        """检测目标键的风格"""
        if self._symbol_transformer is None:
            from .transformers.symbol_transformer import SymbolTransformer
            self._symbol_transformer = SymbolTransformer()
        return self._symbol_transformer._detect_target_key_style_case(example, accepted)
