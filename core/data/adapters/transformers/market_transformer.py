"""
市场转换器
"""

from typing import Any, Dict, Optional
from .base import BaseTransformer
from ..base import TransformContext
from ..stock_symbol import StockSymbol
from ..conversion_rules import ConversionRules


class MarketTransformer(BaseTransformer):
    """市场转换器"""
    
    MARKET_KEYS = ["market", "exchange"]
    MARKET_ONLY_KEYS = ["market"]
    EXCHANGE_KEYS = ["exchange"]
    
    def __init__(self):
        super().__init__()
        self.supported_markets = ['SH', 'SZ', 'BJ', 'HK', 'US']
    
    def can_transform(self, context: TransformContext) -> bool:
        """检查是否有市场需要转换"""
        return any(key in context.source_params for key in self.MARKET_KEYS)
    
    def transform(self, context: TransformContext) -> TransformContext:
        """执行市场转换"""
        if context.has_source_key("market"):
            market_value = context.source_params["market"]
            if market_value is not None:
                converted_market = self._convert_market(market_value, context)
                context.set_target_value("market", converted_market)
        
        if context.has_source_key("exchange"):
            exchange_value = context.source_params["exchange"]
            if exchange_value is not None:
                converted_exchange = self._convert_exchange(exchange_value, context)
                context.set_target_value("exchange", converted_exchange)
        
        if context.has_target_key("market") and not context.has_target_key("exchange") and "exchange" in context.accepted_keys:
            market = context.target_params["market"]
            exchange = ConversionRules.get_exchange_from_market(market)
            context.set_target_value("exchange", exchange)
        
        return context
    
    def _convert_market(self, value: Any, context: TransformContext) -> str:
        """转换市场代码"""
        if isinstance(value, str):
            canon_market = ConversionRules.canon_market(value)
            if canon_market in self.supported_markets:
                return canon_market
        
        return str(value) if value is not None else ""
    
    def _convert_exchange(self, value: Any, context: TransformContext) -> str:
        """转换交易所代码"""
        if isinstance(value, str):
            canon_exchange = ConversionRules.canon_market(value)
            return ConversionRules.get_exchange_from_market(canon_exchange)
        
        return str(value) if value is not None else ""
    
    def _get_market_hint(self, params: Dict[str, Any], example: Dict[str, Any]) -> str:
        """获取市场提示"""
        allowed_markets = {"SH", "SZ", "BJ", "HK", "US"}
        for key in ("market", "exchange"):
            if key in params and isinstance(params[key], str):
                v = params[key].strip()
                if v:
                    canon = ConversionRules.canon_market(v)
                    if canon in allowed_markets:
                        return canon
            if key in example and isinstance(example[key], str):
                v = example[key].strip()
                if v:
                    canon = ConversionRules.canon_market(v)
                    if canon in allowed_markets:
                        return canon
        return ""
