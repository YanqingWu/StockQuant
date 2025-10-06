"""
适配器工具函数
"""

from typing import Any, Dict, Union, Callable, List
from .standard_params import StandardParams
from .akshare_adapter import AkshareStockParamAdapter
from .param_normalizer import ParamNormalizer
from .transformers import (
    SymbolTransformer, DateTransformer, TimeTransformer, 
    PeriodTransformer, AdjustTransformer, MarketTransformer, 
    KeywordTransformer
)


def to_standard_params(params: Union[StandardParams, Dict[str, Any]]) -> StandardParams:
    """将输入参数规范化为 StandardParams 格式"""
    # 参数类型验证
    if params is None:
        raise ValueError("参数不能为 None")
    
    if isinstance(params, StandardParams):
        return params

    if not isinstance(params, dict):
        raise ValueError(f"参数类型错误，期望 dict 或 StandardParams，实际: {type(params)}")
    
    # 确保字典不为空
    if not params:
        raise ValueError("参数字典不能为空")
    
    src: Dict[str, Any] = dict(params)
    adapter = AkshareStockParamAdapter()
    normalizer = ParamNormalizer()

    # 使用参数标准化器处理各种参数
    symbol_norm = normalizer.normalize_symbols(src, adapter)
    date_data = normalizer.normalize_dates(src, adapter)
    time_data = normalizer.normalize_times(src, adapter)
    period_norm = normalizer.normalize_periods(src, adapter)
    adjust_norm = normalizer.normalize_adjusts(src, adapter)
    market_norm, exchange_norm = normalizer.normalize_markets(src, adapter)
    keyword_norm = normalizer.normalize_keywords(src, adapter)
    pagination_data = normalizer.normalize_pagination(src)

    # 组装严格格式
    return StandardParams(
        symbol=symbol_norm,
        start_date=date_data.get('start_date'),
        end_date=date_data.get('end_date'),
        start_time=time_data.get('start_time'),
        end_time=time_data.get('end_time'),
        period=period_norm,
        adjust=adjust_norm,
        market=market_norm,
        exchange=exchange_norm,
        keyword=keyword_norm,
        page=pagination_data.get('page'),
        page_size=pagination_data.get('page_size'),
        offset=pagination_data.get('offset'),
        limit=pagination_data.get('limit'),
        extra=_extract_extra_params(src)
    )


def adapt_params_for_interface(interface_name: str, params: Union[StandardParams, Dict[str, Any]]) -> Dict[str, Any]:
    """便捷函数：对单个接口调用做参数适配（Akshare）。
    
    Args:
        interface_name: 接口名称
        params: 参数，可以是 StandardParams 实例或原始字典
        
    Returns:
        适配后的参数字典
        
    Raises:
        AdapterError: 当适配过程中发生错误时
    """
    adapter = AkshareStockParamAdapter()
    # 接受 StandardParams 实例
    try:
        from typing import cast
        if isinstance(params, StandardParams):  # type: ignore[arg-type]
            raw = cast(StandardParams, params).to_dict()
        else:
            raw = params
    except Exception:
        raw = params
    return adapter.adapt(interface_name, raw)


def pick_from_aliases(src: Dict[str, Any], aliases: List[str]) -> Any:
    """从别名中选取值
    
    Args:
        src: 源参数字典
        aliases: 别名列表
        
    Returns:
        找到的第一个值，如果没有找到则返回None
    """
    for k in aliases:
        if k in src:
            return src[k]
    return None


def _extract_extra_params(src: Dict[str, Any]) -> Dict[str, Any]:
    """提取额外参数
    
    Args:
        src: 源参数字典
        
    Returns:
        不包含标准参数的额外参数字典
    """
    excluded_keys = {
        *SymbolTransformer.SYMBOL_KEYS,
        *DateTransformer.BASE_DATE_KEYS,
        *DateTransformer.START_DATE_KEYS,
        *DateTransformer.END_DATE_KEYS,
        *TimeTransformer.TIME_KEYS,
        *PeriodTransformer.PERIOD_KEYS,
        *AdjustTransformer.ADJUST_KEYS,
        *MarketTransformer.MARKET_KEYS,
        *KeywordTransformer.KEYWORD_KEYS,
        "page", "page_size", "offset", "limit",
    }
    return {k: v for k, v in src.items() if k not in excluded_keys}


def apply_to_value(value: Any, fn: Callable[[Any], Any]) -> Any:
    """支持列表与逗号分隔字符串的转换
    
    Args:
        value: 要转换的值，可以是单个值、列表或逗号分隔的字符串
        fn: 转换函数
        
    Returns:
        转换后的值，保持原始类型结构
    """
    if isinstance(value, list):
        return [fn(v) for v in value]
    if isinstance(value, str) and "," in value:
        parts = [p.strip() for p in value.split(",")]
        if all(p for p in parts):
            return ",".join(str(fn(p)) for p in parts)
    return fn(value)
