"""
市场转换器
"""

from typing import Any, Dict, Optional
from .base import BaseTransformer
from ..base import TransformContext
from ..stock_symbol import StockSymbol


class MarketTransformer(BaseTransformer):
    """市场转换器"""
    
    MARKET_KEYS = ["market", "exchange"]
    MARKET_ONLY_KEYS = ["market"]
    EXCHANGE_KEYS = ["exchange"]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.supported_markets = self._get_config_value('supported_markets', ['SH', 'SZ', 'BJ', 'HK', 'US'])
        self.market_to_exchange = self._get_config_value('market_to_exchange', {
            "SZ": "SZSE", 
            "SH": "SSE", 
            "BJ": "BSE",
            "HK": "HKEX",
            "US": "US"
        })
    
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
            exchange = self.market_to_exchange.get(market, market)
            context.set_target_value("exchange", exchange)
        
        return context
    
    def _convert_market(self, value: Any, context: TransformContext) -> str:
        """转换市场代码"""
        if isinstance(value, str):
            canon_market = StockSymbol._canon_market(value)
            if canon_market in self.supported_markets:
                return canon_market
        
        return str(value) if value is not None else ""
    
    def _convert_exchange(self, value: Any, context: TransformContext) -> str:
        """转换交易所代码"""
        if isinstance(value, str):
            canon_exchange = StockSymbol._canon_market(value)
            if canon_exchange in self.market_to_exchange:
                return self.market_to_exchange[canon_exchange]
            return canon_exchange
        
        return str(value) if value is not None else ""
    
    def _get_market_hint(self, params: Dict[str, Any], example: Dict[str, Any]) -> str:
        """获取市场提示"""
        allowed_markets = {"SH", "SZ", "BJ", "HK", "US"}
        for key in ("market", "exchange"):
            if key in params and isinstance(params[key], str):
                v = params[key].strip()
                if v:
                    canon = StockSymbol._canon_market(v)
                    if canon in allowed_markets:
                        return canon
            if key in example and isinstance(example[key], str):
                v = example[key].strip()
                if v:
                    canon = StockSymbol._canon_market(v)
                    if canon in allowed_markets:
                        return canon
        return ""
