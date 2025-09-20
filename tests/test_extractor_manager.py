import os
import sys
import pandas as pd
import pytest

# 确保可以导入本仓库内的 core 包
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.data.extractor.extractor_manager import ExtractorManager, ExtractionResult
from core.data.extractor.adapter import StandardParams, StockSymbol


# --------- 公共工具 ---------
TODAY = "2025-09-20"
START = "2025-09-14"
END = "2025-09-20"


def _sym(code: str = "000001.SZ") -> StockSymbol:
    return StockSymbol.parse(code)


def _is_enabled(manager: ExtractorManager, category: str, data_type: str) -> bool:
    available = manager.get_available_data_types()
    return data_type in available.get(category, [])


def _assert_result(manager: ExtractorManager, category: str, data_type: str, result: ExtractionResult, method_name: str) -> None:
    """收紧断言：真实使用场景中，启用的接口应当返回成功，否则视为失败以暴露问题。"""
    assert isinstance(result, ExtractionResult), f"{method_name} 应返回 ExtractionResult"
    if result.success:
        assert isinstance(result.data, pd.DataFrame), f"{method_name} 成功时 data 应为 DataFrame"
        assert not result.data.empty, f"{method_name} 返回 DataFrame 不应为空"
        standard_fields = manager.get_standard_fields(category, data_type)
        if standard_fields:
            unexpected_cols = [c for c in result.data.columns if c not in standard_fields]
            if unexpected_cols:
                print(f"[WARN] {method_name} 返回包含未在标准字段中的列: {unexpected_cols}")
    else:
        # 之前宽松地只要求有 error，这会掩盖大量真实失败，这里直接失败以暴露问题
        pytest.fail(f"{method_name} 失败: {result.error}")


# --------- 适配器真实调用保障测试 ---------

def test_adapter_is_called_and_filters_unknown_keys(monkeypatch):
    """
    确认 ExtractorManager 在真实调用链上确实使用了 AkshareStockParamAdapter，且适配器会过滤未知参数键。
    通过 monkeypatch 将 extractor_manager.AkshareStockParamAdapter 替换为 SpyAdapter，记录调用与产出。
    """
    import core.data.extractor.extractor_manager as em
    import core.data.extractor.adapter as ad

    OriginalAdapter = ad.AkshareStockParamAdapter

    calls = {"count": 0, "last": None}

    class SpyAdapter(OriginalAdapter):
        def adapt(self, interface_name: str, params):
            calls["count"] += 1
            res = super().adapt(interface_name, params)
            # 记录一次调用（浅拷贝避免外部修改影响断言）
            try:
                calls["last"] = (interface_name, dict(params), dict(res))
            except Exception:
                calls["last"] = (interface_name, params, res)
            return res

    # 将 ExtractorManager 内部引用替换为 SpyAdapter
    monkeypatch.setattr(em, "AkshareStockParamAdapter", SpyAdapter, raising=True)

    manager = ExtractorManager()
    # 选一个最小参数接口：优先 real-time quote，如未启用则跳过
    if not _is_enabled(manager, "market_data", "realtime_quote"):
        pytest.skip("market_data.realtime_quote 未启用，跳过")

    # 注入一个未知参数键，验证会被适配器过滤
    params = StandardParams(symbol=_sym(), extra={"bad_key": "SHOULD_BE_FILTERED"})
    res = manager.get_realtime_quote(params)

    # 确认适配器被调用
    assert calls["count"] > 0, "AkshareStockParamAdapter.adapt 未被调用"

    # 确认未知键被过滤
    if calls["last"] is not None:
        _, raw_params, adapted = calls["last"]
        assert "bad_key" in raw_params, "测试前置错误：raw_params 未包含注入的未知键"
        assert "bad_key" not in adapted, "适配器未过滤未知键，导致向底层传入未声明参数"

    # 同时复用通用断言，要求该接口成功（若此处失败，将暴露真实链路问题）
    _assert_result(manager, "market_data", "realtime_quote", res, "get_realtime_quote")


# --------- 占位测试 ---------

def test_placeholder():
    assert True


# ==================== 静态信息类 ====================

def test_get_stock_basic_info():
    manager = ExtractorManager()
    if not _is_enabled(manager, "static_info", "stock_basic_info"):
        pytest.skip("static_info.stock_basic_info 未启用，跳过")
    params = StandardParams(symbol=_sym())
    res = manager.get_stock_basic_info(params)
    _assert_result(manager, "static_info", "stock_basic_info", res, "get_stock_basic_info")


def test_get_company_profile():
    manager = ExtractorManager()
    if not _is_enabled(manager, "static_info", "company_profile"):
        pytest.skip("static_info.company_profile 未启用，跳过")
    params = StandardParams(symbol=_sym())
    res = manager.get_company_profile(params)
    _assert_result(manager, "static_info", "company_profile", res, "get_company_profile")


def test_get_industry_classification():
    manager = ExtractorManager()
    if not _is_enabled(manager, "static_info", "industry_classification"):
        pytest.skip("static_info.industry_classification 未启用，跳过")
    params = StandardParams(symbol=_sym())
    res = manager.get_industry_classification(params)
    _assert_result(manager, "static_info", "industry_classification", res, "get_industry_classification")


# ==================== 市场数据类 ====================

def test_get_realtime_quote():
    manager = ExtractorManager()
    if not _is_enabled(manager, "market_data", "realtime_quote"):
        pytest.skip("market_data.realtime_quote 未启用，跳过")
    params = StandardParams(symbol=_sym())
    res = manager.get_realtime_quote(params)
    _assert_result(manager, "market_data", "realtime_quote", res, "get_realtime_quote")


def test_get_historical_quote():
    manager = ExtractorManager()
    if not _is_enabled(manager, "market_data", "historical_quote"):
        pytest.skip("market_data.historical_quote 未启用，跳过")
    params = StandardParams(symbol=_sym(), start_date=START, end_date=END, period="daily", adjust="qfq")
    res = manager.get_historical_quote(params)
    _assert_result(manager, "market_data", "historical_quote", res, "get_historical_quote")


def test_get_intraday_data():
    manager = ExtractorManager()
    if not _is_enabled(manager, "market_data", "intraday_data"):
        pytest.skip("market_data.intraday_data 未启用，跳过")
    params = StandardParams(symbol=_sym(), date=TODAY)
    res = manager.get_intraday_data(params)
    _assert_result(manager, "market_data", "intraday_data", res, "get_intraday_data")


# ==================== 财务数据类 ====================

def test_get_financial_statements():
    manager = ExtractorManager()
    if not _is_enabled(manager, "financial_data", "financial_statements"):
        pytest.skip("financial_data.financial_statements 未启用，跳过")
    params = StandardParams(symbol=_sym(), extra={"report_date": "2023-12-31"})
    res = manager.get_financial_statements(params)
    _assert_result(manager, "financial_data", "financial_statements", res, "get_financial_statements")


def test_get_financial_indicators():
    manager = ExtractorManager()
    if not _is_enabled(manager, "financial_data", "financial_indicators"):
        pytest.skip("financial_data.financial_indicators 未启用，跳过")
    params = StandardParams(symbol=_sym(), extra={"report_date": "2023-12-31"})
    res = manager.get_financial_indicators(params)
    _assert_result(manager, "financial_data", "financial_indicators", res, "get_financial_indicators")


def test_get_dividend_info():
    manager = ExtractorManager()
    if not _is_enabled(manager, "financial_data", "dividend_info"):
        pytest.skip("financial_data.dividend_info 未启用，跳过")
    params = StandardParams(symbol=_sym(), extra={"year": 2023})
    res = manager.get_dividend_info(params)
    _assert_result(manager, "financial_data", "dividend_info", res, "get_dividend_info")


# ==================== 技术分析类 ====================

def test_get_technical_indicators():
    manager = ExtractorManager()
    if not _is_enabled(manager, "technical_data", "technical_indicators"):
        pytest.skip("technical_data.technical_indicators 未启用，跳过")
    params = StandardParams(symbol=_sym(), date=TODAY)
    res = manager.get_technical_indicators(params)
    _assert_result(manager, "technical_data", "technical_indicators", res, "get_technical_indicators")


def test_get_market_sentiment():
    manager = ExtractorManager()
    if not _is_enabled(manager, "technical_data", "market_sentiment"):
        pytest.skip("technical_data.market_sentiment 未启用，跳过")
    params = StandardParams(symbol=_sym(), date=TODAY)
    res = manager.get_market_sentiment(params)
    _assert_result(manager, "technical_data", "market_sentiment", res, "get_market_sentiment")


# ==================== 市场宏观类 ====================

def test_get_market_indices():
    manager = ExtractorManager()
    if not _is_enabled(manager, "market_macro", "market_indices"):
        pytest.skip("market_macro.market_indices 未启用，跳过")
    params = StandardParams(start_date=START, end_date=END, extra={"index_code": "000300.SH"})
    res = manager.get_market_indices(params)
    _assert_result(manager, "market_macro", "market_indices", res, "get_market_indices")


def test_get_market_overview():
    manager = ExtractorManager()
    if not _is_enabled(manager, "market_macro", "market_overview"):
        pytest.skip("market_macro.market_overview 未启用，跳过")
    params = StandardParams(date=TODAY)
    res = manager.get_market_overview(params)
    _assert_result(manager, "market_macro", "market_overview", res, "get_market_overview")


# ==================== 特殊数据类 ====================

def test_get_research_reports():
    manager = ExtractorManager()
    if not _is_enabled(manager, "special_data", "research_reports"):
        pytest.skip("special_data.research_reports 未启用，跳过")
    params = StandardParams(symbol=_sym(), extra={"limit": 5})
    res = manager.get_research_reports(params)
    _assert_result(manager, "special_data", "research_reports", res, "get_research_reports")


def test_get_news_events():
    manager = ExtractorManager()
    if not _is_enabled(manager, "special_data", "news_events"):
        pytest.skip("special_data.news_events 未启用，跳过")
    params = StandardParams(symbol=_sym(), extra={"limit": 5})
    res = manager.get_news_events(params)
    _assert_result(manager, "special_data", "news_events", res, "get_news_events")


def test_get_other_data():
    manager = ExtractorManager()
    if not _is_enabled(manager, "special_data", "other_data"):
        pytest.skip("special_data.other_data 未启用，跳过")
    params = StandardParams(symbol=_sym(), extra={"data_type": "custom"})
    res = manager.get_other_data(params)
    _assert_result(manager, "special_data", "other_data", res, "get_other_data")