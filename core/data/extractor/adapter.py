"""
股票标的统一表达与接口参数适配器
- 不改动现有接口与执行器，仅提供工具类/适配器供上层在调用前做参数转换
- 通过已注册接口的 example_params 自动推断目标参数的股票代码风格
- 扩展：日期/时间/周期/复权等常见参数也做格式适配；参数名按接口元数据收敛，过滤未知参数
"""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List, Tuple, Union

from ..interfaces.base import get_interface_metadata


class StockSymbol:
    """
    统一的股票标的表达。
    - 内部统一为 (market, code)，如 ("SZ", "000001")
    - 支持解析以下输入：
      - "000001.SZ" / "600000.SH"（点后缀）
      - "SZ000001" / "SH600000"（前缀）
      - "000001"（纯代码，可结合 hint_market 或按简单规则推断）
    - 提供多种格式化输出：dot、prefix、code-only
    """

    MARKET_ALIASES = {
        "sz": "SZ",
        "sh": "SH",
        "bj": "BJ",
        "hk": "HK",
        "us": "US",
        "szse": "SZ",
        "sse": "SH",
        "bse": "BJ",
        "hkex": "HK",
        "nasdaq": "US",
        "nyse": "US",
        "港股": "HK",
        "美股": "US",
    }

    DOT_RE = re.compile(r"^(?P<code>\d{5,6}|[A-Z]{1,5})\.(?P<mkt>[A-Za-z]{2})$")
    PREFIX_RE = re.compile(r"^(?P<mkt>[A-Za-z]{2})(?P<code>\d{5,6}|[A-Z]{1,5})$")
    HK_CODE_RE = re.compile(r"^(?P<code>\d{5})$")  # 港股5位数字代码
    US_CODE_RE = re.compile(r"^(?P<code>[A-Z]{1,5})$")  # 美股字母代码

    def __init__(self, market: str, code: str) -> None:
        self.market = self._canon_market(market)
        self.code = code

    def __repr__(self) -> str:
        return f"StockSymbol(market={self.market!r}, code={self.code!r})"

    @classmethod
    def _canon_market(cls, market: Optional[str]) -> str:
        if not market:
            return ""
        key = str(market).strip().lower()
        return cls.MARKET_ALIASES.get(key, key.upper())

    @classmethod
    def parse(
        cls,
        value: Union[str, Dict[str, Any], Tuple[str, str]],
        *,
        hint_market: Optional[str] = None,
    ) -> Optional["StockSymbol"]:
        if value is None:
            return None
        if isinstance(value, cls):
            return value
        if isinstance(value, tuple) and len(value) == 2:
            return cls(value[0], value[1])
        if isinstance(value, dict):
            m = value.get("market") or value.get("exchange")
            c = value.get("code") or value.get("symbol") or value.get("stock")
            if isinstance(c, str):
                return cls._parse_from_str(c, hint_market=m or hint_market)
            if m and c:
                return cls(m, str(c))
            return None
        if isinstance(value, str):
            return cls._parse_from_str(value, hint_market=hint_market)
        return None

    @classmethod
    def _parse_from_str(cls, s: str, *, hint_market: Optional[str] = None) -> Optional["StockSymbol"]:
        if not s:
            return None
        s2 = s.strip().upper()
        # 忽略中文或非股票代码的情况
        if re.search(r"[\u4e00-\u9fff]", s2):
            return None
        # 点后缀
        m = cls.DOT_RE.match(s2)
        if m:
            return cls(m.group("mkt"), m.group("code"))
        
        # 纯代码优先匹配（避免被前缀模式误匹配）
        # A股6位数字代码
        if re.fullmatch(r"\d{6}", s2):
            mkt = cls._canon_market(hint_market) or cls._infer_market_by_code(s2)
            return cls(mkt, s2)
        
        # 港股5位数字代码
        m = cls.HK_CODE_RE.match(s2)
        if m:
            mkt = cls._canon_market(hint_market) or "HK"
            return cls(mkt, m.group("code"))
        
        # 美股字母代码
        m = cls.US_CODE_RE.match(s2)
        if m:
            mkt = cls._canon_market(hint_market) or "US"
            return cls(mkt, m.group("code"))
        
        # 前缀（放在最后，避免误匹配纯代码）
        m = cls.PREFIX_RE.match(s2)
        if m:
            return cls(m.group("mkt"), m.group("code"))
        
        return None

    @staticmethod
    def _infer_market_by_code(code: str) -> str:
        # 简单规则：
        # - 6 打头 -> SH (上海A股)
        # - 0/2/3 打头 -> SZ (深圳A股)
        # - 8 打头 -> BJ（北交所/新三板）
        # - 5位数字 -> HK (港股)
        # - 字母代码 -> US (美股)
        if not code:
            return ""
        
        # 港股：5位数字代码
        if re.fullmatch(r"\d{5}", code):
            return "HK"
        
        # 美股：字母代码
        if re.fullmatch(r"[A-Z]{1,5}", code):
            return "US"
        
        # A股：6位数字代码
        if code.startswith("6"):
            return "SH"
        if code[0] in {"0", "2", "3"}:
            return "SZ"
        if code.startswith("8"):
            return "BJ"
        
        return ""

    # 格式化输出
    def to_dot(self) -> str:
        return f"{self.code}.{self.market}" if self.market else self.code

    def to_prefix(self) -> str:
        return f"{self.market}{self.code}" if self.market else self.code

    def to_code(self) -> str:
        return self.code

    def to_tuple(self) -> Tuple[str, str]:
        return (self.market, self.code)

# ---- NEW: Unified standard parameter class ----
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

# ---- NEW: normalize any inputs to strict StandardParams ----
def to_standard_params(params: Union[StandardParams, Dict[str, Any]]) -> StandardParams:
    """
    将宽松/多风格输入规范化为严格格式的 StandardParams。
    - 若传入 StandardParams，视为已规范化，直接返回（不做二次转换）。
    - 若传入 dict，执行以下收敛：
      symbol -> StockSymbol 对象（内部统一表示）；date/time -> YYYY-MM-DD / HH:MM:SS；
      period -> {daily,1min,5min,15min,30min,60min}；adjust -> {none,qfq,hfq}；
      market/exchange -> {SZ,SH,BJ}/{SZSE,SSE,BSE}；支持常见别名与逗号分隔/列表输入。
    """
    if isinstance(params, StandardParams):
        return params

    src: Dict[str, Any] = dict(params or {})
    adapter = AkshareStockParamAdapter()

    def as_list_or_single(value: Any, convert_one):
        # 允许列表或逗号分隔字符串，输出保持为单个对象或对象列表
        if isinstance(value, list):
            return [convert_one(v) for v in value]
        if isinstance(value, str) and "," in value:
            parts = [p.strip() for p in value.split(",") if p.strip()]
            result = [convert_one(p) for p in parts]
            return result
        return convert_one(value)

    # market hint
    hint = AkshareStockParamAdapter._get_market_hint(src, example={})

    # symbol -> StockSymbol
    symbol_val = adapter._pick_from_aliases(src, adapter.SYMBOL_KEYS)

    def sym_to_obj(v: Any) -> Any:
        if v is None:
            return None
        return StockSymbol.parse(v, hint_market=hint)

    symbol_norm: Optional[Union[StockSymbol, List[StockSymbol]]] = None
    if symbol_val is not None:
        symbol_norm = as_list_or_single(symbol_val, sym_to_obj)

    # date family -> YYYY-MM-DD
    def to_date(v: Any) -> Any:
        style = "y-m-d"
        return adapter._convert_date(str(v), style) if v is not None else v

    date_norm = None
    start_date_norm = None
    end_date_norm = None

    date_val = adapter._pick_from_aliases(src, adapter.DATE_KEYS)
    if date_val is not None:
        date_norm = adapter._apply_to_value(date_val, to_date)

    start_date_val = adapter._pick_from_aliases(src, adapter.START_DATE_KEYS)
    if start_date_val is not None:
        start_date_norm = adapter._apply_to_value(start_date_val, to_date)

    end_date_val = adapter._pick_from_aliases(src, adapter.END_DATE_KEYS)
    if end_date_val is not None:
        end_date_norm = adapter._apply_to_value(end_date_val, to_date)

    # time family -> HH:MM:SS
    def to_time(v: Any) -> Any:
        style = "h:m:s"
        return adapter._convert_time(str(v), style) if v is not None else v

    start_time_norm = None
    end_time_norm = None

    start_time_val = adapter._pick_from_aliases(src, adapter.START_TIME_KEYS)
    if start_time_val is not None:
        start_time_norm = adapter._apply_to_value(start_time_val, to_time)

    end_time_val = adapter._pick_from_aliases(src, adapter.END_TIME_KEYS)
    if end_time_val is not None:
        end_time_norm = adapter._apply_to_value(end_time_val, to_time)

    # period -> canonical set
    period_norm = None
    period_val = adapter._pick_from_aliases(src, adapter.PERIOD_KEYS)
    if period_val is not None:
        def to_period(v: Any) -> Any:
            if not isinstance(v, (str, int)):
                return v
            s = str(v).strip().lower()
            if s in {"daily", "day", "d"}:
                return "daily"
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
    adjust_val = adapter._pick_from_aliases(src, adapter.ADJUST_KEYS)
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

    m_val = adapter._pick_from_aliases(src, adapter.MARKET_KEYS)
    if isinstance(m_val, str) and m_val.strip():
        market_norm = StockSymbol._canon_market(m_val)
    e_val = adapter._pick_from_aliases(src, adapter.EXCHANGE_KEYS)
    if isinstance(e_val, str) and e_val.strip():
        e_key = e_val.strip().upper()
        ex_alias = {"SZ": "SZSE", "SH": "SSE", "BJ": "BSE", "SZSE": "SZSE", "SSE": "SSE", "BSE": "BSE"}
        exchange_norm = ex_alias.get(e_key, e_key)

    # 若只有 symbol 推断出 market/exchange
    if market_norm is None and symbol_norm is not None:
        sample = symbol_norm[0] if isinstance(symbol_norm, list) and symbol_norm else symbol_norm
        if isinstance(sample, StockSymbol) and sample.market:
            market_norm = sample.market
            exchange_norm = {"SZ": "SZSE", "SH": "SSE", "BJ": "BSE"}.get(sample.market, sample.market)

    # keyword/name
    keyword_norm = adapter._pick_from_aliases(src, adapter.KEYWORD_KEYS)

    # pagination
    def to_int(v: Any) -> Optional[int]:
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
            "symbol","stock","code","ts_code",
            "date","trade_date","start_date","from_date","begin_date",
            "end_date","to_date","start_time","end_time",
            "period","freq","frequency","adjust","fq","adj",
            "market","exchange","keyword","name",
            "page","page_size","offset","limit",
        }}
    )


class ParamAdapter(ABC):
    """参数适配器抽象类。"""

    @abstractmethod
    def adapt(self, interface_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """根据接口名称与输入参数返回转换后的新参数。失败时应回退原值。"""
        raise NotImplementedError


class AkshareStockParamAdapter(ParamAdapter):
    """
    Akshare 参数适配器：
    - 通过接口的 example_params 推断目标风格（dot/prefix/code-only）
    - 将输入中的股票代码统一解析后，按目标风格回写到参数中
    - 日期/时间/周期/复权参数做格式适配
    - 参数名按接口元数据收敛，过滤未知参数，避免向底层函数传递未定义的 kwargs
    - 尽量不改动与上述无关的参数；转换失败回退原值
    """

    SYMBOL_KEYS = ["symbol", "stock", "code", "ts_code", "index_code"]
    DATE_KEYS = ["date", "trade_date"]
    START_DATE_KEYS = ["start_date", "from_date", "begin_date"]
    END_DATE_KEYS = ["end_date", "to_date"]
    START_TIME_KEYS = ["start_time"]
    END_TIME_KEYS = ["end_time"]
    PERIOD_KEYS = ["period", "freq", "frequency"]
    ADJUST_KEYS = ["adjust", "fq", "adj"]
    MARKET_KEYS = ["market"]
    EXCHANGE_KEYS = ["exchange"]
    KEYWORD_KEYS = ["keyword", "name"]

    def adapt(self, interface_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        metadata = get_interface_metadata(interface_name)
        if not metadata:
            return params
        example = metadata.example_params or {}
        accepted_keys = set((metadata.required_params or []) + (metadata.optional_params or []))

        # 原始拷贝，用于从别名读取
        source_params = dict(params)
        new_params: Dict[str, Any] = {}

        # 如果接口不接受任何参数，直接返回空字典
        if not accepted_keys:
            return {}

        # 1) symbol 家族
        self._adapt_symbol_family(new_params, source_params, example, accepted_keys)

        # 2) 日期/时间 家族
        self._adapt_date_like(new_params, source_params, example, accepted_keys)
        self._adapt_time_like(new_params, source_params, example, accepted_keys)

        # 3) period 家族
        self._adapt_period(new_params, source_params, example, accepted_keys)

        # 4) adjust 家族
        self._adapt_adjust(new_params, source_params, example, accepted_keys)

        # 5) market/exchange（若在目标 keys 中）
        self._adapt_market_exchange(new_params, source_params, example, accepted_keys)

        # 6) keyword/name 简单同义映射
        self._map_synonym_family(new_params, source_params, self.KEYWORD_KEYS, accepted_keys)

        # 7) 复制剩余：保留所有被接受且尚未设置的原始键
        for k, v in source_params.items():
            if k in accepted_keys and k not in new_params:
                new_params[k] = v

        return new_params

    # ---- symbol ----
    def _adapt_symbol_family(
        self,
        out: Dict[str, Any],
        src: Dict[str, Any],
        example: Dict[str, Any],
        accepted: set,
    ) -> None:
        target = self._detect_target_key_style_case(example, accepted)
        if not target:
            return
        target_key, target_style, target_case = target
        src_key = self._find_symbol_key(src, prefer=target_key)
        if not src_key:
            return
        value = src.get(src_key)
        if value is None:
            return
        market_hint = self._get_market_hint(src, example)

        def apply_case(market: str) -> str:
            if target_case == "lower":
                return market.lower()
            if target_case == "upper":
                return market.upper()
            return market

        def convert_one(v: Any) -> Any:
            sym = StockSymbol.parse(v, hint_market=market_hint)
            if not sym:
                # 兼容如 "000001.沪深京" 等非标准市场后缀；若目标为 code，则尽量抽取 6 位代码
                if isinstance(v, str) and target_style == "code":
                    m = re.search(r"(\d{6})", v)
                    if m:
                        return m.group(1)
                return v
            if target_style == "dot":
                m = apply_case(sym.market)
                # 仅当市场为 2 位字母时输出 dot 风格，否则仅输出代码
                return f"{sym.code}.{m}" if re.fullmatch(r"[A-Za-z]{2}", m or "") else sym.code
            if target_style == "prefix":
                m = apply_case(sym.market)
                return f"{m}{sym.code}" if re.fullmatch(r"[A-Za-z]{2}", m or "") else sym.code
            if target_style == "code":
                return sym.to_code()
            return v

        converted = self._apply_to_value(value, convert_one)
        if target_key in accepted:
            out[target_key] = converted
        self._maybe_fill_market_fields(out, example, converted)

    def _detect_target_key_style_case(self, example: Dict[str, Any], accepted: set) -> Optional[Tuple[str, str, str]]:
        for k in self.SYMBOL_KEYS:
            if k in accepted:
                v = example.get(k)
                s = self._detect_symbol_style(v)
                if s:
                    case = self._detect_market_case(v)
                    return k, s, case
        for k in self.SYMBOL_KEYS:
            if k in accepted:
                return k, "unknown", "upper"
        return None

    @staticmethod
    def _detect_market_case(v: Any) -> str:
        if not isinstance(v, str):
            return "upper"
        if re.search(r"\.[a-z]{2}\b", v):
            return "lower"
        if re.search(r"\.[A-Z]{2}\b", v):
            return "upper"
        if re.search(r"\b[a-z]{2}\d{6}$", v):
            return "lower"
        if re.search(r"\b[A-Z]{2}\d{6}$", v):
            return "upper"
        return "upper"

    @staticmethod
    def _detect_symbol_style(v: Any) -> Optional[str]:
        if not isinstance(v, str):
            return None
        s = v.strip().upper()
        if re.fullmatch(r"\d{6}\.(SZ|SH|BJ)", s):
            return "dot"
        if re.fullmatch(r"(SZ|SH|BJ)\d{6}", s):
            return "prefix"
        if re.fullmatch(r"\d{6}", s):
            return "code"
        return None

    def _find_symbol_key(self, params: Dict[str, Any], *, prefer: Optional[str] = None) -> Optional[str]:
        if prefer and prefer in params:
            return prefer
        for k in self.SYMBOL_KEYS:
            if k in params:
                return k
        for k, v in params.items():
            if isinstance(v, dict):
                for kk in self.SYMBOL_KEYS:
                    if kk in v:
                        return k
        return None

    @classmethod
    def _get_market_hint(cls, params: Dict[str, Any], example: Dict[str, Any]) -> Optional[str]:
        # 1) 显式字段 market / exchange
        for key in ("market", "exchange"):
            if key in params and isinstance(params[key], str):
                v = params[key].strip()
                if v:
                    return StockSymbol._canon_market(v)
            if key in example and isinstance(example[key], str):
                v = example[key].strip()
                if v:
                    return StockSymbol._canon_market(v)
        # 2) 回退：从示例中的 symbol 风格解析出市场
        for k in getattr(cls, "SYMBOL_KEYS", ["symbol", "stock", "code", "ts_code"]):
            if k in example and isinstance(example[k], str):
                sym = StockSymbol.parse(example[k])
                if sym and sym.market:
                    return sym.market
        return None

    @staticmethod
    def _maybe_fill_market_fields(params_out: Dict[str, Any], example: Dict[str, Any], sym_val: Any) -> None:
        if not isinstance(sym_val, str):
            return
        sym = StockSymbol.parse(sym_val)
        if not sym:
            return
        market_short = sym.market
        if "market" in example and "market" not in params_out:
            params_out["market"] = market_short
        if "exchange" in example and "exchange" not in params_out:
            mapping = {"SZ": "SZSE", "SH": "SSE", "BJ": "BSE"}
            params_out["exchange"] = mapping.get(market_short, market_short)

    # ---- 日期/时间 ----
    def _adapt_date_like(self, out: Dict[str, Any], src: Dict[str, Any], example: Dict[str, Any], accepted: set) -> None:
        # date / trade_date
        target_date_key = self._pick_target_key(accepted, self.DATE_KEYS)
        if target_date_key:
            example_style = self._detect_date_style(example.get(target_date_key))
            value = self._pick_from_aliases(src, self.DATE_KEYS)
            if value is not None:
                out[target_date_key] = self._apply_to_value(value, lambda v: self._convert_date(v, example_style))
        # start_date
        target_start_key = self._pick_target_key(accepted, self.START_DATE_KEYS)
        if target_start_key:
            example_style = self._detect_date_style(example.get(target_start_key))
            value = self._pick_from_aliases(src, self.START_DATE_KEYS)
            if value is not None:
                out[target_start_key] = self._apply_to_value(value, lambda v: self._convert_date(v, example_style))
        # end_date
        target_end_key = self._pick_target_key(accepted, self.END_DATE_KEYS)
        if target_end_key:
            example_style = self._detect_date_style(example.get(target_end_key))
            value = self._pick_from_aliases(src, self.END_DATE_KEYS)
            if value is not None:
                out[target_end_key] = self._apply_to_value(value, lambda v: self._convert_date(v, example_style))

    def _adapt_time_like(self, out: Dict[str, Any], src: Dict[str, Any], example: Dict[str, Any], accepted: set) -> None:
        # start_time
        target_key = self._pick_target_key(accepted, self.START_TIME_KEYS)
        if target_key:
            example_style = self._detect_time_style(example.get(target_key))
            value = self._pick_from_aliases(src, self.START_TIME_KEYS)
            if value is not None:
                out[target_key] = self._apply_to_value(value, lambda v: self._convert_time(v, example_style))
        # end_time
        target_key = self._pick_target_key(accepted, self.END_TIME_KEYS)
        if target_key:
            example_style = self._detect_time_style(example.get(target_key))
            value = self._pick_from_aliases(src, self.END_TIME_KEYS)
            if value is not None:
                out[target_key] = self._apply_to_value(value, lambda v: self._convert_time(v, example_style))

    @staticmethod
    def _detect_date_style(v: Any) -> str:
        if isinstance(v, str) and re.fullmatch(r"\d{8}", v.strip()):
            return "ymd"
        if isinstance(v, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", v.strip()):
            return "y-m-d"
        # 默认使用 ymd
        return "ymd"

    @staticmethod
    def _convert_date(v: Any, target_style: str) -> Any:
        if not isinstance(v, str):
            return v
        s = v.strip()
        if not s:
            return v
        # 解析
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
            y, m, d = s.split("-")
        elif re.fullmatch(r"\d{8}", s):
            y, m, d = s[0:4], s[4:6], s[6:8]
        else:
            return v
        if target_style == "y-m-d":
            return f"{y}-{m}-{d}"
        return f"{y}{m}{d}"

    @staticmethod
    def _detect_time_style(v: Any) -> str:
        if isinstance(v, str) and re.fullmatch(r"\d{2}:\d{2}:\d{2}", v.strip()):
            return "h:m:s"
        if isinstance(v, str) and re.fullmatch(r"\d{6}", v.strip()):
            return "hms"
        return "h:m:s"

    @staticmethod
    def _convert_time(v: Any, target_style: str) -> Any:
        if not isinstance(v, str):
            return v
        s = v.strip()
        if not s:
            return v
        if re.fullmatch(r"\d{2}:\d{2}:\d{2}", s):
            hh, mm, ss = s.split(":")
        elif re.fullmatch(r"\d{6}", s):
            hh, mm, ss = s[0:2], s[2:4], s[4:6]
        else:
            return v
        if target_style == "hms":
            return f"{hh}{mm}{ss}"
        return f"{hh}:{mm}:{ss}"

    # ---- period ----
    def _adapt_period(self, out: Dict[str, Any], src: Dict[str, Any], example: Dict[str, Any], accepted: set) -> None:
        target_key = self._pick_target_key(accepted, self.PERIOD_KEYS)
        if not target_key:
            return
        example_val = example.get(target_key)
        target_is_numeric = isinstance(example_val, str) and bool(re.fullmatch(r"\d+", example_val))
        value = self._pick_from_aliases(src, self.PERIOD_KEYS)
        if value is None:
            return

        def convert(v: Any) -> Any:
            if not isinstance(v, (str, int)):
                return v
            s = str(v).strip().lower()
            # 常见输入：'5m' -> '5'
            m = re.fullmatch(r"(\d+)(m|min|minute)?", s)
            if m:
                return m.group(1) if target_is_numeric else s if s in {"daily"} else "daily"
            if s in {"daily", "day", "d"}:
                return "daily" if not target_is_numeric else s  # 数字目标无法从 daily 推断分钟，保持原值
            return v

        out[target_key] = self._apply_to_value(value, convert)

    # ---- adjust ----
    def _adapt_adjust(self, out: Dict[str, Any], src: Dict[str, Any], example: Dict[str, Any], accepted: set) -> None:
        target_key = self._pick_target_key(accepted, self.ADJUST_KEYS)
        if not target_key:
            return
        example_val = example.get(target_key, "")
        value = self._pick_from_aliases(src, self.ADJUST_KEYS)

        def norm(v: Any) -> Any:
            if v is None or (isinstance(v, str) and v.strip() == ""):
                return example_val
            if isinstance(v, str):
                s = v.strip().lower()
                if s in {"none", "no", "na", "n", "null"}:
                    return ""
                if s in {"qfq", "hfq"}:
                    return s
            return v

        if value is not None:
            out[target_key] = self._apply_to_value(value, norm)
        else:
            # 未提供时，如果示例给了默认值，写入默认值
            if example_val is not None:
                out[target_key] = example_val

    # ---- market / exchange ----
    def _adapt_market_exchange(self, out: Dict[str, Any], src: Dict[str, Any], example: Dict[str, Any], accepted: set) -> None:
        # 优先从 symbol 推断，一旦 symbol 已处理，_maybe_fill_market_fields 已经尽量补齐
        # 这里再做一次别名映射：如果接口需要 exchange 而输入给了 market（或反之）
        market_val = self._pick_from_aliases(src, self.MARKET_KEYS)
        exchange_val = self._pick_from_aliases(src, self.EXCHANGE_KEYS)
        if self._pick_target_key(accepted, self.MARKET_KEYS) and market_val is not None and "market" not in out:
            out["market"] = market_val
        if self._pick_target_key(accepted, self.EXCHANGE_KEYS) and exchange_val is not None and "exchange" not in out:
            out["exchange"] = exchange_val

    # ---- 通用别名拷贝 ----
    def _map_synonym_family(self, out: Dict[str, Any], src: Dict[str, Any], aliases: List[str], accepted: set) -> None:
        target_key = self._pick_target_key(accepted, aliases)
        if not target_key:
            return
        value = self._pick_from_aliases(src, aliases)
        if value is not None:
            out[target_key] = value

    # ---- 小工具 ----
    @staticmethod
    def _pick_target_key(accepted: set, aliases: List[str]) -> Optional[str]:
        for k in aliases:
            if k in accepted:
                return k
        return None

    @staticmethod
    def _pick_from_aliases(src: Dict[str, Any], aliases: List[str]) -> Any:
        for k in aliases:
            if k in src:
                return src[k]
        return None

    @staticmethod
    def _apply_to_value(value: Any, fn):
        # 支持列表与逗号分隔字符串
        if isinstance(value, list):
            return [fn(v) for v in value]
        if isinstance(value, str) and "," in value:
            parts = [p.strip() for p in value.split(",")]
            if all(p for p in parts):
                return ",".join(str(fn(p)) for p in parts)
        return fn(value)


def adapt_params_for_interface(interface_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
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


__all__ = [
    "StockSymbol",
    "StandardParams",
    "ParamAdapter",
    "AkshareStockParamAdapter",
    "adapt_params_for_interface",
    "to_standard_params",
]