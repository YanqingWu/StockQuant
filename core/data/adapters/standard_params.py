"""
标准参数类
定义统一的参数格式和转换方法
"""

import re
from typing import Any, Dict, Optional, List, Union
from .stock_symbol import StockSymbol


class StandardParams:
    """
    简化版标准参数类，统一参数格式
    
    核心参数：
    - symbol: StockSymbol (支持单个或列表)
    - start_date/end_date: "YYYY-MM-DD" 格式的日期范围
    - period: daily/1min/5min/15min/30min/60min (默认daily)
    - adjust: none/qfq/hfq (默认qfq)
    
    扩展参数：
    - indicator: 财务指标类型 (财务数据接口使用)
    - date: 单日期参数 (部分接口使用)
    - market: 市场代码 (可选，优先从symbol推断，支持SZ/SH/BJ/HK/US)
    
    其他参数通过extra传递，保持向后兼容性
    """

    def __init__(
        self,
        *,
        # 核心参数
        symbol: Optional[Union[StockSymbol, str, List[Union[StockSymbol, str]]]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = "daily",
        adjust: Optional[str] = "qfq",
        
        # 扩展参数
        indicator: Optional[str] = None,
        date: Optional[str] = None,
        market: Optional[str] = None,
        
        # 其他参数通过extra传递，保持向后兼容性
        **extra
    ) -> None:
        # 处理 symbol 参数：支持单个或列表
        if symbol is not None:
            if isinstance(symbol, list):
                self.symbol = [StockSymbol.parse(s) if isinstance(s, str) else s for s in symbol]
            elif isinstance(symbol, str):
                self.symbol = StockSymbol.parse(symbol)
            else:
                self.symbol = symbol
        else:
            self.symbol = None
            
        # 核心参数
        self.start_date = start_date
        self.end_date = end_date
        self.period = period
        self.adjust = adjust
        
        # 扩展参数
        self.indicator = indicator
        self.date = date
        self.market = market
        
        # 其他参数
        self.extra = extra
        
        # 参数验证
        self._validate_params()

    def _validate_params(self) -> None:
        """验证参数的有效性和一致性"""
        # 验证 symbol 类型（如果提供了）
        if self.symbol is not None:
            if isinstance(self.symbol, list):
                for i, s in enumerate(self.symbol):
                    if not isinstance(s, StockSymbol):
                        raise ValueError(f"symbol列表第{i}个元素必须是StockSymbol类型，实际: {type(s)}")
            elif not isinstance(self.symbol, StockSymbol):
                raise ValueError(f"symbol必须是StockSymbol类型，实际: {type(self.symbol)}")
        
        # 验证日期格式（如果提供了）
        for date_param in [self.start_date, self.end_date, self.date]:
            if date_param and not self._is_valid_date_format(date_param):
                raise ValueError(f"日期格式错误: {date_param}，期望 YYYY-MM-DD 格式")
        
        # 验证日期参数：start_date 不能晚于 end_date
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("start_date 不能晚于 end_date")
        
        # 验证枚举值
        if self.period and self.period not in ["daily", "1min", "5min", "15min", "30min", "60min"]:
            raise ValueError(f"period值无效: {self.period}，期望: daily/1min/5min/15min/30min/60min")
        
        if self.adjust and self.adjust not in ["none", "qfq", "hfq"]:
            raise ValueError(f"adjust值无效: {self.adjust}，期望: none/qfq/hfq")
        
        if self.market and self.market not in ["SZ", "SH", "BJ", "HK", "US"]:
            raise ValueError(f"market值无效: {self.market}，期望: SZ/SH/BJ/HK/US")
        
        # 验证字符串参数不能为空字符串
        for param_name, value in [
            ("start_date", self.start_date), ("end_date", self.end_date),
            ("date", self.date), ("period", self.period), ("adjust", self.adjust),
            ("indicator", self.indicator), ("market", self.market)
        ]:
            if value is not None and isinstance(value, str) and not value.strip():
                raise ValueError(f"{param_name} 不能为空字符串")
    
    def _is_valid_date_format(self, date_str: str) -> bool:
        """验证日期格式 YYYY-MM-DD"""
        import re
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(pattern, date_str):
            return False
        
        try:
            from datetime import datetime
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def _is_valid_time_format(self, time_str: str) -> bool:
        """验证时间格式 HH:MM:SS"""
        import re
        pattern = r'^\d{2}:\d{2}:\d{2}$'
        if not re.match(pattern, time_str):
            return False
        
        try:
            from datetime import datetime
            datetime.strptime(time_str, '%H:%M:%S')
            return True
        except ValueError:
            return False

    @staticmethod
    def _maybe_strip(v: Any) -> Any:
        return v.strip() if isinstance(v, str) else v

    def _symbol_to_dot(self, v: Any) -> Any:
        # 将 StockSymbol 或其列表/逗号分隔字符串输出为 dot 风格字符串或字符串列表
        def one(x: Any) -> Any:
            if isinstance(x, StockSymbol):
                m = x.market.upper() if x.market else ""
                return f"{x.code}.{m}" if re.fullmatch(r"[A-Za-z]{2}", m or "") else x.code
            if isinstance(x, str):
                sym = StockSymbol.parse(x)
                if sym:
                    m = sym.market
                    return f"{sym.code}.{m}" if (m and re.fullmatch(r"[A-Za-z]{2}", m)) else sym.code
                return x
            return x
        if isinstance(v, list):
            return [one(i) for i in v]
        return one(v)

    def to_dict(self) -> Dict[str, Any]:
        """
        输出严格格式的标准键名字典，仅包含非 None 值；extra 中的键在不与标准键冲突时透传。
        - symbol 字段在序列化时统一输出为 dot 风格字符串或字符串列表，便于后续适配到目标接口示例风格。
        """
        d: Dict[str, Any] = {}
        
        # 核心参数
        if self.symbol is not None:
            d["symbol"] = self._symbol_to_dot(self.symbol)
        if self.start_date is not None:
            d["start_date"] = self._maybe_strip(self.start_date)
        if self.end_date is not None:
            d["end_date"] = self._maybe_strip(self.end_date)
        if self.period is not None:
            d["period"] = self._maybe_strip(self.period)
        if self.adjust is not None:
            d["adjust"] = self._maybe_strip(self.adjust)
        
        # 扩展参数
        if self.indicator is not None:
            d["indicator"] = self._maybe_strip(self.indicator)
        if self.date is not None:
            d["date"] = self._maybe_strip(self.date)
        if self.market is not None:
            d["market"] = self._maybe_strip(self.market)

        # 透传额外键（不覆盖标准键）
        for k, v in self.extra.items():
            if k not in d:
                d[k] = v
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StandardParams":
        """从严格格式字典构建。非标准键将进入 extra，不做自动转换。
        - 若 symbol 为字符串或列表字符串，自动解析为 StockSymbol 或其列表。
        """
        known_keys = {
            "symbol", "start_date", "end_date", "period", "adjust",
            "indicator", "date", "market"
        }
        std_kwargs = {k: data[k] for k in known_keys if k in data}
        
        # 处理 symbol -> StockSymbol
        if "symbol" in std_kwargs:
            sym_val = std_kwargs["symbol"]
            def to_obj(x: Any) -> Any:
                if isinstance(x, StockSymbol):
                    return x
                return StockSymbol.parse(x)
            if isinstance(sym_val, list):
                std_kwargs["symbol"] = [to_obj(i) for i in sym_val]
            else:
                std_kwargs["symbol"] = to_obj(sym_val)
        
        # 其他参数进入extra
        extra = {k: v for k, v in data.items() if k not in known_keys}
        return cls(**std_kwargs, **extra)
