"""
适配器工具函数
"""

from typing import Any, Dict, Union
from .standard_params import StandardParams
from .akshare_adapter import AkshareStockParamAdapter
from .transformers.symbol_transformer import SymbolTransformer
from .transformers.date_transformer import DateTransformer
from .transformers.time_transformer import TimeTransformer
from .transformers.period_transformer import PeriodTransformer
from .transformers.adjust_transformer import AdjustTransformer
from .transformers.market_transformer import MarketTransformer
from .transformers.keyword_transformer import KeywordTransformer


def to_standard_params(params: Union[StandardParams, Dict[str, Any]]) -> StandardParams:
    """将输入参数规范化为 StandardParams 格式"""
    if isinstance(params, StandardParams):
        return params

    src: Dict[str, Any] = dict(params or {})
    adapter = AkshareStockParamAdapter()

    def as_list_or_single(value: Any, convert_one):
        if isinstance(value, list):
            return [convert_one(v) for v in value]
        if isinstance(value, str) and "," in value:
            parts = [p.strip() for p in value.split(",") if p.strip()]
            result = [convert_one(p) for p in parts]
            return result
        return convert_one(value)

    hint = adapter._get_market_hint(src, example={})
    symbol_val = adapter._pick_from_aliases(src, SymbolTransformer.SYMBOL_KEYS)

    def sym_to_obj(v: Any) -> Any:
        if v is None:
            return None
        from .stock_symbol import StockSymbol
        return StockSymbol.parse(v, hint_market=hint)

    symbol_norm: Any = None
    if symbol_val is not None:
        symbol_norm = as_list_or_single(symbol_val, sym_to_obj)

    # date family -> YYYY-MM-DD
    def to_date(v: Any) -> Any:
        style = "y-m-d"
        return adapter._convert_date(str(v), style) if v is not None else v

    date_norm = None
    start_date_norm = None
    end_date_norm = None

    date_val = adapter._pick_from_aliases(src, DateTransformer.BASE_DATE_KEYS)
    if date_val is not None:
        date_norm = adapter._apply_to_value(date_val, to_date)

    start_date_val = adapter._pick_from_aliases(src, DateTransformer.START_DATE_KEYS)
    if start_date_val is not None:
        start_date_norm = adapter._apply_to_value(start_date_val, to_date)

    end_date_val = adapter._pick_from_aliases(src, DateTransformer.END_DATE_KEYS)
    if end_date_val is not None:
        end_date_norm = adapter._apply_to_value(end_date_val, to_date)

    # time family -> HH:MM:SS
    def to_time(v: Any) -> Any:
        style = "h:m:s"
        return adapter._convert_time(str(v), style) if v is not None else v

    start_time_norm = None
    end_time_norm = None

    start_time_val = adapter._pick_from_aliases(src, TimeTransformer.START_TIME_KEYS)
    if start_time_val is not None:
        start_time_norm = adapter._apply_to_value(start_time_val, to_time)

    end_time_val = adapter._pick_from_aliases(src, TimeTransformer.END_TIME_KEYS)
    if end_time_val is not None:
        end_time_norm = adapter._apply_to_value(end_time_val, to_time)

    # period -> canonical set
    period_norm = None
    period_val = adapter._pick_from_aliases(src, PeriodTransformer.PERIOD_KEYS)
    if period_val is not None:
        def to_period(v: Any) -> Any:
            if not isinstance(v, (str, int)):
                return v
            s = str(v).strip().lower()
            if s in {"daily", "day", "d"}:
                return "daily"
            import re
            m = re.fullmatch(r"(\d+)\s*(m|min|minute)$", s)
            if m:
                return f"{m.group(1)}min"
            if s in {"1min","5min","15min","30min","60min"}:
                return s
            # 不可识别时返回原值
            return v
        period_norm = adapter._apply_to_value(period_val, to_period)

    # adjust -> {none,qfq,hfq}
    adjust_norm = None
    adjust_val = adapter._pick_from_aliases(src, AdjustTransformer.ADJUST_KEYS)
    if adjust_val is not None:
        def to_adjust(v: Any) -> Any:
            if not isinstance(v, str):
                return v
            s = v.strip().lower()
            if s in {"none", "no", "null", "na", "n", ""}:
                return "none"
            if s in {"qfq", "hfq"}:
                return s
            return v
        adjust_norm = adapter._apply_to_value(adjust_val, to_adjust)

    # market/exchange
    market_norm = None
    exchange_norm = None

    m_val = adapter._pick_from_aliases(src, MarketTransformer.MARKET_ONLY_KEYS)
    if isinstance(m_val, str) and m_val.strip():
        from .stock_symbol import StockSymbol
        market_norm = StockSymbol._canon_market(m_val)
    e_val = adapter._pick_from_aliases(src, MarketTransformer.EXCHANGE_KEYS)
    if isinstance(e_val, str) and e_val.strip():
        e_key = e_val.strip().upper()
        # 使用StockSymbol中统一的交易所映射
        from .stock_symbol import StockSymbol
        exchange_norm = StockSymbol.MARKET_TO_EXCHANGE.get(e_key, e_key)

    # 若只有 symbol 推断出 market/exchange
    if market_norm is None and symbol_norm is not None:
        sample = symbol_norm[0] if isinstance(symbol_norm, list) and symbol_norm else symbol_norm
        if hasattr(sample, 'market') and sample.market:
            market_norm = sample.market
            from .stock_symbol import StockSymbol
            exchange_norm = StockSymbol.MARKET_TO_EXCHANGE.get(sample.market, sample.market)

    # keyword/name
    keyword_norm = adapter._pick_from_aliases(src, KeywordTransformer.KEYWORD_KEYS)

    # pagination
    def to_int(v: Any) -> Any:
        if v is None:
            return None
        if isinstance(v, int):
            return v
        if isinstance(v, str) and v.strip().isdigit():
            return int(v.strip())
        return None

    page = to_int(src.get("page"))
    page_size = to_int(src.get("page_size"))
    offset = to_int(src.get("offset"))
    limit = to_int(src.get("limit"))

    # 组装严格格式
    return StandardParams(
        symbol=symbol_norm,
        date=date_norm,
        start_date=start_date_norm,
        end_date=end_date_norm,
        start_time=start_time_norm,
        end_time=end_time_norm,
        period=period_norm,
        adjust=adjust_norm,
        market=market_norm,
        exchange=exchange_norm,
        keyword=keyword_norm,
        page=page,
        page_size=page_size,
        offset=offset,
        limit=limit,
        extra={k: v for k, v in src.items() if k not in {
            *SymbolTransformer.SYMBOL_KEYS,
            *DateTransformer.DATE_KEYS,
            *TimeTransformer.TIME_KEYS,
            *PeriodTransformer.PERIOD_KEYS,
            *AdjustTransformer.ADJUST_KEYS,
            *MarketTransformer.MARKET_KEYS,
            *KeywordTransformer.KEYWORD_KEYS,
            "page","page_size","offset","limit",
        }}
    )


def adapt_params_for_interface(interface_name: str, params: Union[StandardParams, Dict[str, Any]]) -> Dict[str, Any]:
    """便捷函数：对单个接口调用做参数适配（Akshare）。
    支持传入 StandardParams 或原始 dict。
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


def pick_from_aliases(src: Dict[str, Any], aliases: list) -> Any:
    """从别名中选取值"""
    for k in aliases:
        if k in src:
            return src[k]
    return None


def apply_to_value(value: Any, fn) -> Any:
    """支持列表与逗号分隔字符串的转换"""
    if isinstance(value, list):
        return [fn(v) for v in value]
    if isinstance(value, str) and "," in value:
        parts = [p.strip() for p in value.split(",")]
        if all(p for p in parts):
            return ",".join(str(fn(p)) for p in parts)
    return fn(value)
