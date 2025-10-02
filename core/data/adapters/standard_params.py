"""
标准参数类
从原adapter.py中提取
"""

import re
from typing import Any, Dict, Optional, List, Union
from .stock_symbol import StockSymbol


class StandardParams:
    """
    统一的标准参数类（严格格式）。外部模块应仅通过该类设置/传递参数。

    严格格式定义（必须满足，不做多种风格）：
    - symbol: StockSymbol 或 List[StockSymbol]；统一用对象表示股票标的，禁止混入字符串；
      仅在序列化（to_dict）时输出为 6 位代码 + 点 + 2 位大写市场后缀（例如 "000001.SZ"、"600000.SH"）。
    - date/start_date/end_date: str；格式严格为 "YYYY-MM-DD"（例如 "2024-01-31"）。
    - start_time/end_time: str；格式严格为 "HH:MM:SS"（例如 "09:30:00"）。
    - period: str；取值集合之一：{"daily", "1min", "5min", "15min", "30min", "60min"}。
    - adjust: str；取值集合之一：{"none", "qfq", "hfq"}。
    - market: str；取值集合之一：{"SZ", "SH", "BJ"}。
    - exchange: str；取值集合之一：{"SZSE", "SSE", "BSE"}。
    - keyword: str；任意关键词/名称（UTF-8）。
    - page: int >= 1；page_size: int >= 1；offset: int >= 0；limit: int >= 1。

    说明：严格格式由本模块的适配器工具负责转换收敛（如 to_standard_params），
    StandardParams 仅承载已经规范化后的值，不再接受多种输入风格的自动转换。
    """

    def __init__(
        self,
        *,
        symbol: Optional[Union[StockSymbol, List[StockSymbol]]] = None,
        date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        period: Optional[str] = None,
        adjust: Optional[str] = None,
        market: Optional[str] = None,
        exchange: Optional[str] = None,
        keyword: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        ranking_type: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.symbol = symbol
        self.date = date
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.period = period
        self.adjust = adjust
        self.market = market
        self.exchange = exchange
        self.keyword = keyword
        self.page = page
        self.page_size = page_size
        self.offset = offset
        self.limit = limit
        self.ranking_type = ranking_type
        self.extra = dict(extra) if extra else {}

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
        if self.symbol is not None:
            d["symbol"] = self._symbol_to_dot(self.symbol)
        if self.date is not None:
            d["date"] = self._maybe_strip(self.date)
        if self.start_date is not None:
            d["start_date"] = self._maybe_strip(self.start_date)
        if self.end_date is not None:
            d["end_date"] = self._maybe_strip(self.end_date)
        if self.start_time is not None:
            d["start_time"] = self._maybe_strip(self.start_time)
        if self.end_time is not None:
            d["end_time"] = self._maybe_strip(self.end_time)
        if self.period is not None:
            d["period"] = self._maybe_strip(self.period)
        if self.adjust is not None:
            d["adjust"] = self._maybe_strip(self.adjust)
        if self.market is not None:
            d["market"] = self._maybe_strip(self.market)
        if self.exchange is not None:
            d["exchange"] = self._maybe_strip(self.exchange)
        if self.keyword is not None:
            d["keyword"] = self._maybe_strip(self.keyword)
        if self.page is not None:
            d["page"] = self.page
        if self.page_size is not None:
            d["page_size"] = self.page_size
        if self.offset is not None:
            d["offset"] = self.offset
        if self.limit is not None:
            d["limit"] = self.limit
        if self.ranking_type is not None:
            d["ranking_type"] = self._maybe_strip(self.ranking_type)

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
            "symbol","date","start_date","end_date","start_time","end_time",
            "period","adjust","market","exchange","keyword",
            "page","page_size","offset","limit",
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
        extra = {k: v for k, v in data.items() if k not in known_keys}
        std_kwargs["extra"] = extra
        return cls(**std_kwargs)
