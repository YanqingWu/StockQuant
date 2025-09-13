# -*- coding: utf-8 -*-
"""
AKShare数据源接口提供者
自动生成于 2025-09-13 22:42:58
总共 366 个接口
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

        interfaces.extend(self._register_other_interfaces())
        interfaces.extend(self._register_stock_financial_interfaces())
        interfaces.extend(self._register_stock_quote_interfaces())
        interfaces.extend(self._register_market_index_interfaces())
        interfaces.extend(self._register_stock_basic_interfaces())
        interfaces.extend(self._register_industry_data_interfaces())
        interfaces.extend(self._register_market_overview_interfaces())
        interfaces.extend(self._register_stock_technical_interfaces())
        interfaces.extend(self._register_fund_data_interfaces())
        interfaces.extend(self._register_forex_data_interfaces())

        # 批量注册所有接口
        self.registry.register_interfaces(interfaces)

    def _register_other_interfaces(self) -> List[InterfaceMetadata]:
        """注册OTHER接口"""
        return [
        create_interface("stock_a_all_pb")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("全部A股-等权重市净率、中位数市净率")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("pb", "all", "A股", "a", "stock")\
            .build(),

        create_interface("stock_a_below_net_asset_statistics")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("破净股统计历史走势")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("A股", "a", "below", "asset", "statistics")\
            .with_example_params({"symbol": '全部A股'})\
            .build(),

        create_interface("stock_a_code_to_symbol")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("输入股票代码判断股票市场")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("a", "stock", "code", "股票", "symbol")\
            .with_example_params({"symbol": '000300'})\
            .build(),

        create_interface("stock_a_congestion_lg")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("乐咕乐股-大盘拥挤度")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "lg", "a", "congestion")\
            .build(),

        create_interface("stock_a_gxl_lg")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("乐咕乐股-股息率-A 股股息率")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("A股", "a", "gxl", "stock", "lg")\
            .with_example_params({"symbol": '上证A股'})\
            .build(),

        create_interface("stock_a_high_low_statistics")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("乐咕乐股-创新高、新低的股票数量")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("int")\
            .with_keywords("a", "high", "statistics", "stock", "股票")\
            .with_example_params({"symbol": 'all'})\
            .build(),

        create_interface("stock_a_ttm_lyr")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("全部 A 股-等权重市盈率、中位数市盈率")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("A股", "a", "stock", "ttm", "lyr")\
            .build(),

        create_interface("stock_account_statistics_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-股票账户统计")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("int")\
            .with_keywords("em", "statistics", "stock", "股票", "account")\
            .build(),

        create_interface("stock_add_stock")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-发行与分配-增发")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "add")\
            .with_example_params({"symbol": '688166'})\
            .build(),

        create_interface("stock_allotment_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("巨潮资讯-个股-配股实施方案")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "cninfo", "allotment")\
            .with_example_params({"symbol": '600030', "start_date": '19700101', "end_date": '22220222'})\
            .build(),

        create_interface("stock_analyst_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-研究报告-东方财富分析师指数-东方财富分析师指数2020最新排行-分析师详情")\
            .with_optional_params("analyst_id", "indicator")\
            .with_pattern(ParameterPattern.from_params(["analyst_id", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "detail", "指数", "analyst")\
            .with_example_params({"analyst_id": '11000200926', "indicator": '最新跟踪成分股'})\
            .build(),

        create_interface("stock_analyst_rank_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-研究报告-东方财富分析师指数-东方财富分析师指数")\
            .with_optional_params("year")\
            .with_pattern(ParameterPattern.from_params(["year"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "指数", "analyst", "rank")\
            .with_example_params({"year": '2024'})\
            .build(),

        create_interface("stock_bid_ask_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-行情报价")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("bid", "em", "stock", "股票", "ask")\
            .with_example_params({"symbol": '000001'})\
            .build(),

        create_interface("stock_board_change_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-行情中心-当日板块异动详情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "change", "em", "board")\
            .build(),

        create_interface("stock_board_concept_cons_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-沪深板块-概念板块-板块成份")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("cons", "board", "em", "stock", "concept")\
            .with_example_params({"symbol": '融资融券'})\
            .build(),

        create_interface("stock_board_concept_name_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-行情中心-沪深京板块-概念板块-名称")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("name", "board", "em", "stock", "concept")\
            .build(),

        create_interface("stock_board_concept_name_em_async")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-行情中心-沪深京板块-概念板块-名称 (同步接口)")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("name", "board", "em", "stock", "async")\
            .build(),

        create_interface("stock_board_concept_name_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-板块-概念板块-概念")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("name", "board", "stock", "ths", "concept")\
            .build(),

        create_interface("stock_board_concept_summary_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-概念板块-概念时间表")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("summary", "board", "stock", "ths", "concept")\
            .build(),

        create_interface("stock_cg_equity_mortgage_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("巨潮资讯-数据中心-专题统计-公司治理-股权质押")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("equity", "cg", "mortgage", "stock", "cninfo")\
            .with_example_params({"date": '20210930'})\
            .build(),

        create_interface("stock_cg_guarantee_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("巨潮资讯-数据中心-专题统计-公司治理-对外担保")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "cg", "cninfo", "guarantee")\
            .with_example_params({"symbol": '全部', "start_date": '20180630', "end_date": '20210927'})\
            .build(),

        create_interface("stock_changes_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-行情中心-盘口异动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "changes", "em")\
            .with_example_params({"symbol": '大笔买入'})\
            .build(),

        create_interface("stock_circulate_stock_holder")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-股东股本-流通股东")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "holder", "circulate")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_classify_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("按 symbol 分类后的股票")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "stock", "股票", "classify", "sina")\
            .with_example_params({"symbol": '热门概念'})\
            .build(),

        create_interface("stock_comment_detail_zhpj_lspf_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-千股千评-综合评价-历史评分")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zhpj", "lspf", "em", "stock", "股票")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_comment_detail_zlkp_jgcyd_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-千股千评-主力控盘-机构参与度")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("jgcyd", "zlkp", "em", "stock", "股票")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_comment_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-千股千评")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "comment")\
            .build(),

        create_interface("stock_concept_cons_futu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("富途牛牛-主题投资-概念板块-成分股")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "futu", "cons", "concept")\
            .with_example_params({"symbol": '特朗普概念股'})\
            .build(),

        create_interface("stock_cyq_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-概念板-行情中心-日K-筹码分布")\
            .with_optional_params("symbol", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "em", "cyq")\
            .with_example_params({"symbol": '000001', "adjust": ''})\
            .build(),

        create_interface("stock_dividend_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("巨潮资讯-个股-历史分红")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "cninfo", "dividend")\
            .with_example_params({"symbol": '600009'})\
            .build(),

        create_interface("stock_dxsyl_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-新股申购-打新收益率")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "dxsyl", "em")\
            .build(),

        create_interface("stock_dzjy_hygtj")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-大宗交易-活跃 A 股统计")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hygtj", "dzjy")\
            .with_example_params({"symbol": '近三月'})\
            .build(),

        create_interface("stock_dzjy_hyyybtj")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-大宗交易-活跃营业部统计")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hyyybtj", "dzjy")\
            .with_example_params({"symbol": '近3日'})\
            .build(),

        create_interface("stock_dzjy_mrmx")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-大宗交易-每日明细")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("mrmx", "A股", "B股", "基金", "stock")\
            .with_example_params({"symbol": '基金', "start_date": '20220104', "end_date": '20220104'})\
            .build(),

        create_interface("stock_dzjy_mrtj")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-大宗交易-每日统计")\
            .with_optional_params("start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "mrtj", "dzjy")\
            .with_example_params({"start_date": '20220105', "end_date": '20220105'})\
            .build(),

        create_interface("stock_dzjy_sctj")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-大宗交易-市场统计")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sctj", "dzjy")\
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
            .with_keywords("stock", "lg", "ebs")\
            .build(),

        create_interface("stock_esg_hz_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-ESG评级中心-ESG评级-华证指数")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("esg", "stock", "hz", "指数", "sina")\
            .build(),

        create_interface("stock_esg_msci_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-ESG评级中心-ESG评级-MSCI")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "msci", "esg", "sina")\
            .build(),

        create_interface("stock_esg_rate_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-ESG评级中心-ESG评级-ESG评级数据")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "esg", "sina", "rate")\
            .build(),

        create_interface("stock_esg_rft_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-ESG评级中心-ESG评级-路孚特")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "rft", "esg", "sina")\
            .build(),

        create_interface("stock_esg_zd_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-ESG评级中心-ESG评级-秩鼎")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "zd", "esg", "sina")\
            .build(),

        create_interface("stock_fhps_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-分红送配-分红送配详情")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "股票", "detail", "fhps")\
            .with_example_params({"symbol": '300073'})\
            .build(),

        create_interface("stock_fhps_detail_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-分红情况")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "detail", "fhps", "ths")\
            .with_example_params({"symbol": '603444'})\
            .build(),

        create_interface("stock_fhps_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-年报季报-分红送配")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "fhps", "em")\
            .with_example_params({"date": '20231231'})\
            .build(),

        create_interface("stock_gddh_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-股东大会")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "gddh", "em")\
            .build(),

        create_interface("stock_ggcg_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-高管持股")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "ggcg")\
            .with_example_params({"symbol": '全部'})\
            .build(),

        create_interface("stock_gpzy_distribute_statistics_bank_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("gpzy", "bank", "statistics", "em", "stock")\
            .build(),

        create_interface("stock_gpzy_distribute_statistics_company_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-证券公司")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("gpzy", "company", "statistics", "em", "stock")\
            .build(),

        create_interface("stock_gpzy_pledge_ratio_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("gpzy", "pledge", "em", "stock", "ratio")\
            .build(),

        create_interface("stock_gpzy_pledge_ratio_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-股权质押-上市公司质押比例")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gpzy", "pledge", "em", "stock", "ratio")\
            .with_example_params({"date": '20240906'})\
            .build(),

        create_interface("stock_gpzy_profile_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-股权质押-股权质押市场概况")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "gpzy", "profile", "em")\
            .build(),

        create_interface("stock_gsrl_gsdt_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-股市日历-公司动态")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "gsdt", "gsrl")\
            .with_example_params({"date": '20230808'})\
            .build(),

        create_interface("stock_hk_company_profile_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-港股-公司资料")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("company", "hk", "em", "stock", "股票")\
            .with_example_params({"symbol": '03900'})\
            .build(),

        create_interface("stock_hk_fhpx_detail_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-港股-分红派息")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("fhpx", "hk", "stock", "detail", "ths")\
            .with_example_params({"symbol": '0700'})\
            .build(),

        create_interface("stock_hk_ggt_components_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-行情中心-港股市场-港股通成份股")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("components", "hk", "em", "ggt", "stock")\
            .build(),

        create_interface("stock_hk_gxl_lg")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("乐咕乐股-股息率-恒生指数股息率")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("gxl", "hk", "stock", "lg", "指数")\
            .build(),

        create_interface("stock_hk_hot_rank_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-个股人气榜-历史趋势")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("hk", "em", "hot", "stock", "detail")\
            .with_example_params({"symbol": '00700'})\
            .build(),

        create_interface("stock_hk_hot_rank_detail_realtime_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-个股人气榜-实时变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("hk", "em", "hot", "stock", "realtime")\
            .with_example_params({"symbol": '00700'})\
            .build(),

        create_interface("stock_hk_hot_rank_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-个股人气榜-人气榜-港股市场")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("hk", "em", "hot", "stock", "rank")\
            .build(),

        create_interface("stock_hk_hot_rank_latest_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-个股人气榜-最新排名")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("latest", "hk", "em", "hot", "stock")\
            .with_example_params({"symbol": '00700'})\
            .build(),

        create_interface("stock_hk_security_profile_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-港股-证券资料")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("hk", "em", "stock", "股票", "security")\
            .with_example_params({"symbol": '03900'})\
            .build(),

        create_interface("stock_hk_valuation_baidu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("百度股市通-港股-财务报表-估值数据")\
            .with_optional_params("symbol", "indicator", "period")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator", "period"]))\
            .with_return_type("DataFrame")\
            .with_keywords("hk", "baidu", "stock", "股票", "财务")\
            .with_example_params({"symbol": '06969', "indicator": '总市值', "period": 'daily'})\
            .build(),

        create_interface("stock_hold_change_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("巨潮资讯-数据中心-专题统计-股东股本-股本变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "change", "cninfo", "hold")\
            .with_example_params({"symbol": '全部'})\
            .build(),

        create_interface("stock_hold_control_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("巨潮资讯-数据中心-专题统计-股东股本-实际控制人持股变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "cninfo", "control", "hold")\
            .with_example_params({"symbol": '全部'})\
            .build(),

        create_interface("stock_hold_management_detail_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("巨潮资讯-数据中心-专题统计-股东股本-高管持股变动明细")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "management", "detail", "cninfo", "hold")\
            .with_example_params({"symbol": '增持'})\
            .build(),

        create_interface("stock_hold_management_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-高管持股-董监高及相关人员持股变动明细")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "stock", "detail", "management", "hold")\
            .build(),

        create_interface("stock_hold_management_person_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-高管持股-人员增减持股变动明细")\
            .with_optional_params("symbol", "name")\
            .with_pattern(ParameterPattern.from_params(["symbol", "name"]))\
            .with_return_type("DataFrame")\
            .with_keywords("person", "em", "stock", "股票", "management")\
            .with_example_params({"symbol": '001308', "name": '吴远'})\
            .build(),

        create_interface("stock_hold_num_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("巨潮资讯-数据中心-专题统计-股东股本-股东人数及持股集中度")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("int")\
            .with_keywords("stock", "cninfo", "hold", "num")\
            .with_example_params({"date": '20210630'})\
            .build(),

        create_interface("stock_hot_deal_xq")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("雪球-沪深股市-热度排行榜-分享交易排行榜")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "xq", "deal", "hot")\
            .with_example_params({"symbol": '最热门'})\
            .build(),

        create_interface("stock_hot_follow_xq")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("雪球-沪深股市-热度排行榜-关注排行榜")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "xq", "follow", "hot")\
            .with_example_params({"symbol": '最热门'})\
            .build(),

        create_interface("stock_hot_keyword_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-个股人气榜-热门关键词")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "hot", "keyword")\
            .with_example_params({"symbol": 'SZ000665'})\
            .build(),

        create_interface("stock_hot_rank_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-个股人气榜-历史趋势及粉丝特征")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "hot", "stock", "detail", "rank")\
            .with_example_params({"symbol": 'SZ000665'})\
            .build(),

        create_interface("stock_hot_rank_detail_realtime_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-个股人气榜-实时变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "hot", "stock", "realtime", "detail")\
            .with_example_params({"symbol": 'SZ000665'})\
            .build(),

        create_interface("stock_hot_rank_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-个股人气榜-人气榜")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "hot", "rank")\
            .build(),

        create_interface("stock_hot_rank_latest_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-个股人气榜-最新排名")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("latest", "em", "hot", "stock", "rank")\
            .with_example_params({"symbol": 'SZ000665'})\
            .build(),

        create_interface("stock_hot_rank_relate_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-个股人气榜-相关股票")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "relate", "hot", "stock", "股票")\
            .with_example_params({"symbol": 'SZ000665'})\
            .build(),

        create_interface("stock_hot_search_baidu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("百度股市通-热搜股票")\
            .with_optional_params("symbol", "date", "time")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date", "time"]))\
            .with_return_type("DataFrame")\
            .with_keywords("A股", "hot", "baidu", "stock", "search")\
            .with_example_params({"symbol": 'A股', "date": '20250616', "time": '今日'})\
            .build(),

        create_interface("stock_hot_tweet_xq")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("雪球-沪深股市-热度排行榜-讨论排行榜")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "xq", "tweet", "hot")\
            .with_example_params({"symbol": '最热门'})\
            .build(),

        create_interface("stock_hot_up_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-个股人气榜-飙升榜")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "up", "em", "hot")\
            .build(),

        create_interface("stock_hsgt_board_rank_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-沪深港通持股-行业板块排行-北向资金增持行业板块排行")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "board", "em", "stock", "hsgt")\
            .with_example_params({"symbol": '北向资金增持行业板块排行', "indicator": '今日'})\
            .build(),

        create_interface("stock_hsgt_hold_stock_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-数据中心-沪深港通持股-个股排行")\
            .with_optional_params("market", "indicator")\
            .with_pattern(ParameterPattern.from_params(["market", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "hold", "hsgt")\
            .with_example_params({"market": '沪股通', "indicator": '5日排行'})\
            .build(),

        create_interface("stock_hsgt_individual_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-数据中心-沪深港通-沪深港通持股-具体股票")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "individual", "stock", "股票", "hsgt")\
            .with_example_params({"symbol": '002008'})\
            .build(),

        create_interface("stock_hsgt_stock_statistics_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-沪深港通-沪深港通持股-每日个股统计")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("int")\
            .with_keywords("stock", "em", "statistics", "hsgt")\
            .with_example_params({"symbol": '北向持股', "start_date": '20240110', "end_date": '20240110'})\
            .build(),

        create_interface("stock_inner_trade_xq")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("雪球-行情中心-沪深股市-内部交易")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "xq", "inner", "trade")\
            .build(),

        create_interface("stock_institute_hold")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-股票-机构持股一览表")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "institute", "股票", "hold")\
            .with_example_params({"symbol": '20051'})\
            .build(),

        create_interface("stock_institute_hold_detail")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-股票-机构持股详情")\
            .with_optional_params("stock", "quarter")\
            .with_pattern(ParameterPattern.from_params(["stock", "quarter"]))\
            .with_return_type("DataFrame")\
            .with_keywords("institute", "stock", "股票", "detail", "hold")\
            .with_example_params({"stock": '600433', "quarter": '20201'})\
            .build(),

        create_interface("stock_institute_recommend")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-机构推荐池-最新投资评级")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "institute", "recommend", "stock", "股票")\
            .with_example_params({"symbol": '投资评级选股'})\
            .build(),

        create_interface("stock_institute_recommend_detail")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-机构推荐池-股票评级记录")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("institute", "recommend", "stock", "股票", "detail")\
            .with_example_params({"symbol": '000001'})\
            .build(),

        create_interface("stock_intraday_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-分时数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "intraday", "em")\
            .with_example_params({"symbol": '000001'})\
            .build(),

        create_interface("stock_ipo_info")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-发行与分配-新股发行")\
            .with_optional_params("stock")\
            .with_pattern(ParameterPattern.from_params(["stock"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "info", "股票", "ipo")\
            .with_example_params({"stock": '600004'})\
            .build(),

        create_interface("stock_ipo_summary_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("巨潮资讯-个股-上市相关")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("ipo", "summary", "stock", "股票", "cninfo")\
            .with_example_params({"symbol": '600030'})\
            .build(),

        create_interface("stock_irm_ans_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("互动易-回答")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "irm", "cninfo", "ans")\
            .with_example_params({"symbol": '1513586704097333248'})\
            .build(),

        create_interface("stock_irm_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("互动易-提问")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "irm", "股票", "cninfo")\
            .with_example_params({"symbol": '002594'})\
            .build(),

        create_interface("stock_jgdy_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-机构调研-机构调研详细")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "jgdy", "em", "detail")\
            .with_example_params({"date": '20241211'})\
            .build(),

        create_interface("stock_jgdy_tj_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-机构调研-机构调研统计")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "tj", "jgdy", "em")\
            .with_example_params({"date": '20220101'})\
            .build(),

        create_interface("stock_js_weibo_nlp_time")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("https://datacenter.jin10.com/market")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("weibo", "time", "stock", "js", "nlp")\
            .build(),

        create_interface("stock_js_weibo_report")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("金十数据中心-实时监控-微博舆情报告")\
            .with_optional_params("time_period")\
            .with_pattern(ParameterPattern.from_params(["time_period"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "weibo", "report", "js")\
            .with_example_params({"time_period": 'CNHOUR12'})\
            .build(),

        create_interface("stock_lh_yyb_capital")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-营业部排名-资金实力最强")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "lh", "capital", "yyb")\
            .build(),

        create_interface("stock_lh_yyb_control")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-营业部排名-抱团操作实力")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "lh", "control", "yyb")\
            .build(),

        create_interface("stock_lh_yyb_most")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-营业部排名-上榜次数最多")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "lh", "yyb", "most")\
            .build(),

        create_interface("stock_lhb_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-龙虎榜单-龙虎榜详情")\
            .with_optional_params("start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "lhb", "detail")\
            .with_example_params({"start_date": '20230403', "end_date": '20230417'})\
            .build(),

        create_interface("stock_lhb_ggtj_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("龙虎榜-个股上榜统计")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ggtj", "lhb", "sina")\
            .with_example_params({"symbol": '5'})\
            .build(),

        create_interface("stock_lhb_hyyyb_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-龙虎榜单-每日活跃营业部")\
            .with_optional_params("start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hyyyb", "em", "lhb")\
            .with_example_params({"start_date": '20220324', "end_date": '20220324'})\
            .build(),

        create_interface("stock_lhb_jgmmtj_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-龙虎榜单-机构买卖每日统计")\
            .with_optional_params("start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "jgmmtj", "em", "lhb")\
            .with_example_params({"start_date": '20240417', "end_date": '20240430'})\
            .build(),

        create_interface("stock_lhb_jgmx_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("龙虎榜-机构席位成交明细")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sina", "lhb", "jgmx")\
            .build(),

        create_interface("stock_lhb_jgstatistic_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-龙虎榜单-机构席位追踪")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "lhb", "jgstatistic")\
            .with_example_params({"symbol": '近一月'})\
            .build(),

        create_interface("stock_lhb_jgzz_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("龙虎榜-机构席位追踪")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "jgzz", "lhb", "sina")\
            .with_example_params({"symbol": '5'})\
            .build(),

        create_interface("stock_lhb_stock_detail_date_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-龙虎榜单-个股龙虎榜详情-日期")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("date", "em", "lhb", "stock", "股票")\
            .with_example_params({"symbol": '600077'})\
            .build(),

        create_interface("stock_lhb_stock_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-龙虎榜单-个股龙虎榜详情")\
            .with_optional_params("symbol", "date", "flag")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date", "flag"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "lhb", "stock", "股票", "detail")\
            .with_example_params({"symbol": '000788', "date": '20220315', "flag": '卖出'})\
            .build(),

        create_interface("stock_lhb_stock_statistic_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-龙虎榜单-个股上榜统计")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "statistic", "em", "lhb")\
            .with_example_params({"symbol": '近一月'})\
            .build(),

        create_interface("stock_lhb_traderstatistic_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-龙虎榜单-营业部统计")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "lhb", "traderstatistic")\
            .with_example_params({"symbol": '近一月'})\
            .build(),

        create_interface("stock_lhb_yyb_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-龙虎榜单-营业部历史交易明细-营业部交易明细")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "yyb", "lhb", "stock", "detail")\
            .with_example_params({"symbol": '10188715'})\
            .build(),

        create_interface("stock_lhb_yybph_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-龙虎榜单-营业部排行")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "lhb", "yybph")\
            .with_example_params({"symbol": '近一月'})\
            .build(),

        create_interface("stock_lhb_yytj_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("龙虎榜-营业部上榜统计")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "yytj", "lhb", "sina")\
            .with_example_params({"symbol": '5'})\
            .build(),

        create_interface("stock_lrb_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-数据中心-年报季报-业绩快报-利润表")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "lrb")\
            .with_example_params({"date": '20240331'})\
            .build(),

        create_interface("stock_main_stock_holder")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-股本股东-主要股东")\
            .with_optional_params("stock")\
            .with_pattern(ParameterPattern.from_params(["stock"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "main", "holder", "股票")\
            .with_example_params({"stock": '600004'})\
            .build(),

        create_interface("stock_management_change_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-公司大事-高管持股变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("change", "stock", "股票", "management", "ths")\
            .with_example_params({"symbol": '688981'})\
            .build(),

        create_interface("stock_margin_account_info")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-融资融券-融资融券账户统计-两融账户信息")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("int")\
            .with_keywords("stock", "info", "account", "margin")\
            .build(),

        create_interface("stock_margin_detail_sse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("上海证券交易所-融资融券数据-融资融券明细")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sse", "margin", "detail")\
            .with_example_params({"date": '20230922'})\
            .build(),

        create_interface("stock_margin_detail_szse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("深证证券交易所-融资融券数据-融资融券交易明细")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "szse", "margin", "detail")\
            .with_example_params({"date": '20230925'})\
            .build(),

        create_interface("stock_margin_ratio_pa")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("融资融券-标的证券名单及保证金比例查询")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("List[str]")\
            .with_keywords("stock", "ratio", "pa", "margin")\
            .with_example_params({"date": '20231013'})\
            .build(),

        create_interface("stock_margin_sse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("上海证券交易所-融资融券数据-融资融券汇总")\
            .with_optional_params("start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sse", "margin")\
            .with_example_params({"start_date": '20010106', "end_date": '20230922'})\
            .build(),

        create_interface("stock_margin_szse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("深圳证券交易所-融资融券数据-融资融券汇总")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "szse", "margin")\
            .with_example_params({"date": '20240411'})\
            .build(),

        create_interface("stock_market_activity_legu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("乐咕乐股网-赚钱效应分析")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "legu", "market", "activity")\
            .build(),

        create_interface("stock_new_ipo_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("巨潮资讯-数据中心-新股数据-新股发行")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "cninfo", "ipo", "new")\
            .build(),

        create_interface("stock_notice_report")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-公告大全-沪深京 A 股公告")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "report", "notice", "财务")\
            .with_example_params({"symbol": '全部', "date": '20220511'})\
            .build(),

        create_interface("stock_pg_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-新股数据-配股")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "pg")\
            .build(),

        create_interface("stock_price_js")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("美股目标价 or 港股目标价")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "price", "js")\
            .with_example_params({"symbol": 'us'})\
            .build(),

        create_interface("stock_profile_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("巨潮资讯-个股-公司概况")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "profile", "cninfo")\
            .with_example_params({"symbol": '600030'})\
            .build(),

        create_interface("stock_qbzf_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-新股数据-增发-全部增发")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "qbzf")\
            .build(),

        create_interface("stock_qsjy_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-券商业绩月报")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "qsjy")\
            .with_example_params({"date": '20200731'})\
            .build(),

        create_interface("stock_rank_cxd_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-技术选股-创新低")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "cxd", "ths", "rank")\
            .with_example_params({"symbol": '创月新低'})\
            .build(),

        create_interface("stock_rank_cxfl_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-技术选股-持续放量")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ths", "cxfl", "rank")\
            .build(),

        create_interface("stock_rank_cxg_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-技术选股-创新高")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "cxg", "ths", "rank")\
            .with_example_params({"symbol": '创月新高'})\
            .build(),

        create_interface("stock_rank_cxsl_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-技术选股-持续缩量")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "cxsl", "ths", "rank")\
            .build(),

        create_interface("stock_rank_forecast_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("巨潮资讯-数据中心-评级预测-投资评级")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "cninfo", "forecast", "rank")\
            .with_example_params({"date": '20230817'})\
            .build(),

        create_interface("stock_rank_ljqd_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-技术选股-量价齐跌")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ljqd", "ths", "rank")\
            .build(),

        create_interface("stock_rank_ljqs_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-技术选股-量价齐升")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ljqs", "ths", "rank")\
            .build(),

        create_interface("stock_rank_lxsz_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-技术选股-连续上涨")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "lxsz", "ths", "rank")\
            .build(),

        create_interface("stock_rank_lxxd_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-技术选股-连续下跌")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "lxxd", "ths", "rank")\
            .build(),

        create_interface("stock_rank_xstp_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-技术选股-向上突破")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ths", "xstp", "rank")\
            .with_example_params({"symbol": '500日均线'})\
            .build(),

        create_interface("stock_rank_xxtp_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-技术选股-向下突破")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "xxtp", "ths", "rank")\
            .with_example_params({"symbol": '500日均线'})\
            .build(),

        create_interface("stock_rank_xzjp_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-技术选股-险资举牌")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "xzjp", "ths", "rank")\
            .build(),

        create_interface("stock_register_bj")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-新股数据-IPO审核信息-北交所")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "register", "bj")\
            .build(),

        create_interface("stock_register_cyb")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-新股数据-IPO审核信息-创业板")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "cyb", "register")\
            .build(),

        create_interface("stock_register_db")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-新股数据-IPO审核信息-达标企业")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "db", "register")\
            .build(),

        create_interface("stock_register_kcb")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-新股数据-IPO审核信息-科创板")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "kcb", "register")\
            .build(),

        create_interface("stock_register_sh")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-新股数据-IPO审核信息-上海主板")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "register", "sh")\
            .build(),

        create_interface("stock_register_sz")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-新股数据-IPO审核信息-深圳主板")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "register", "sz")\
            .build(),

        create_interface("stock_repurchase_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-股票回购-股票回购数据")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "repurchase", "em")\
            .build(),

        create_interface("stock_restricted_release_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-限售股解禁-解禁详情一览")\
            .with_optional_params("start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "restricted", "stock", "detail", "release")\
            .with_example_params({"start_date": '20221202', "end_date": '20241202'})\
            .build(),

        create_interface("stock_restricted_release_queue_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-个股限售解禁-解禁批次")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "restricted", "stock", "股票", "release")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_restricted_release_queue_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-发行分配-限售解禁")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("restricted", "stock", "股票", "release", "queue")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_restricted_release_stockholder_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-个股限售解禁-解禁股东")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "restricted", "stock", "股票", "stockholder")\
            .with_example_params({"symbol": '600000', "date": '20200904'})\
            .build(),

        create_interface("stock_restricted_release_summary_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-限售股解禁")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("A股", "summary", "em", "restricted", "stock")\
            .with_example_params({"symbol": '全部股票', "start_date": '20221101', "end_date": '20221209'})\
            .build(),

        create_interface("stock_sector_detail")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪行业-板块行情-成份详情")\
            .with_optional_params("sector")\
            .with_pattern(ParameterPattern.from_params(["sector"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sector", "行业", "detail")\
            .with_example_params({"sector": 'gn_gfgn'})\
            .build(),

        create_interface("stock_share_change_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("巨潮资讯-股本股东-公司股本变动")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("change", "stock", "share", "股票", "cninfo")\
            .with_example_params({"symbol": '002594', "start_date": '20091227', "end_date": '20241021'})\
            .build(),

        create_interface("stock_share_hold_change_bse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("北京证券交易所-信息披露-监管信息-董监高及相关人员持股变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("change", "bse", "stock", "share", "股票")\
            .with_example_params({"symbol": '430489'})\
            .build(),

        create_interface("stock_share_hold_change_sse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("上海证券交易所-披露-监管信息公开-公司监管-董董监高人员股份变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("sse", "change", "stock", "share", "股票")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_share_hold_change_szse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("深圳证券交易所-信息披露-监管信息公开-董监高人员股份变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("change", "szse", "stock", "share", "股票")\
            .with_example_params({"symbol": '全部'})\
            .build(),

        create_interface("stock_shareholder_change_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-公司大事-股东持股变动")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("change", "shareholder", "stock", "股票", "ths")\
            .with_example_params({"symbol": '688981'})\
            .build(),

        create_interface("stock_sns_sseinfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("上证e互动-提问与回答")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "sns", "sseinfo")\
            .with_example_params({"symbol": '603119'})\
            .build(),

        create_interface("stock_sse_summary")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("上海证券交易所-总貌")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "summary", "sse")\
            .build(),

        create_interface("stock_staq_net_stop")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-行情中心-沪深个股-两网及退市")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "staq", "stop", "net")\
            .build(),

        create_interface("stock_sy_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-商誉-个股商誉明细")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sy", "em")\
            .with_example_params({"date": '20231231'})\
            .build(),

        create_interface("stock_sy_profile_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-商誉-A股商誉市场概况")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("A股", "em", "stock", "sy", "profile")\
            .build(),

        create_interface("stock_sy_yq_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-商誉-商誉减值预期明细")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sy", "em", "yq")\
            .with_example_params({"date": '20240630'})\
            .build(),

        create_interface("stock_szse_area_summary")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("深证证券交易所-总貌-地区交易排序")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "area", "summary", "szse")\
            .with_example_params({"date": '2024-01-01'})\
            .build(),

        create_interface("stock_szse_sector_summary")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("深圳证券交易所-统计资料-股票行业成交数据")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "sector", "summary", "szse", "stock")\
            .with_example_params({"symbol": '当月', "date": '2024-01-01'})\
            .build(),

        create_interface("stock_szse_summary")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("深证证券交易所-总貌-证券类别统计")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "summary", "szse")\
            .with_example_params({"date": '20240830'})\
            .build(),

        create_interface("stock_tfp_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-停复牌信息")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "tfp", "em")\
            .with_example_params({"date": '20240426'})\
            .build(),

        create_interface("stock_value_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-估值分析-每日互动-每日互动-估值分析")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "em", "value")\
            .with_example_params({"symbol": '300766'})\
            .build(),

        create_interface("stock_xgsglb_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新股申购与中签查询")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "xgsglb", "em")\
            .with_example_params({"symbol": '全部股票'})\
            .build(),

        create_interface("stock_xgsr_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-数据中心-新股数据-新股上市首日")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "xgsr", "ths")\
            .build(),

        create_interface("stock_xjll_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-数据中心-年报季报-业绩快报-现金流量表")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "xjll")\
            .with_example_params({"date": '20240331'})\
            .build(),

        create_interface("stock_yjbb_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-数据中心-年报季报-业绩快报-业绩报表")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "yjbb", "em")\
            .with_example_params({"date": '20200331'})\
            .build(),

        create_interface("stock_yjkb_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-数据中心-年报季报-业绩快报")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "yjkb")\
            .with_example_params({"date": '20211231'})\
            .build(),

        create_interface("stock_yjyg_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-数据中心-年报季报-业绩预告")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "yjyg", "em")\
            .with_example_params({"date": '20200331'})\
            .build(),

        create_interface("stock_yysj_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-数据中心-年报季报-预约披露时间")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "A股", "yysj")\
            .with_example_params({"symbol": '沪深A股', "date": '20200331'})\
            .build(),

        create_interface("stock_yzxdr_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-一致行动人")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "yzxdr")\
            .with_example_params({"date": '20240930'})\
            .build(),

        create_interface("stock_zcfz_bj_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-数据中心-年报季报-业绩快报-资产负债表")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "zcfz", "em", "bj")\
            .with_example_params({"date": '20240331'})\
            .build(),

        create_interface("stock_zcfz_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-数据中心-年报季报-业绩快报-资产负债表")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "zcfz", "em")\
            .with_example_params({"date": '20240331'})\
            .build(),

        create_interface("stock_zdhtmx_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-重大合同-重大合同明细")\
            .with_optional_params("start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "zdhtmx")\
            .with_example_params({"start_date": '20200819', "end_date": '20230819'})\
            .build(),

        create_interface("stock_zh_a_disclosure_relation_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("巨潮资讯-首页-数据-预约披露调研")\
            .with_optional_params("symbol", "market", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "market", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("a", "zh", "disclosure", "基金", "stock")\
            .with_example_params({"symbol": '000001', "market": '沪深京', "start_date": '20230618', "end_date": '20231219'})\
            .build(),

        create_interface("stock_zh_a_gbjg_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富-A股数据-股本结构")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gbjg", "A股", "a", "em", "zh")\
            .with_example_params({"symbol": '603392.SH'})\
            .build(),

        create_interface("stock_zh_a_gdhs")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-股东户数")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "zh", "a", "gdhs")\
            .with_example_params({"symbol": '20230930'})\
            .build(),

        create_interface("stock_zh_a_gdhs_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-数据中心-特色数据-股东户数详情")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gdhs", "a", "zh", "em", "stock")\
            .with_example_params({"symbol": '000001'})\
            .build(),

        create_interface("stock_zh_a_new")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("新浪财经-行情中心-沪深股市-次新股")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "zh", "a", "new")\
            .build(),

        create_interface("stock_zh_a_new_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-行情中心-沪深个股-新股")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("a", "em", "zh", "new", "stock")\
            .build(),

        create_interface("stock_zh_a_st_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-行情中心-沪深个股-风险警示板")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("a", "em", "zh", "stock", "st")\
            .build(),

        create_interface("stock_zh_a_stop_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-行情中心-沪深个股-两网及退市")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("a", "em", "zh", "stock", "stop")\
            .build(),

        create_interface("stock_zh_a_tick_tx_js")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("腾讯财经-历史分笔数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("tick", "a", "zh", "stock", "股票")\
            .with_example_params({"symbol": 'sz000001'})\
            .build(),

        create_interface("stock_zh_ab_comparison_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-行情中心-沪深京个股-AB股比价-全部AB股比价")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "zh", "comparison", "B股", "stock")\
            .build(),

        create_interface("stock_zh_ah_name")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("腾讯财经-港股-AH-股票名称")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("name", "zh", "stock", "股票", "ah")\
            .build(),

        create_interface("stock_zh_valuation_baidu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("百度股市通-A股-财务报表-估值数据")\
            .with_optional_params("symbol", "indicator", "period")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator", "period"]))\
            .with_return_type("DataFrame")\
            .with_keywords("A股", "zh", "baidu", "stock", "股票")\
            .with_example_params({"symbol": '002044', "indicator": '总市值', "period": 'daily'})\
            .build(),

        create_interface("stock_zh_vote_baidu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("百度股市通- A 股或指数-股评-投票")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("vote", "zh", "baidu", "stock", "股票")\
            .with_example_params({"symbol": '000001', "indicator": '指数'})\
            .build(),

        create_interface("stock_zt_pool_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-行情中心-涨停板行情-涨停股池")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "pool", "zt")\
            .with_example_params({"date": '20241008'})\
            .build(),

        create_interface("stock_zt_pool_previous_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-行情中心-涨停板行情-昨日涨停股池")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("pool", "zt", "em", "previous", "stock")\
            .with_example_params({"date": '20240415'})\
            .build(),

        create_interface("stock_zt_pool_strong_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-行情中心-涨停板行情-强势股池")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("strong", "pool", "zt", "em", "stock")\
            .with_example_params({"date": '20241231'})\
            .build(),

        create_interface("stock_zt_pool_sub_new_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-行情中心-涨停板行情-次新股池")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("pool", "zt", "sub", "em", "new")\
            .with_example_params({"date": '20241231'})\
            .build(),

        create_interface("stock_zygc_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("东方财富网-个股-主营构成")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "em", "zygc")\
            .with_example_params({"symbol": 'SH688041'})\
            .build(),

        create_interface("stock_zyjs_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.OTHER)\
            .with_description("同花顺-主营介绍")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "zyjs", "ths")\
            .with_example_params({"symbol": '000066'})\
            .build(),
        ]

    def _register_stock_financial_interfaces(self) -> List[InterfaceMetadata]:
        """注册STOCK_FINANCIAL接口"""
        return [
        create_interface("stock_balance_sheet_by_report_delisted_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-资产负债表-已退市股票-按报告期")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("List[str]")\
            .with_keywords("delisted", "sheet", "em", "stock", "股票")\
            .with_example_params({"symbol": 'SZ000013'})\
            .build(),

        create_interface("stock_balance_sheet_by_report_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-资产负债表-按报告期")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("sheet", "em", "stock", "股票", "balance")\
            .with_example_params({"symbol": 'SH600519'})\
            .build(),

        create_interface("stock_balance_sheet_by_yearly_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-资产负债表-按年度")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("sheet", "em", "stock", "yearly", "股票")\
            .with_example_params({"symbol": 'SH600036'})\
            .build(),

        create_interface("stock_cash_flow_sheet_by_quarterly_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-现金流量表-按单季度")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("flow", "sheet", "em", "stock", "股票")\
            .with_example_params({"symbol": 'SH600519'})\
            .build(),

        create_interface("stock_cash_flow_sheet_by_report_delisted_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-现金流量表-已退市股票-按报告期")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("List[str]")\
            .with_keywords("flow", "delisted", "sheet", "em", "stock")\
            .with_example_params({"symbol": 'SZ000013'})\
            .build(),

        create_interface("stock_cash_flow_sheet_by_report_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-现金流量表-按报告期")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("flow", "sheet", "em", "stock", "股票")\
            .with_example_params({"symbol": 'SH600519'})\
            .build(),

        create_interface("stock_cash_flow_sheet_by_yearly_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-现金流量表-按年度")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("flow", "sheet", "em", "stock", "yearly")\
            .with_example_params({"symbol": 'SH600519'})\
            .build(),

        create_interface("stock_financial_abstract")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("新浪财经-财务报表-关键指标")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "financial", "财务", "abstract")\
            .with_example_params({"symbol": '600004'})\
            .build(),

        create_interface("stock_financial_abstract_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("同花顺-财务指标-主要指标")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("财务", "stock", "股票", "financial", "abstract")\
            .with_example_params({"symbol": '000063', "indicator": '按报告期'})\
            .build(),

        create_interface("stock_financial_benefit_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("同花顺-财务指标-利润表")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "financial", "财务", "benefit")\
            .with_example_params({"symbol": '000063', "indicator": '按报告期'})\
            .build(),

        create_interface("stock_financial_cash_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("同花顺-财务指标-现金流量表")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "financial", "财务", "cash")\
            .with_example_params({"symbol": '000063', "indicator": '按报告期'})\
            .build(),

        create_interface("stock_financial_debt_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("同花顺-财务指标-资产负债表")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "debt", "financial", "财务")\
            .with_example_params({"symbol": '000063', "indicator": '按报告期'})\
            .build(),

        create_interface("stock_financial_hk_report_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-港股-财务报表-三大报表")\
            .with_optional_params("stock", "symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["stock", "symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("hk", "em", "stock", "股票", "financial")\
            .with_example_params({"stock": '00700', "symbol": '资产负债表', "indicator": '年度'})\
            .build(),

        create_interface("stock_financial_report_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("新浪财经-财务报表-三大报表")\
            .with_optional_params("stock", "symbol")\
            .with_pattern(ParameterPattern.from_params(["stock", "symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "financial", "财务", "report")\
            .with_example_params({"stock": 'sh600600', "symbol": '资产负债表'})\
            .build(),

        create_interface("stock_financial_us_report_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-美股-财务分析-三大报表")\
            .with_optional_params("stock", "symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["stock", "symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "us", "stock", "股票", "financial")\
            .with_example_params({"stock": 'TSLA', "symbol": '资产负债表', "indicator": '年报'})\
            .build(),

        create_interface("stock_hk_profit_forecast_et")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("经济通-公司资料-盈利预测")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("hk", "forecast", "stock", "股票", "profit")\
            .with_example_params({"symbol": '09999', "indicator": '盈利预测概览'})\
            .build(),

        create_interface("stock_profit_forecast_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富网-数据中心-研究报告-盈利预测")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "em", "forecast", "stock", "profit")\
            .with_example_params({"symbol": '000001'})\
            .build(),

        create_interface("stock_profit_forecast_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("同花顺-盈利预测")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("forecast", "stock", "股票", "profit", "ths")\
            .with_example_params({"symbol": '600519', "indicator": '预测年报每股收益'})\
            .build(),

        create_interface("stock_profit_sheet_by_quarterly_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-利润表-按单季度")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("sheet", "em", "stock", "股票", "profit")\
            .with_example_params({"symbol": 'SH600519'})\
            .build(),

        create_interface("stock_profit_sheet_by_report_delisted_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-利润表-已退市股票-按报告期")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("List[str]")\
            .with_keywords("delisted", "sheet", "em", "stock", "股票")\
            .with_example_params({"symbol": 'SZ000013'})\
            .build(),

        create_interface("stock_profit_sheet_by_report_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-利润表-报告期")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("sheet", "em", "stock", "股票", "profit")\
            .with_example_params({"symbol": 'SH600519'})\
            .build(),

        create_interface("stock_profit_sheet_by_yearly_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_FINANCIAL)\
            .with_description("东方财富-股票-财务分析-利润表-按年度")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("sheet", "em", "stock", "yearly", "股票")\
            .with_example_params({"symbol": 'SH600519'})\
            .build(),
        ]

    def _register_stock_quote_interfaces(self) -> List[InterfaceMetadata]:
        """注册STOCK_QUOTE接口"""
        return [
        create_interface("stock_bj_a_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-京 A 股-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "a", "em", "bj", "stock")\
            .build(),

        create_interface("stock_board_concept_hist_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-沪深板块-概念板块-历史行情")\
            .with_optional_params("symbol", "period", "start_date", "end_date", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period", "start_date", "end_date", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("board", "hist", "em", "stock", "concept")\
            .with_example_params({"symbol": '绿色电力', "period": 'daily', "start_date": '20220101', "end_date": '20221128', "adjust": ''})\
            .build(),

        create_interface("stock_board_concept_hist_min_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-沪深板块-概念板块-分时历史行情")\
            .with_optional_params("symbol", "period")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period"]))\
            .with_return_type("DataFrame")\
            .with_keywords("board", "hist", "em", "stock", "min")\
            .with_example_params({"symbol": '长寿药', "period": '5'})\
            .build(),

        create_interface("stock_board_concept_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情中心-沪深京板块-概念板块-实时行情")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "board", "em", "stock", "concept")\
            .with_example_params({"symbol": '可燃冰'})\
            .build(),

        create_interface("stock_board_industry_hist_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-沪深板块-行业板块-历史行情")\
            .with_optional_params("symbol", "start_date", "end_date", "period", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date", "period", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "board", "hist", "em", "stock")\
            .with_example_params({"symbol": '小金属', "start_date": '20211201', "end_date": '20220401', "period": 'daily', "adjust": ''})\
            .build(),

        create_interface("stock_board_industry_hist_min_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-沪深板块-行业板块-分时历史行情")\
            .with_optional_params("symbol", "period")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "board", "hist", "em", "stock")\
            .with_example_params({"symbol": '小金属', "period": '5'})\
            .build(),

        create_interface("stock_board_industry_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-沪深板块-行业板块-实时行情")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "spot", "board", "em", "stock")\
            .with_example_params({"symbol": '小金属'})\
            .build(),

        create_interface("stock_comment_detail_scrd_desire_daily_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-特色数据-千股千评-市场热度-日度市场参与意愿")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("daily", "em", "scrd", "stock", "股票")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_concept_fund_flow_hist")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-资金流向-概念资金流-概念历史资金流")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("flow", "fund", "hist", "stock", "concept")\
            .with_example_params({"symbol": '数据要素'})\
            .build(),

        create_interface("stock_cy_a_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-创业板-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "a", "em", "stock", "cy")\
            .build(),

        create_interface("stock_history_dividend")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-发行与分配-历史分红")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "history", "股票", "dividend")\
            .build(),

        create_interface("stock_history_dividend_detail")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-发行与分配-分红配股详情")\
            .with_optional_params("symbol", "indicator", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("history", "stock", "股票", "detail", "dividend")\
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

        create_interface("stock_hk_famous_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情中心-港股市场-知名港股")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "famous", "hk", "em", "stock")\
            .build(),

        create_interface("stock_hk_hist")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情-港股-每日行情")\
            .with_optional_params("symbol", "period", "start_date", "end_date", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period", "start_date", "end_date", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hist", "hk")\
            .with_example_params({"symbol": '00593', "period": 'daily', "start_date": '19700101', "end_date": '22220101', "adjust": ''})\
            .build(),

        create_interface("stock_hk_hist_min_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情-港股-每日分时行情")\
            .with_optional_params("symbol", "period", "adjust", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period", "adjust", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("hist", "hk", "em", "stock", "股票")\
            .with_example_params({"symbol": '01611', "period": '1', "adjust": '', "start_date": '2024-01-01', "end_date": '2024-01-31'})\
            .build(),

        create_interface("stock_hk_index_daily_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-港股-股票指数数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("daily", "hk", "em", "stock", "股票")\
            .with_example_params({"symbol": 'HSTECF2L'})\
            .build(),

        create_interface("stock_hk_index_daily_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-港股指数-历史行情数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("daily", "hk", "stock", "index", "指数")\
            .with_example_params({"symbol": 'CES100'})\
            .build(),

        create_interface("stock_hk_index_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情中心-港股-指数实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "hk", "em", "stock", "index")\
            .build(),

        create_interface("stock_hk_index_spot_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-行情中心-港股指数")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "hk", "stock", "index", "指数")\
            .build(),

        create_interface("stock_hk_main_board_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-港股-主板-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "board", "hk", "em", "stock")\
            .build(),

        create_interface("stock_hk_spot")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-港股的所有港股的实时行情数据")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hk", "spot")\
            .build(),

        create_interface("stock_hk_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-港股-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hk", "em", "spot")\
            .build(),

        create_interface("stock_hsgt_hist_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-资金流向-沪深港通资金流向-沪深港通历史数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hist", "em", "hsgt")\
            .with_example_params({"symbol": '北向资金'})\
            .build(),

        create_interface("stock_hsgt_sh_hk_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情中心-沪深港通-港股通(沪>港)-股票")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "hk", "em", "stock", "股票")\
            .build(),

        create_interface("stock_industry_clf_hist_sw")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("申万宏源研究-行业分类-全部行业分类")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "hist", "stock", "industry", "clf")\
            .build(),

        create_interface("stock_kc_a_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-科创板-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "a", "kc", "em", "stock")\
            .build(),

        create_interface("stock_lhb_detail_daily_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("龙虎榜-每日详情")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("daily", "lhb", "stock", "detail", "sina")\
            .with_example_params({"date": '20240222'})\
            .build(),

        create_interface("stock_new_a_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-新股-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "a", "em", "new", "stock")\
            .build(),

        create_interface("stock_sector_fund_flow_hist")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-数据中心-资金流向-行业资金流-行业历史资金流")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "sector", "flow", "fund", "hist")\
            .with_example_params({"symbol": '汽车服务'})\
            .build(),

        create_interface("stock_sector_spot")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪行业-板块行情")\
            .with_optional_params("indicator")\
            .with_pattern(ParameterPattern.from_params(["indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "sector", "行业", "spot")\
            .with_example_params({"indicator": '新浪行业'})\
            .build(),

        create_interface("stock_sh_a_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-沪 A 股-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "a", "em", "stock", "sh")\
            .build(),

        create_interface("stock_sse_deal_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("上海证券交易所-数据-股票数据-成交概况-股票成交概况-每日股票情况")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("sse", "daily", "stock", "股票", "deal")\
            .with_example_params({"date": '20241216'})\
            .build(),

        create_interface("stock_sz_a_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-深 A 股-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "a", "sz", "em", "stock")\
            .build(),

        create_interface("stock_us_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-美股")\
            .with_optional_params("symbol", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "daily", "股票", "us")\
            .with_example_params({"symbol": 'FB', "adjust": ''})\
            .build(),

        create_interface("stock_us_famous_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情中心-美股市场-知名美股")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "famous", "em", "us", "stock")\
            .with_example_params({"symbol": '科技类'})\
            .build(),

        create_interface("stock_us_hist")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情-美股-每日行情")\
            .with_optional_params("symbol", "period", "start_date", "end_date", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period", "start_date", "end_date", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hist", "股票", "us")\
            .with_example_params({"symbol": '105.MSFT', "period": 'daily', "start_date": '19700101', "end_date": '22220101', "adjust": ''})\
            .build(),

        create_interface("stock_us_hist_min_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情首页-美股-每日分时行情")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("hist", "em", "us", "stock", "股票")\
            .with_example_params({"symbol": '105.ATER', "start_date": '2024-01-01', "end_date": '2024-01-31'})\
            .build(),

        create_interface("stock_us_pink_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情中心-美股市场-粉单市场")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("pink", "spot", "em", "us", "stock")\
            .build(),

        create_interface("stock_us_spot")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-所有美股的数据, 注意延迟 15 分钟")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "股票", "us", "spot")\
            .build(),

        create_interface("stock_us_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-美股-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "em", "us", "spot")\
            .build(),

        create_interface("stock_zh_a_cdr_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-A股-CDR个股的历史行情数据, 大量抓取容易封 IP")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("cdr", "A股", "a", "daily", "zh")\
            .with_example_params({"symbol": 'sh689009', "start_date": '19900101', "end_date": '22201116'})\
            .build(),

        create_interface("stock_zh_a_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-A 股-个股的历史行情数据, 大量抓取容易封 IP")\
            .with_optional_params("symbol", "start_date", "end_date", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "daily", "zh", "a")\
            .with_example_params({"symbol": 'sh603843', "start_date": '19900101', "end_date": '21000118', "adjust": ''})\
            .build(),

        create_interface("stock_zh_a_hist")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情首页-沪深京 A 股-每日行情")\
            .with_optional_params("symbol", "period", "start_date", "end_date", "adjust", "timeout")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period", "start_date", "end_date", "adjust", "timeout"]))\
            .with_return_type("DataFrame")\
            .with_keywords("a", "hist", "zh", "stock", "股票")\
            .with_example_params({"symbol": '000001', "period": 'daily', "start_date": '19700101', "end_date": '20500101', "adjust": ''})\
            .build(),

        create_interface("stock_zh_a_hist_min_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情首页-沪深京 A 股-每日分时行情")\
            .with_optional_params("symbol", "start_date", "end_date", "period", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date", "period", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("a", "hist", "zh", "em", "stock")\
            .with_example_params({"symbol": '000001', "start_date": '2024-01-01', "end_date": '2024-01-31', "period": '5', "adjust": ''})\
            .build(),

        create_interface("stock_zh_a_hist_pre_min_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情首页-沪深京 A 股-每日分时行情包含盘前数据")\
            .with_optional_params("symbol", "start_time", "end_time")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_time", "end_time"]))\
            .with_return_type("DataFrame")\
            .with_keywords("a", "hist", "zh", "em", "pre")\
            .with_example_params({"symbol": '000001', "start_time": '09:00:00', "end_time": '15:50:00'})\
            .build(),

        create_interface("stock_zh_a_hist_tx")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("腾讯证券-日频-股票历史数据")\
            .with_optional_params("symbol", "start_date", "end_date", "adjust", "timeout")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date", "adjust", "timeout"]))\
            .with_return_type("DataFrame")\
            .with_keywords("a", "hist", "zh", "stock", "股票")\
            .with_example_params({"symbol": 'sz000001', "start_date": '19000101', "end_date": '20500101', "adjust": ''})\
            .build(),

        create_interface("stock_zh_a_minute")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("股票及股票指数历史行情数据-分钟数据")\
            .with_optional_params("symbol", "period", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("a", "zh", "stock", "股票", "minute")\
            .with_example_params({"symbol": 'sh600519', "period": '1', "adjust": ''})\
            .build(),

        create_interface("stock_zh_a_spot")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-所有 A 股的实时行情数据; 重复运行本函数会被新浪暂时封 IP")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "a", "zh", "stock", "股票")\
            .build(),

        create_interface("stock_zh_a_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-沪深京 A 股-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "a", "em", "zh", "stock")\
            .build(),

        create_interface("stock_zh_a_spot_em_async")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-沪深京 A 股-实时行情 (同步接口)")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "a", "em", "zh", "stock")\
            .build(),

        create_interface("stock_zh_ah_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("腾讯财经-港股-AH-股票历史行情")\
            .with_optional_params("symbol", "start_year", "end_year", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_year", "end_year", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("daily", "zh", "stock", "股票", "ah")\
            .with_example_params({"symbol": '02318', "start_year": '2000', "end_year": '2019', "adjust": ''})\
            .build(),

        create_interface("stock_zh_ah_spot")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("腾讯财经-港股-AH-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "ah", "zh", "spot")\
            .build(),

        create_interface("stock_zh_ah_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情中心-沪深港通-AH股比价-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "em", "zh", "stock", "ah")\
            .build(),

        create_interface("stock_zh_b_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-B 股-个股的历史行情数据, 大量抓取容易封 IP")\
            .with_optional_params("symbol", "start_date", "end_date", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "b", "zh", "daily")\
            .with_example_params({"symbol": 'sh900901', "start_date": '19900101', "end_date": '21000118', "adjust": ''})\
            .build(),

        create_interface("stock_zh_b_minute")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("股票及股票指数历史行情数据-分钟数据")\
            .with_optional_params("symbol", "period", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "period", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("zh", "stock", "b", "股票", "minute")\
            .with_example_params({"symbol": 'sh900901', "period": '1', "adjust": ''})\
            .build(),

        create_interface("stock_zh_b_spot")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-所有 B 股的实时行情数据; 重复运行本函数会被新浪暂时封 IP")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "zh", "stock", "b", "股票")\
            .build(),

        create_interface("stock_zh_b_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网- B 股-实时行情")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "em", "zh", "stock", "b")\
            .build(),

        create_interface("stock_zh_index_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-指数-历史行情数据, 大量抓取容易封 IP")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("daily", "zh", "stock", "index", "指数")\
            .with_example_params({"symbol": 'sh000922'})\
            .build(),

        create_interface("stock_zh_index_daily_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-股票指数数据")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("daily", "zh", "em", "stock", "股票")\
            .with_example_params({"symbol": 'csi931151', "start_date": '19900101', "end_date": '20500101'})\
            .build(),

        create_interface("stock_zh_index_daily_tx")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("腾讯证券-日频-股票或者指数历史数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("daily", "zh", "stock", "股票", "index")\
            .with_example_params({"symbol": 'sz980017'})\
            .build(),

        create_interface("stock_zh_index_hist_csindex")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("中证指数-具体指数-历史行情数据")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("csindex", "hist", "zh", "stock", "index")\
            .with_example_params({"symbol": '000928', "start_date": '20180526', "end_date": '20240604'})\
            .build(),

        create_interface("stock_zh_index_spot_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("东方财富网-行情中心-沪深京指数")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("spot", "em", "zh", "stock", "index")\
            .with_example_params({"symbol": '上证系列指数'})\
            .build(),

        create_interface("stock_zh_index_spot_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-行情中心首页-A股-分类-所有指数")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("A股", "spot", "zh", "stock", "index")\
            .build(),

        create_interface("stock_zh_kcb_daily")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-科创板股票的历史行情数据, 大量抓取容易封IP")\
            .with_optional_params("symbol", "adjust")\
            .with_pattern(ParameterPattern.from_params(["symbol", "adjust"]))\
            .with_return_type("DataFrame")\
            .with_keywords("daily", "zh", "stock", "kcb", "股票")\
            .with_example_params({"symbol": 'sh688399', "adjust": ''})\
            .build(),

        create_interface("stock_zh_kcb_spot")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_QUOTE)\
            .with_description("新浪财经-科创板实时行情数据, 大量抓取容易封IP")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "kcb", "zh", "spot")\
            .build(),
        ]

    def _register_market_index_interfaces(self) -> List[InterfaceMetadata]:
        """注册MARKET_INDEX接口"""
        return [
        create_interface("stock_board_concept_index_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.MARKET_INDEX)\
            .with_description("同花顺-板块-概念板块-指数数据")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("board", "stock", "index", "指数", "ths")\
            .with_example_params({"symbol": '阿里巴巴概念', "start_date": '20200101', "end_date": '20250228'})\
            .build(),

        create_interface("stock_board_industry_index_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.MARKET_INDEX)\
            .with_description("同花顺-板块-行业板块-指数数据")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "board", "stock", "industry", "index")\
            .with_example_params({"symbol": '元件', "start_date": '20200101', "end_date": '20240108'})\
            .build(),

        create_interface("stock_buffett_index_lg")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.MARKET_INDEX)\
            .with_description("乐估乐股-底部研究-巴菲特指标")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "index", "lg", "buffett")\
            .build(),

        create_interface("stock_index_pb_lg")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.MARKET_INDEX)\
            .with_description("乐咕乐股-指数市净率")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("pb", "stock", "index", "lg", "指数")\
            .with_example_params({"symbol": '上证50'})\
            .build(),

        create_interface("stock_index_pe_lg")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.MARKET_INDEX)\
            .with_description("乐咕乐股-指数市盈率")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "index", "lg", "pe", "指数")\
            .with_example_params({"symbol": '沪深300'})\
            .build(),
        ]

    def _register_stock_basic_interfaces(self) -> List[InterfaceMetadata]:
        """注册STOCK_BASIC接口"""
        return [
        create_interface("stock_board_concept_info_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-板块-概念板块-板块简介")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("board", "stock", "info", "ths", "concept")\
            .with_example_params({"symbol": '阿里巴巴概念'})\
            .build(),

        create_interface("stock_board_industry_info_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺-板块-行业板块-板块简介")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "board", "stock", "industry", "info")\
            .with_example_params({"symbol": '半导体'})\
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

        create_interface("stock_info_a_code_name")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("沪深京 A 股列表")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("List[str]")\
            .with_keywords("name", "a", "stock", "code", "info")\
            .build(),

        create_interface("stock_info_bj_name_code")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("北京证券交易所-股票列表")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("List[str]")\
            .with_keywords("name", "bj", "stock", "code", "股票")\
            .build(),

        create_interface("stock_info_change_name")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("新浪财经-股票曾用名")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("name", "change", "stock", "股票", "info")\
            .with_example_params({"symbol": '000503'})\
            .build(),

        create_interface("stock_info_cjzc_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富-财经早餐")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "info", "em", "cjzc")\
            .build(),

        create_interface("stock_info_global_cls")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("财联社-电报")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "info", "global", "cls")\
            .with_example_params({"symbol": '全部'})\
            .build(),

        create_interface("stock_info_global_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("东方财富-全球财经快讯")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "info", "global", "em")\
            .build(),

        create_interface("stock_info_global_futu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("富途牛牛-快讯")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "info", "global", "futu")\
            .build(),

        create_interface("stock_info_global_sina")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("新浪财经-全球财经快讯")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "info", "global", "sina")\
            .build(),

        create_interface("stock_info_global_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("同花顺财经-全球财经直播")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "info", "global", "ths")\
            .build(),

        create_interface("stock_info_sh_delist")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("上海证券交易所-终止上市公司")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("List[str]")\
            .with_keywords("stock", "info", "sh", "delist")\
            .with_example_params({"symbol": '全部'})\
            .build(),

        create_interface("stock_info_sh_name_code")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("上海证券交易所-股票列表")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("List[str]")\
            .with_keywords("name", "A股", "B股", "stock", "code")\
            .with_example_params({"symbol": '主板A股'})\
            .build(),

        create_interface("stock_info_sz_change_name")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("深证证券交易所-市场数据-股票数据-名称变更")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("name", "sz", "change", "stock", "股票")\
            .with_example_params({"symbol": '全称变更'})\
            .build(),

        create_interface("stock_info_sz_delist")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("深证证券交易所-暂停上市公司-终止上市公司")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("List[str]")\
            .with_keywords("stock", "info", "delist", "sz")\
            .with_example_params({"symbol": '终止上市公司'})\
            .build(),

        create_interface("stock_info_sz_name_code")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("深圳证券交易所-股票列表")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("List[str]")\
            .with_keywords("name", "A股", "sz", "B股", "stock")\
            .with_example_params({"symbol": 'A股列表'})\
            .build(),

        create_interface("stock_margin_underlying_info_szse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_BASIC)\
            .with_description("深圳证券交易所-融资融券数据-标的证券信息")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("underlying", "szse", "margin", "stock", "info")\
            .with_example_params({"date": '20221129'})\
            .build(),
        ]

    def _register_industry_data_interfaces(self) -> List[InterfaceMetadata]:
        """注册INDUSTRY_DATA接口"""
        return [
        create_interface("stock_board_industry_cons_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.INDUSTRY_DATA)\
            .with_description("东方财富网-沪深板块-行业板块-板块成份")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "cons", "board", "em", "stock")\
            .with_example_params({"symbol": '小金属'})\
            .build(),

        create_interface("stock_board_industry_name_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.INDUSTRY_DATA)\
            .with_description("东方财富网-沪深板块-行业板块-名称")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "name", "board", "em", "stock")\
            .build(),

        create_interface("stock_board_industry_name_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.INDUSTRY_DATA)\
            .with_description("同花顺-板块-行业板块-行业")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "name", "board", "stock", "industry")\
            .build(),

        create_interface("stock_board_industry_summary_ths")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.INDUSTRY_DATA)\
            .with_description("同花顺-数据中心-行业板块-同花顺行业一览表")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "summary", "board", "stock", "industry")\
            .build(),

        create_interface("stock_gpzy_industry_data_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.INDUSTRY_DATA)\
            .with_description("东方财富网-数据中心-特色数据-股权质押-上市公司质押比例-行业数据")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "gpzy", "data", "em", "stock")\
            .build(),

        create_interface("stock_industry_category_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.INDUSTRY_DATA)\
            .with_description("巨潮资讯-行业分类数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "stock", "industry", "cninfo", "category")\
            .with_example_params({"symbol": '巨潮行业分类标准'})\
            .build(),

        create_interface("stock_industry_change_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.INDUSTRY_DATA)\
            .with_description("巨潮资讯-上市公司行业归属的变动情况")\
            .with_optional_params("symbol", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "change", "stock", "股票", "industry")\
            .with_example_params({"symbol": '002594', "start_date": '20091227', "end_date": '20220713'})\
            .build(),

        create_interface("stock_news_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.INDUSTRY_DATA)\
            .with_description("东方财富-个股新闻-最近 100 条新闻")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("news", "新闻", "em", "stock", "股票")\
            .with_example_params({"symbol": '603777'})\
            .build(),

        create_interface("stock_news_main_cx")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.INDUSTRY_DATA)\
            .with_description("财新网-财新数据通")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "news", "main", "cx")\
            .build(),

        create_interface("stock_report_disclosure")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.INDUSTRY_DATA)\
            .with_description("巨潮资讯-首页-数据-预约披露")\
            .with_optional_params("market", "period")\
            .with_pattern(ParameterPattern.from_params(["market", "period"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "report", "disclosure")\
            .with_example_params({"market": '沪深京', "period": 'daily'})\
            .build(),

        create_interface("stock_research_report_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.INDUSTRY_DATA)\
            .with_description("东方财富网-数据中心-研究报告-个股研报")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "research", "em", "report")\
            .with_example_params({"symbol": '000001'})\
            .build(),

        create_interface("stock_zh_a_disclosure_report_cninfo")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.INDUSTRY_DATA)\
            .with_description("巨潮资讯-首页-公告查询-信息披露公告")\
            .with_optional_params("symbol", "market", "keyword", "category", "start_date", "end_date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "market", "keyword", "category", "start_date", "end_date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("a", "zh", "disclosure", "基金", "stock")\
            .with_example_params({"symbol": '000001', "market": '沪深京', "keyword": '', "category": '', "start_date": '20230618', "end_date": '20231219'})\
            .build(),

        create_interface("stock_zh_kcb_report_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.INDUSTRY_DATA)\
            .with_description("科创板报告内容")\
            .with_optional_params("from_page", "to_page")\
            .with_pattern(ParameterPattern.from_params(["from_page", "to_page"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "zh", "stock", "kcb", "report")\
            .with_example_params({"from_page": 1, "to_page": 100})\
            .build(),
        ]

    def _register_market_overview_interfaces(self) -> List[InterfaceMetadata]:
        """注册MARKET_OVERVIEW接口"""
        return [
        create_interface("stock_comment_detail_scrd_desire_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.MARKET_OVERVIEW)\
            .with_description("东方财富网-数据中心-特色数据-千股千评-市场热度-市场参与意愿")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "scrd", "stock", "股票", "desire")\
            .with_example_params({"symbol": '600000'})\
            .build(),

        create_interface("stock_comment_detail_scrd_focus_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.MARKET_OVERVIEW)\
            .with_description("东方财富网-数据中心-特色数据-千股千评-市场热度-用户关注指数")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("em", "scrd", "stock", "股票", "detail")\
            .with_example_params({"symbol": '600000'})\
            .build(),
        ]

    def _register_stock_technical_interfaces(self) -> List[InterfaceMetadata]:
        """注册STOCK_TECHNICAL接口"""
        return [
        create_interface("stock_financial_analysis_indicator")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("新浪财经-财务分析-财务指标")\
            .with_optional_params("symbol", "start_year")\
            .with_pattern(ParameterPattern.from_params(["symbol", "start_year"]))\
            .with_return_type("DataFrame")\
            .with_keywords("indicator", "stock", "股票", "financial", "财务")\
            .with_example_params({"symbol": '600004', "start_year": '1900'})\
            .build(),

        create_interface("stock_financial_analysis_indicator_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("东方财富-A股-财务分析-主要指标")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("indicator", "A股", "em", "stock", "股票")\
            .with_example_params({"symbol": '301389.SZ', "indicator": '按报告期'})\
            .build(),

        create_interface("stock_financial_hk_analysis_indicator_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("东方财富-港股-财务分析-主要指标")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("indicator", "hk", "em", "stock", "股票")\
            .with_example_params({"symbol": '00853', "indicator": '年度'})\
            .build(),

        create_interface("stock_financial_us_analysis_indicator_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("东方财富-美股-财务分析-主要指标")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("indicator", "em", "us", "stock", "股票")\
            .with_example_params({"symbol": 'TSLA', "indicator": '年报'})\
            .build(),

        create_interface("stock_hk_indicator_eniu")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.STOCK_TECHNICAL)\
            .with_description("亿牛网-港股指标")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "hk", "indicator", "eniu")\
            .with_example_params({"symbol": 'hk01093', "indicator": '市盈率'})\
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
            .with_keywords("flow", "fund", "stock", "big", "deal")\
            .build(),

        create_interface("stock_fund_flow_individual")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("同花顺-数据中心-资金流向-个股资金流")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "individual", "flow", "fund")\
            .with_example_params({"symbol": '即时'})\
            .build(),

        create_interface("stock_fund_flow_industry")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("同花顺-数据中心-资金流向-行业资金流")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "flow", "fund", "stock", "industry")\
            .with_example_params({"symbol": '即时'})\
            .build(),

        create_interface("stock_fund_stock_holder")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("新浪财经-股本股东-基金持股")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("holder", "fund", "基金", "stock", "股票")\
            .with_example_params({"symbol": '600004'})\
            .build(),

        create_interface("stock_hsgt_fund_flow_summary_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("东方财富网-数据中心-资金流向-沪深港通资金流向")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("flow", "fund", "summary", "em", "stock")\
            .build(),

        create_interface("stock_hsgt_fund_min_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("东方财富-数据中心-沪深港通-市场概括-分时数据")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("fund", "em", "stock", "min", "hsgt")\
            .with_example_params({"symbol": '北向资金'})\
            .build(),

        create_interface("stock_individual_fund_flow")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("东方财富网-数据中心-资金流向-个股")\
            .with_optional_params("stock", "market")\
            .with_pattern(ParameterPattern.from_params(["stock", "market"]))\
            .with_return_type("DataFrame")\
            .with_keywords("flow", "fund", "individual", "stock", "股票")\
            .with_example_params({"stock": '600094', "market": 'sh'})\
            .build(),

        create_interface("stock_individual_fund_flow_rank")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("东方财富网-数据中心-资金流向-排名")\
            .with_optional_params("indicator")\
            .with_pattern(ParameterPattern.from_params(["indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("flow", "fund", "individual", "stock", "rank")\
            .with_example_params({"indicator": '5日'})\
            .build(),

        create_interface("stock_individual_fund_flow_rank_async")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("东方财富网-数据中心-资金流向-排名 (同步接口)")\
            .with_optional_params("indicator")\
            .with_pattern(ParameterPattern.from_params(["indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("flow", "fund", "individual", "stock", "async")\
            .with_example_params({"indicator": '5日'})\
            .build(),

        create_interface("stock_main_fund_flow")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("东方财富网-数据中心-资金流向-主力净流入排名")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("A股", "flow", "fund", "B股", "stock")\
            .with_example_params({"symbol": '全部股票'})\
            .build(),

        create_interface("stock_market_fund_flow")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("东方财富网-数据中心-资金流向-大盘")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("stock", "market", "flow", "fund")\
            .build(),

        create_interface("stock_report_fund_hold")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("东方财富网-数据中心-主力数据-基金持仓")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("hold", "fund", "基金", "stock", "report")\
            .with_example_params({"symbol": '基金持仓', "date": '20210331'})\
            .build(),

        create_interface("stock_report_fund_hold_detail")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("东方财富网-数据中心-主力数据-基金持仓-明细")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("hold", "fund", "基金", "stock", "detail")\
            .with_example_params({"symbol": '008286', "date": '20220331'})\
            .build(),

        create_interface("stock_sector_fund_flow_rank")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("东方财富网-数据中心-资金流向-板块资金流-排名")\
            .with_optional_params("indicator", "sector_type")\
            .with_pattern(ParameterPattern.from_params(["indicator", "sector_type"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "sector", "flow", "fund", "stock")\
            .with_example_params({"indicator": '今日', "sector_type": '行业资金流'})\
            .build(),

        create_interface("stock_sector_fund_flow_summary")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FUND_DATA)\
            .with_description("东方财富网-数据中心-资金流向-行业资金流-xx行业个股资金流")\
            .with_optional_params("symbol", "indicator")\
            .with_pattern(ParameterPattern.from_params(["symbol", "indicator"]))\
            .with_return_type("DataFrame")\
            .with_keywords("行业", "sector", "flow", "fund", "summary")\
            .with_example_params({"symbol": '电源设备', "indicator": '今日'})\
            .build(),
        ]

    def _register_forex_data_interfaces(self) -> List[InterfaceMetadata]:
        """注册FOREX_DATA接口"""
        return [
        create_interface("stock_gdfx_free_holding_analyse_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("东方财富网-数据中心-股东分析-股东持股分析-十大流通股东")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gdfx", "analyse", "em", "stock", "holding")\
            .with_example_params({"date": '20230930'})\
            .build(),

        create_interface("stock_gdfx_free_holding_change_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("东方财富网-数据中心-股东分析-股东持股变动统计-十大流通股东")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gdfx", "change", "em", "stock", "holding")\
            .with_example_params({"date": '20210930'})\
            .build(),

        create_interface("stock_gdfx_free_holding_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("东方财富网-数据中心-股东分析-股东持股明细-十大流通股东")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gdfx", "em", "stock", "holding", "free")\
            .with_example_params({"date": '20210930'})\
            .build(),

        create_interface("stock_gdfx_free_holding_statistics_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("东方财富网-数据中心-股东分析-股东持股统计-十大流通股东")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gdfx", "statistics", "em", "stock", "holding")\
            .with_example_params({"date": '20210630'})\
            .build(),

        create_interface("stock_gdfx_free_holding_teamwork_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("东方财富网-数据中心-股东分析-股东协同-十大流通股东")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gdfx", "em", "teamwork", "基金", "stock")\
            .with_example_params({"symbol": '社保'})\
            .build(),

        create_interface("stock_gdfx_free_top_10_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("东方财富网-个股-十大流通股东")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gdfx", "10", "top", "em", "stock")\
            .with_example_params({"symbol": 'sh688686', "date": '20240930'})\
            .build(),

        create_interface("stock_gdfx_holding_analyse_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("东方财富网-数据中心-股东分析-股东持股分析-十大股东")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gdfx", "analyse", "em", "stock", "holding")\
            .with_example_params({"date": '20230331'})\
            .build(),

        create_interface("stock_gdfx_holding_change_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("东方财富网-数据中心-股东分析-股东持股变动统计-十大股东")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gdfx", "change", "em", "stock", "holding")\
            .with_example_params({"date": '20210930'})\
            .build(),

        create_interface("stock_gdfx_holding_detail_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("东方财富网-数据中心-股东分析-股东持股明细-十大股东")\
            .with_optional_params("date", "indicator", "symbol")\
            .with_pattern(ParameterPattern.from_params(["date", "indicator", "symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gdfx", "em", "基金", "stock", "holding")\
            .with_example_params({"date": '20230331', "indicator": '个人', "symbol": '新进'})\
            .build(),

        create_interface("stock_gdfx_holding_statistics_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("东方财富网-数据中心-股东分析-股东持股统计-十大股东")\
            .with_optional_params("date")\
            .with_pattern(ParameterPattern.from_params(["date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gdfx", "em", "statistics", "stock", "holding")\
            .with_example_params({"date": '20210930'})\
            .build(),

        create_interface("stock_gdfx_holding_teamwork_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("东方财富网-数据中心-股东分析-股东协同-十大股东")\
            .with_optional_params("symbol")\
            .with_pattern(ParameterPattern.from_params(["symbol"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gdfx", "em", "teamwork", "基金", "stock")\
            .with_example_params({"symbol": '社保'})\
            .build(),

        create_interface("stock_gdfx_top_10_em")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("东方财富网-个股-十大股东")\
            .with_optional_params("symbol", "date")\
            .with_pattern(ParameterPattern.from_params(["symbol", "date"]))\
            .with_return_type("DataFrame")\
            .with_keywords("gdfx", "10", "top", "em", "stock")\
            .with_example_params({"symbol": 'sh688686', "date": '20210630'})\
            .build(),

        create_interface("stock_sgt_reference_exchange_rate_sse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("沪港通-港股通信息披露-参考汇率")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("reference", "sse", "stock", "sgt", "rate")\
            .build(),

        create_interface("stock_sgt_reference_exchange_rate_szse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("深港通-港股通业务信息-参考汇率")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("reference", "szse", "stock", "sgt", "rate")\
            .build(),

        create_interface("stock_sgt_settlement_exchange_rate_sse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("沪港通-港股通信息披露-结算汇兑")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("sse", "stock", "settlement", "sgt", "rate")\
            .build(),

        create_interface("stock_sgt_settlement_exchange_rate_szse")\
            .with_source(DataSource.AKSHARE)\
            .with_category(FunctionCategory.FOREX_DATA)\
            .with_description("深港通-港股通业务信息-结算汇率")\
            .with_pattern(ParameterPattern.from_params([]))\
            .with_return_type("DataFrame")\
            .with_keywords("szse", "stock", "settlement", "sgt", "rate")\
            .build(),
        ]


# 创建提供者实例并注册
akshare_provider = AkshareProvider()

# 注册到全局管理器
from .base import register_provider
register_provider(akshare_provider)
