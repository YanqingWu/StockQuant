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
    # 选一个最小参数接口：优先 stock profile，如未启用则跳过
    if not _is_enabled(manager, "stock", "profile"):
        pytest.skip("stock.profile 未启用，跳过")

    # 注入一个未知参数键，验证会被适配器过滤
    params = StandardParams(symbol=_sym(), extra={"bad_key": "SHOULD_BE_FILTERED"})
    res = manager.get_stock_profile(params)

    # 确认适配器被调用
    assert calls["count"] > 0, "AkshareStockParamAdapter.adapt 未被调用"

    # 确认未知键被过滤
    if calls["last"] is not None:
        _, raw_params, adapted = calls["last"]
        assert "bad_key" in raw_params, "测试前置错误：raw_params 未包含注入的未知键"
        assert "bad_key" not in adapted, "适配器未过滤未知键，导致向底层传入未声明参数"

    # 同时复用通用断言，要求该接口成功（若此处失败，将暴露真实链路问题）
    _assert_result(manager, "stock", "profile", res, "get_stock_profile")


# --------- 占位测试 ---------

def test_placeholder():
    assert True


# ==================== 股票相关接口 ====================

def test_get_stock_profile():
    """测试获取股票基础信息"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "stock", "profile"):
        pytest.skip("stock.profile 未启用，跳过")
    params = StandardParams(symbol=_sym())
    res = manager.get_stock_profile(params)
    _assert_result(manager, "stock", "profile", res, "get_stock_profile")


def test_get_stock_company_profile():
    """测试获取公司详细信息"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "stock", "company_profile"):
        pytest.skip("stock.company_profile 未启用，跳过")
    params = StandardParams(symbol=_sym())
    res = manager.get_stock_company_profile(params)
    _assert_result(manager, "stock", "company_profile", res, "get_stock_company_profile")


def test_get_stock_daily_quote():
    """测试获取股票日行情数据"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "stock", "daily_market.quote"):
        pytest.skip("stock.daily_market.quote 未启用，跳过")
    params = StandardParams(symbol=_sym(), start_date=START, end_date=END, period="daily", adjust="qfq")
    res = manager.get_stock_daily_quote(params)
    _assert_result(manager, "stock", "daily_market.quote", res, "get_stock_daily_quote")


def test_get_stock_financing_data():
    """测试获取融资融券数据"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "stock", "daily_market.financing"):
        pytest.skip("stock.daily_market.financing 未启用，跳过")
    params = StandardParams(symbol=_sym(), start_date=START, end_date=END)
    res = manager.get_stock_financing_data(params)
    _assert_result(manager, "stock", "daily_market.financing", res, "get_stock_financing_data")


def test_get_stock_fund_flow():
    """测试获取股票资金流向数据"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "stock", "daily_market.fund_flow"):
        pytest.skip("stock.daily_market.fund_flow 未启用，跳过")
    params = StandardParams(symbol=_sym(), start_date=START, end_date=END)
    res = manager.get_stock_fund_flow(params)
    _assert_result(manager, "stock", "daily_market.fund_flow", res, "get_stock_fund_flow")


def test_get_stock_dragon_tiger():
    """测试获取龙虎榜数据"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "stock", "daily_market.dragon_tiger"):
        pytest.skip("stock.daily_market.dragon_tiger 未启用，跳过")
    params = StandardParams(symbol=_sym(), start_date=START, end_date=END)
    res = manager.get_stock_dragon_tiger(params)
    _assert_result(manager, "stock", "daily_market.dragon_tiger", res, "get_stock_dragon_tiger")


def test_get_stock_sentiment():
    """测试获取股票情绪数据"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "stock", "daily_market.sentiment"):
        pytest.skip("stock.daily_market.sentiment 未启用，跳过")
    params = StandardParams(symbol=_sym(), start_date=START, end_date=END)
    res = manager.get_stock_sentiment(params)
    _assert_result(manager, "stock", "daily_market.sentiment", res, "get_stock_sentiment")


def test_get_stock_news():
    """测试获取股票新闻数据"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "stock", "daily_market.news"):
        pytest.skip("stock.daily_market.news 未启用，跳过")
    params = StandardParams(symbol=_sym(), extra={"limit": 10})
    res = manager.get_stock_news(params)
    _assert_result(manager, "stock", "daily_market.news", res, "get_stock_news")


# ==================== 财务数据接口 ====================

def test_get_stock_balance_sheet():
    """测试获取资产负债表"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "stock", "financials.balance_sheet"):
        pytest.skip("stock.financials.balance_sheet 未启用，跳过")
    params = StandardParams(symbol=_sym(), extra={"report_date": "2023-12-31"})
    res = manager.get_stock_balance_sheet(params)
    _assert_result(manager, "stock", "financials.balance_sheet", res, "get_stock_balance_sheet")


def test_get_stock_income_statement():
    """测试获取利润表"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "stock", "financials.income_statement"):
        pytest.skip("stock.financials.income_statement 未启用，跳过")
    params = StandardParams(symbol=_sym(), extra={"report_date": "2023-12-31"})
    res = manager.get_stock_income_statement(params)
    _assert_result(manager, "stock", "financials.income_statement", res, "get_stock_income_statement")


def test_get_stock_cash_flow():
    """测试获取现金流量表"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "stock", "financials.cash_flow"):
        pytest.skip("stock.financials.cash_flow 未启用，跳过")
    params = StandardParams(symbol=_sym(), extra={"report_date": "2023-12-31"})
    res = manager.get_stock_cash_flow(params)
    _assert_result(manager, "stock", "financials.cash_flow", res, "get_stock_cash_flow")


# ==================== 市场相关接口 ====================

def test_get_stock_list():
    """测试获取股票列表数据"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "market", "stock_list"):
        pytest.skip("market.stock_list 未启用，跳过")
    params = StandardParams()
    res = manager.get_stock_list(params)
    _assert_result(manager, "market", "stock_list", res, "get_stock_list")


def test_get_market_overview():
    """测试获取市场概览数据"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "market", "market_overview"):
        pytest.skip("market.market_overview 未启用，跳过")
    params = StandardParams(date=TODAY)
    res = manager.get_market_overview(params)
    _assert_result(manager, "market", "market_overview", res, "get_market_overview")


def test_get_market_indices():
    """测试获取市场指数数据"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "market", "market_indices"):
        pytest.skip("market.market_indices 未启用，跳过")
    params = StandardParams(start_date=START, end_date=END, extra={"index_code": "000300.SH"})
    res = manager.get_market_indices(params)
    _assert_result(manager, "market", "market_indices", res, "get_market_indices")


def test_get_market_activity():
    """测试获取市场活跃度数据"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "market", "market_activity"):
        pytest.skip("market.market_activity 未启用，跳过")
    params = StandardParams(date=TODAY)
    res = manager.get_market_activity(params)
    _assert_result(manager, "market", "market_activity", res, "get_market_activity")


# ==================== 行业板块接口 ====================

def test_get_industry_sector_metadata():
    """测试获取行业板块元数据"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "market", "industry_sector.metadata"):
        pytest.skip("market.industry_sector.metadata 未启用，跳过")
    params = StandardParams()
    res = manager.get_industry_sector_metadata(params)
    _assert_result(manager, "market", "industry_sector.metadata", res, "get_industry_sector_metadata")


def test_get_industry_sector_quote():
    """测试获取行业板块行情"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "market", "industry_sector.quote"):
        pytest.skip("market.industry_sector.quote 未启用，跳过")
    params = StandardParams(start_date=START, end_date=END)
    res = manager.get_industry_sector_quote(params)
    _assert_result(manager, "market", "industry_sector.quote", res, "get_industry_sector_quote")


def test_get_industry_sector_constituents():
    """测试获取行业板块成分股"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "market", "industry_sector.constituents"):
        pytest.skip("market.industry_sector.constituents 未启用，跳过")
    params = StandardParams(extra={"sector_code": "801010"})
    res = manager.get_industry_sector_constituents(params)
    _assert_result(manager, "market", "industry_sector.constituents", res, "get_industry_sector_constituents")


# ==================== 概念板块接口 ====================

def test_get_concept_sector_metadata():
    """测试获取概念板块元数据"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "market", "concept_sector.metadata"):
        pytest.skip("market.concept_sector.metadata 未启用，跳过")
    params = StandardParams()
    res = manager.get_concept_sector_metadata(params)
    _assert_result(manager, "market", "concept_sector.metadata", res, "get_concept_sector_metadata")


def test_get_concept_sector_quote():
    """测试获取概念板块行情"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "market", "concept_sector.quote"):
        pytest.skip("market.concept_sector.quote 未启用，跳过")
    params = StandardParams(start_date=START, end_date=END)
    res = manager.get_concept_sector_quote(params)
    _assert_result(manager, "market", "concept_sector.quote", res, "get_concept_sector_quote")


def test_get_concept_sector_constituents():
    """测试获取概念板块成分股"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "market", "concept_sector.constituents"):
        pytest.skip("market.concept_sector.constituents 未启用，跳过")
    params = StandardParams(extra={"concept_code": "BK0001"})
    res = manager.get_concept_sector_constituents(params)
    _assert_result(manager, "market", "concept_sector.constituents", res, "get_concept_sector_constituents")


# ==================== 技术分析接口 ====================

def test_get_technical_indicators():
    """测试获取技术指标数据"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "market", "technical_analysis.indicators"):
        pytest.skip("market.technical_analysis.indicators 未启用，跳过")
    params = StandardParams(symbol=_sym(), date=TODAY)
    res = manager.get_technical_indicators(params)
    _assert_result(manager, "market", "technical_analysis.indicators", res, "get_technical_indicators")


def test_get_technical_ranking():
    """测试获取技术分析排名数据"""
    manager = ExtractorManager()
    if not _is_enabled(manager, "market", "technical_analysis.ranking"):
        pytest.skip("market.technical_analysis.ranking 未启用，跳过")
    params = StandardParams(date=TODAY)
    res = manager.get_technical_ranking(params)
    _assert_result(manager, "market", "technical_analysis.ranking", res, "get_technical_ranking")


# ==================== 工具方法测试 ====================

def test_get_available_data_types():
    """测试获取可用数据类型"""
    manager = ExtractorManager()
    available_types = manager.get_available_data_types()
    assert isinstance(available_types, dict), "get_available_data_types 应返回字典"
    print(f"可用数据类型: {available_types}")


def test_get_standard_fields():
    """测试获取标准字段"""
    manager = ExtractorManager()
    fields = manager.get_standard_fields("stock", "profile")
    assert isinstance(fields, list), "get_standard_fields 应返回列表"
    if fields:
        print(f"stock.profile 标准字段: {fields}")


def test_reload_config():
    """测试重新加载配置"""
    manager = ExtractorManager()
    # 这个测试不会失败，只是确保方法可以调用
    manager.reload_config()
    print("配置重新加载成功")