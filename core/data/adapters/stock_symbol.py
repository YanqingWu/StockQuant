"""
股票代码统一表达类
支持多种股票代码格式的解析和转换
"""

import re
from typing import Any, Dict, Optional, List, Tuple, Union


class StockSymbol:
    """
    股票代码统一表达类
    
    支持格式：
    - "000001.SZ" (点后缀)
    - "SZ000001" (前缀)
    - "000001" (纯代码)
    """

    # 市场映射已移至ConversionRules中统一管理

    DOT_RE = re.compile(r"^(?P<code>\d{5,6}|[A-Z]{1,5})\.(?P<mkt>[A-Za-z]{2})$")
    PREFIX_RE = re.compile(r"^(?P<mkt>[A-Za-z]{2})(?P<code>\d{5,6}|[A-Z]{1,5})$")
    US_CODE_RE = re.compile(r"^(?P<code>[A-Z]{1,5})$")  # 美股字母代码

    def __init__(self, market: str, code: str) -> None:
        # 参数校验
        self._validate_inputs(market, code)
        
        self.market = self._canon_market(market)
        self.code = code.strip() if isinstance(code, str) else str(code)

    def __repr__(self) -> str:
        return f"StockSymbol(market={self.market!r}, code={self.code!r})"

    @classmethod
    def _validate_inputs(cls, market: str, code: str) -> None:
        """校验输入参数的有效性"""
        # 校验market参数
        if not market:
            raise ValueError("市场代码不能为空")
        
        if not isinstance(market, str):
            raise ValueError(f"市场代码必须是字符串类型，当前类型: {type(market).__name__}")
        
        market_clean = market.strip()
        if not market_clean:
            raise ValueError("市场代码不能为空字符串")
        
        # 校验code参数
        if not code:
            raise ValueError("股票代码不能为空")
        
        if not isinstance(code, (str, int)):
            raise ValueError(f"股票代码必须是字符串或数字类型，当前类型: {type(code).__name__}")
        
        code_str = str(code).strip()
        if not code_str:
            raise ValueError("股票代码不能为空字符串")
        
        # 校验市场代码格式
        canon_market = cls._canon_market(market)
        if canon_market and canon_market not in {"SH", "SZ", "BJ", "HK", "US"}:
            raise ValueError(f"不支持的市场代码: {market} (标准化后: {canon_market})")
        
        # 校验股票代码格式与市场的匹配性
        cls._validate_code_market_consistency(code_str, canon_market)
    
    @classmethod
    def _validate_code_market_consistency(cls, code: str, market: str) -> None:
        """校验股票代码格式与市场代码的一致性"""
        if not market:  # 如果市场为空，跳过一致性检查
            return
            
        # A股市场代码格式校验
        if market in {"SH", "SZ", "BJ"}:
            if not re.fullmatch(r"\d{6}", code):
                raise ValueError(f"A股代码必须是6位数字，当前代码: {code}")
            
            # 进一步校验代码前缀与市场的匹配
            inferred_market = cls._infer_market_by_code(code)
            # 指数代码特殊情况：上证指数等以 000 开头，但市场以前缀确定（如 sh000001）
            if market == "SH" and re.fullmatch(r"000\d{3}", code):
                return
            if inferred_market and inferred_market != market:
                raise ValueError(
                    f"股票代码 {code} 的格式表明它属于 {inferred_market} 市场，"
                    f"但指定的市场是 {market}"
                )
        
        # 港股代码格式校验
        elif market == "HK":
            if not re.fullmatch(r"\d{5}", code):
                raise ValueError(f"港股代码必须是5位数字，当前代码: {code}")
        
        # 美股代码格式校验
        elif market == "US":
            if not re.fullmatch(r"[A-Z]{1,5}", code.upper()):
                raise ValueError(f"美股代码必须是1-5位字母，当前代码: {code}")

    @classmethod
    def _canon_market(cls, market: Optional[str]) -> str:
        """标准化市场代码 - 委托给ConversionRules"""
        from .conversion_rules import ConversionRules
        return ConversionRules.canon_market(market)

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
        # 港股5位数字代码（如 00700）
        if re.fullmatch(r"\d{5}", s2):
            # 明确以代码前缀为准，若显式 market 与代码推断不一致，则以代码推断覆盖
            inferred = "HK"
            canon_hint = cls._canon_market(hint_market)
            mkt = inferred if canon_hint and canon_hint != inferred else (canon_hint or inferred)
            return cls(mkt, s2)
        
        # A股6位数字代码
        if re.fullmatch(r"\d{6}", s2):
            inferred = cls._infer_market_by_code(s2)
            canon_hint = cls._canon_market(hint_market)
            # 如果显式提示是A股市场但与代码推断不一致，则使用代码推断，以避免后续一致性报错
            if canon_hint in {"SH", "SZ", "BJ"} and canon_hint != inferred:
                mkt = inferred
            else:
                mkt = canon_hint or inferred
            return cls(mkt, s2)
        
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
        # - 4/8 打头 -> BJ（北交所/新三板）
        # - 920 打头 -> BJ（北交所新代码号段）
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
        if code[0] in {"4", "8"}:  # 新三板和北交所
            return "BJ"
        if code.startswith("920"):  # 北交所新代码号段
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
