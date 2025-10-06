"""
标准参数类
定义统一的参数格式和转换方法
"""

import re
from typing import Any, Dict, Optional, List, Union
from .stock_symbol import StockSymbol


class StandardParams:
    """
    标准参数类，统一参数格式
    
    核心参数：
    - symbol: StockSymbol 对象或列表
    - start_date/end_date: "YYYY-MM-DD" 格式的日期范围
    - start_time/end_time: "HH:MM:SS" 格式的时间范围
    - period: daily/1min/5min/15min/30min/60min
    - adjust: none/qfq/hfq
    - market: SZ/SH/BJ (优先使用)
    - exchange: SZSE/SSE/BSE (补充)
    
    搜索参数：
    - keyword: 搜索关键词
    - ranking_type: 排名类型
    
    分页参数（二选一）：
    - page/page_size: 页码分页
    - offset/limit: 偏移分页
    """

    def __init__(
        self,
        *,
        symbol: Optional[Union[StockSymbol]] = None,
        # 时间参数：使用 start_date/end_date 替代单一的 date
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        period: Optional[str] = None,
        adjust: Optional[str] = None,
        # 市场参数：优先使用 market，exchange 作为补充
        market: Optional[str] = None,
        exchange: Optional[str] = None,
        # 搜索参数
        keyword: Optional[str] = None,
        ranking_type: Optional[str] = None,
        # 分页参数：统一使用 page/page_size 或 offset/limit
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.period = period
        self.adjust = adjust
        self.market = market
        self.exchange = exchange
        self.keyword = keyword
        self.ranking_type = ranking_type
        self.page = page
        self.page_size = page_size
        self.offset = offset
        self.limit = limit
        self.extra = dict(extra) if extra else {}
        
        # 参数验证
        self._validate_params()

    def _validate_params(self) -> None:
        """验证参数的有效性和一致性"""
        # 验证分页参数：不能同时使用 page/page_size 和 offset/limit
        if (self.page is not None or self.page_size is not None) and (self.offset is not None or self.limit is not None):
            raise ValueError("不能同时使用 page/page_size 和 offset/limit 分页参数")
        
        # 验证日期参数：start_date 不能晚于 end_date
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("start_date 不能晚于 end_date")
        
        # 验证时间参数：start_time 不能晚于 end_time
        if self.start_time and self.end_time and self.start_time > self.end_time:
            raise ValueError("start_time 不能晚于 end_time")
        
        # 验证数值参数不能为负数
        for param_name, value in [
            ("page", self.page), ("page_size", self.page_size),
            ("offset", self.offset), ("limit", self.limit)
        ]:
            if value is not None and value < 0:
                raise ValueError(f"{param_name} 不能为负数")

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
            "symbol", "start_date", "end_date", "start_time", "end_time",
            "period", "adjust", "market", "exchange", "keyword", "ranking_type",
            "page", "page_size", "offset", "limit",
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
