#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKShare数据接口提供者 - 自动生成
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
        interfaces.extend(self._register_stock_quote_interfaces())
        interfaces.extend(self._register_stock_financial_interfaces())
        interfaces.extend(self._register_stock_technical_interfaces())
        interfaces.extend(self._register_market_index_interfaces())
        interfaces.extend(self._register_market_overview_interfaces())
        interfaces.extend(self._register_industry_data_interfaces())
        interfaces.extend(self._register_fund_data_interfaces())
        interfaces.extend(self._register_forex_data_interfaces())
        
        # 批量注册所有接口
        self.registry.register_interfaces(interfaces)

    def _register_stock_basic_interfaces(self) -> List[InterfaceMetadata]:
        """注册股票基础接口"""
        return [
            # stock_info_a_code_name - 完整元数据
            create_interface("stock_info_a_code_name")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("沪深京 A 股股票代码和股票简称数据")\
                .with_return_type("DataFrame")\
                .with_keywords("code", "股票", "stock", "未明确说明", "a")\
                .build(),
            # stock_notice_report - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_notice_report")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-公告大全-沪深京 A 股公告")\
                .with_required_params("symbol", "date")\
                .with_return_type("DataFrame")\
                .with_keywords("notice", "stock", "report", "东方财富网")\
                .with_example_params({"symbol": '000001', "date": '20231201'})\
                .build(),
            # stock_sy_profile_em - 完整元数据
            create_interface("stock_sy_profile_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-商誉-A股商誉市场概况")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "A股", "stock", "profile", "东方财富网")\
                .build(),
            # stock_zh_a_gbjg_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_zh_a_gbjg_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-A股数据-股本结构")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "em", "A股", "stock", "gbjg")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_zh_ab_comparison_em - 完整元数据
            create_interface("stock_zh_ab_comparison_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-行情中心-沪深京个股-AB股比价-全部AB股比价")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "em", "stock", "comparison", "东方财富网")\
                .build(),
            # stock_a_all_pb - 完整元数据
            create_interface("stock_a_all_pb")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("乐咕乐股-A 股等权重与中位数市净率")\
                .with_return_type("DataFrame")\
                .with_keywords("all", "stock", "a", "乐咕乐股", "pb")\
                .build(),
            # stock_a_below_net_asset_statistics - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_a_below_net_asset_statistics")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("乐咕乐股-A 股破净股统计数据")\
                .with_required_params("symbol")\
                .with_return_type("int")\
                .with_keywords("statistics", "asset", "stock", "a", "net")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_a_congestion_lg - 完整元数据
            create_interface("stock_a_congestion_lg")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("乐咕乐股-大盘拥挤度")\
                .with_return_type("DataFrame")\
                .with_keywords("lg", "stock", "a", "congestion", "乐咕乐股")\
                .build(),
            # stock_a_gxl_lg - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_a_gxl_lg")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("乐咕乐股-股息率-A 股股息率")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("gxl", "lg", "stock", "a", "乐咕乐股")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_a_high_low_statistics - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_a_high_low_statistics")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("不同市场的创新高和新低的股票数量")\
                .with_required_params("symbol")\
                .with_return_type("int")\
                .with_keywords("股票", "low", "statistics", "stock", "a")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_a_ttm_lyr - 完整元数据
            create_interface("stock_a_ttm_lyr")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("乐咕乐股-A 股等权重市盈率与中位数市盈率")\
                .with_return_type("DataFrame")\
                .with_keywords("ttm", "stock", "a", "lyr", "乐咕乐股")\
                .build(),
            # stock_account_statistics_em - 完整元数据
            create_interface("stock_account_statistics_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-股票账户统计")\
                .with_return_type("int")\
                .with_keywords("股票", "em", "statistics", "account", "stock")\
                .build(),
            # stock_add_stock - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_add_stock")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-发行与分配-增发")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "stock", "add")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_allotment_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_allotment_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-个股-配股实施方案")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("未明确说明", "stock", "allotment", "cninfo")\
                .with_example_params({"symbol": '000001', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_analyst_detail_em - 完整元数据
            # analyst_id: ['1000001', '1000002', '1000003']
            # indicator: ['按报告期', '按单季度', '按年度']
            create_interface("stock_analyst_detail_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-研究报告-东方财富分析师指数-分析师详情")\
                .with_required_params("analyst_id")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "analyst", "stock", "东方财富网", "detail")\
                .with_example_params({"analyst_id": '1000001', "indicator": '按报告期'})\
                .build(),
            # stock_analyst_rank_em - 完整元数据
            # year: ['2023', '2022', '2021']
            create_interface("stock_analyst_rank_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-研究报告-东方财富分析师指数")\
                .with_required_params("year")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "analyst", "stock", "东方财富网", "指数")\
                .with_example_params({"year": '2023'})\
                .build(),
            # stock_bid_ask_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_bid_ask_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-行情报价")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "ask", "stock", "东方财富网", "bid")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_board_change_em - 完整元数据
            create_interface("stock_board_change_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-行情中心-当日板块异动详情")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "board", "change", "东方财富网")\
                .build(),
            # stock_board_concept_cons_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_board_concept_cons_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-沪深板块-概念板块-板块成份")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "concept", "cons", "board")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_board_concept_info_ths - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            create_interface("stock_board_concept_info_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("同花顺-板块-概念板块-板块简介")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "未明确说明", "concept", "board", "info")\
                .with_example_params({"symbol": '000001.SZ'})\
                .build(),
            # stock_board_concept_name_em - 完整元数据
            create_interface("stock_board_concept_name_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-行情中心-沪深京板块-概念板块")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "concept", "board", "东方财富网")\
                .build(),
            # stock_cg_equity_mortgage_cninfo - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_cg_equity_mortgage_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-数据中心-专题统计-公司治理-股权质押")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("mortgage", "stock", "未明确说明", "cg", "cninfo")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_cg_guarantee_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_cg_guarantee_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-数据中心-专题统计-公司治理-对外担保")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("未明确说明", "stock", "guarantee", "cg", "cninfo")\
                .with_example_params({"symbol": '000001', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_cg_lawsuit_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_cg_lawsuit_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-数据中心-专题统计-公司治理-公司诉讼")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("未明确说明", "stock", "lawsuit", "cg", "cninfo")\
                .with_example_params({"symbol": '000001', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_changes_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_changes_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-行情中心-盘口异动数据")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "em", "changes", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_circulate_stock_holder - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_circulate_stock_holder")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-股东股本-流通股东")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "stock", "holder", "circulate")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_comment_detail_scrd_desire_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_comment_detail_scrd_desire_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-千股千评-市场热度-市场参与意愿")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "comment", "stock", "desire", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_comment_detail_scrd_focus_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_comment_detail_scrd_focus_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-千股千评-市场热度-用户关注指数")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "comment", "stock", "东方财富网", "detail")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_comment_detail_zhpj_lspf_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_comment_detail_zhpj_lspf_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-千股千评-综合评价-历史评分")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "comment", "stock", "lspf", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_comment_detail_zlkp_jgcyd_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_comment_detail_zlkp_jgcyd_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-千股千评-主力控盘-机构参与度")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("jgcyd", "em", "comment", "stock", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_comment_em - 完整元数据
            create_interface("stock_comment_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-千股千评")\
                .with_return_type("DataFrame")\
                .with_keywords("comment", "stock", "em", "东方财富网")\
                .build(),
            # stock_concept_cons_futu - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_concept_cons_futu")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("富途牛牛-主题投资-概念板块-成分股")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "未明确说明", "concept", "cons", "futu")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_cyq_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # adjust: ['qfq": "前复权', 'hfq": "后复权', ': "不复权']
            create_interface("stock_cyq_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-概念板-行情中心-日K-筹码分布")\
                .with_required_params("symbol")\
                .with_optional_params("adjust")\
                .with_return_type("DataFrame")\
                .with_keywords("cyq", "stock", "em", "东方财富网")\
                .with_example_params({"symbol": '000001', "adjust": 'qfq": "前复权'})\
                .build(),
            # stock_dividend_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_dividend_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-个股-历史分红")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("未明确说明", "stock", "dividend", "cninfo")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_dzjy_hygtj - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_dzjy_hygtj")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-大宗交易-活跃 A 股统计")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("dzjy", "stock", "东方财富网", "hygtj")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_dzjy_hyyybtj - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_dzjy_hyyybtj")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-大宗交易-活跃营业部统计")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("hyyybtj", "dzjy", "stock", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_dzjy_mrmx - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_dzjy_mrmx")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-大宗交易-每日明细")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("dzjy", "stock", "mrmx", "东方财富网")\
                .with_example_params({"symbol": '000001', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_dzjy_mrtj - 完整元数据
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_dzjy_mrtj")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-大宗交易-每日统计")\
                .with_required_params("start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("dzjy", "stock", "东方财富网", "mrtj")\
                .with_example_params({"start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_dzjy_sctj - 完整元数据
            create_interface("stock_dzjy_sctj")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-大宗交易-市场统计")\
                .with_return_type("DataFrame")\
                .with_keywords("dzjy", "stock", "东方财富网", "sctj")\
                .build(),
            # stock_dzjy_yybph - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_dzjy_yybph")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-大宗交易-营业部排行")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("dzjy", "stock", "东方财富网", "yybph")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_ebs_lg - 完整元数据
            create_interface("stock_ebs_lg")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("乐咕乐股-股债利差")\
                .with_return_type("DataFrame")\
                .with_keywords("ebs", "stock", "lg", "乐咕乐股")\
                .build(),
            # stock_esg_hz_sina - 完整元数据
            create_interface("stock_esg_hz_sina")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-ESG评级中心-ESG评级-华证指数")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "hz", "esg", "stock", "sina")\
                .build(),
            # stock_esg_msci_sina - 完整元数据
            create_interface("stock_esg_msci_sina")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-ESG评级中心-ESG评级-MSCI")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "esg", "stock", "sina", "msci")\
                .build(),
            # stock_esg_rate_sina - 完整元数据
            create_interface("stock_esg_rate_sina")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-ESG评级中心-ESG评级-ESG评级数据")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "rate", "esg", "stock", "sina")\
                .build(),
            # stock_esg_rft_sina - 完整元数据
            create_interface("stock_esg_rft_sina")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-ESG评级中心-ESG评级-路孚特")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "esg", "stock", "rft", "sina")\
                .build(),
            # stock_esg_zd_sina - 完整元数据
            create_interface("stock_esg_zd_sina")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-ESG评级中心-ESG评级-秩鼎")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "esg", "stock", "sina", "zd")\
                .build(),
            # stock_fhps_detail_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_fhps_detail_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-分红送配-分红送配详情")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "东方财富网", "fhps", "detail")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_fhps_detail_ths - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            create_interface("stock_fhps_detail_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("同花顺-分红情况")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "未明确说明", "fhps", "detail", "ths")\
                .with_example_params({"symbol": '000001.SZ'})\
                .build(),
            # stock_fhps_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_fhps_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-数据中心-年报季报-分红配送")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "fhps", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_gddh_em - 完整元数据
            create_interface("stock_gddh_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-股东大会")\
                .with_return_type("DataFrame")\
                .with_keywords("gddh", "stock", "em", "东方财富网")\
                .build(),
            # stock_gdfx_free_holding_analyse_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_gdfx_free_holding_analyse_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-股东分析-股东持股分析-十大流通股东")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "free", "stock", "holding", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_gdfx_free_holding_change_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_gdfx_free_holding_change_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-股东分析-股东持股变动统计-十大流通股东")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "free", "stock", "change", "holding")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_gdfx_free_holding_detail_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_gdfx_free_holding_detail_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-股东分析-股东持股明细-十大流通股东")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "free", "stock", "holding", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_gdfx_free_holding_statistics_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_gdfx_free_holding_statistics_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-股东分析-股东持股统计-十大股东")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "statistics", "free", "stock", "holding")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_gdfx_free_holding_teamwork_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_gdfx_free_holding_teamwork_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-股东分析-股东协同-十大流通股东")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "teamwork", "free", "stock", "holding")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_gdfx_free_top_10_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_gdfx_free_top_10_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-个股-十大流通股东")\
                .with_required_params("symbol", "date")\
                .with_return_type("DataFrame")\
                .with_keywords("10", "em", "free", "stock", "东方财富网")\
                .with_example_params({"symbol": '000001', "date": '20231201'})\
                .build(),
            # stock_gdfx_holding_analyse_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_gdfx_holding_analyse_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-股东分析-股东持股分析-十大股东")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "holding", "东方财富网", "analyse")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_gdfx_holding_change_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_gdfx_holding_change_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-股东分析-股东持股变动统计-十大股东")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "holding", "change", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_gdfx_holding_detail_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            # indicator: ['个人', '基金', 'QFII']
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_gdfx_holding_detail_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-股东分析-股东持股明细-十大股东")\
                .with_required_params("date", "symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "holding", "东方财富网", "detail")\
                .with_example_params({"date": '20231201', "indicator": '个人', "symbol": '000001'})\
                .build(),
            # stock_gdfx_holding_statistics_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_gdfx_holding_statistics_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-股东分析-股东持股统计-十大股东")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "statistics", "stock", "holding", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_gdfx_holding_teamwork_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_gdfx_holding_teamwork_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-股东分析-股东协同-十大股东")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "teamwork", "stock", "holding", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_gdfx_top_10_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_gdfx_top_10_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-个股-十大股东")\
                .with_required_params("symbol", "date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "10", "stock", "东方财富网", "gdfx")\
                .with_example_params({"symbol": '000001', "date": '20231201'})\
                .build(),
            # stock_ggcg_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_ggcg_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-高管持股")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "em", "东方财富网", "ggcg")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_gpzy_distribute_statistics_bank_em - 完整元数据
            create_interface("stock_gpzy_distribute_statistics_bank_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "bank", "statistics", "stock", "东方财富网")\
                .build(),
            # stock_gpzy_distribute_statistics_company_em - 完整元数据
            create_interface("stock_gpzy_distribute_statistics_company_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-证券公司")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "statistics", "stock", "company", "东方财富网")\
                .build(),
            # stock_gpzy_pledge_ratio_detail_em - 完整元数据
            create_interface("stock_gpzy_pledge_ratio_detail_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "pledge", "stock", "ratio", "东方财富网")\
                .build(),
            # stock_gpzy_pledge_ratio_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_gpzy_pledge_ratio_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-股权质押-上市公司质押比例")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "pledge", "stock", "ratio", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_gpzy_profile_em - 完整元数据
            create_interface("stock_gpzy_profile_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-股权质押-股权质押市场概况")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "profile", "东方财富网", "gpzy")\
                .build(),
            # stock_gsrl_gsdt_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_gsrl_gsdt_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-股市日历-公司动态")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "gsrl", "stock", "gsdt", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_hk_gxl_lg - 完整元数据
            create_interface("stock_hk_gxl_lg")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("乐咕乐股-股息率-恒生指数股息率")\
                .with_return_type("DataFrame")\
                .with_keywords("gxl", "lg", "hk", "stock", "乐咕乐股")\
                .build(),
            # stock_hk_hot_rank_detail_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_hk_hot_rank_detail_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-股票热度-历史趋势")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "hk", "stock", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hk_hot_rank_detail_realtime_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_hk_hot_rank_detail_realtime_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-个股人气榜-实时变动")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "hk", "realtime", "stock", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hk_hot_rank_latest_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_hk_hot_rank_latest_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-个股人气榜-最新排名")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "hk", "stock", "东方财富网", "hot")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hold_change_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_hold_change_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-数据中心-专题统计-股东股本-股本变动")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("未明确说明", "stock", "cninfo", "change", "hold")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hold_control_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_hold_control_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-数据中心-专题统计-股东股本-实际控制人持股变动")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("未明确说明", "stock", "control", "cninfo", "hold")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hold_management_detail_cninfo - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_hold_management_detail_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-数据中心-专题统计-股东股本-高管持股变动明细")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "management", "未明确说明", "cninfo", "detail")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hold_management_detail_em - 完整元数据
            create_interface("stock_hold_management_detail_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-高管持股-董监高及相关人员持股变动明细")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "management", "东方财富网", "detail")\
                .build(),
            # stock_hold_management_person_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # name: ['平安银行', '贵州茅台', '招商银行']
            create_interface("stock_hold_management_person_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-高管持股-人员增减持股变动明细")\
                .with_required_params("symbol", "name")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "management", "person", "东方财富网")\
                .with_example_params({"symbol": '000001', "name": '平安银行'})\
                .build(),
            # stock_hold_num_cninfo - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_hold_num_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-数据中心-专题统计-股东股本-股东人数及持股集中度")\
                .with_required_params("date")\
                .with_return_type("int")\
                .with_keywords("num", "未明确说明", "stock", "cninfo", "hold")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_hot_deal_xq - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_hot_deal_xq")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("雪球-沪深股市-热度排行榜-交易排行榜")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("xq", "stock", "deal", "hot", "雪球")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hot_follow_xq - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_hot_follow_xq")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("雪球-沪深股市-热度排行榜-关注排行榜")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("xq", "stock", "hot", "follow", "雪球")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hot_keyword_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_hot_keyword_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-个股人气榜-热门关键词")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "东方财富网", "hot", "keyword")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hot_rank_detail_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_hot_rank_detail_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-股票热度-历史趋势及粉丝特征")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "stock", "东方财富网", "hot")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hot_rank_detail_realtime_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_hot_rank_detail_realtime_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-个股人气榜-实时变动")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "realtime", "stock", "东方财富网", "hot")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hot_rank_em - 完整元数据
            create_interface("stock_hot_rank_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网站-股票热度")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "stock", "东方财富网", "hot")\
                .build(),
            # stock_hot_rank_latest_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_hot_rank_latest_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-个股人气榜-最新排名")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "东方财富网", "hot", "latest")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hot_rank_relate_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_hot_rank_relate_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-个股人气榜-相关股票")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "stock", "relate", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hot_search_baidu - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # date: ['20231201', '20231101', '20231001']
            # time: ['09:30:00', '10:00:00', '14:00:00']
            create_interface("stock_hot_search_baidu")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("百度股市通-热搜股票")\
                .with_required_params("symbol", "date", "time")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "stock", "未明确说明", "search", "hot")\
                .with_example_params({"symbol": '000001', "date": '20231201', "time": '09:30:00'})\
                .build(),
            # stock_hot_tweet_xq - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_hot_tweet_xq")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("雪球-沪深股市-热度排行榜-讨论排行榜")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("xq", "stock", "hot", "tweet", "雪球")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hot_up_em - 完整元数据
            create_interface("stock_hot_up_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-个股人气榜-飙升榜")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "up", "stock", "东方财富网", "hot")\
                .build(),
            # stock_individual_basic_info_hk_xq - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # timeout: [5, 10, 30]
            create_interface("stock_individual_basic_info_hk_xq")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("雪球-个股-公司概况-公司简介")\
                .with_required_params("symbol")\
                .with_optional_params("token", "timeout")\
                .with_return_type("DataFrame")\
                .with_keywords("hk", "xq", "stock", "basic", "individual")\
                .with_example_params({"symbol": '000001', "timeout": 5})\
                .build(),
            # stock_individual_basic_info_us_xq - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # timeout: [5, 10, 30]
            create_interface("stock_individual_basic_info_us_xq")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("雪球-个股-公司概况-公司简介")\
                .with_required_params("symbol")\
                .with_optional_params("token", "timeout")\
                .with_return_type("DataFrame")\
                .with_keywords("xq", "stock", "basic", "us", "individual")\
                .with_example_params({"symbol": '000001', "timeout": 5})\
                .build(),
            # stock_individual_basic_info_xq - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # timeout: [5, 10, 30]
            create_interface("stock_individual_basic_info_xq")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("雪球财经-个股-公司概况-公司简介")\
                .with_required_params("symbol")\
                .with_optional_params("token", "timeout")\
                .with_return_type("DataFrame")\
                .with_keywords("xq", "stock", "basic", "individual", "info")\
                .with_example_params({"symbol": '000001', "timeout": 5})\
                .build(),
            # stock_individual_info_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # timeout: [5, 10, 30]
            create_interface("stock_individual_info_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-个股-股票信息")\
                .with_required_params("symbol")\
                .with_optional_params("timeout")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "stock", "东方财富网", "individual")\
                .with_example_params({"symbol": '000001', "timeout": 5})\
                .build(),
            # stock_info_bj_name_code - 完整元数据
            create_interface("stock_info_bj_name_code")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("北京证券交易所股票代码和简称数据")\
                .with_return_type("DataFrame")\
                .with_keywords("code", "股票", "stock", "北京证券交易所", "info")\
                .build(),
            # stock_info_change_name - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_info_change_name")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-股票曾用名")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "新浪财经", "stock", "change", "info")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_info_sh_delist - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_info_sh_delist")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("上海证券交易所暂停/终止上市股票")\
                .with_required_params("symbol")\
                .with_return_type("List[str]")\
                .with_keywords("上海证券交易所", "股票", "stock", "sh", "info")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_info_sh_name_code - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_info_sh_name_code")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("上海证券交易所股票代码和简称数据")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("code", "股票", "上海证券交易所", "stock", "sh")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_info_sz_change_name - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_info_sz_change_name")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("深证证券交易所-市场数据-股票数据-名称变更")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "sz", "stock", "change", "info")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_info_sz_delist - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_info_sz_delist")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("深证证券交易所终止/暂停上市股票")\
                .with_required_params("symbol")\
                .with_return_type("List[str]")\
                .with_keywords("股票", "sz", "stock", "info", "delist")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_info_sz_name_code - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_info_sz_name_code")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("深证证券交易所股票代码和股票简称数据")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("code", "股票", "sz", "stock", "info")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_inner_trade_xq - 完整元数据
            create_interface("stock_inner_trade_xq")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("雪球-行情中心-沪深股市-内部交易")\
                .with_return_type("DataFrame")\
                .with_keywords("xq", "stock", "trade", "inner", "雪球")\
                .build(),
            # stock_institute_hold - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_institute_hold")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-机构持股-机构持股一览表")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("hold", "stock", "新浪财经", "institute")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_institute_hold_detail - 完整元数据
            # stock: ['000001', 'sh000001', '000001.SZ']
            # quarter: ['1', '2', '3']
            create_interface("stock_institute_hold_detail")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-机构持股-机构持股详情")\
                .with_required_params("stock", "quarter")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "stock", "institute", "detail", "hold")\
                .with_example_params({"stock": '000001', "quarter": '1'})\
                .build(),
            # stock_institute_recommend - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_institute_recommend")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-机构推荐池-具体指标的数据")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "stock", "recommend", "institute")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_institute_recommend_detail - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_institute_recommend_detail")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-机构推荐池-股票评级记录")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "新浪财经", "stock", "recommend", "institute")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_intraday_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_intraday_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-分时数据")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "em", "东方财富网", "intraday")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_intraday_sina - 完整元数据
            # symbol: ['sh000001', 'sz000002', 'sh600000']
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_intraday_sina")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-日内分时数据")\
                .with_required_params("symbol", "date")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "stock", "sina", "intraday")\
                .with_example_params({"symbol": 'sh000001', "date": '20231201'})\
                .build(),
            # stock_ipo_declare - 完整元数据
            create_interface("stock_ipo_declare")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-新股申购-首发申报信息-首发申报企业信息")\
                .with_return_type("DataFrame")\
                .with_keywords("declare", "stock", "ipo", "东方财富网")\
                .build(),
            # stock_ipo_info - 完整元数据
            # stock: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_ipo_info")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-发行与分配-新股发行")\
                .with_required_params("stock")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "stock", "ipo", "info")\
                .with_example_params({"stock": '000001'})\
                .build(),
            # stock_irm_ans_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_irm_ans_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("互动易-回答")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("irm", "未明确说明", "stock", "ans", "cninfo")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_irm_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_irm_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("互动易-提问")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("未明确说明", "stock", "cninfo", "irm")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_jgdy_detail_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_jgdy_detail_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-机构调研-机构调研详细")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "jgdy", "东方财富网", "detail")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_jgdy_tj_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_jgdy_tj_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-机构调研-机构调研统计")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "tj", "stock", "jgdy", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_lh_yyb_capital - 完整元数据
            create_interface("stock_lh_yyb_capital")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("龙虎榜-营业部排行-资金实力最强")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "yyb", "同花顺", "capital", "lh")\
                .build(),
            # stock_lh_yyb_control - 完整元数据
            create_interface("stock_lh_yyb_control")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("龙虎榜-营业部排行-抱团操作实力")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "control", "yyb", "同花顺", "lh")\
                .build(),
            # stock_lh_yyb_most - 完整元数据
            create_interface("stock_lh_yyb_most")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("龙虎榜-营业部排行-上榜次数最多")\
                .with_return_type("DataFrame")\
                .with_keywords("most", "stock", "yyb", "同花顺", "lh")\
                .build(),
            # stock_lhb_detail_em - 完整元数据
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_lhb_detail_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-龙虎榜单-龙虎榜详情")\
                .with_required_params("start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "lhb", "东方财富网", "detail")\
                .with_example_params({"start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_lhb_ggtj_sina - 完整元数据
            # symbol: ['sh000001', 'sz000002', 'sh600000']
            create_interface("stock_lhb_ggtj_sina")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-龙虎榜-个股上榜统计")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "ggtj", "stock", "lhb", "sina")\
                .with_example_params({"symbol": 'sh000001'})\
                .build(),
            # stock_lhb_hyyyb_em - 完整元数据
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_lhb_hyyyb_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-龙虎榜单-每日活跃营业部")\
                .with_required_params("start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "hyyyb", "stock", "lhb", "东方财富网")\
                .with_example_params({"start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_lhb_jgmmtj_em - 完整元数据
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_lhb_jgmmtj_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-龙虎榜单-机构买卖每日统计")\
                .with_required_params("start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "lhb", "东方财富网", "jgmmtj")\
                .with_example_params({"start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_lhb_jgmx_sina - 完整元数据
            create_interface("stock_lhb_jgmx_sina")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-龙虎榜-机构席位成交明细")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "stock", "lhb", "jgmx", "sina")\
                .build(),
            # stock_lhb_jgstatistic_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_lhb_jgstatistic_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-龙虎榜单-机构席位追踪")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "lhb", "东方财富网", "jgstatistic")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_lhb_jgzz_sina - 完整元数据
            # symbol: ['sh000001', 'sz000002', 'sh600000']
            create_interface("stock_lhb_jgzz_sina")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-龙虎榜-机构席位追踪")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "jgzz", "stock", "lhb", "sina")\
                .with_example_params({"symbol": 'sh000001'})\
                .build(),
            # stock_lhb_stock_detail_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # date: ['20231201', '20231101', '20231001']
            # flag: ['买入', '卖出']
            create_interface("stock_lhb_stock_detail_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-龙虎榜单-个股龙虎榜详情")\
                .with_required_params("symbol", "date", "flag")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "lhb", "东方财富网", "detail")\
                .with_example_params({"symbol": '000001', "date": '20231201', "flag": '买入'})\
                .build(),
            # stock_lhb_stock_statistic_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_lhb_stock_statistic_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-龙虎榜单-个股上榜统计")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "lhb", "东方财富网", "statistic")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_lhb_traderstatistic_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_lhb_traderstatistic_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-龙虎榜单-营业部统计")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "lhb", "东方财富网", "traderstatistic")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_lhb_yyb_detail_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_lhb_yyb_detail_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-龙虎榜单-营业部历史交易明细-营业部交易明细")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "lhb", "yyb", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_lhb_yybph_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_lhb_yybph_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-龙虎榜单-营业部排行")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "lhb", "东方财富网", "yybph")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_lhb_yytj_sina - 完整元数据
            # symbol: ['sh000001', 'sz000002', 'sh600000']
            create_interface("stock_lhb_yytj_sina")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-龙虎榜-营业上榜统计")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "stock", "lhb", "sina", "yytj")\
                .with_example_params({"symbol": 'sh000001'})\
                .build(),
            # stock_lrb_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_lrb_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-数据中心-年报季报-业绩快报-利润表")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "lrb", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_main_stock_holder - 完整元数据
            # stock: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_main_stock_holder")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-股本股东-主要股东")\
                .with_required_params("stock")\
                .with_return_type("DataFrame")\
                .with_keywords("main", "stock", "holder", "新浪财经")\
                .with_example_params({"stock": '000001'})\
                .build(),
            # stock_management_change_ths - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_management_change_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("同花顺-公司大事-高管持股变动")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "management", "未明确说明", "change", "ths")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_margin_account_info - 完整元数据
            create_interface("stock_margin_account_info")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-融资融券-融资融券账户统计-两融账户信息")\
                .with_return_type("int")\
                .with_keywords("account", "stock", "东方财富网", "margin", "info")\
                .build(),
            # stock_margin_detail_sse - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_margin_detail_sse")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("上海证券交易所-融资融券数据-融资融券明细数据")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("上海证券交易所", "sse", "stock", "margin", "detail")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_margin_detail_szse - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_margin_detail_szse")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("深证证券交易所-融资融券数据-融资融券交易明细数据")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "margin", "detail", "深圳证券交易所", "szse")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_margin_ratio_pa - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_margin_ratio_pa")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("融资融券-标的证券名单及保证金比例查询")\
                .with_required_params("date")\
                .with_return_type("List[str]")\
                .with_keywords("pa", "未明确说明", "stock", "ratio", "margin")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_margin_sse - 完整元数据
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_margin_sse")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("上海证券交易所-融资融券数据-融资融券汇总数据")\
                .with_required_params("start_date", "end_date")\
                .with_return_type("int")\
                .with_keywords("上海证券交易所", "sse", "stock", "margin")\
                .with_example_params({"start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_margin_szse - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_margin_szse")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("深圳证券交易所-融资融券数据-融资融券汇总数据")\
                .with_required_params("date")\
                .with_return_type("int")\
                .with_keywords("stock", "margin", "szse", "深圳证券交易所")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_margin_underlying_info_szse - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_margin_underlying_info_szse")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("深圳证券交易所-融资融券数据-标的证券信息")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "underlying", "margin", "info", "szse")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_market_activity_legu - 完整元数据
            create_interface("stock_market_activity_legu")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("乐咕乐股网-赚钱效应分析数据")\
                .with_return_type("DataFrame")\
                .with_keywords("legu", "stock", "market", "乐咕乐股", "activity")\
                .build(),
            # stock_market_pb_lg - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_market_pb_lg")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("乐咕乐股-主板市净率")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("lg", "stock", "market", "乐咕乐股", "pb")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_market_pe_lg - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_market_pe_lg")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("乐咕乐股-主板市盈率")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("lg", "stock", "market", "pe", "乐咕乐股")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_new_gh_cninfo - 完整元数据
            create_interface("stock_new_gh_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-数据中心-新股数据-新股过会")\
                .with_return_type("DataFrame")\
                .with_keywords("未明确说明", "stock", "cninfo", "gh", "new")\
                .build(),
            # stock_new_ipo_cninfo - 完整元数据
            create_interface("stock_new_ipo_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-数据中心-新股数据-新股发行")\
                .with_return_type("DataFrame")\
                .with_keywords("ipo", "未明确说明", "stock", "cninfo", "new")\
                .build(),
            # stock_pg_em - 完整元数据
            create_interface("stock_pg_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-新股数据-配股")\
                .with_return_type("DataFrame")\
                .with_keywords("pg", "stock", "em", "东方财富网")\
                .build(),
            # stock_profile_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_profile_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-个股-公司概况")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("未明确说明", "stock", "profile", "cninfo")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_qbzf_em - 完整元数据
            create_interface("stock_qbzf_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-新股数据-增发-全部增发")\
                .with_return_type("DataFrame")\
                .with_keywords("东方财富网", "stock", "em", "qbzf")\
                .build(),
            # stock_rank_cxfl_ths - 完整元数据
            create_interface("stock_rank_cxfl_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("同花顺-数据中心-技术选股-持续放量")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "同花顺", "rank", "ths", "cxfl")\
                .build(),
            # stock_rank_cxsl_ths - 完整元数据
            create_interface("stock_rank_cxsl_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("同花顺-数据中心-技术选股-持续缩量")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "同花顺", "cxsl", "ths", "rank")\
                .build(),
            # stock_rank_forecast_cninfo - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_rank_forecast_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-数据中心-评级预测-投资评级")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("未明确说明", "stock", "forecast", "cninfo", "rank")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_rank_ljqd_ths - 完整元数据
            create_interface("stock_rank_ljqd_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("同花顺-数据中心-技术选股-量价齐跌")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "ljqd", "同花顺", "ths", "rank")\
                .build(),
            # stock_rank_ljqs_ths - 完整元数据
            create_interface("stock_rank_ljqs_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("同花顺-数据中心-技术选股-量价齐升")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "同花顺", "ths", "rank", "ljqs")\
                .build(),
            # stock_rank_xstp_ths - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            create_interface("stock_rank_xstp_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("同花顺-数据中心-技术选股-向上突破")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "同花顺", "ths", "xstp", "rank")\
                .with_example_params({"symbol": '000001.SZ'})\
                .build(),
            # stock_rank_xxtp_ths - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            create_interface("stock_rank_xxtp_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("同花顺-数据中心-技术选股-向下突破")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "xxtp", "同花顺", "ths", "rank")\
                .with_example_params({"symbol": '000001.SZ'})\
                .build(),
            # stock_rank_xzjp_ths - 完整元数据
            create_interface("stock_rank_xzjp_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("同花顺-数据中心-技术选股-险资举牌")\
                .with_return_type("DataFrame")\
                .with_keywords("xzjp", "stock", "同花顺", "ths", "rank")\
                .build(),
            # stock_register_bj - 完整元数据
            create_interface("stock_register_bj")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-新股数据-IPO审核信息-北交所")\
                .with_return_type("DataFrame")\
                .with_keywords("register", "stock", "东方财富网", "bj")\
                .build(),
            # stock_register_cyb - 完整元数据
            create_interface("stock_register_cyb")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-新股数据-IPO审核信息-创业板")\
                .with_return_type("DataFrame")\
                .with_keywords("register", "stock", "cyb", "东方财富网")\
                .build(),
            # stock_register_db - 完整元数据
            create_interface("stock_register_db")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-新股数据-注册制审核-达标企业")\
                .with_return_type("DataFrame")\
                .with_keywords("register", "stock", "db", "东方财富网")\
                .build(),
            # stock_register_sh - 完整元数据
            create_interface("stock_register_sh")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-新股数据-IPO审核信息-上海主板")\
                .with_return_type("DataFrame")\
                .with_keywords("register", "stock", "东方财富网", "sh")\
                .build(),
            # stock_register_sz - 完整元数据
            create_interface("stock_register_sz")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-新股数据-IPO审核信息-深圳主板")\
                .with_return_type("DataFrame")\
                .with_keywords("sz", "register", "stock", "东方财富网")\
                .build(),
            # stock_repurchase_em - 完整元数据
            create_interface("stock_repurchase_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-股票回购-股票回购数据")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "stock", "repurchase", "东方财富网")\
                .build(),
            # stock_restricted_release_detail_em - 完整元数据
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_restricted_release_detail_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-限售股解禁-解禁详情一览")\
                .with_required_params("start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("release", "em", "stock", "东方财富网", "detail")\
                .with_example_params({"start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_restricted_release_queue_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_restricted_release_queue_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-个股限售解禁-解禁批次")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("release", "em", "stock", "queue", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_restricted_release_queue_sina - 完整元数据
            # symbol: ['sh000001', 'sz000002', 'sh600000']
            create_interface("stock_restricted_release_queue_sina")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-发行分配-限售解禁")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "release", "stock", "queue", "sina")\
                .with_example_params({"symbol": 'sh000001'})\
                .build(),
            # stock_restricted_release_stockholder_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_restricted_release_stockholder_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-个股限售解禁-解禁股东")\
                .with_required_params("symbol", "date")\
                .with_return_type("DataFrame")\
                .with_keywords("release", "em", "stockholder", "stock", "东方财富网")\
                .with_example_params({"symbol": '000001', "date": '20231201'})\
                .build(),
            # stock_share_change_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_share_change_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-数据-公司股本变动")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("未明确说明", "stock", "cninfo", "change", "share")\
                .with_example_params({"symbol": '000001', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_share_hold_change_bse - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_share_hold_change_bse")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("北京证券交易所-信息披露-监管信息-董监高及相关人员持股变动")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "北京证券交易所", "change", "bse", "hold")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_share_hold_change_sse - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_share_hold_change_sse")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("上海证券交易所-披露-监管信息公开-公司监管-董董监高人员股份变动")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("上海证券交易所", "sse", "stock", "change", "hold")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_share_hold_change_szse - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_share_hold_change_szse")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("深圳证券交易所-信息披露-监管信息公开-董监高人员股份变动")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "change", "szse", "深圳证券交易所", "hold")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_shareholder_change_ths - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            create_interface("stock_shareholder_change_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("同花顺-公司大事-股东持股变动")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("shareholder", "stock", "未明确说明", "change", "ths")\
                .with_example_params({"symbol": '000001.SZ'})\
                .build(),
            # stock_sns_sseinfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_sns_sseinfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("上证e互动-提问与回答")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("未明确说明", "stock", "sseinfo", "sns")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_staq_net_stop - 完整元数据
            create_interface("stock_staq_net_stop")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-行情中心-沪深个股-两网及退市")\
                .with_return_type("DataFrame")\
                .with_keywords("staq", "stock", "net", "东方财富网", "stop")\
                .build(),
            # stock_sy_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_sy_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-商誉-个股商誉明细")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "em", "东方财富网", "sy")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_sy_hy_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_sy_hy_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-商誉-行业商誉")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "东方财富网", "hy", "sy")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_sy_jz_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_sy_jz_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-商誉-个股商誉减值明细")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("jz", "em", "stock", "东方财富网", "sy")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_sy_yq_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_sy_yq_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-商誉-商誉减值预期明细")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "东方财富网", "sy", "yq")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_tfp_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_tfp_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-停复牌信息")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "em", "东方财富网", "tfp")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_value_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_value_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-估值分析-每日互动-每日互动-估值分析")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("value", "stock", "em", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_xgsglb_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_xgsglb_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-新股数据-新股申购-新股申购与中签查询")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("东方财富网", "stock", "em", "xgsglb")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_xgsr_ths - 完整元数据
            create_interface("stock_xgsr_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("同花顺-数据中心-新股数据-新股上市首日")\
                .with_return_type("DataFrame")\
                .with_keywords("ths", "同花顺", "stock", "xgsr")\
                .build(),
            # stock_xjll_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_xjll_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-数据中心-年报季报-业绩快报-现金流量表")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("xjll", "stock", "em", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_yjbb_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_yjbb_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-数据中心-年报季报-业绩报表")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("yjbb", "stock", "em", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_yjkb_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_yjkb_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-数据中心-年报季报-业绩快报")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "yjkb", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_yjyg_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_yjyg_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-数据中心-年报季报-业绩预告")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "em", "东方财富网", "yjyg")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_yysj_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_yysj_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-数据中心-年报季报-预约披露时间")\
                .with_required_params("symbol", "date")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "em", "yysj", "东方财富网")\
                .with_example_params({"symbol": '000001', "date": '20231201'})\
                .build(),
            # stock_yzxdr_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_yzxdr_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-一致行动人")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "em", "东方财富网", "yzxdr")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_zcfz_bj_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_zcfz_bj_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-数据中心-年报季报-业绩快报-资产负债表")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "东方财富网", "bj", "zcfz")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_zcfz_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_zcfz_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-数据中心-年报季报-业绩快报-资产负债表")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "zcfz", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_zdhtmx_em - 完整元数据
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_zdhtmx_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-重大合同-重大合同明细")\
                .with_required_params("start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("zdhtmx", "stock", "em", "东方财富网")\
                .with_example_params({"start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_zh_a_disclosure_relation_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # market: ['沪深京', '港股', '三板']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_zh_a_disclosure_relation_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-首页-公告查询-信息披露调研-沪深京")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_optional_params("market")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "stock", "disclosure", "a", "未明确说明")\
                .with_example_params({"symbol": '000001', "market": '沪深京', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_zh_a_disclosure_report_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # market: ['沪深京', '港股', '三板']
            # keyword: ['银行', '新能源', '芯片']
            # category: ['年报', '半年报', '一季报']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_zh_a_disclosure_report_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("巨潮资讯-首页-公告查询-信息披露公告-沪深京")\
                .with_required_params("symbol", "keyword", "category", "start_date", "end_date")\
                .with_optional_params("market")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "stock", "disclosure", "a", "未明确说明")\
                .with_example_params({"symbol": '000001', "market": '沪深京', "keyword": '银行', "category": '年报', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_zh_a_gdhs - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_zh_a_gdhs")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-股东户数数据")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("gdhs", "zh", "stock", "a", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_zh_a_gdhs_detail_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_zh_a_gdhs_detail_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-股东户数详情")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("gdhs", "zh", "em", "stock", "a")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_zh_a_new - 完整元数据
            create_interface("stock_zh_a_new")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("新浪财经-行情中心-沪深股市-次新股")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "zh", "stock", "a", "new")\
                .build(),
            # stock_zh_a_new_em - 完整元数据
            create_interface("stock_zh_a_new_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-行情中心-沪深个股-新股")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "em", "stock", "a", "东方财富网")\
                .build(),
            # stock_zh_a_st_em - 完整元数据
            create_interface("stock_zh_a_st_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-行情中心-沪深个股-风险警示板")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "em", "st", "stock", "a")\
                .build(),
            # stock_zh_a_stop_em - 完整元数据
            create_interface("stock_zh_a_stop_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-行情中心-沪深个股-两网及退市")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "em", "stock", "a", "东方财富网")\
                .build(),
            # stock_zh_a_tick_tx_js - 完整元数据
            # symbol: ['sh000001', 'sz000002', 'sh600000']
            create_interface("stock_zh_a_tick_tx_js")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("每个交易日 16:00 提供当日数据; 如遇到数据缺失, 请使用 **ak.stock_zh_a_tick_163()** 接口(注意数据会有一定差异)")\
                .with_optional_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "stock", "未明确说明", "a", "tx")\
                .with_example_params({"symbol": 'sh000001'})\
                .build(),
            # stock_zh_ah_name - 完整元数据
            create_interface("stock_zh_ah_name")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("A+H 股数据是从腾讯财经获取的数据, 历史数据按日频率更新")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "未明确说明", "stock", "ah", "name")\
                .build(),
            # stock_zh_valuation_baidu - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # indicator: ['总市值', '市盈率(TTM)', '市盈率(静)']
            # period: ['近一年', '近三年', '近五年']
            create_interface("stock_zh_valuation_baidu")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("百度股市通-A 股-财务报表-估值数据")\
                .with_required_params("symbol", "period")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "财务", "valuation", "stock", "未明确说明")\
                .with_example_params({"symbol": '000001', "indicator": '总市值', "period": '近一年'})\
                .build(),
            # stock_zh_vote_baidu - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # indicator: ['指数', '股票']
            create_interface("stock_zh_vote_baidu")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("百度股市通- A 股或指数-股评-投票")\
                .with_required_params("symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "stock", "未明确说明", "baidu", "vote")\
                .with_example_params({"symbol": '000001', "indicator": '指数'})\
                .build(),
            # stock_zt_pool_dtgc_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_zt_pool_dtgc_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-行情中心-涨停板行情-跌停股池")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "zt", "stock", "dtgc", "pool")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_zt_pool_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_zt_pool_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-行情中心-涨停板行情-涨停股池")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "zt", "stock", "pool", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_zt_pool_previous_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_zt_pool_previous_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-行情中心-涨停板行情-昨日涨停股池")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "zt", "stock", "pool", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_zt_pool_strong_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_zt_pool_strong_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-行情中心-涨停板行情-强势股池")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "zt", "stock", "pool", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_zt_pool_sub_new_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_zt_pool_sub_new_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-行情中心-涨停板行情-次新股池")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("sub", "em", "zt", "stock", "pool")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_zt_pool_zbgc_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_zt_pool_zbgc_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-行情中心-涨停板行情-炸板股池")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "zt", "stock", "pool", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_zygc_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_zygc_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-个股-主营构成")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("zygc", "stock", "em", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_zyjs_ths - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            create_interface("stock_zyjs_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("同花顺-主营介绍")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("ths", "stock", "zyjs", "未明确说明")\
                .with_example_params({"symbol": '000001.SZ'})\
                .build(),
            # stock_qsjy_em - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_qsjy_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-特色数据-券商业绩月报")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "qsjy", "东方财富网")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_dxsyl_em - 完整元数据
            create_interface("stock_dxsyl_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-新股申购-打新收益率")\
                .with_return_type("DataFrame")\
                .with_keywords("dxsyl", "stock", "em", "东方财富网")\
                .build(),
            # stock_hsgt_board_rank_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # indicator: ['今日', '3日', '5日']
            create_interface("stock_hsgt_board_rank_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-沪深港通持股-板块排行")\
                .with_required_params("symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "board", "东方财富网", "hsgt")\
                .with_example_params({"symbol": '000001', "indicator": '今日'})\
                .build(),
            # stock_hsgt_hold_stock_em - 完整元数据
            # market: ['北向', '沪股通', '深股通']
            # indicator: ['今日排行', '3日排行', '5日排行']
            create_interface("stock_hsgt_hold_stock_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-沪深港通持股-个股排行")\
                .with_optional_params("market", "indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "东方财富网", "hsgt", "hold")\
                .with_example_params({"market": '北向', "indicator": '今日排行'})\
                .build(),
            # stock_hsgt_individual_detail_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_hsgt_individual_detail_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-沪深港通-沪深港通持股-具体股票-个股详情")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "stock", "东方财富网", "individual")\
                .with_example_params({"symbol": '000001', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_hsgt_individual_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_hsgt_individual_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-沪深港通-沪深港通持股-具体股票")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "stock", "东方财富网", "individual")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hsgt_institution_statistics_em - 完整元数据
            # market: ['北向持股', '沪股通持股', '深股通持股']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_hsgt_institution_statistics_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-沪深港通-沪深港通持股-机构排行")\
                .with_required_params("start_date", "end_date")\
                .with_optional_params("market")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "statistics", "stock", "institution", "东方财富网")\
                .with_example_params({"market": '北向持股', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_hsgt_stock_statistics_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_hsgt_stock_statistics_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-沪深港通-沪深港通持股-每日个股统计")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "statistics", "stock", "东方财富网", "hsgt")\
                .with_example_params({"symbol": '000001', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_hk_company_profile_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_hk_company_profile_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-港股-公司资料")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "hk", "stock", "profile", "company")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hk_fhpx_detail_ths - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            create_interface("stock_hk_fhpx_detail_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("同花顺-港股-分红派息")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("fhpx", "hk", "stock", "未明确说明", "detail")\
                .with_example_params({"symbol": '000001.SZ'})\
                .build(),
            # stock_hk_ggt_components_em - 完整元数据
            create_interface("stock_hk_ggt_components_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-行情中心-港股市场-港股通成份股")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "hk", "stock", "东方财富网", "components")\
                .build(),
            # stock_hk_hot_rank_em - 完整元数据
            create_interface("stock_hk_hot_rank_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-个股人气榜-人气榜-港股市场")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "hk", "stock", "东方财富网", "hot")\
                .build(),
            # stock_hk_security_profile_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_hk_security_profile_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富-港股-证券资料")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "hk", "stock", "profile", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hk_valuation_baidu - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # indicator: ['总市值', '市盈率(TTM)', '市盈率(静)']
            # period: ['近一年', '近三年', '全部']
            create_interface("stock_hk_valuation_baidu")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("百度股市通-港股-财务报表-估值数据")\
                .with_required_params("symbol", "period")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("hk", "财务", "valuation", "stock", "未明确说明")\
                .with_example_params({"symbol": '000001', "indicator": '总市值', "period": '近一年'})\
                .build(),
            # stock_register_kcb - 完整元数据
            create_interface("stock_register_kcb")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_BASIC)\
                .with_description("东方财富网-数据中心-新股数据-IPO审核信息-科创板")\
                .with_return_type("DataFrame")\
                .with_keywords("register", "stock", "kcb", "东方财富网")\
                .build(),
        ]

    def _register_stock_quote_interfaces(self) -> List[InterfaceMetadata]:
        """注册股票行情接口"""
        return [
            # stock_zh_a_daily - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            # adjust: ['', 'qfq', 'hfq']
            create_interface("stock_zh_a_daily")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("新浪财经-沪深京 A 股的数据, 历史数据按日频率更新; 注意其中的 **sh689009** 为 CDR, 请 通过 **ak.stock_zh_a_cdr_daily** 接口获取")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_optional_params("adjust")\
                .with_return_type("DataFrame")\
                .with_keywords("daily", "新浪财经", "zh", "stock", "a")\
                .with_example_params({"symbol": '000001', "start_date": '20230101', "end_date": '20231231', "adjust": ''})\
                .build(),
            # stock_zh_a_hist - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # period: ['daily', 'weekly', 'monthly']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            # adjust: ['', 'qfq', 'hfq']
            # timeout: [5, 10, 30]
            create_interface("stock_zh_a_hist")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富-沪深京 A 股日频率数据; 历史数据按日频率更新, 当日收盘价请在收盘后获取")\
                .with_required_params("symbol", "period", "start_date", "end_date")\
                .with_optional_params("adjust", "timeout")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "stock", "a", "东方财富网", "hist")\
                .with_example_params({"symbol": '000001', "period": 'daily', "start_date": '20230101', "end_date": '20231231', "adjust": '', "timeout": 5})\
                .build(),
            # stock_zh_a_hist_min_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            # period: ['1', '5', '15']
            # adjust: ['qfq', 'hfq']
            create_interface("stock_zh_a_hist_min_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-行情首页-沪深京 A 股-每日分时行情; 该接口只能获取近期的分时数据，注意时间周期的设置")\
                .with_required_params("symbol", "period")\
                .with_optional_params("start_date", "end_date", "adjust")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "em", "stock", "min", "a")\
                .with_example_params({"symbol": '000001', "start_date": '20230101', "end_date": '20231231', "period": '1', "adjust": 'qfq'})\
                .build(),
            # stock_zh_a_minute - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # period: ['daily', 'weekly', 'monthly']
            # adjust: ['', 'qfq', 'hfq']
            create_interface("stock_zh_a_minute")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("新浪财经-沪深京 A 股股票或者指数的分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率, 可以指定是否复权")\
                .with_required_params("symbol", "period")\
                .with_optional_params("adjust")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "zh", "新浪财经", "stock", "a")\
                .with_example_params({"symbol": '000001', "period": 'daily', "adjust": ''})\
                .build(),
            # stock_zh_a_spot - 完整元数据
            create_interface("stock_zh_a_spot")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("新浪财经-沪深京 A 股数据, 重复运行本函数会被新浪暂时封 IP, 建议增加时间间隔")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "zh", "spot", "stock", "a")\
                .build(),
            # stock_zh_a_spot_em - 完整元数据
            create_interface("stock_zh_a_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-沪深京 A 股-实时行情数据")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "em", "spot", "stock", "a")\
                .build(),
            # stock_zh_a_cdr_daily - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_zh_a_cdr_daily")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("上海证券交易所-科创板-CDR")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("daily", "新浪财经", "zh", "cdr", "stock")\
                .with_example_params({"symbol": '000001', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_bj_a_spot_em - 完整元数据
            create_interface("stock_bj_a_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-京 A 股-实时行情数据")\
                .with_return_type("DataFrame")\
                .with_keywords("spot", "em", "stock", "a", "东方财富网")\
                .build(),
            # stock_board_concept_hist_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # period: ['daily', 'weekly', 'monthly']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            # adjust: [': 不复权', '默认; "qfq": 前复权', 'hfq": 后复权']
            create_interface("stock_board_concept_hist_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富-沪深板块-概念板块-历史行情数据")\
                .with_required_params("symbol", "period", "start_date", "end_date")\
                .with_optional_params("adjust")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "concept", "board", "东方财富网")\
                .with_example_params({"symbol": '000001', "period": 'daily', "start_date": '20230101', "end_date": '20231231', "adjust": ': 不复权'})\
                .build(),
            # stock_board_concept_hist_min_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # period: ['1', '5', '15']
            create_interface("stock_board_concept_hist_min_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富-沪深板块-概念板块-分时历史行情数据")\
                .with_required_params("symbol", "period")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "min", "concept", "board")\
                .with_example_params({"symbol": '000001', "period": '1'})\
                .build(),
            # stock_board_concept_spot_em - 完整元数据
            create_interface("stock_board_concept_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-行情中心-沪深京板块-概念板块-实时行情")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "spot", "stock", "concept", "board")\
                .build(),
            # stock_board_industry_hist_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            # period: ['日k', '周k', '月k']
            # adjust: [': 不复权', '默认; "qfq": 前复权', 'hfq": 后复权']
            create_interface("stock_board_industry_hist_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富-沪深板块-行业板块-历史行情数据")\
                .with_required_params("symbol", "start_date", "end_date", "period")\
                .with_optional_params("adjust")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "board", "industry", "东方财富网")\
                .with_example_params({"symbol": '000001', "start_date": '20230101', "end_date": '20231231', "period": '日k', "adjust": ': 不复权'})\
                .build(),
            # stock_board_industry_hist_min_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # period: ['1', '5', '15']
            create_interface("stock_board_industry_hist_min_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富-沪深板块-行业板块-分时历史行情数据")\
                .with_required_params("symbol", "period")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "min", "board", "industry")\
                .with_example_params({"symbol": '000001', "period": '1'})\
                .build(),
            # stock_board_industry_spot_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_board_industry_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-沪深板块-行业板块-实时行情")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "spot", "stock", "board", "industry")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_comment_detail_scrd_desire_daily_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_comment_detail_scrd_desire_daily_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-数据中心-特色数据-千股千评-市场热度-日度市场参与意愿")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("daily", "em", "comment", "stock", "desire")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_concept_fund_flow_hist - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_concept_fund_flow_hist")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-数据中心-资金流向-概念资金流-概念历史资金流")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("fund", "stock", "concept", "东方财富网", "hist")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_cy_a_spot_em - 完整元数据
            create_interface("stock_cy_a_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-创业板-实时行情")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "spot", "stock", "a", "cy")\
                .build(),
            # stock_history_dividend - 完整元数据
            create_interface("stock_history_dividend")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("新浪财经-发行与分配-历史分红")\
                .with_return_type("DataFrame")\
                .with_keywords("history", "stock", "dividend", "新浪财经")\
                .build(),
            # stock_history_dividend_detail - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # indicator: ['分红', '配股']
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_history_dividend_detail")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("新浪财经-发行与分配-分红配股")\
                .with_required_params("symbol", "date")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "stock", "dividend", "detail", "history")\
                .with_example_params({"symbol": '000001', "indicator": '分红', "date": '20231201'})\
                .build(),
            # stock_individual_spot_xq - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # timeout: [5, 10, 30]
            create_interface("stock_individual_spot_xq")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("雪球-行情中心-个股")\
                .with_required_params("symbol")\
                .with_optional_params("token", "timeout")\
                .with_return_type("DataFrame")\
                .with_keywords("spot", "xq", "stock", "individual", "雪球")\
                .with_example_params({"symbol": '000001', "timeout": 5})\
                .build(),
            # stock_industry_clf_hist_sw - 完整元数据
            create_interface("stock_industry_clf_hist_sw")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("申万宏源研究-行业分类-全部行业分类")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "未明确说明", "industry", "sw", "hist")\
                .build(),
            # stock_lhb_detail_daily_sina - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_lhb_detail_daily_sina")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("新浪财经-龙虎榜-每日详情")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("daily", "新浪财经", "stock", "lhb", "detail")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_new_a_spot_em - 完整元数据
            create_interface("stock_new_a_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-新股-实时行情数据")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "spot", "stock", "a", "东方财富网")\
                .build(),
            # stock_price_js - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_price_js")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("美港电讯-美港目标价数据")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("未明确说明", "stock", "price", "js")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_sector_fund_flow_hist - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_sector_fund_flow_hist")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-数据中心-资金流向-行业资金流-行业历史资金流")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("fund", "stock", "sector", "东方财富网", "hist")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_sector_spot - 完整元数据
            # indicator: ['新浪行业', '启明星行业', '概念']
            create_interface("stock_sector_spot")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("新浪行业-板块行情")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "spot", "stock", "sector", "行业")\
                .with_example_params({"indicator": '新浪行业'})\
                .build(),
            # stock_sh_a_spot_em - 完整元数据
            create_interface("stock_sh_a_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-沪 A 股-实时行情数据")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "spot", "stock", "a", "sh")\
                .build(),
            # stock_sse_deal_daily - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_sse_deal_daily")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("上海证券交易所-数据-股票数据-成交概况-股票成交概况-每日股票情况")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("daily", "股票", "上海证券交易所", "sse", "stock")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_sz_a_spot_em - 完整元数据
            create_interface("stock_sz_a_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-深 A 股-实时行情数据")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "spot", "sz", "stock", "a")\
                .build(),
            # stock_zh_a_hist_pre_min_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # start_time: ['09:00:00', '09:15:00', '09:30:00']
            # end_time: ['15:40:00', '15:30:00', '15:00:00']
            create_interface("stock_zh_a_hist_pre_min_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富-股票行情-盘前数据")\
                .with_required_params("symbol")\
                .with_optional_params("start_time", "end_time")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "zh", "em", "stock", "a")\
                .with_example_params({"symbol": '000001', "start_time": '09:00:00', "end_time": '15:40:00'})\
                .build(),
            # stock_zh_a_hist_tx - 完整元数据
            # symbol: ['sh000001', 'sz000002', 'sh600000']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            # adjust: ['', 'qfq', 'hfq']
            # timeout: [5, 10, 30]
            create_interface("stock_zh_a_hist_tx")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("腾讯证券-日频-股票历史数据; 历史数据按日频率更新, 当日收盘价请在收盘后获取")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_optional_params("adjust", "timeout")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "zh", "stock", "未明确说明", "a")\
                .with_example_params({"symbol": 'sh000001', "start_date": '20230101', "end_date": '20231231', "adjust": '', "timeout": 5})\
                .build(),
            # stock_zh_ah_daily - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # start_year: ['2023', '2022', '2021']
            # end_year: ['2023', '2022', '2021']
            # adjust: ['', 'qfq', 'hfq']
            create_interface("stock_zh_ah_daily")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("腾讯财经-A+H 股数据")\
                .with_required_params("symbol", "start_year", "end_year")\
                .with_optional_params("adjust")\
                .with_return_type("DataFrame")\
                .with_keywords("daily", "zh", "stock", "未明确说明", "ah")\
                .with_example_params({"symbol": '000001', "start_year": '2023', "end_year": '2023', "adjust": ''})\
                .build(),
            # stock_zh_ah_spot - 完整元数据
            create_interface("stock_zh_ah_spot")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("A+H 股数据是从腾讯财经获取的数据, 延迟 15 分钟更新")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "spot", "未明确说明", "stock", "ah")\
                .build(),
            # stock_zh_b_daily - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            # adjust: ['', 'qfq', 'hfq']
            create_interface("stock_zh_b_daily")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("B 股数据是从新浪财经获取的数据, 历史数据按日频率更新")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_optional_params("adjust")\
                .with_return_type("DataFrame")\
                .with_keywords("daily", "新浪财经", "zh", "stock", "b")\
                .with_example_params({"symbol": '000001', "start_date": '20230101', "end_date": '20231231', "adjust": ''})\
                .build(),
            # stock_zh_b_minute - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # period: ['daily', 'weekly', 'monthly']
            # adjust: ['', 'qfq', 'hfq']
            create_interface("stock_zh_b_minute")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("新浪财经 B 股股票或者指数的分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率, 可以指定是否复权")\
                .with_required_params("symbol", "period")\
                .with_optional_params("adjust")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "zh", "新浪财经", "stock", "b")\
                .with_example_params({"symbol": '000001', "period": 'daily', "adjust": ''})\
                .build(),
            # stock_zh_b_spot - 完整元数据
            create_interface("stock_zh_b_spot")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("B 股数据是从新浪财经获取的数据, 重复运行本函数会被新浪暂时封 IP, 建议增加时间间隔")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "zh", "spot", "stock", "b")\
                .build(),
            # stock_zh_b_spot_em - 完整元数据
            create_interface("stock_zh_b_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-实时行情数据")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "em", "spot", "stock", "b")\
                .build(),
            # stock_hsgt_hist_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_hsgt_hist_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-数据中心-资金流向-沪深港通资金流向-沪深港通历史数据")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "东方财富网", "hsgt", "hist")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_zh_ah_spot_em - 完整元数据
            create_interface("stock_zh_ah_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-行情中心-沪深港通-AH股比价-实时行情, 延迟 15 分钟更新")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "em", "spot", "stock", "东方财富网")\
                .build(),
            # stock_hk_daily - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # adjust: ['', 'qfq', 'hfq']
            create_interface("stock_hk_daily")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("港股-历史行情数据, 可以选择返回复权后数据,更新频率为日频")\
                .with_required_params("symbol")\
                .with_optional_params("adjust")\
                .with_return_type("DataFrame")\
                .with_keywords("daily", "新浪财经", "stock", "hk")\
                .with_example_params({"symbol": '000001', "adjust": ''})\
                .build(),
            # stock_hk_famous_spot_em - 完整元数据
            create_interface("stock_hk_famous_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-行情中心-港股市场-知名港股实时行情数据")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "spot", "hk", "stock", "东方财富网")\
                .build(),
            # stock_hk_hist - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # period: ['daily', 'weekly', 'monthly']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            # adjust: ['', 'qfq', 'hfq']
            create_interface("stock_hk_hist")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("港股-历史行情数据, 可以选择返回复权后数据, 更新频率为日频")\
                .with_required_params("symbol", "period", "start_date", "end_date")\
                .with_optional_params("adjust")\
                .with_return_type("DataFrame")\
                .with_keywords("hist", "stock", "hk", "东方财富网")\
                .with_example_params({"symbol": '000001', "period": 'daily', "start_date": '20230101', "end_date": '20231231', "adjust": ''})\
                .build(),
            # stock_hk_hist_min_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # period: ['1', '5', '15']
            # adjust: ['qfq', 'hfq']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_hk_hist_min_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-行情首页-港股-每日分时行情")\
                .with_required_params("symbol", "period")\
                .with_optional_params("adjust", "start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "hk", "stock", "min", "东方财富网")\
                .with_example_params({"symbol": '000001', "period": '1', "adjust": 'qfq', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_hk_main_board_spot_em - 完整元数据
            create_interface("stock_hk_main_board_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("港股主板的实时行情数据; 该数据有 15 分钟延时")\
                .with_return_type("DataFrame")\
                .with_keywords("spot", "hk", "em", "stock", "board")\
                .build(),
            # stock_hk_spot - 完整元数据
            create_interface("stock_hk_spot")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("获取所有港股的实时行情数据 15 分钟延时")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "stock", "spot", "hk")\
                .build(),
            # stock_hk_spot_em - 完整元数据
            create_interface("stock_hk_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("所有港股的实时行情数据; 该数据有 15 分钟延时")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "spot", "hk", "stock", "东方财富网")\
                .build(),
            # stock_hsgt_sh_hk_spot_em - 完整元数据
            create_interface("stock_hsgt_sh_hk_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-行情中心-沪深港通-港股通(沪>港)-股票；按股票代码排序")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "spot", "hk", "em", "stock")\
                .build(),
            # stock_kc_a_spot_em - 完整元数据
            create_interface("stock_kc_a_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-科创板-实时行情")\
                .with_return_type("DataFrame")\
                .with_keywords("kc", "em", "spot", "stock", "a")\
                .build(),
            # stock_zh_kcb_daily - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # adjust: ['', 'qfq', 'hfq']
            create_interface("stock_zh_kcb_daily")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("新浪财经-科创板股票历史行情数据")\
                .with_required_params("symbol")\
                .with_optional_params("adjust")\
                .with_return_type("DataFrame")\
                .with_keywords("daily", "股票", "zh", "新浪财经", "stock")\
                .with_example_params({"symbol": '000001', "adjust": ''})\
                .build(),
            # stock_zh_kcb_spot - 完整元数据
            create_interface("stock_zh_kcb_spot")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("新浪财经-科创板股票实时行情数据")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "zh", "spot", "新浪财经", "stock")\
                .build(),
            # stock_us_daily - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # adjust: ['', 'qfq', 'hfq']
            create_interface("stock_us_daily")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("美股历史行情数据，设定 adjust=\"qfq\" 则返回前复权后的数据，默认 adjust=\"\", 则返回未复权的数据，历史数据按日频率更新")\
                .with_required_params("symbol")\
                .with_optional_params("adjust")\
                .with_return_type("DataFrame")\
                .with_keywords("daily", "us", "stock", "新浪财经")\
                .with_example_params({"symbol": '000001', "adjust": ''})\
                .build(),
            # stock_us_famous_spot_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_us_famous_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("美股-知名美股的实时行情数据")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "spot", "stock", "us", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_us_hist - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # period: ['daily', 'weekly', 'monthly']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            # adjust: ['', 'qfq', 'hfq']
            create_interface("stock_us_hist")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-行情-美股-每日行情")\
                .with_required_params("symbol", "period", "start_date", "end_date")\
                .with_optional_params("adjust")\
                .with_return_type("DataFrame")\
                .with_keywords("hist", "us", "stock", "东方财富网")\
                .with_example_params({"symbol": '000001', "period": 'daily', "start_date": '20230101', "end_date": '20231231', "adjust": ''})\
                .build(),
            # stock_us_hist_min_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_us_hist_min_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-行情首页-美股-每日分时行情")\
                .with_required_params("symbol")\
                .with_optional_params("start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "min", "us", "东方财富网")\
                .with_example_params({"symbol": '000001', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_us_pink_spot_em - 完整元数据
            create_interface("stock_us_pink_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("美股粉单市场的实时行情数据")\
                .with_return_type("DataFrame")\
                .with_keywords("spot", "em", "stock", "pink", "us")\
                .build(),
            # stock_us_spot - 完整元数据
            create_interface("stock_us_spot")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("新浪财经-美股; 获取的数据有 15 分钟延迟; 建议使用 ak.stock_us_spot_em() 来获取数据")\
                .with_return_type("DataFrame")\
                .with_keywords("us", "stock", "spot", "新浪财经")\
                .build(),
            # stock_us_spot_em - 完整元数据
            create_interface("stock_us_spot_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_QUOTE)\
                .with_description("东方财富网-美股-实时行情")\
                .with_return_type("DataFrame")\
                .with_keywords("spot", "em", "stock", "us", "东方财富网")\
                .build(),
        ]

    def _register_stock_financial_interfaces(self) -> List[InterfaceMetadata]:
        """注册财务数据接口"""
        return [
            # stock_financial_analysis_indicator_em - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            # indicator: ['按报告期', '按单季度']
            create_interface("stock_financial_analysis_indicator_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-A股-财务分析-主要指标")\
                .with_required_params("symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("financial", "em", "A股", "财务", "stock")\
                .with_example_params({"symbol": '000001.SZ', "indicator": '按报告期'})\
                .build(),
            # stock_financial_abstract - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_financial_abstract")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("新浪财经-财务报表-关键指标")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("financial", "新浪财经", "abstract", "财务", "stock")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_financial_abstract_ths - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            # indicator: ['按报告期', '按年度', '按单季度']
            create_interface("stock_financial_abstract_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("同花顺-财务指标-主要指标")\
                .with_required_params("symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("financial", "abstract", "财务", "stock", "未明确说明")\
                .with_example_params({"symbol": '000001.SZ', "indicator": '按报告期'})\
                .build(),
            # stock_financial_benefit_ths - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            # indicator: ['按报告期', '按年度', '按单季度']
            create_interface("stock_financial_benefit_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("同花顺-财务指标-利润表")\
                .with_required_params("symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("financial", "财务", "stock", "未明确说明", "ths")\
                .with_example_params({"symbol": '000001.SZ', "indicator": '按报告期'})\
                .build(),
            # stock_financial_cash_ths - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            # indicator: ['按报告期', '按年度', '按单季度']
            create_interface("stock_financial_cash_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("同花顺-财务指标-现金流量表")\
                .with_required_params("symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("financial", "财务", "stock", "未明确说明", "cash")\
                .with_example_params({"symbol": '000001.SZ', "indicator": '按报告期'})\
                .build(),
            # stock_financial_debt_ths - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            # indicator: ['按报告期', '按年度', '按单季度']
            create_interface("stock_financial_debt_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("同花顺-财务指标-资产负债表")\
                .with_required_params("symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("financial", "财务", "stock", "未明确说明", "ths")\
                .with_example_params({"symbol": '000001.SZ', "indicator": '按报告期'})\
                .build(),
            # stock_financial_report_sina - 完整元数据
            # stock: ['sh000001', 'sz000002', 'sh600000']
            # symbol: ['sh000001', 'sz000002', 'sh600000']
            create_interface("stock_financial_report_sina")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("新浪财经-财务报表-三大报表")\
                .with_required_params("stock", "symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("financial", "新浪财经", "财务", "stock", "sina")\
                .with_example_params({"stock": 'sh000001', "symbol": 'sh000001'})\
                .build(),
            # stock_hk_profit_forecast_et - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # indicator: ['评级总览', '去年度业绩表现', '综合盈利预测']
            create_interface("stock_hk_profit_forecast_et")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("经济通-公司资料-盈利预测")\
                .with_required_params("symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("hk", "et", "stock", "forecast", "未明确说明")\
                .with_example_params({"symbol": '000001', "indicator": '评级总览'})\
                .build(),
            # stock_ipo_benefit_ths - 完整元数据
            create_interface("stock_ipo_benefit_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("同花顺-数据中心-新股数据-IPO受益股")\
                .with_return_type("DataFrame")\
                .with_keywords("ipo", "stock", "同花顺", "ths", "benefit")\
                .build(),
            # stock_profit_forecast_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_profit_forecast_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富网-数据中心-研究报告-盈利预测; 该数据源网页端返回数据有异常, 本接口已修复该异常")\
                .with_optional_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "forecast", "东方财富网", "profit")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_profit_forecast_ths - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            # indicator: ['预测年报每股收益', '预测年报净利润', '业绩预测详表-机构']
            create_interface("stock_profit_forecast_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("同花顺-盈利预测")\
                .with_required_params("symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "forecast", "未明确说明", "ths", "profit")\
                .with_example_params({"symbol": '000001.SZ', "indicator": '预测年报每股收益'})\
                .build(),
            # stock_financial_hk_analysis_indicator_em - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            # indicator: ['年度', '报告期']
            create_interface("stock_financial_hk_analysis_indicator_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-港股-财务分析-主要指标")\
                .with_required_params("symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("financial", "em", "hk", "财务", "stock")\
                .with_example_params({"symbol": '000001.SZ', "indicator": '年度'})\
                .build(),
            # stock_financial_hk_report_em - 完整元数据
            # stock: ['000001.SZ', '000002.SZ', '600000.SH']
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            # indicator: ['年度', '报告期']
            create_interface("stock_financial_hk_report_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-港股-财务报表-三大报表")\
                .with_required_params("stock", "symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("financial", "em", "hk", "财务", "stock")\
                .with_example_params({"stock": '000001.SZ', "symbol": '000001.SZ', "indicator": '年度'})\
                .build(),
            # stock_financial_us_analysis_indicator_em - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            # indicator: ['年报', '单季报', '累计季报']
            create_interface("stock_financial_us_analysis_indicator_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-美股-财务分析-主要指标")\
                .with_required_params("symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("financial", "em", "财务", "stock", "us")\
                .with_example_params({"symbol": '000001.SZ', "indicator": '年报'})\
                .build(),
            # stock_financial_us_report_em - 完整元数据
            # stock: ['000001.SZ', '000002.SZ', '600000.SH']
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            # indicator: ['年报', '单季报', '累计季报']
            create_interface("stock_financial_us_report_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-美股-财务分析-三大报表")\
                .with_required_params("stock", "symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("financial", "em", "财务", "stock", "us")\
                .with_example_params({"stock": '000001.SZ', "symbol": '000001.SZ', "indicator": '年报'})\
                .build(),
            # stock_balance_sheet_by_report_delisted_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_balance_sheet_by_report_delisted_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-股票-财务分析-资产负债表-已退市股票-按报告期")\
                .with_required_params("symbol")\
                .with_return_type("List[str]")\
                .with_keywords("股票", "em", "财务", "stock", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_balance_sheet_by_report_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_balance_sheet_by_report_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-股票-财务分析-资产负债表-按报告期")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "财务", "stock", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_balance_sheet_by_yearly_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_balance_sheet_by_yearly_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-股票-财务分析-资产负债表-按年度")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "财务", "stock", "yearly")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_cash_flow_sheet_by_quarterly_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_cash_flow_sheet_by_quarterly_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-股票-财务分析-现金流量表-按单季度")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "财务", "stock", "quarterly")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_cash_flow_sheet_by_report_delisted_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_cash_flow_sheet_by_report_delisted_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-股票-财务分析-现金流量表-已退市股票-按报告期")\
                .with_required_params("symbol")\
                .with_return_type("List[str]")\
                .with_keywords("股票", "em", "财务", "stock", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_cash_flow_sheet_by_report_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_cash_flow_sheet_by_report_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-股票-财务分析-现金流量表-按报告期")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "财务", "stock", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_cash_flow_sheet_by_yearly_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_cash_flow_sheet_by_yearly_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-股票-财务分析-现金流量表-按年度")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "财务", "stock", "yearly")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_financial_analysis_indicator - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # start_year: ['2023', '2022', '2021']
            create_interface("stock_financial_analysis_indicator")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("新浪财经-财务分析-财务指标")\
                .with_required_params("symbol", "start_year")\
                .with_return_type("DataFrame")\
                .with_keywords("financial", "新浪财经", "财务", "stock", "indicator")\
                .with_example_params({"symbol": '000001', "start_year": '2023'})\
                .build(),
            # stock_profit_sheet_by_quarterly_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_profit_sheet_by_quarterly_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-股票-财务分析-利润表-按单季度")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "财务", "stock", "quarterly")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_profit_sheet_by_report_delisted_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_profit_sheet_by_report_delisted_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-股票-财务分析-利润表-已退市股票-按报告期")\
                .with_required_params("symbol")\
                .with_return_type("List[str]")\
                .with_keywords("股票", "em", "财务", "stock", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_profit_sheet_by_report_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_profit_sheet_by_report_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-股票-财务分析-利润表-报告期")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "财务", "stock", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_profit_sheet_by_yearly_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_profit_sheet_by_yearly_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_FINANCIAL)\
                .with_description("东方财富-股票-财务分析-利润表-按年度")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "em", "财务", "stock", "yearly")\
                .with_example_params({"symbol": '000001'})\
                .build(),
        ]

    def _register_stock_technical_interfaces(self) -> List[InterfaceMetadata]:
        """注册技术指标接口"""
        return [
            # stock_a_indicator_lg - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_a_indicator_lg")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_TECHNICAL)\
                .with_description("乐咕乐股-A 股个股指标: 市盈率, 市净率, 股息率")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("lg", "stock", "a", "indicator", "乐咕乐股")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_hk_indicator_eniu - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # indicator: ['港股', '市盈率', '市净率']
            create_interface("stock_hk_indicator_eniu")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.STOCK_TECHNICAL)\
                .with_description("亿牛网-港股个股指标: 市盈率, 市净率, 股息率, ROE, 市值")\
                .with_required_params("symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("hk", "未明确说明", "stock", "indicator", "eniu")\
                .with_example_params({"symbol": '000001', "indicator": '港股'})\
                .build(),
        ]

    def _register_market_index_interfaces(self) -> List[InterfaceMetadata]:
        """注册市场指数接口"""
        return [
            # stock_board_concept_index_ths - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_board_concept_index_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.MARKET_INDEX)\
                .with_description("同花顺-板块-概念板块-指数日频率数据")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "未明确说明", "concept", "board", "index")\
                .with_example_params({"symbol": '000001.SZ', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_board_industry_index_ths - 完整元数据
            # symbol: ['000001.SZ', '000002.SZ', '600000.SH']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_board_industry_index_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.MARKET_INDEX)\
                .with_description("同花顺-板块-行业板块-指数日频率数据")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "未明确说明", "board", "industry", "index")\
                .with_example_params({"symbol": '000001.SZ', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_buffett_index_lg - 完整元数据
            create_interface("stock_buffett_index_lg")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.MARKET_INDEX)\
                .with_description("乐估乐股-底部研究-巴菲特指标")\
                .with_return_type("DataFrame")\
                .with_keywords("lg", "buffett", "stock", "index", "乐咕乐股")\
                .build(),
            # stock_index_pb_lg - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_index_pb_lg")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.MARKET_INDEX)\
                .with_description("乐咕乐股-指数市净率")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("lg", "stock", "index", "乐咕乐股", "指数")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_index_pe_lg - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_index_pe_lg")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.MARKET_INDEX)\
                .with_description("乐咕乐股-指数市盈率")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("lg", "stock", "pe", "index", "乐咕乐股")\
                .with_example_params({"symbol": '000001'})\
                .build(),
        ]

    def _register_market_overview_interfaces(self) -> List[InterfaceMetadata]:
        """注册市场概览接口"""
        return [
            # stock_board_industry_summary_ths - 完整元数据
            create_interface("stock_board_industry_summary_ths")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.MARKET_OVERVIEW)\
                .with_description("同花顺-同花顺行业一览表")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "未明确说明", "board", "industry", "ths")\
                .build(),
            # stock_ipo_summary_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_ipo_summary_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.MARKET_OVERVIEW)\
                .with_description("巨潮资讯-个股-上市相关")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("ipo", "未明确说明", "stock", "cninfo", "summary")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_restricted_release_summary_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_restricted_release_summary_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.MARKET_OVERVIEW)\
                .with_description("东方财富网-数据中心-特色数据-限售股解禁")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("release", "em", "stock", "东方财富网", "summary")\
                .with_example_params({"symbol": '000001', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_sector_fund_flow_summary - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # indicator: ['今日', '5日', '10日']
            create_interface("stock_sector_fund_flow_summary")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.MARKET_OVERVIEW)\
                .with_description("东方财富网-数据中心-资金流向-行业资金流-xx行业个股资金流")\
                .with_required_params("symbol")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("fund", "stock", "sector", "东方财富网", "summary")\
                .with_example_params({"symbol": '000001', "indicator": '今日'})\
                .build(),
            # stock_sse_summary - 完整元数据
            create_interface("stock_sse_summary")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.MARKET_OVERVIEW)\
                .with_description("上海证券交易所-股票数据总貌")\
                .with_return_type("DataFrame")\
                .with_keywords("上海证券交易所", "股票", "sse", "stock", "summary")\
                .build(),
            # stock_szse_area_summary - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_szse_area_summary")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.MARKET_OVERVIEW)\
                .with_description("深圳证券交易所-市场总貌-地区交易排序")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("area", "stock", "szse", "深圳证券交易所", "summary")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_szse_sector_summary - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_szse_sector_summary")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.MARKET_OVERVIEW)\
                .with_description("深圳证券交易所-统计资料-股票行业成交数据")\
                .with_required_params("symbol", "date")\
                .with_return_type("DataFrame")\
                .with_keywords("股票", "stock", "sector", "szse", "深圳证券交易所")\
                .with_example_params({"symbol": '000001', "date": '20231201'})\
                .build(),
            # stock_szse_summary - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_szse_summary")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.MARKET_OVERVIEW)\
                .with_description("深圳证券交易所-市场总貌-证券类别统计")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("summary", "stock", "szse", "深圳证券交易所")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_hsgt_fund_flow_summary_em - 完整元数据
            create_interface("stock_hsgt_fund_flow_summary_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.MARKET_OVERVIEW)\
                .with_description("东方财富网-数据中心-资金流向-沪深港通资金流向")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "fund", "stock", "东方财富网", "hsgt")\
                .build(),
        ]

    def _register_industry_data_interfaces(self) -> List[InterfaceMetadata]:
        """注册行业数据接口"""
        return [
            # news_report_time_baidu - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("news_report_time_baidu")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.INDUSTRY_DATA)\
                .with_description("百度股市通-财报发行")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("time", "未明确说明", "news", "baidu", "report")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # news_trade_notify_dividend_baidu - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("news_trade_notify_dividend_baidu")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.INDUSTRY_DATA)\
                .with_description("百度股市通-交易提醒-分红派息")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("未明确说明", "notify", "news", "dividend", "baidu")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # news_trade_notify_suspend_baidu - 完整元数据
            # date: ['20231201', '20231101', '20231001']
            create_interface("news_trade_notify_suspend_baidu")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.INDUSTRY_DATA)\
                .with_description("百度股市通-交易提醒-停复牌")\
                .with_required_params("date")\
                .with_return_type("DataFrame")\
                .with_keywords("suspend", "未明确说明", "notify", "news", "baidu")\
                .with_example_params({"date": '20231201'})\
                .build(),
            # stock_board_industry_cons_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_board_industry_cons_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.INDUSTRY_DATA)\
                .with_description("东方财富-沪深板块-行业板块-板块成份")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "board", "cons", "industry")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_board_industry_name_em - 完整元数据
            create_interface("stock_board_industry_name_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.INDUSTRY_DATA)\
                .with_description("东方财富-沪深京板块-行业板块")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "board", "industry", "东方财富网")\
                .build(),
            # stock_gpzy_industry_data_em - 完整元数据
            create_interface("stock_gpzy_industry_data_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.INDUSTRY_DATA)\
                .with_description("东方财富网-数据中心-特色数据-股权质押-上市公司质押比例-行业数据")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "industry", "data", "东方财富网")\
                .build(),
            # stock_industry_category_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_industry_category_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.INDUSTRY_DATA)\
                .with_description("巨潮资讯-数据-行业分类数据")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "未明确说明", "cninfo", "industry", "category")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_industry_change_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # start_date: ['20230101', '20230301', '20230601']
            # end_date: ['20231231', '20230331', '20230630']
            create_interface("stock_industry_change_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.INDUSTRY_DATA)\
                .with_description("巨潮资讯-数据-上市公司行业归属的变动情况")\
                .with_required_params("symbol", "start_date", "end_date")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "未明确说明", "cninfo", "change", "industry")\
                .with_example_params({"symbol": '000001', "start_date": '20230101', "end_date": '20231231'})\
                .build(),
            # stock_industry_pe_ratio_cninfo - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_industry_pe_ratio_cninfo")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.INDUSTRY_DATA)\
                .with_description("巨潮资讯-数据中心-行业分析-行业市盈率")\
                .with_required_params("symbol", "date")\
                .with_return_type("DataFrame")\
                .with_keywords("stock", "未明确说明", "ratio", "pe", "cninfo")\
                .with_example_params({"symbol": '000001', "date": '20231201'})\
                .build(),
            # stock_news_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_news_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.INDUSTRY_DATA)\
                .with_description("东方财富指定个股的新闻资讯数据")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "stock", "news", "新闻", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_news_main_cx - 完整元数据
            create_interface("stock_news_main_cx")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.INDUSTRY_DATA)\
                .with_description("财新网-财新数据通-内容精选")\
                .with_return_type("DataFrame")\
                .with_keywords("cx", "stock", "news", "财新网", "main")\
                .build(),
            # stock_report_disclosure - 完整元数据
            # market: ['沪深京', '深市', '深主板']
            # period: ['2021一季', '2021半年报', '2021三季']
            create_interface("stock_report_disclosure")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.INDUSTRY_DATA)\
                .with_description("巨潮资讯-数据-预约披露的数据")\
                .with_required_params("period")\
                .with_optional_params("market")\
                .with_return_type("DataFrame")\
                .with_keywords("未明确说明", "stock", "report", "disclosure")\
                .with_example_params({"market": '沪深京', "period": '2021一季'})\
                .build(),
            # stock_research_report_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_research_report_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.INDUSTRY_DATA)\
                .with_description("东方财富网-数据中心-研究报告-个股研报")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "research", "stock", "东方财富网", "report")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_sector_detail - 完整元数据
            # sector: ['银行', '消费', '科技']
            create_interface("stock_sector_detail")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.INDUSTRY_DATA)\
                .with_description("新浪行业-板块行情-成份详情, 由于新浪网页提供的统计数据有误, 部分行业数量大于统计数")\
                .with_required_params("sector")\
                .with_return_type("int")\
                .with_keywords("新浪财经", "stock", "sector", "detail", "行业")\
                .with_example_params({"sector": '银行'})\
                .build(),
            # stock_zh_kcb_report_em - 完整元数据
            # from_page: [1, 5, 10]
            # to_page: [1, 5, 10]
            create_interface("stock_zh_kcb_report_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.INDUSTRY_DATA)\
                .with_description("东方财富-科创板报告数据")\
                .with_required_params("from_page", "to_page")\
                .with_return_type("DataFrame")\
                .with_keywords("zh", "em", "stock", "东方财富网", "kcb")\
                .with_example_params({"from_page": 1, "to_page": 1})\
                .build(),
        ]

    def _register_fund_data_interfaces(self) -> List[InterfaceMetadata]:
        """注册基金接口"""
        return [
            # stock_fund_flow_big_deal - 完整元数据
            create_interface("stock_fund_flow_big_deal")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FUND_DATA)\
                .with_description("同花顺-数据中心-资金流向-大单追踪")\
                .with_return_type("DataFrame")\
                .with_keywords("fund", "big", "stock", "deal", "同花顺")\
                .build(),
            # stock_fund_flow_concept - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_fund_flow_concept")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FUND_DATA)\
                .with_description("同花顺-数据中心-资金流向-概念资金流")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("fund", "stock", "concept", "同花顺", "flow")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_fund_flow_individual - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_fund_flow_individual")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FUND_DATA)\
                .with_description("同花顺-数据中心-资金流向-个股资金流")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("fund", "stock", "同花顺", "individual", "flow")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_fund_flow_industry - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_fund_flow_industry")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FUND_DATA)\
                .with_description("同花顺-数据中心-资金流向-行业资金流")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("fund", "stock", "industry", "同花顺", "flow")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_fund_stock_holder - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_fund_stock_holder")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FUND_DATA)\
                .with_description("新浪财经-股本股东-基金持股")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("新浪财经", "fund", "stock", "holder", "基金")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_individual_fund_flow - 完整元数据
            # stock: ['000001', 'sh000001', '000001.SZ']
            # market: ['all', 'sh', 'sz']
            create_interface("stock_individual_fund_flow")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FUND_DATA)\
                .with_description("东方财富网-数据中心-个股资金流向")\
                .with_required_params("stock")\
                .with_optional_params("market")\
                .with_return_type("DataFrame")\
                .with_keywords("fund", "stock", "东方财富网", "individual", "flow")\
                .with_example_params({"stock": '000001', "market": 'all'})\
                .build(),
            # stock_individual_fund_flow_rank - 完整元数据
            # indicator: ['按报告期', '按单季度', '按年度']
            create_interface("stock_individual_fund_flow_rank")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FUND_DATA)\
                .with_description("东方财富网-数据中心-资金流向-排名")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("fund", "stock", "东方财富网", "individual", "flow")\
                .with_example_params({"indicator": '按报告期'})\
                .build(),
            # stock_main_fund_flow - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            create_interface("stock_main_fund_flow")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FUND_DATA)\
                .with_description("东方财富网-数据中心-资金流向-主力净流入排名")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("fund", "stock", "东方财富网", "main", "flow")\
                .with_example_params({"symbol": '000001'})\
                .build(),
            # stock_market_fund_flow - 完整元数据
            create_interface("stock_market_fund_flow")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FUND_DATA)\
                .with_description("东方财富网-数据中心-资金流向-大盘")\
                .with_return_type("DataFrame")\
                .with_keywords("fund", "stock", "market", "东方财富网", "flow")\
                .build(),
            # stock_report_fund_hold - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_report_fund_hold")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FUND_DATA)\
                .with_description("东方财富网-数据中心-主力数据-基金持仓")\
                .with_required_params("symbol", "date")\
                .with_return_type("DataFrame")\
                .with_keywords("fund", "stock", "hold", "东方财富网", "基金")\
                .with_example_params({"symbol": '000001', "date": '20231201'})\
                .build(),
            # stock_report_fund_hold_detail - 完整元数据
            # symbol: ['000001', 'sh000001', '000001.SZ']
            # date: ['20231201', '20231101', '20231001']
            create_interface("stock_report_fund_hold_detail")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FUND_DATA)\
                .with_description("东方财富网-数据中心-主力数据-基金持仓-基金持仓明细表")\
                .with_required_params("symbol", "date")\
                .with_return_type("DataFrame")\
                .with_keywords("fund", "基金", "stock", "东方财富网", "detail")\
                .with_example_params({"symbol": '000001', "date": '20231201'})\
                .build(),
            # stock_sector_fund_flow_rank - 完整元数据
            # indicator: ['今日', '5日', '10日']
            # sector_type: ['行业资金流', '概念资金流', '地域资金流']
            create_interface("stock_sector_fund_flow_rank")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FUND_DATA)\
                .with_description("东方财富网-数据中心-资金流向-板块资金流-排名")\
                .with_required_params("sector_type")\
                .with_optional_params("indicator")\
                .with_return_type("DataFrame")\
                .with_keywords("fund", "stock", "sector", "东方财富网", "flow")\
                .with_example_params({"indicator": '今日', "sector_type": '行业资金流'})\
                .build(),
            # stock_hsgt_fund_min_em - 完整元数据
            # symbol: ['000001', '000002', '600000']
            create_interface("stock_hsgt_fund_min_em")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FUND_DATA)\
                .with_description("东方财富-数据中心-沪深港通-市场概括-分时数据")\
                .with_required_params("symbol")\
                .with_return_type("DataFrame")\
                .with_keywords("em", "fund", "stock", "min", "东方财富网")\
                .with_example_params({"symbol": '000001'})\
                .build(),
        ]

    def _register_forex_data_interfaces(self) -> List[InterfaceMetadata]:
        """注册外汇接口"""
        return [
            # stock_sgt_reference_exchange_rate_sse - 完整元数据
            create_interface("stock_sgt_reference_exchange_rate_sse")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FOREX_DATA)\
                .with_description("沪港通-港股通信息披露-参考汇率")\
                .with_return_type("DataFrame")\
                .with_keywords("上海证券交易所", "rate", "exchange", "sse", "stock")\
                .build(),
            # stock_sgt_reference_exchange_rate_szse - 完整元数据
            create_interface("stock_sgt_reference_exchange_rate_szse")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FOREX_DATA)\
                .with_description("深港通-港股通业务信息-参考汇率")\
                .with_return_type("DataFrame")\
                .with_keywords("rate", "exchange", "stock", "reference", "szse")\
                .build(),
            # stock_sgt_settlement_exchange_rate_sse - 完整元数据
            create_interface("stock_sgt_settlement_exchange_rate_sse")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FOREX_DATA)\
                .with_description("沪港通-港股通信息披露-结算汇兑")\
                .with_return_type("DataFrame")\
                .with_keywords("上海证券交易所", "rate", "exchange", "sse", "stock")\
                .build(),
            # stock_sgt_settlement_exchange_rate_szse - 完整元数据
            create_interface("stock_sgt_settlement_exchange_rate_szse")\
                .with_source(DataSource.AKSHARE)\
                .with_category(FunctionCategory.FOREX_DATA)\
                .with_description("深港通-港股通业务信息-结算汇率")\
                .with_return_type("DataFrame")\
                .with_keywords("rate", "exchange", "stock", "sgt", "szse")\
                .build(),
        ]


# 创建提供者实例
akshare_provider = AkshareProvider()