"""
参数标准化器
将to_standard_params函数拆分为多个小函数
"""

from typing import Any, Dict, List, Optional, Union, Callable
from .standard_params import StandardParams
from .stock_symbol import StockSymbol
from .conversion_rules import ConversionRules
from .transformers import (
    SymbolTransformer, DateTransformer, TimeTransformer, 
    PeriodTransformer, AdjustTransformer, MarketTransformer, 
    KeywordTransformer
)


class ParamNormalizer:
    """参数标准化器"""
    
    def __init__(self):
        self.conversion_rules = ConversionRules()
    
    def normalize_symbols(self, src: Dict[str, Any], adapter) -> Optional[Union[StockSymbol, List[StockSymbol]]]:
        """标准化股票代码参数"""
        hint = adapter._get_market_hint(src, example={})
        symbol_val = adapter._pick_from_aliases(src, SymbolTransformer.SYMBOL_KEYS)
        
        if symbol_val is None:
            return None
        
        def sym_to_obj(v: Any) -> Any:
            if v is None:
                return None
            return StockSymbol.parse(v, hint_market=hint)
        
        return self._as_list_or_single(symbol_val, sym_to_obj)
    
    def normalize_dates(self, src: Dict[str, Any], adapter) -> Dict[str, Any]:
        """标准化日期参数"""
        result = {}
        
        # 基础日期
        date_val = adapter._pick_from_aliases(src, DateTransformer.BASE_DATE_KEYS)
        if date_val is not None:
            result['date'] = self._normalize_date_value(date_val, adapter)
        
        # 开始日期
        start_date_val = adapter._pick_from_aliases(src, DateTransformer.START_DATE_KEYS)
        if start_date_val is not None:
            result['start_date'] = self._normalize_date_value(start_date_val, adapter)
        
        # 结束日期
        end_date_val = adapter._pick_from_aliases(src, DateTransformer.END_DATE_KEYS)
        if end_date_val is not None:
            result['end_date'] = self._normalize_date_value(end_date_val, adapter)
        
        return result
    
    def normalize_times(self, src: Dict[str, Any], adapter) -> Dict[str, Any]:
        """标准化时间参数"""
        result = {}
        
        # 开始时间
        start_time_val = adapter._pick_from_aliases(src, TimeTransformer.START_TIME_KEYS)
        if start_time_val is not None:
            result['start_time'] = self._normalize_time_value(start_time_val, adapter)
        
        # 结束时间
        end_time_val = adapter._pick_from_aliases(src, TimeTransformer.END_TIME_KEYS)
        if end_time_val is not None:
            result['end_time'] = self._normalize_time_value(end_time_val, adapter)
        
        return result
    
    def normalize_periods(self, src: Dict[str, Any], adapter) -> Optional[Any]:
        """标准化周期参数"""
        period_val = adapter._pick_from_aliases(src, PeriodTransformer.PERIOD_KEYS)
        if period_val is None:
            return None
        
        def to_period(v: Any) -> Any:
            return self.conversion_rules.convert_period(v)
        
        return adapter._apply_to_value(period_val, to_period)
    
    def normalize_adjusts(self, src: Dict[str, Any], adapter) -> Optional[Any]:
        """标准化复权参数"""
        adjust_val = adapter._pick_from_aliases(src, AdjustTransformer.ADJUST_KEYS)
        if adjust_val is None:
            return None
        
        def to_adjust(v: Any) -> Any:
            return self.conversion_rules.convert_adjust(v)
        
        return adapter._apply_to_value(adjust_val, to_adjust)
    
    def normalize_markets(self, src: Dict[str, Any], adapter) -> tuple[Optional[str], Optional[str]]:
        """标准化市场和交易所参数"""
        market_norm = None
        exchange_norm = None
        
        # 市场参数
        m_val = adapter._pick_from_aliases(src, MarketTransformer.MARKET_ONLY_KEYS)
        if isinstance(m_val, str) and m_val.strip():
            market_norm = self.conversion_rules.canon_market(m_val)
        
        # 交易所参数
        e_val = adapter._pick_from_aliases(src, MarketTransformer.EXCHANGE_KEYS)
        if isinstance(e_val, str) and e_val.strip():
            e_key = e_val.strip().upper()
            exchange_norm = self.conversion_rules.get_exchange_from_market(e_key)
        
        # 从股票代码推断市场
        if market_norm is None:
            symbol_val = adapter._pick_from_aliases(src, SymbolTransformer.SYMBOL_KEYS)
            if symbol_val is not None:
                sample = symbol_val[0] if isinstance(symbol_val, list) and symbol_val else symbol_val
                if isinstance(sample, StockSymbol) and sample.market:
                    market_norm = sample.market
                    exchange_norm = self.conversion_rules.get_exchange_from_market(sample.market)
        
        return market_norm, exchange_norm
    
    def normalize_pagination(self, src: Dict[str, Any]) -> Dict[str, Optional[int]]:
        """标准化分页参数"""
        def to_int(v: Any) -> Optional[int]:
            if v is None:
                return None
            if isinstance(v, int):
                return v
            if isinstance(v, str) and v.strip().isdigit():
                return int(v.strip())
            return None
        
        return {
            'page': to_int(src.get("page")),
            'page_size': to_int(src.get("page_size")),
            'offset': to_int(src.get("offset")),
            'limit': to_int(src.get("limit"))
        }
    
    def normalize_keywords(self, src: Dict[str, Any], adapter) -> Optional[str]:
        """标准化关键词参数"""
        return adapter._pick_from_aliases(src, KeywordTransformer.KEYWORD_KEYS)
    
    def _normalize_date_value(self, value: Any, adapter) -> Any:
        """标准化单个日期值"""
        def to_date(v: Any) -> Any:
            style = "y-m-d"
            return adapter._convert_date(str(v), style) if v is not None else v
        
        return adapter._apply_to_value(value, to_date)
    
    def _normalize_time_value(self, value: Any, adapter) -> Any:
        """标准化单个时间值"""
        def to_time(v: Any) -> Any:
            style = "h:m:s"
            return adapter._convert_time(str(v), style) if v is not None else v
        
        return adapter._apply_to_value(value, to_time)
    
    def _as_list_or_single(self, value: Any, convert_one: Callable[[Any], Any]) -> Any:
        """支持列表与逗号分隔字符串的转换"""
        if isinstance(value, list):
            return [convert_one(v) for v in value]
        if isinstance(value, str) and "," in value:
            parts = [p.strip() for p in value.split(",") if p.strip()]
            result = [convert_one(p) for p in parts]
            return result
        return convert_one(value)
