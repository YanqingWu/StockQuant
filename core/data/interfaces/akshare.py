# -*- coding: utf-8 -*-
"""
AKShare数据源接口提供者
自动生成于 2025-09-14 00:18:08
总共 340 个接口
"""

from typing import List
from .base import (
    BaseAPIProvider, InterfaceMetadata, FunctionCategory, create_interface,
    DataSource, ParameterPattern
)

class AkshareProvider(BaseAPIProvider):
    """AKShare数据接口提供者"""

    def __init__(self):
        super().__init__("akshare", DataSource.AKSHARE)

    def register_interfaces(self) -> None:
        """注册所有接口"""
        interfaces = []

        interfaces.extend(self._register_stock_basic_interfaces())
        interfaces.extend(self._register_other_interfaces())
        interfaces.extend(self._register_stock_technical_interfaces())
        interfaces.extend(self._register_stock_financial_interfaces())
        interfaces.extend(self._register_stock_quote_interfaces())
        interfaces.extend(self._register_market_index_interfaces())
        interfaces.extend(self._register_fund_data_interfaces())
        interfaces.extend(self._register_industry_data_interfaces())
        interfaces.extend(self._register_market_overview_interfaces())

        # 批量注册所有接口
        self.registry.register_interfaces(interfaces)

    def _register_stock_basic_interfaces(self) -> List[InterfaceMetadata]:
        """注册STOCK_BASIC接口"""
        return [
        create_interface("stock_a_all_pb")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("全部A股-等权重市净率、中位数市净率")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "A股", "a", "all", "pb")\
            .build(),

        create_interface("stock_a_below_net_asset_statistics")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("破净股统计历史走势")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "A股", "a", "net", "asset")\
            .with_example_params({"symbol": '全部A股'})\
            .build(),

        create_interface("stock_a_code_to_symbol")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("输入股票代码判断股票市场")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "to", "symbol", "股票", "code")\
            .with_example_params({"symbol": '000300'})\
            .build(),

        create_interface("stock_a_high_low_statistics")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("乐咕乐股-创新高、新低的股票数量")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("int")\
            .with_keywords("stock", "high", "股票", "a", "low")\
            .with_example_params({"symbol": 'all'})\
            .build(),

        create_interface("stock_a_ttm_lyr")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("全部 A 股-等权重市盈率、中位数市盈率")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "A股", "ttm", "a", "lyr")\
            .build(),

        create_interface("stock_account_statistics_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-股票账户统计")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("int")\
            .with_keywords("em", "account", "stock", "股票", "statistics")\
            .build(),

        create_interface("stock_allotment_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-个股-配股实施方案")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "allotment", "cninfo")\
            .with_example_params({"symbol": '600030', "start_date": '19700101', "end_date": '22220222'})\
            .build(),

        create_interface("stock_board_change_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富-行情中心-当日板块异动详情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "board", "change")\
            .build(),

        create_interface("stock_board_concept_index_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-板块-概念板块-指数数据")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "指数", "index", "ths", "concept")\
            .with_example_params({"symbol": '阿里巴巴概念', "start_date": '20200101', "end_date": '20250228'})\
            .build(),

        create_interface("stock_board_concept_info_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-板块-概念板块-板块简介")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ths", "info", "concept", "board")\
            .with_example_params({"symbol": '阿里巴巴概念'})\
            .build(),

        create_interface("stock_board_concept_name_em_async")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-行情中心-沪深京板块-概念板块-名称 (同步接口)")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "async", "stock", "name", "concept")\
            .build(),

        create_interface("stock_board_concept_name_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-板块-概念板块-概念")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "name", "ths", "concept", "board")\
            .build(),

        create_interface("stock_board_concept_summary_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-数据中心-概念板块-概念时间表")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ths", "summary", "concept", "board")\
            .build(),

        create_interface("stock_board_industry_index_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-板块-行业板块-指数数据")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "行业", "指数", "index", "industry")\
            .with_example_params({"symbol": '元件', "start_date": '20200101', "end_date": '20240108'})\
            .build(),

        create_interface("stock_board_industry_info_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-板块-行业板块-板块简介")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "行业", "industry", "info", "ths")\
            .with_example_params({"symbol": '半导体'})\
            .build(),

        create_interface("stock_board_industry_name_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-沪深板块-行业板块-名称")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "行业", "name", "industry")\
            .build(),

        create_interface("stock_board_industry_name_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-板块-行业板块-行业")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "行业", "name", "industry", "ths")\
            .build(),

        create_interface("stock_board_industry_summary_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-数据中心-行业板块-同花顺行业一览表")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "行业", "summary", "industry", "ths")\
            .build(),

        create_interface("stock_cg_equity_mortgage_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-数据中心-专题统计-公司治理-股权质押")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "cninfo", "equity", "mortgage", "cg")\
            .with_example_params({"date": '20210930'})\
            .build(),

        create_interface("stock_cg_guarantee_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-数据中心-专题统计-公司治理-对外担保")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "cninfo", "guarantee", "cg")\
            .with_example_params({"symbol": '全部', "start_date": '20180630', "end_date": '20210927'})\
            .build(),

        create_interface("stock_changes_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富-行情中心-盘口异动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "changes")\
            .with_example_params({"symbol": '大笔买入'})\
            .build(),

        create_interface("stock_circulate_stock_holder")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("新浪财经-股东股本-流通股东")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "holder", "circulate")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_comment_detail_scrd_desire_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-千股千评-市场热度-市场参与意愿")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("desire", "em", "stock", "detail", "scrd")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_comment_detail_scrd_focus_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-千股千评-市场热度-用户关注指数")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "focus", "指数", "detail")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_comment_detail_zhpj_lspf_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-千股千评-综合评价-历史评分")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "lspf", "detail", "股票")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_comment_detail_zlkp_jgcyd_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-千股千评-主力控盘-机构参与度")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zlkp", "jgcyd", "em", "stock", "detail")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_comment_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-千股千评")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("comment", "stock", "em")\
            .build(),

        create_interface("stock_concept_cons_futu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("富途牛牛-主题投资-概念板块-成分股")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("futu", "stock", "concept", "cons")\
            .with_example_params({"symbol": '特朗普概念股'})\
            .build(),

        create_interface("stock_dividend_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-个股-历史分红")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "dividend", "cninfo")\
            .with_example_params({"symbol": '600009'})\
            .build(),

        create_interface("stock_dzjy_hygtj")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-大宗交易-活跃 A 股统计")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "dzjy", "hygtj")\
            .with_example_params({"symbol": '近三月'})\
            .build(),

        create_interface("stock_dzjy_hyyybtj")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-大宗交易-活跃营业部统计")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hyyybtj", "dzjy")\
            .with_example_params({"symbol": '近3日'})\
            .build(),

        create_interface("stock_dzjy_mrtj")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-大宗交易-每日统计")\
            .with_optional_params("start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("mrtj", "stock", "dzjy")\
            .with_example_params({"start_date": '20220105', "end_date": '20220105'})\
            .build(),

        create_interface("stock_dzjy_sctj")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-大宗交易-市场统计")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "dzjy", "sctj")\
            .build(),

        create_interface("stock_fhps_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-分红送配-分红送配详情")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "detail", "股票", "fhps")\
            .with_example_params({"symbol": '300073'})\
            .build(),

        create_interface("stock_fhps_detail_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-分红情况")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "detail", "股票", "fhps", "ths")\
            .with_example_params({"symbol": '603444'})\
            .build(),

        create_interface("stock_fhps_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-年报季报-分红送配")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "fhps", "em")\
            .with_example_params({"date": '20231231'})\
            .build(),

        create_interface("stock_fund_stock_holder")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("新浪财经-股本股东-基金持股")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("fund", "stock", "股票", "基金", "holder")\
            .with_example_params({"symbol": '600004'})\
            .build(),

        create_interface("stock_gddh_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-股东大会")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("gddh", "stock", "em")\
            .build(),

        create_interface("stock_gdfx_free_holding_analyse_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-股东分析-股东持股分析-十大流通股东")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "free", "stock", "analyse", "holding")\
            .with_example_params({"date": '20230930'})\
            .build(),

        create_interface("stock_gdfx_free_holding_change_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-股东分析-股东持股变动统计-十大流通股东")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "free", "stock", "holding", "change")\
            .with_example_params({"date": '20210930'})\
            .build(),

        create_interface("stock_gdfx_free_holding_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-股东分析-股东持股明细-十大流通股东")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "free", "stock", "holding", "gdfx")\
            .with_example_params({"date": '20210930'})\
            .build(),

        create_interface("stock_gdfx_free_holding_statistics_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-股东分析-股东持股统计-十大流通股东")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "free", "stock", "holding", "gdfx")\
            .with_example_params({"date": '20210630'})\
            .build(),

        create_interface("stock_gdfx_free_holding_teamwork_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-股东分析-股东协同-十大流通股东")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "free", "stock", "holding", "gdfx")\
            .with_example_params({"symbol": '社保'})\
            .build(),

        create_interface("stock_gdfx_free_top_10_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-个股-十大流通股东")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "free", "stock", "gdfx", "10")\
            .with_example_params({"symbol": 'sh688686', "date": '20240930'})\
            .build(),

        create_interface("stock_gdfx_holding_analyse_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-股东分析-股东持股分析-十大股东")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "analyse", "holding", "gdfx")\
            .with_example_params({"date": '20230331'})\
            .build(),

        create_interface("stock_gdfx_holding_change_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-股东分析-股东持股变动统计-十大股东")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "holding", "gdfx", "change")\
            .with_example_params({"date": '20210930'})\
            .build(),

        create_interface("stock_gdfx_holding_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-股东分析-股东持股明细-十大股东")\
            .with_optional_params("date", "indicator", "symbol")\
            .with_pattern(ParameterPattern.from_params(["date", "indicator", "symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "holding", "gdfx", "detail")\
            .with_example_params({"date": '20230331', "indicator": '个人', "symbol": '新进'})\
            .build(),

        create_interface("stock_gdfx_holding_statistics_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-股东分析-股东持股统计-十大股东")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "holding", "gdfx", "statistics")\
            .with_example_params({"date": '20210930'})\
            .build(),

        create_interface("stock_gdfx_holding_teamwork_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-股东分析-股东协同-十大股东")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "holding", "gdfx", "基金")\
            .with_example_params({"symbol": '社保'})\
            .build(),

        create_interface("stock_gdfx_top_10_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-个股-十大股东")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "gdfx", "10", "股票")\
            .with_example_params({"symbol": 'sh688686', "date": '20210630'})\
            .build(),

        create_interface("stock_ggcg_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-高管持股")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ggcg", "em")\
            .with_example_params({"symbol": '全部'})\
            .build(),

        create_interface("stock_gpzy_distribute_statistics_bank_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "gpzy", "stock", "bank", "distribute")\
            .build(),

        create_interface("stock_gpzy_distribute_statistics_company_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-证券公司")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "gpzy", "stock", "distribute", "statistics")\
            .build(),

        create_interface("stock_gpzy_industry_data_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-股权质押-上市公司质押比例-行业数据")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "gpzy", "stock", "行业", "data")\
            .build(),

        create_interface("stock_gpzy_pledge_ratio_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "gpzy", "stock", "ratio", "pledge")\
            .build(),

        create_interface("stock_gpzy_pledge_ratio_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-股权质押-上市公司质押比例")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "gpzy", "stock", "ratio", "pledge")\
            .with_example_params({"date": '20240906'})\
            .build(),

        create_interface("stock_gpzy_profile_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-股权质押-股权质押市场概况")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("profile", "stock", "em", "gpzy")\
            .build(),

        create_interface("stock_hk_company_profile_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富-港股-公司资料")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "profile", "股票", "hk")\
            .with_example_params({"symbol": '03900'})\
            .build(),

        create_interface("stock_hk_fhpx_detail_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-港股-分红派息")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "fhpx", "detail", "ths", "hk")\
            .with_example_params({"symbol": '0700'})\
            .build(),

        create_interface("stock_hk_security_profile_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富-港股-证券资料")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "security", "profile", "股票")\
            .with_example_params({"symbol": '03900'})\
            .build(),

        create_interface("stock_hold_change_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-数据中心-专题统计-股东股本-股本变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hold", "cninfo", "change")\
            .with_example_params({"symbol": '全部'})\
            .build(),

        create_interface("stock_hold_control_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-数据中心-专题统计-股东股本-实际控制人持股变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hold", "control", "cninfo")\
            .with_example_params({"symbol": '全部'})\
            .build(),

        create_interface("stock_hold_management_detail_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-数据中心-专题统计-股东股本-高管持股变动明细")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("management", "stock", "hold", "cninfo", "detail")\
            .with_example_params({"symbol": '增持'})\
            .build(),

        create_interface("stock_hold_management_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-高管持股-董监高及相关人员持股变动明细")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "management", "stock", "hold", "detail")\
            .build(),

        create_interface("stock_hold_management_person_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-高管持股-人员增减持股变动明细")\
            .with_optional_params("symbol", "name")\
            .with_pattern(ParameterPattern.from_params(["symbol", "name"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "management", "stock", "hold", "股票")\
            .with_example_params({"symbol": '001308', "name": '吴远'})\
            .build(),

        create_interface("stock_hold_num_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-数据中心-专题统计-股东股本-股东人数及持股集中度")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("int")\
            .with_keywords("stock", "hold", "cninfo", "num")\
            .with_example_params({"date": '20210630'})\
            .build(),

        create_interface("stock_hot_keyword_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富-个股人气榜-热门关键词")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("keyword", "stock", "em", "hot")\
            .with_example_params({"symbol": 'SZ000665'})\
            .build(),

        create_interface("stock_hot_search_baidu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("百度股市通-热搜股票")\
            .with_optional_params("symbol", "date", "time")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date", "time"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "A股", "search", "股票", "hot")\
            .with_example_params({"symbol": 'A股', "date": '20250616', "time": '今日'})\
            .build(),

        create_interface("stock_hsgt_hold_stock_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富-数据中心-沪深港通持股-个股排行")\
            .with_optional_params("market", "indicator")\
            .with_pattern(ParameterPattern.from_params(["market", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hold", "em", "hsgt")\
            .with_example_params({"market": '沪股通', "indicator": '5日排行'})\
            .build(),

        create_interface("stock_hsgt_individual_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富-数据中心-沪深港通-沪深港通持股-具体股票")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "individual", "hsgt", "stock", "股票")\
            .with_example_params({"symbol": '002008'})\
            .build(),

        create_interface("stock_hsgt_stock_statistics_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-沪深港通-沪深港通持股-每日个股统计")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("int")\
            .with_keywords("stock", "em", "statistics", "hsgt")\
            .with_example_params({"symbol": '北向持股', "start_date": '20240110', "end_date": '20240110'})\
            .build(),

        create_interface("stock_index_pb_lg")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("乐咕乐股-指数市净率")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "指数", "index", "lg", "pb")\
            .with_example_params({"symbol": '上证50'})\
            .build(),

        create_interface("stock_index_pe_lg")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("乐咕乐股-指数市盈率")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("pe", "stock", "指数", "index", "lg")\
            .with_example_params({"symbol": '沪深300'})\
            .build(),

        create_interface("stock_individual_info_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富-个股-股票信息")\
            .with_optional_params("symbol", "timeout")\
            .with_pattern(ParameterPattern.from_params(["symbol", "timeout"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "individual", "stock", "股票", "info")\
            .with_example_params({"symbol": '603777'})\
            .build(),

        create_interface("stock_industry_category_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-行业分类数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "行业", "cninfo", "industry", "category")\
            .with_example_params({"symbol": '巨潮行业分类标准'})\
            .build(),

        create_interface("stock_industry_change_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-上市公司行业归属的变动情况")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "行业", "cninfo", "change", "股票")\
            .with_example_params({"symbol": '002594', "start_date": '20091227', "end_date": '20220713'})\
            .build(),

        create_interface("stock_info_a_code_name")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("沪深京 A 股列表")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("List[str]")\
            .with_keywords("stock", "name", "code", "a", "info")\
            .build(),

        create_interface("stock_info_bj_name_code")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("北京证券交易所-股票列表")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("List[str]")\
            .with_keywords("stock", "name", "股票", "code", "info")\
            .build(),

        create_interface("stock_info_change_name")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("新浪财经-股票曾用名")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "name", "change", "股票", "info")\
            .with_example_params({"symbol": '000503'})\
            .build(),

        create_interface("stock_info_cjzc_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富-财经早餐")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "cjzc", "em", "info")\
            .build(),

        create_interface("stock_info_global_cls")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("财联社-电报")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("global", "stock", "cls", "info")\
            .with_example_params({"symbol": '全部'})\
            .build(),

        create_interface("stock_info_global_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富-全球财经快讯")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("global", "stock", "em", "info")\
            .build(),

        create_interface("stock_info_global_futu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("富途牛牛-快讯")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("global", "stock", "futu", "info")\
            .build(),

        create_interface("stock_info_global_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("新浪财经-全球财经快讯")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("global", "stock", "sina", "info")\
            .build(),

        create_interface("stock_info_global_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺财经-全球财经直播")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("global", "stock", "ths", "info")\
            .build(),

        create_interface("stock_info_sh_delist")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("上海证券交易所-终止上市公司")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("List[str]")\
            .with_keywords("stock", "delist", "sh", "info")\
            .with_example_params({"symbol": '全部'})\
            .build(),

        create_interface("stock_info_sh_name_code")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("上海证券交易所-股票列表")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("List[str]")\
            .with_keywords("B股", "stock", "A股", "name", "sh")\
            .with_example_params({"symbol": '主板A股'})\
            .build(),

        create_interface("stock_info_sz_change_name")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("深证证券交易所-市场数据-股票数据-名称变更")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("sz", "stock", "name", "change", "股票")\
            .with_example_params({"symbol": '全称变更'})\
            .build(),

        create_interface("stock_info_sz_delist")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("深证证券交易所-暂停上市公司-终止上市公司")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("List[str]")\
            .with_keywords("stock", "sz", "delist", "info")\
            .with_example_params({"symbol": '终止上市公司'})\
            .build(),

        create_interface("stock_info_sz_name_code")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("深圳证券交易所-股票列表")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("List[str]")\
            .with_keywords("sz", "B股", "stock", "A股", "name")\
            .with_example_params({"symbol": 'A股列表'})\
            .build(),

        create_interface("stock_institute_hold")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("新浪财经-股票-机构持股一览表")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "hold", "institute")\
            .with_example_params({"symbol": '20051'})\
            .build(),

        create_interface("stock_institute_hold_detail")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("新浪财经-股票-机构持股详情")\
            .with_optional_params("stock", "quarter")\
            .with_pattern(ParameterPattern.from_params(["stock", "quarter"]))\
            .with_return_type("DataFrame")\
            .with_keywords("institute", "stock", "hold", "detail", "股票")\
            .with_example_params({"stock": '600433', "quarter": '20201'})\
            .build(),

        create_interface("stock_ipo_info")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("新浪财经-发行与分配-新股发行")\
            .with_optional_params("stock")\
            .with_pattern(ParameterPattern.from_params(["stock"]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "ipo", "info")\
            .with_example_params({"stock": '600004'})\
            .build(),

        create_interface("stock_ipo_summary_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-个股-上市相关")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ipo", "cninfo", "summary", "股票")\
            .with_example_params({"symbol": '600030'})\
            .build(),

        create_interface("stock_irm_ans_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("互动易-回答")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "irm", "cninfo", "ans")\
            .with_example_params({"symbol": '1513586704097333248'})\
            .build(),

        create_interface("stock_irm_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("互动易-提问")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "irm", "cninfo")\
            .with_example_params({"symbol": '002594'})\
            .build(),

        create_interface("stock_jgdy_tj_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-机构调研-机构调研统计")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("tj", "stock", "em", "jgdy")\
            .with_example_params({"date": '20220101'})\
            .build(),

        create_interface("stock_lh_yyb_control")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-数据中心-营业部排名-抱团操作实力")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "yyb", "control", "lh")\
            .build(),

        create_interface("stock_lhb_ggtj_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("龙虎榜-个股上榜统计")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("ggtj", "stock", "sina", "lhb")\
            .with_example_params({"symbol": '5'})\
            .build(),

        create_interface("stock_lhb_jgmmtj_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-龙虎榜单-机构买卖每日统计")\
            .with_optional_params("start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "jgmmtj", "em", "lhb")\
            .with_example_params({"start_date": '20240417', "end_date": '20240430'})\
            .build(),

        create_interface("stock_lhb_stock_statistic_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-龙虎榜单-个股上榜统计")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "statistic", "lhb")\
            .with_example_params({"symbol": '近一月'})\
            .build(),

        create_interface("stock_lhb_traderstatistic_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-龙虎榜单-营业部统计")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "traderstatistic", "lhb")\
            .with_example_params({"symbol": '近一月'})\
            .build(),

        create_interface("stock_lhb_yytj_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("龙虎榜-营业部上榜统计")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sina", "yytj", "lhb")\
            .with_example_params({"symbol": '5'})\
            .build(),

        create_interface("stock_main_stock_holder")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("新浪财经-股本股东-主要股东")\
            .with_optional_params("stock")\
            .with_pattern(ParameterPattern.from_params(["stock"]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "holder", "main")\
            .with_example_params({"stock": '600004'})\
            .build(),

        create_interface("stock_management_change_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-公司大事-高管持股变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("management", "stock", "change", "股票", "ths")\
            .with_example_params({"symbol": '688981'})\
            .build(),

        create_interface("stock_margin_account_info")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-融资融券-融资融券账户统计-两融账户信息")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("int")\
            .with_keywords("account", "stock", "margin", "info")\
            .build(),

        create_interface("stock_margin_underlying_info_szse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("深圳证券交易所-融资融券数据-标的证券信息")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "margin", "info", "szse", "underlying")\
            .with_example_params({"date": '20221129'})\
            .build(),

        create_interface("stock_new_ipo_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-数据中心-新股数据-新股发行")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ipo", "new", "cninfo")\
            .build(),

        create_interface("stock_news_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富-个股新闻-最近 100 条新闻")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "news", "股票", "新闻")\
            .with_example_params({"symbol": '603777'})\
            .build(),

        create_interface("stock_news_main_cx")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("财新网-财新数据通")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "cx", "news", "main")\
            .build(),

        create_interface("stock_pg_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-新股数据-配股")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "pg", "em")\
            .build(),

        create_interface("stock_profile_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-个股-公司概况")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("profile", "stock", "股票", "cninfo")\
            .with_example_params({"symbol": '600030'})\
            .build(),

        create_interface("stock_qbzf_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-新股数据-增发-全部增发")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "qbzf")\
            .build(),

        create_interface("stock_rank_forecast_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-数据中心-评级预测-投资评级")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "rank", "cninfo", "forecast")\
            .with_example_params({"date": '20230817'})\
            .build(),

        create_interface("stock_register_bj")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-新股数据-IPO审核信息-北交所")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "register", "bj")\
            .build(),

        create_interface("stock_register_cyb")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-新股数据-IPO审核信息-创业板")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("cyb", "stock", "register")\
            .build(),

        create_interface("stock_register_db")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-新股数据-IPO审核信息-达标企业")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "register", "db")\
            .build(),

        create_interface("stock_register_kcb")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-新股数据-IPO审核信息-科创板")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "register", "kcb")\
            .build(),

        create_interface("stock_register_sh")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-新股数据-IPO审核信息-上海主板")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sh", "register")\
            .build(),

        create_interface("stock_register_sz")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-新股数据-IPO审核信息-深圳主板")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sz", "register")\
            .build(),

        create_interface("stock_repurchase_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-股票回购-股票回购数据")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "em", "repurchase")\
            .build(),

        create_interface("stock_restricted_release_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-限售股解禁-解禁详情一览")\
            .with_optional_params("start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "restricted", "stock", "detail", "release")\
            .with_example_params({"start_date": '20221202', "end_date": '20241202'})\
            .build(),

        create_interface("stock_restricted_release_queue_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-个股限售解禁-解禁批次")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("queue", "em", "restricted", "stock", "股票")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_restricted_release_queue_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("新浪财经-发行分配-限售解禁")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("sina", "queue", "restricted", "stock", "股票")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_restricted_release_stockholder_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-个股限售解禁-解禁股东")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "restricted", "stock", "股票", "release")\
            .with_example_params({"symbol": '600000', "date": '20200904'})\
            .build(),

        create_interface("stock_restricted_release_summary_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-限售股解禁")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "restricted", "stock", "A股", "summary")\
            .with_example_params({"symbol": '全部股票', "start_date": '20221101', "end_date": '20221209'})\
            .build(),

        create_interface("stock_sector_detail")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("新浪行业-板块行情-成份详情")\
            .with_optional_params("sector")\
            .with_pattern(ParameterPattern.from_params(["sector"]))\
            .with_return_type("DataFrame")\
            .with_keywords("detail", "stock", "行业", "sector")\
            .with_example_params({"sector": 'gn_gfgn'})\
            .build(),

        create_interface("stock_sgt_reference_exchange_rate_sse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("沪港通-港股通信息披露-参考汇率")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sse", "rate", "sgt", "reference")\
            .build(),

        create_interface("stock_sgt_reference_exchange_rate_szse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("深港通-港股通业务信息-参考汇率")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "szse", "rate", "sgt", "reference")\
            .build(),

        create_interface("stock_sgt_settlement_exchange_rate_sse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("沪港通-港股通信息披露-结算汇兑")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("settlement", "stock", "sse", "rate", "sgt")\
            .build(),

        create_interface("stock_sgt_settlement_exchange_rate_szse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("深港通-港股通业务信息-结算汇率")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("settlement", "stock", "rate", "sgt", "szse")\
            .build(),

        create_interface("stock_share_change_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-股本股东-公司股本变动")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "cninfo", "change", "股票", "share")\
            .with_example_params({"symbol": '002594', "start_date": '20091227', "end_date": '20241021'})\
            .build(),

        create_interface("stock_share_hold_change_bse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("北京证券交易所-信息披露-监管信息-董监高及相关人员持股变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("bse", "stock", "hold", "change", "share")\
            .with_example_params({"symbol": '430489'})\
            .build(),

        create_interface("stock_share_hold_change_sse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("上海证券交易所-披露-监管信息公开-公司监管-董董监高人员股份变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hold", "sse", "change", "share")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_share_hold_change_szse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("深圳证券交易所-信息披露-监管信息公开-董监高人员股份变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hold", "change", "share", "股票")\
            .with_example_params({"symbol": '000001'})\
            .build(),

        create_interface("stock_shareholder_change_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-公司大事-股东持股变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "change", "股票", "shareholder", "ths")\
            .with_example_params({"symbol": '688981'})\
            .build(),

        create_interface("stock_sns_sseinfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("上证e互动-提问与回答")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "sseinfo", "sns")\
            .with_example_params({"symbol": '603119'})\
            .build(),

        create_interface("stock_sy_profile_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-商誉-A股商誉市场概况")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "A股", "sy", "profile")\
            .build(),

        create_interface("stock_szse_sector_summary")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("深圳证券交易所-统计资料-股票行业成交数据")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "行业", "sector", "summary", "股票")\
            .with_example_params({"symbol": '当月', "date": '2024-01-01'})\
            .build(),

        create_interface("stock_szse_summary")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("深证证券交易所-总貌-证券类别统计")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "szse", "summary")\
            .with_example_params({"date": '20240830'})\
            .build(),

        create_interface("stock_tfp_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-停复牌信息")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "tfp")\
            .with_example_params({"date": '20240426'})\
            .build(),

        create_interface("stock_xgsglb_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("新股申购与中签查询")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "xgsglb", "em")\
            .with_example_params({"symbol": '全部股票'})\
            .build(),

        create_interface("stock_xgsr_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-数据中心-新股数据-新股上市首日")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ths", "xgsr")\
            .build(),

        create_interface("stock_zh_a_disclosure_relation_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-首页-数据-预约披露调研")\
            .with_optional_params("symbol", "market", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "market", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("relation", "zh", "stock", "债券", "cninfo")\
            .with_example_params({"symbol": '000001', "market": '沪深京', "start_date": '20230618', "end_date": '20231219'})\
            .build(),

        create_interface("stock_zh_a_disclosure_report_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("巨潮资讯-首页-公告查询-信息披露公告")\
            .with_optional_params("symbol", "market", "keyword", "category", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "market", "keyword", "category", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "stock", "债券", "cninfo", "股票")\
            .with_example_params({"symbol": '000001', "market": '沪深京', "keyword": '', "category": '', "start_date": '20230618', "end_date": '20231219'})\
            .build(),

        create_interface("stock_zh_a_gdhs")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-股东户数")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "zh", "gdhs", "a")\
            .with_example_params({"symbol": '20230930'})\
            .build(),

        create_interface("stock_zh_a_gdhs_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-数据中心-特色数据-股东户数详情")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "em", "stock", "detail", "股票")\
            .with_example_params({"symbol": '000001'})\
            .build(),

        create_interface("stock_zh_a_new")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("新浪财经-行情中心-沪深股市-次新股")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "zh", "new", "a")\
            .build(),

        create_interface("stock_zh_a_new_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-行情中心-沪深个股-新股")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "em", "stock", "a", "new")\
            .build(),

        create_interface("stock_zh_a_st_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-行情中心-沪深个股-风险警示板")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "em", "stock", "a", "st")\
            .build(),

        create_interface("stock_zh_ah_name")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("腾讯财经-港股-AH-股票名称")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "stock", "name", "股票", "ah")\
            .build(),

        create_interface("stock_zt_pool_sub_new_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富网-行情中心-涨停板行情-次新股池")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "zt", "sub", "pool")\
            .with_example_params({"date": '20241231'})\
            .build(),
        ]

    def _register_other_interfaces(self) -> List[InterfaceMetadata]:
        """注册OTHER接口"""
        return [
        create_interface("stock_a_congestion_lg")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("乐咕乐股-大盘拥挤度")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("congestion", "stock", "lg", "a")\
            .build(),

        create_interface("stock_add_stock")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-发行与分配-增发")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "add")\
            .with_example_params({"symbol": '688166'})\
            .build(),

        create_interface("stock_classify_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("按 symbol 分类后的股票")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("sina", "classify", "stock", "行业", "股票")\
            .with_example_params({"symbol": '热门概念'})\
            .build(),

        create_interface("stock_dzjy_yybph")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-大宗交易-营业部排行")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "yybph", "dzjy")\
            .with_example_params({"symbol": '近三月'})\
            .build(),

        create_interface("stock_ebs_lg")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("乐咕乐股-股债利差")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("ebs", "stock", "lg")\
            .build(),

        create_interface("stock_esg_msci_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-ESG评级中心-ESG评级-MSCI")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sina", "msci", "esg")\
            .build(),

        create_interface("stock_esg_rate_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-ESG评级中心-ESG评级-ESG评级数据")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sina", "esg", "rate")\
            .build(),

        create_interface("stock_esg_rft_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-ESG评级中心-ESG评级-路孚特")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sina", "rft", "esg")\
            .build(),

        create_interface("stock_esg_zd_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-ESG评级中心-ESG评级-秩鼎")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("sina", "stock", "zd", "esg")\
            .build(),

        create_interface("stock_gsrl_gsdt_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-股市日历-公司动态")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gsrl", "stock", "em", "gsdt")\
            .with_example_params({"date": '20230808'})\
            .build(),

        create_interface("stock_hot_tweet_xq")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("雪球-沪深股市-热度排行榜-讨论排行榜")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hot", "tweet", "xq")\
            .with_example_params({"symbol": '最热门'})\
            .build(),

        create_interface("stock_institute_recommend")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-机构推荐池-最新投资评级")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("recommend", "institute", "stock", "行业", "股票")\
            .with_example_params({"symbol": '投资评级选股'})\
            .build(),

        create_interface("stock_institute_recommend_detail")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-机构推荐池-股票评级记录")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("recommend", "institute", "stock", "股票", "detail")\
            .with_example_params({"symbol": '000001'})\
            .build(),

        # about two hours
        create_interface("stock_jgdy_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-机构调研-机构调研详细")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("detail", "stock", "em", "jgdy")\
            .with_example_params({"date": '20241211'})\
            .build(),

        create_interface("stock_js_weibo_nlp_time")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("https://datacenter.jin10.com/market")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("weibo", "nlp", "js", "stock", "time")\
            .build(),

        create_interface("stock_sse_summary")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("上海证券交易所-总貌")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sse", "summary")\
            .build(),

        create_interface("stock_sy_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-商誉-个股商誉明细")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "sy")\
            .with_example_params({"date": '20231231'})\
            .build(),

        create_interface("stock_sy_yq_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-商誉-商誉减值预期明细")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("yq", "stock", "em", "sy")\
            .with_example_params({"date": '20240630'})\
            .build(),

        create_interface("stock_szse_area_summary")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("深证证券交易所-总貌-地区交易排序")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "area", "szse", "summary")\
            .with_example_params({"date": '2024-01-01'})\
            .build(),

        create_interface("stock_value_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-估值分析-每日互动-每日互动-估值分析")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "em", "value")\
            .with_example_params({"symbol": '300766'})\
            .build(),

        create_interface("stock_yzxdr_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-一致行动人")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "yzxdr", "em")\
            .with_example_params({"date": '20240930'})\
            .build(),

        create_interface("stock_zdhtmx_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-重大合同-重大合同明细")\
            .with_optional_params("start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "zdhtmx", "em")\
            .with_example_params({"start_date": '20200819', "end_date": '20230819'})\
            .build(),

        create_interface("stock_zygc_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-个股-主营构成")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "em", "zygc")\
            .with_example_params({"symbol": 'SH688041'})\
            .build(),

        create_interface("stock_zyjs_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-主营介绍")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "ths", "zyjs")\
            .with_example_params({"symbol": '000066'})\
            .build(),
        ]

    def _register_stock_technical_interfaces(self) -> List[InterfaceMetadata]:
        """注册STOCK_TECHNICAL接口"""
        return [
        create_interface("stock_a_gxl_lg")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("乐咕乐股-股息率-A 股股息率")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "A股", "lg", "a", "gxl")\
            .with_example_params({"symbol": '上证A股'})\
            .build(),

        create_interface("stock_buffett_index_lg")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("乐估乐股-底部研究-巴菲特指标")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "lg", "buffett", "index")\
            .build(),

        create_interface("stock_rank_cxd_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("同花顺-数据中心-技术选股-创新低")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ths", "rank", "cxd")\
            .with_example_params({"symbol": '创月新低'})\
            .build(),

        create_interface("stock_rank_cxfl_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("同花顺-数据中心-技术选股-持续放量")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ths", "rank", "cxfl")\
            .build(),

        create_interface("stock_rank_cxg_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("同花顺-数据中心-技术选股-创新高")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ths", "rank", "cxg")\
            .with_example_params({"symbol": '创月新高'})\
            .build(),

        create_interface("stock_rank_cxsl_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("同花顺-数据中心-技术选股-持续缩量")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ths", "rank", "cxsl")\
            .build(),

        create_interface("stock_rank_ljqd_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("同花顺-数据中心-技术选股-量价齐跌")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ths", "rank", "ljqd")\
            .build(),

        create_interface("stock_rank_ljqs_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("同花顺-数据中心-技术选股-量价齐升")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ths", "rank", "ljqs")\
            .build(),

        create_interface("stock_rank_lxsz_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("同花顺-数据中心-技术选股-连续上涨")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("lxsz", "stock", "ths", "rank")\
            .build(),

        create_interface("stock_rank_lxxd_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("同花顺-数据中心-技术选股-连续下跌")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("lxxd", "stock", "ths", "rank")\
            .build(),

        create_interface("stock_rank_xstp_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("同花顺-数据中心-技术选股-向上突破")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ths", "rank", "xstp")\
            .with_example_params({"symbol": '500日均线'})\
            .build(),

        create_interface("stock_rank_xxtp_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("同花顺-数据中心-技术选股-向下突破")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "xxtp", "rank", "ths")\
            .with_example_params({"symbol": '500日均线'})\
            .build(),

        create_interface("stock_rank_xzjp_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("同花顺-数据中心-技术选股-险资举牌")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "xzjp", "rank", "ths")\
            .build(),

        create_interface("stock_sector_fund_flow_rank")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("东方财富网-数据中心-资金流向-板块资金流-排名")\
            .with_optional_params("indicator", "sector_type")\
            .with_pattern(ParameterPattern.from_params(["indicator", "sector_type"]))\
            .with_return_type("DataFrame")\
            .with_keywords("rank", "fund", "stock", "行业", "sector")\
            .with_example_params({"indicator": '今日', "sector_type": '行业资金流'})\
            .build(),
        ]

    def _register_stock_financial_interfaces(self) -> List[InterfaceMetadata]:
        """注册STOCK_FINANCIAL接口"""
        return [
        create_interface("stock_analyst_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富网-数据中心-研究报告-东方财富分析师指数-东方财富分析师指数2020最新排行-分析师详情")\
            .with_optional_params("analyst_id", "indicator")\
            .with_pattern(ParameterPattern.from_params(["analyst_id", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "指数", "analyst", "detail")\
            .with_example_params({"analyst_id": '11000200926', "indicator": '最新跟踪成分股'})\
            .build(),

        create_interface("stock_analyst_rank_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富网-数据中心-研究报告-东方财富分析师指数-东方财富分析师指数")\
            .with_optional_params("year")\
            .with_pattern(ParameterPattern.from_params(["year"]))\
            .with_return_type("DataFrame")\
            .with_keywords("rank", "em", "stock", "指数", "analyst")\
            .with_example_params({"year": '2024'})\
            .build(),

        create_interface("stock_balance_sheet_by_report_delisted_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-资产负债表-已退市股票-按报告期")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("List[str]")\
            .with_keywords("em", "sheet", "stock", "by", "delisted")\
            .with_example_params({"symbol": 'SZ000013'})\
            .build(),

        create_interface("stock_balance_sheet_by_report_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-资产负债表-按报告期")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "sheet", "stock", "by", "股票")\
            .with_example_params({"symbol": 'SH600519'})\
            .build(),

        create_interface("stock_balance_sheet_by_yearly_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-资产负债表-按年度")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "sheet", "stock", "by", "股票")\
            .with_example_params({"symbol": 'SH600036'})\
            .build(),

        create_interface("stock_cash_flow_sheet_by_quarterly_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-现金流量表-按单季度")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "sheet", "quarterly", "stock", "by")\
            .with_example_params({"symbol": 'SH600519'})\
            .build(),

        create_interface("stock_cash_flow_sheet_by_report_delisted_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-现金流量表-已退市股票-按报告期")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("List[str]")\
            .with_keywords("em", "sheet", "stock", "by", "delisted")\
            .with_example_params({"symbol": 'SZ000013'})\
            .build(),

        create_interface("stock_cash_flow_sheet_by_report_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-现金流量表-按报告期")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "sheet", "stock", "by", "股票")\
            .with_example_params({"symbol": 'SH600519'})\
            .build(),

        create_interface("stock_cash_flow_sheet_by_yearly_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-现金流量表-按年度")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "sheet", "stock", "by", "股票")\
            .with_example_params({"symbol": 'SH600519'})\
            .build(),

        create_interface("stock_dxsyl_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富网-数据中心-新股申购-打新收益率")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "dxsyl")\
            .build(),

        create_interface("stock_financial_abstract")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("新浪财经-财务报表-关键指标")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "财务", "financial", "abstract")\
            .with_example_params({"symbol": '600004'})\
            .build(),

        create_interface("stock_financial_abstract_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("同花顺-财务指标-主要指标")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "财务", "ths", "financial")\
            .with_example_params({"symbol": '000063', "indicator": '按报告期'})\
            .build(),

        create_interface("stock_financial_analysis_indicator")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("新浪财经-财务分析-财务指标")\
            .with_optional_params("symbol", "start_year")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_year"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "财务", "analysis", "financial")\
            .with_example_params({"symbol": '600004', "start_year": '1900'})\
            .build(),

        create_interface("stock_financial_analysis_indicator_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-A股-财务分析-主要指标")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "A股", "股票", "财务")\
            .with_example_params({"symbol": '301389.SZ', "indicator": '按报告期'})\
            .build(),

        create_interface("stock_financial_benefit_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("同花顺-财务指标-利润表")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "benefit", "股票", "财务", "ths")\
            .with_example_params({"symbol": '000063', "indicator": '按报告期'})\
            .build(),

        create_interface("stock_financial_cash_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("同花顺-财务指标-现金流量表")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "财务", "cash", "ths")\
            .with_example_params({"symbol": '000063', "indicator": '按报告期'})\
            .build(),

        create_interface("stock_financial_debt_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("同花顺-财务指标-资产负债表")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("debt", "stock", "股票", "财务", "ths")\
            .with_example_params({"symbol": '000063', "indicator": '按报告期'})\
            .build(),

        create_interface("stock_financial_hk_analysis_indicator_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-港股-财务分析-主要指标")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "hk", "股票", "财务")\
            .with_example_params({"symbol": '00853', "indicator": '年度'})\
            .build(),

        create_interface("stock_financial_hk_report_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-港股-财务报表-三大报表")\
            .with_optional_params("stock", "symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["stock", "symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "hk", "股票", "财务")\
            .with_example_params({"stock": '00700', "symbol": '资产负债表', "indicator": '年度'})\
            .build(),

        create_interface("stock_financial_report_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("新浪财经-财务报表-三大报表")\
            .with_optional_params("stock", "symbol")\
            .with_pattern(ParameterPattern.from_params(["stock", "symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("sina", "stock", "股票", "财务", "report")\
            .with_example_params({"stock": 'sh600600', "symbol": '资产负债表'})\
            .build(),

        create_interface("stock_financial_us_analysis_indicator_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-美股-财务分析-主要指标")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "us", "股票", "财务")\
            .with_example_params({"symbol": 'TSLA', "indicator": '年报'})\
            .build(),

        create_interface("stock_financial_us_report_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-美股-财务分析-三大报表")\
            .with_optional_params("stock", "symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["stock", "symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "股票", "财务", "report")\
            .with_example_params({"stock": 'TSLA', "symbol": '资产负债表', "indicator": '年报'})\
            .build(),

        create_interface("stock_hk_profit_forecast_et")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("经济通-公司资料-盈利预测")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("forecast", "et", "stock", "profit", "股票")\
            .with_example_params({"symbol": '09999', "indicator": '盈利预测概览'})\
            .build(),

        create_interface("stock_hk_valuation_baidu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("百度股市通-港股-财务报表-估值数据")\
            .with_optional_params("symbol", "indicator", "period")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator", "period"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "valuation", "股票", "财务", "baidu")\
            .with_example_params({"symbol": '06969', "indicator": '总市值', "period": 'daily'})\
            .build(),

        create_interface("stock_js_weibo_report")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("金十数据中心-实时监控-微博舆情报告")\
            .with_optional_params("time_period")\
            .with_pattern(ParameterPattern.from_params(["time_period"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "weibo", "report", "js")\
            .with_example_params({"time_period": 'CNHOUR12'})\
            .build(),

        create_interface("stock_lrb_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-数据中心-年报季报-业绩快报-利润表")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "lrb")\
            .with_example_params({"date": '20240331'})\
            .build(),

        create_interface("stock_notice_report")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富网-数据中心-公告大全-沪深京 A 股公告")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "report", "notice", "财务")\
            .with_example_params({"symbol": '全部', "date": '20220511'})\
            .build(),

        create_interface("stock_profit_forecast_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富网-数据中心-研究报告-盈利预测")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "forecast", "行业", "stock", "profit")\
            .with_example_params({"symbol": '000001'})\
            .build(),

        create_interface("stock_profit_forecast_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("同花顺-盈利预测")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("forecast", "stock", "profit", "股票", "ths")\
            .with_example_params({"symbol": '600519', "indicator": '预测年报每股收益'})\
            .build(),

        create_interface("stock_profit_sheet_by_quarterly_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-利润表-按单季度")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "sheet", "quarterly", "stock", "by")\
            .with_example_params({"symbol": 'SH600519'})\
            .build(),

        create_interface("stock_profit_sheet_by_report_delisted_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-利润表-已退市股票-按报告期")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("List[str]")\
            .with_keywords("em", "sheet", "stock", "by", "delisted")\
            .with_example_params({"symbol": 'SZ000013'})\
            .build(),

        create_interface("stock_profit_sheet_by_report_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-利润表-报告期")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "sheet", "stock", "by", "profit")\
            .with_example_params({"symbol": 'SH600519'})\
            .build(),

        create_interface("stock_profit_sheet_by_yearly_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-利润表-按年度")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "sheet", "stock", "by", "profit")\
            .with_example_params({"symbol": 'SH600519'})\
            .build(),

        create_interface("stock_report_disclosure")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("巨潮资讯-首页-数据-预约披露")\
            .with_optional_params("market", "period")\
            .with_pattern(ParameterPattern.from_params(["market", "period"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "disclosure", "report")\
            .with_example_params({"market": '沪深京', "period": 'daily'})\
            .build(),

        create_interface("stock_report_fund_hold")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富网-数据中心-主力数据-基金持仓")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("fund", "stock", "hold", "基金", "report")\
            .with_example_params({"symbol": '基金持仓', "date": '20210331'})\
            .build(),

        create_interface("stock_report_fund_hold_detail")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富网-数据中心-主力数据-基金持仓-明细")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("fund", "stock", "hold", "detail", "基金")\
            .with_example_params({"symbol": '008286', "date": '20220331'})\
            .build(),

        create_interface("stock_research_report_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富网-数据中心-研究报告-个股研报")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "report", "em", "research")\
            .with_example_params({"symbol": '000001'})\
            .build(),

        create_interface("stock_staq_net_stop")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富网-行情中心-沪深个股-两网及退市")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "stop", "net", "staq")\
            .build(),

        create_interface("stock_xjll_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-数据中心-年报季报-业绩快报-现金流量表")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "xjll")\
            .with_example_params({"date": '20240331'})\
            .build(),

        create_interface("stock_yjbb_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-数据中心-年报季报-业绩快报-业绩报表")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("yjbb", "stock", "em")\
            .with_example_params({"date": '20200331'})\
            .build(),

        create_interface("stock_yjkb_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-数据中心-年报季报-业绩快报")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "yjkb")\
            .with_example_params({"date": '20211231'})\
            .build(),

        create_interface("stock_yjyg_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-数据中心-年报季报-业绩预告")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "yjyg")\
            .with_example_params({"date": '20200331'})\
            .build(),

        create_interface("stock_zcfz_bj_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-数据中心-年报季报-业绩快报-资产负债表")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "zcfz", "em", "bj")\
            .with_example_params({"date": '20240331'})\
            .build(),

        create_interface("stock_zcfz_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-数据中心-年报季报-业绩快报-资产负债表")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "zcfz", "em")\
            .with_example_params({"date": '20240331'})\
            .build(),

        create_interface("stock_zh_kcb_report_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("科创板报告内容")\
            .with_optional_params("from_page", "to_page")\
            .with_pattern(ParameterPattern.from_params(["from_page", "to_page"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "em", "kcb", "stock", "report")\
            .with_example_params({"from_page": 1, "to_page": 100})\
            .build(),

        create_interface("stock_zh_valuation_baidu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("百度股市通-A股-财务报表-估值数据")\
            .with_optional_params("symbol", "indicator", "period")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator", "period"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "stock", "A股", "valuation", "股票")\
            .with_example_params({"symbol": '002044', "indicator": '总市值', "period": 'daily'})\
            .build(),
        ]

    def _register_stock_quote_interfaces(self) -> List[InterfaceMetadata]:
        """注册STOCK_QUOTE接口"""
        return [
        create_interface("stock_bid_ask_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富-行情报价")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("ask", "em", "stock", "bid", "股票")\
            .with_example_params({"symbol": '000001'})\
            .build(),

        create_interface("stock_board_concept_hist_min_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-沪深板块-概念板块-分时历史行情")\
            .with_optional_params("symbol", "period")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "hist", "min", "concept")\
            .with_example_params({"symbol": '长寿药', "period": '5'})\
            .build(),

        create_interface("stock_board_concept_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情中心-沪深京板块-概念板块-实时行情")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "spot", "stock", "concept", "board")\
            .with_example_params({"symbol": '可燃冰'})\
            .build(),

        create_interface("stock_board_industry_hist_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-沪深板块-行业板块-历史行情")\
            .with_optional_params("symbol", "start_date", "end_date", "period", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date", "period", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "行业", "hist", "industry")\
            .with_example_params({"symbol": '小金属', "start_date": '20211201', "end_date": '20220401', "period": 'daily', "adjust": ''})\
            .build(),

        create_interface("stock_board_industry_hist_min_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-沪深板块-行业板块-分时历史行情")\
            .with_optional_params("symbol", "period")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "行业", "hist", "industry")\
            .with_example_params({"symbol": '小金属', "period": '5'})\
            .build(),

        create_interface("stock_board_industry_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-沪深板块-行业板块-实时行情")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "spot", "stock", "行业", "industry")\
            .with_example_params({"symbol": '小金属'})\
            .build(),

        create_interface("stock_comment_detail_scrd_desire_daily_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-特色数据-千股千评-市场热度-日度市场参与意愿")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("desire", "em", "stock", "detail", "scrd")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_cy_a_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-创业板-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "spot", "cy", "stock", "a")\
            .build(),

        create_interface("stock_cyq_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-概念板-行情中心-日K-筹码分布")\
            .with_optional_params("symbol", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "em", "cyq")\
            .with_example_params({"symbol": '000001', "adjust": ''})\
            .build(),

        create_interface("stock_dzjy_mrmx")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-大宗交易-每日明细")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("B股", "mrmx", "stock", "A股", "债券")\
            .with_example_params({"symbol": '基金', "start_date": '20220104', "end_date": '20220104'})\
            .build(),

        create_interface("stock_fund_flow_individual")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("同花顺-数据中心-资金流向-个股资金流")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "flow", "individual", "fund")\
            .with_example_params({"symbol": '即时'})\
            .build(),

        create_interface("stock_history_dividend")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-发行与分配-历史分红")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "history", "dividend")\
            .build(),

        create_interface("stock_history_dividend_detail")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-发行与分配-分红配股详情")\
            .with_optional_params("symbol", "indicator", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "dividend", "detail", "history", "股票")\
            .with_example_params({"symbol": '000002', "indicator": '分红', "date": '2024-01-01'})\
            .build(),

        create_interface("stock_hk_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-港股-个股的历史行情数据")\
            .with_optional_params("symbol", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "daily", "hk")\
            .with_example_params({"symbol": '00981', "adjust": ''})\
            .build(),

        create_interface("stock_hk_gxl_lg")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("乐咕乐股-股息率-恒生指数股息率")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "指数", "lg", "gxl", "hk")\
            .build(),

        create_interface("stock_hk_hist")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情-港股-每日行情")\
            .with_optional_params("symbol", "period", "start_date", "end_date", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period", "start_date", "end_date", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("hist", "stock", "hk")\
            .with_example_params({"symbol": '00593', "period": 'daily', "start_date": '19700101', "end_date": '22220101', "adjust": ''})\
            .build(),

        create_interface("stock_hk_hist_min_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情-港股-每日分时行情")\
            .with_optional_params("symbol", "period", "adjust", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period", "adjust", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "hist", "股票", "min")\
            .with_example_params({"symbol": '01611', "period": '1', "adjust": '', "start_date": '2024-01-01', "end_date": '2024-01-31'})\
            .build(),

        create_interface("stock_hk_hot_rank_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富-个股人气榜-历史趋势")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("rank", "em", "stock", "detail", "hot")\
            .with_example_params({"symbol": '00700'})\
            .build(),

        create_interface("stock_hk_hot_rank_detail_realtime_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富-个股人气榜-实时变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("rank", "em", "stock", "realtime", "detail")\
            .with_example_params({"symbol": '00700'})\
            .build(),

        create_interface("stock_hk_hot_rank_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富-个股人气榜-人气榜-港股市场")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("rank", "em", "stock", "hot", "hk")\
            .build(),

        create_interface("stock_hk_hot_rank_latest_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富-个股人气榜-最新排名")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("rank", "em", "stock", "latest", "hot")\
            .with_example_params({"symbol": '00700'})\
            .build(),

        create_interface("stock_hk_index_daily_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-港股指数-历史行情数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("sina", "stock", "指数", "index", "daily")\
            .with_example_params({"symbol": 'CES100'})\
            .build(),

        create_interface("stock_hk_index_spot_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-行情中心-港股指数")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("sina", "spot", "stock", "指数", "index")\
            .build(),

        create_interface("stock_hk_indicator_eniu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("亿牛网-港股指标")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "eniu", "hk", "indicator")\
            .with_example_params({"symbol": 'hk01093', "indicator": '市盈率'})\
            .build(),

        create_interface("stock_hk_spot")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-港股的所有港股的实时行情数据")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hk", "spot")\
            .build(),

        create_interface("stock_hot_deal_xq")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("雪球-沪深股市-热度排行榜-分享交易排行榜")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hot", "deal", "xq")\
            .with_example_params({"symbol": '最热门'})\
            .build(),

        create_interface("stock_hot_follow_xq")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("雪球-沪深股市-热度排行榜-关注排行榜")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "follow", "hot", "xq")\
            .with_example_params({"symbol": '最热门'})\
            .build(),

        create_interface("stock_hot_rank_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富-个股人气榜-历史趋势及粉丝特征")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("rank", "em", "stock", "detail", "hot")\
            .with_example_params({"symbol": 'SZ000665'})\
            .build(),

        create_interface("stock_hot_rank_detail_realtime_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富-个股人气榜-实时变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("rank", "em", "stock", "realtime", "detail")\
            .with_example_params({"symbol": 'SZ000665'})\
            .build(),

        create_interface("stock_hot_rank_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富-个股人气榜-人气榜")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "rank", "hot", "em")\
            .build(),

        create_interface("stock_hot_rank_latest_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富-个股人气榜-最新排名")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("rank", "em", "stock", "latest", "hot")\
            .with_example_params({"symbol": 'SZ000665'})\
            .build(),

        create_interface("stock_hot_rank_relate_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富-个股人气榜-相关股票")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("rank", "em", "stock", "relate", "股票")\
            .with_example_params({"symbol": 'SZ000665'})\
            .build(),

        create_interface("stock_hot_up_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富-个股人气榜-飙升榜")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "up", "em", "hot")\
            .build(),

        create_interface("stock_hsgt_board_rank_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-沪深港通持股-行业板块排行-北向资金增持行业板块排行")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("rank", "em", "hsgt", "stock", "行业")\
            .with_example_params({"symbol": '北向资金增持行业板块排行', "indicator": '今日'})\
            .build(),

        create_interface("stock_hsgt_fund_flow_summary_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-资金流向-沪深港通资金流向")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "hsgt", "fund", "stock", "summary")\
            .build(),

        create_interface("stock_hsgt_fund_min_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富-数据中心-沪深港通-市场概括-分时数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "hsgt", "fund", "stock", "min")\
            .with_example_params({"symbol": '北向资金'})\
            .build(),

        create_interface("stock_hsgt_hist_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-资金流向-沪深港通资金流向-沪深港通历史数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("hist", "stock", "em", "hsgt")\
            .with_example_params({"symbol": '北向资金'})\
            .build(),

        create_interface("stock_individual_fund_flow")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-资金流向-个股")\
            .with_optional_params("stock", "market")\
            .with_pattern(ParameterPattern.from_params(["stock", "market"]))\
            .with_return_type("DataFrame")\
            .with_keywords("individual", "fund", "stock", "股票", "flow")\
            .with_example_params({"stock": '600094', "market": 'sh'})\
            .build(),

        create_interface("stock_industry_clf_hist_sw")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("申万宏源研究-行业分类-全部行业分类")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "行业", "hist", "clf", "industry")\
            .build(),

        create_interface("stock_inner_trade_xq")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("雪球-行情中心-沪深股市-内部交易")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "xq", "trade", "inner")\
            .build(),

        create_interface("stock_intraday_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富-分时数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "em", "intraday")\
            .with_example_params({"symbol": '000001'})\
            .build(),

        create_interface("stock_lh_yyb_capital")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("同花顺-数据中心-营业部排名-资金实力最强")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "yyb", "lh", "capital")\
            .build(),

        create_interface("stock_lh_yyb_most")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("同花顺-数据中心-营业部排名-上榜次数最多")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("most", "stock", "yyb", "lh")\
            .build(),

        create_interface("stock_lhb_detail_daily_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("龙虎榜-每日详情")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("sina", "stock", "lhb", "detail", "daily")\
            .with_example_params({"date": '20240222'})\
            .build(),

        create_interface("stock_lhb_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-龙虎榜单-龙虎榜详情")\
            .with_optional_params("start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("detail", "stock", "em", "lhb")\
            .with_example_params({"start_date": '20230403', "end_date": '20230417'})\
            .build(),

        create_interface("stock_lhb_hyyyb_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-龙虎榜单-每日活跃营业部")\
            .with_optional_params("start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "hyyyb", "lhb")\
            .with_example_params({"start_date": '20220324', "end_date": '20220324'})\
            .build(),

        create_interface("stock_lhb_jgmx_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("龙虎榜-机构席位成交明细")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("sina", "stock", "jgmx", "lhb")\
            .build(),

        create_interface("stock_lhb_jgstatistic_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-龙虎榜单-机构席位追踪")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("jgstatistic", "stock", "em", "lhb")\
            .with_example_params({"symbol": '近一月'})\
            .build(),

        create_interface("stock_lhb_jgzz_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("龙虎榜-机构席位追踪")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sina", "jgzz", "lhb")\
            .with_example_params({"symbol": '5'})\
            .build(),

        create_interface("stock_lhb_stock_detail_date_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-龙虎榜单-个股龙虎榜详情-日期")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "lhb", "detail", "股票")\
            .with_example_params({"symbol": '600077'})\
            .build(),

        create_interface("stock_lhb_stock_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-龙虎榜单-个股龙虎榜详情")\
            .with_optional_params("symbol", "date", "flag")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date", "flag"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "lhb", "detail", "股票")\
            .with_example_params({"symbol": '000788', "date": '20220315', "flag": '卖出'})\
            .build(),

        create_interface("stock_lhb_yyb_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-龙虎榜单-营业部历史交易明细-营业部交易明细")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("yyb", "em", "stock", "lhb", "detail")\
            .with_example_params({"symbol": '10188715'})\
            .build(),

        create_interface("stock_lhb_yybph_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-龙虎榜单-营业部排行")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "yybph", "em", "lhb")\
            .with_example_params({"symbol": '近一月'})\
            .build(),

        create_interface("stock_margin_detail_sse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("上海证券交易所-融资融券数据-融资融券明细")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("detail", "stock", "sse", "margin")\
            .with_example_params({"date": '20230922'})\
            .build(),

        create_interface("stock_margin_detail_szse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("深证证券交易所-融资融券数据-融资融券交易明细")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("detail", "stock", "margin", "szse")\
            .with_example_params({"date": '20230925'})\
            .build(),

        create_interface("stock_margin_ratio_pa")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("融资融券-标的证券名单及保证金比例查询")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("List[str]")\
            .with_keywords("pa", "stock", "ratio", "margin")\
            .with_example_params({"date": '20231013'})\
            .build(),

        create_interface("stock_margin_sse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("上海证券交易所-融资融券数据-融资融券汇总")\
            .with_optional_params("start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sse", "margin")\
            .with_example_params({"start_date": '20010106', "end_date": '20230922'})\
            .build(),

        create_interface("stock_margin_szse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("深圳证券交易所-融资融券数据-融资融券汇总")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "margin", "szse")\
            .with_example_params({"date": '20240411'})\
            .build(),

        create_interface("stock_new_a_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-新股-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "spot", "stock", "a", "new")\
            .build(),

        create_interface("stock_price_js")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("美股目标价 or 港股目标价")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("price", "stock", "js")\
            .with_example_params({"symbol": 'us'})\
            .build(),

        create_interface("stock_qsjy_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-特色数据-券商业绩月报")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "qsjy")\
            .with_example_params({"date": '20200731'})\
            .build(),

        create_interface("stock_sector_fund_flow_summary")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-资金流向-行业资金流-xx行业个股资金流")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("fund", "stock", "行业", "sector", "summary")\
            .with_example_params({"symbol": '电源设备', "indicator": '今日'})\
            .build(),

        create_interface("stock_sector_spot")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪行业-板块行情")\
            .with_optional_params("indicator")\
            .with_pattern(ParameterPattern.from_params(["indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "行业", "sector", "spot")\
            .with_example_params({"indicator": '新浪行业'})\
            .build(),

        create_interface("stock_sse_deal_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("上海证券交易所-数据-股票数据-成交概况-股票成交概况-每日股票情况")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sse", "股票", "daily", "deal")\
            .with_example_params({"date": '20241216'})\
            .build(),

        create_interface("stock_us_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-美股")\
            .with_optional_params("symbol", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("daily", "stock", "us", "股票")\
            .with_example_params({"symbol": 'FB', "adjust": ''})\
            .build(),

        create_interface("stock_us_hist")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情-美股-每日行情")\
            .with_optional_params("symbol", "period", "start_date", "end_date", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period", "start_date", "end_date", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("hist", "stock", "us", "股票")\
            .with_example_params({"symbol": '105.MSFT', "period": 'daily', "start_date": '19700101', "end_date": '22220101', "adjust": ''})\
            .build(),

        create_interface("stock_us_hist_min_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情首页-美股-每日分时行情")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "hist", "股票", "min")\
            .with_example_params({"symbol": '105.ATER', "start_date": '2024-01-01', "end_date": '2024-01-31'})\
            .build(),

        # about half hour
        create_interface("stock_us_spot")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-所有美股的数据, 注意延迟 15 分钟")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("股票", "stock", "us", "spot")\
            .build(),

        create_interface("stock_zh_a_cdr_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-A股-CDR个股的历史行情数据, 大量抓取容易封 IP")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "stock", "A股", "cdr", "daily")\
            .with_example_params({"symbol": 'sh689009', "start_date": '19900101', "end_date": '22201116'})\
            .build(),

        create_interface("stock_zh_a_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-A 股-个股的历史行情数据, 大量抓取容易封 IP")\
            .with_optional_params("symbol", "start_date", "end_date", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "zh", "daily", "a")\
            .with_example_params({"symbol": 'sh603843', "start_date": '19900101', "end_date": '21000118', "adjust": ''})\
            .build(),

        create_interface("stock_zh_a_gbjg_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富-A股数据-股本结构")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "em", "stock", "A股", "股票")\
            .with_example_params({"symbol": '603392.SH'})\
            .build(),

        create_interface("stock_zh_a_hist")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情首页-沪深京 A 股-每日行情")\
            .with_optional_params("symbol", "period", "start_date", "end_date", "adjust", "timeout")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period", "start_date", "end_date", "adjust", "timeout"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "stock", "hist", "股票", "a")\
            .with_example_params({"symbol": '000001', "period": 'daily', "start_date": '19700101', "end_date": '20500101', "adjust": ''})\
            .build(),

        create_interface("stock_zh_a_hist_min_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情首页-沪深京 A 股-每日分时行情")\
            .with_optional_params("symbol", "start_date", "end_date", "period", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date", "period", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "em", "stock", "hist", "股票")\
            .with_example_params({"symbol": '000001', "start_date": '2024-01-01', "end_date": '2024-01-31', "period": '5', "adjust": ''})\
            .build(),

        create_interface("stock_zh_a_hist_pre_min_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情首页-沪深京 A 股-每日分时行情包含盘前数据")\
            .with_optional_params("symbol", "start_time", "end_time")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_time", "end_time"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "em", "stock", "pre", "hist")\
            .with_example_params({"symbol": '000001', "start_time": '09:00:00', "end_time": '15:50:00'})\
            .build(),

        create_interface("stock_zh_a_hist_tx")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("腾讯证券-日频-股票历史数据")\
            .with_optional_params("symbol", "start_date", "end_date", "adjust", "timeout")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date", "adjust", "timeout"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "stock", "tx", "指数", "hist")\
            .with_example_params({"symbol": 'sz000001', "start_date": '19000101', "end_date": '20500101', "adjust": ''})\
            .build(),

        create_interface("stock_zh_a_minute")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("股票及股票指数历史行情数据-分钟数据")\
            .with_optional_params("symbol", "period", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "stock", "minute", "指数", "股票")\
            .with_example_params({"symbol": 'sh600519', "period": '1', "adjust": ''})\
            .build(),

        create_interface("stock_zh_a_spot")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-所有 A 股的实时行情数据; 重复运行本函数会被新浪暂时封 IP")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "spot", "stock", "股票", "a")\
            .build(),

        create_interface("stock_zh_a_tick_tx_js")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("腾讯财经-历史分笔数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "js", "stock", "tx", "股票")\
            .with_example_params({"symbol": 'sz000001'})\
            .build(),

        create_interface("stock_zh_ab_comparison_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情中心-沪深京个股-AB股比价-全部AB股比价")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "em", "ab", "B股", "stock")\
            .build(),

        create_interface("stock_zh_ah_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("腾讯财经-港股-AH-股票历史行情")\
            .with_optional_params("symbol", "start_year", "end_year", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_year", "end_year", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "stock", "股票", "daily", "ah")\
            .with_example_params({"symbol": '02318', "start_year": '2000', "end_year": '2019', "adjust": ''})\
            .build(),

        create_interface("stock_zh_ah_spot")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("腾讯财经-港股-AH-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "zh", "ah", "spot")\
            .build(),

        create_interface("stock_zh_ah_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情中心-沪深港通-AH股比价-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "em", "spot", "stock", "ah")\
            .build(),

        create_interface("stock_zh_b_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-B 股-个股的历史行情数据, 大量抓取容易封 IP")\
            .with_optional_params("symbol", "start_date", "end_date", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("daily", "stock", "zh", "b")\
            .with_example_params({"symbol": 'sh900901', "start_date": '19900101', "end_date": '21000118', "adjust": ''})\
            .build(),

        create_interface("stock_zh_b_minute")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("股票及股票指数历史行情数据-分钟数据")\
            .with_optional_params("symbol", "period", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "stock", "minute", "指数", "股票")\
            .with_example_params({"symbol": 'sh900901', "period": '1', "adjust": ''})\
            .build(),

        create_interface("stock_zh_b_spot")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-所有 B 股的实时行情数据; 重复运行本函数会被新浪暂时封 IP")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "spot", "stock", "股票", "b")\
            .build(),

        create_interface("stock_zh_index_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-指数-历史行情数据, 大量抓取容易封 IP")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "stock", "指数", "index", "daily")\
            .with_example_params({"symbol": 'sh000922'})\
            .build(),

        create_interface("stock_zh_index_daily_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-股票指数数据")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "em", "stock", "指数", "index")\
            .with_example_params({"symbol": 'csi931151', "start_date": '19900101', "end_date": '20500101'})\
            .build(),

        create_interface("stock_zh_index_daily_tx")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("腾讯证券-日频-股票或者指数历史数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "stock", "tx", "指数", "index")\
            .with_example_params({"symbol": 'sz980017'})\
            .build(),

        create_interface("stock_zh_index_hist_csindex")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("中证指数-具体指数-历史行情数据")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "stock", "指数", "index", "hist")\
            .with_example_params({"symbol": '000928', "start_date": '20180526', "end_date": '20240604'})\
            .build(),

        create_interface("stock_zh_index_spot_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-行情中心首页-A股-分类-所有指数")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("sina", "zh", "spot", "stock", "A股")\
            .build(),

        create_interface("stock_zh_kcb_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-科创板股票的历史行情数据, 大量抓取容易封IP")\
            .with_optional_params("symbol", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "kcb", "stock", "股票", "daily")\
            .with_example_params({"symbol": 'sh688399', "adjust": ''})\
            .build(),

        create_interface("stock_zh_kcb_spot")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-科创板实时行情数据, 大量抓取容易封IP")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "zh", "kcb", "spot")\
            .build(),

        create_interface("stock_zt_pool_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情中心-涨停板行情-涨停股池")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "pool", "em", "zt")\
            .with_example_params({"date": '20241008'})\
            .build(),

        create_interface("stock_zt_pool_previous_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情中心-涨停板行情-昨日涨停股池")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "previous", "stock", "zt", "pool")\
            .with_example_params({"date": '20240415'})\
            .build(),

        create_interface("stock_zt_pool_strong_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情中心-涨停板行情-强势股池")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("strong", "em", "stock", "zt", "pool")\
            .with_example_params({"date": '20241231'})\
            .build(),
        ]

    def _register_market_index_interfaces(self) -> List[InterfaceMetadata]:
        """注册MARKET_INDEX接口"""
        return [
        create_interface("stock_esg_hz_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.MARKET_INDEX)\
            .with_description("新浪财经-ESG评级中心-ESG评级-华证指数")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("sina", "stock", "指数", "hz", "esg")\
            .build(),

        create_interface("stock_zh_index_value_csindex")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.MARKET_INDEX)\
            .with_description("中证指数-指数估值数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "value", "stock", "指数", "index")\
            .with_example_params({"symbol": 'H30374'})\
            .build(),

        create_interface("stock_zh_vote_baidu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.MARKET_INDEX)\
            .with_description("百度股市通- A 股或指数-股评-投票")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("vote", "zh", "stock", "指数", "股票")\
            .with_example_params({"symbol": '000001', "indicator": '指数'})\
            .build(),
        ]

    def _register_fund_data_interfaces(self) -> List[InterfaceMetadata]:
        """注册FUND_DATA接口"""
        return [
        create_interface("stock_fund_flow_big_deal")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("同花顺-数据中心-资金流向-大单追踪")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("big", "fund", "stock", "deal", "flow")\
            .build(),

        create_interface("stock_fund_flow_concept")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("同花顺-数据中心-资金流向-概念资金流")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "flow", "concept", "fund")\
            .with_example_params({"symbol": '即时'})\
            .build(),
        ]

    def _register_industry_data_interfaces(self) -> List[InterfaceMetadata]:
        """注册INDUSTRY_DATA接口"""
        return [
        create_interface("stock_fund_flow_industry")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.INDUSTRY_DATA)\
            .with_description("同花顺-数据中心-资金流向-行业资金流")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("fund", "stock", "行业", "industry", "flow")\
            .with_example_params({"symbol": '即时'})\
            .build(),

        create_interface("stock_yysj_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.INDUSTRY_DATA)\
            .with_description("东方财富-数据中心-年报季报-预约披露时间")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "A股", "em", "yysj")\
            .with_example_params({"symbol": '沪深A股', "date": '20200331'})\
            .build(),
        ]

    def _register_market_overview_interfaces(self) -> List[InterfaceMetadata]:
        """注册MARKET_OVERVIEW接口"""
        return [
        create_interface("stock_market_activity_legu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.MARKET_OVERVIEW)\
            .with_description("乐咕乐股网-赚钱效应分析")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "legu", "market", "activity")\
            .build(),

        create_interface("stock_market_fund_flow")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.MARKET_OVERVIEW)\
            .with_description("东方财富网-数据中心-资金流向-大盘")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "flow", "market", "fund")\
            .build(),
        ]


# 创建提供者实例并注册
akshare_provider = AkshareProvider()

# 注册到全局管理器
from .base import register_provider
register_provider(akshare_provider)
