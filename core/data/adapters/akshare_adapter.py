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
    
    # 为了兼容utils.py中的调用，添加一些方法
    def _get_market_hint(self, params: Dict[str, Any], example: Dict[str, Any]) -> str:
        """获取市场提示"""
        # 1) 显式字段 market / exchange
        allowed_markets = {"SH", "SZ", "BJ", "HK", "US"}
        for key in ("market", "exchange"):
            if key in params and isinstance(params[key], str):
                v = params[key].strip()
                if v:
                    from .stock_symbol import StockSymbol
                    canon = StockSymbol._canon_market(v)
                    if canon in allowed_markets:
                        return canon
            if key in example and isinstance(example[key], str):
                v = example[key].strip()
                if v:
                    from .stock_symbol import StockSymbol
                    canon = StockSymbol._canon_market(v)
                    if canon in allowed_markets:
                        return canon
        return ""
    
    def _pick_from_aliases(self, src: Dict[str, Any], aliases: list) -> Any:
        """从别名中选取值"""
        for k in aliases:
            if k in src:
                return src[k]
        return None
    
    def _apply_to_value(self, value: Any, fn) -> Any:
        """支持列表与逗号分隔字符串的转换"""
        if isinstance(value, list):
            return [fn(v) for v in value]
        if isinstance(value, str) and "," in value:
            parts = [p.strip() for p in value.split(",")]
            if all(p for p in parts):
                return ",".join(str(fn(p)) for p in parts)
        return fn(value)
    
    def _convert_date(self, v: str, target_style: str) -> str:
        """转换日期格式"""
        if not isinstance(v, str):
            return v
        s = v.strip()
        if not s:
            return v
        # 解析
        import re
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
            y, m, d = s.split("-")
        elif re.fullmatch(r"\d{8}", s):
            y, m, d = s[0:4], s[4:6], s[6:8]
        else:
            return v
        
        # 如果是年份参数，只返回年份
        if target_style == "year":
            return y
        if target_style == "y-m-d":
            return f"{y}-{m}-{d}"
        if target_style == "compact":
            return f"{y}{m}{d}"
        return f"{y}{m}{d}"
    
    def _convert_time(self, v: str, target_style: str) -> str:
        """转换时间格式"""
        if not isinstance(v, str):
            return v
        s = v.strip()
        if not s:
            return v
        import re
        if re.fullmatch(r"\d{2}:\d{2}:\d{2}", s):
            hh, mm, ss = s.split(":")
        elif re.fullmatch(r"\d{6}", s):
            hh, mm, ss = s[0:2], s[2:4], s[4:6]
        else:
            return v
        if target_style == "hms":
            return f"{hh}{mm}{ss}"
        return f"{hh}:{mm}:{ss}"
    
    # 定义键名列表
    SYMBOL_KEYS = ["symbol", "stock", "code", "ts_code", "index_code"]
    DATE_KEYS = ["date", "trade_date"]
    START_DATE_KEYS = ["start_date", "from_date", "begin_date", "start_year"]
    END_DATE_KEYS = ["end_date", "to_date", "end_year"]
    START_TIME_KEYS = ["start_time"]
    END_TIME_KEYS = ["end_time"]
    PERIOD_KEYS = ["period", "freq", "frequency"]
    ADJUST_KEYS = ["adjust", "fq", "adj"]
    MARKET_KEYS = ["market"]
    EXCHANGE_KEYS = ["exchange"]
    KEYWORD_KEYS = ["keyword", "name"]
    
    def _detect_symbol_style(self, s: str) -> str:
        """检测股票代码风格"""
        if not isinstance(s, str):
            return "unknown"
        
        s = s.strip()
        if "." in s:
            return "dot"
        elif s.startswith(("SH", "SZ", "BJ", "HK", "US")):
            return "prefix"
        elif s.isdigit():
            return "code"
        else:
            return "unknown"
    
    def _detect_target_key_style_case(self, example: Dict[str, Any], accepted: set) -> tuple:
        """检测目标键的风格"""
        # 查找symbol相关的键
        symbol_keys = ["symbol", "stock", "code", "ts_code"]
        for key in symbol_keys:
            if key in accepted and key in example:
                value = example[key]
                if isinstance(value, str):
                    style = self._detect_symbol_style(value)
                    if style != "unknown":
                        return (key, style, "upper" if value.isupper() else "lower")
        return None
