"""
数据服务 - 作为对外的唯一出口
提供用户友好的接口，简化参数传递
"""

from typing import Optional, Union, List, Dict, Any
from datetime import date
from .extractor import Extractor
from .adapters import to_standard_params, StandardParams
from .extractor.types import ExtractionResult
from core.logging import get_logger

logger = get_logger(__name__)

# 类型别名
Symbols = Union[str, List[str]]  # 股票代码，支持单个或批量
DateRange = Union[date, str]     # 日期，支持date对象或字符串


class DataService:
    """数据服务 - 用户友好的接口"""
    
    def __init__(self):
        """
        初始化数据服务
        """
        self.extractor = Extractor()
        logger.info("数据服务初始化完成")
    
    # ==================== 工具方法 ====================
    
    def _build_standard_params(self, **kwargs) -> Union[StandardParams, List[StandardParams]]:
        """
        构建StandardParams对象 - 直接利用to_standard_params的转换能力
        
        Args:
            **kwargs: 参数字典
        
        Returns:
            StandardParams对象或列表
        """
        # 处理symbols参数
        if 'symbols' in kwargs and kwargs['symbols']:
            symbols = kwargs['symbols']
            kwargs.pop('symbols')
            
            # 处理批量参数
            if isinstance(symbols, list):
                # 为每个股票创建参数，保留其他所有参数
                return [self._create_single_params(**{**kwargs, 'symbol': s}) for s in symbols]
            else:
                return self._create_single_params(**kwargs)
        else:
            return self._create_single_params(**kwargs)
    
    def _create_single_params(self, **kwargs) -> StandardParams:
        """
        创建单个StandardParams对象 - 直接传值给to_standard_params
        
        Args:
            **kwargs: 参数字典
        
        Returns:
            StandardParams对象
        """
        # 直接使用to_standard_params，它会处理所有转换和校验
        return to_standard_params(kwargs)
    
    # ==================== 股票基础信息 ====================
    
    def get_stock_profile(self, 
                         symbols: Symbols) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取股票基础信息
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
        
        Returns:
            单个股票返回ExtractionResult，多个股票返回List[ExtractionResult]
        """
        params = self._build_standard_params(symbols=symbols)
        return self.extractor.get_stock_profile(params)
    
    # ==================== 股票行情数据 ====================
    
    def get_stock_daily_quote(self,
                             symbols: Symbols,
                             start_date: Optional[DateRange] = None,
                             end_date: Optional[DateRange] = None,
                             period: str = "daily",
                             adjust: str = "qfq") -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取股票日行情数据
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
            start_date: 开始日期，格式 "2023-01-01" 或 date(2023, 1, 1)
            end_date: 结束日期，格式 "2023-12-31" 或 date(2023, 12, 31)
            period: 数据周期，默认"daily"，支持 daily/1min/5min/15min/30min/60min
            adjust: 复权类型，默认"qfq"，支持 none/qfq/hfq
        
        Returns:
            单个股票返回ExtractionResult，多个股票返回List[ExtractionResult]
        """
        params = self._build_standard_params(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            period=period,
            adjust=adjust
        )
        return self.extractor.get_stock_daily_quote(params)
    
    def get_stock_financing_data(self,
                                symbols: Symbols,
                                start_date: Optional[DateRange] = None,
                                end_date: Optional[DateRange] = None) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取融资融券数据
        
        Args:
            symbols: 股票代码
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            融资融券数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            date=start_date
        )
        return self.extractor.get_stock_financing_data(params)
    
    def get_stock_cost_distribution(self,
                                   symbols: Symbols,
                                   adjust: str = "qfq") -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取成本分布数据
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
            adjust: 复权类型，默认"qfq"，支持 none/qfq/hfq
        
        Returns:
            成本分布数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            adjust=adjust
        )
        return self.extractor.get_stock_cost_distribution(params)
    
    def get_stock_fund_flow(self,
                           symbols: Symbols,
                           start_date: Optional[DateRange] = None,
                           end_date: Optional[DateRange] = None) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取股票资金流向数据
        
        Args:
            symbols: 股票代码
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            股票资金流向数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            date=start_date
        )
        return self.extractor.get_stock_fund_flow(params)
    
    def get_stock_dragon_tiger(self,
                              symbols: Symbols,
                              start_date: Optional[DateRange] = None,
                              end_date: Optional[DateRange] = None) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取龙虎榜数据
        
        Args:
            symbols: 股票代码
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            龙虎榜数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            date=start_date
        )
        return self.extractor.get_stock_dragon_tiger(params)
    
    def get_stock_sentiment(self,
                           symbols: Symbols,
                           date: Optional[str] = None) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取股票情绪数据
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
            date: 指定日期，格式 "2023-01-01"
        
        Returns:
            股票情绪数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            date=date
        )
        return self.extractor.get_stock_sentiment(params)
    
    def get_stock_news(self,
                      symbols: Symbols) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取股票新闻数据
        
        Args:
            symbols: 股票代码
        
        Returns:
            股票新闻数据
        """
        params = self._build_standard_params(symbols=symbols)
        return self.extractor.get_stock_news(params)
    
    # ==================== 股票财务数据 ====================
    
    def get_stock_basic_indicators(self,
                                  symbols: Symbols,
                                  indicator: Optional[str] = None) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取基础财务指标
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
            indicator: 财务指标类型，如 "roe", "pe" 等
        
        Returns:
            基础财务指标数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            indicator=indicator
        )
        return self.extractor.get_stock_basic_indicators(params)
    
    def get_stock_balance_sheet(self,
                               symbols: Symbols,
                               indicator: Optional[str] = None) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取资产负债表
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
            indicator: 财务指标类型，如 "debt" 等
        
        Returns:
            资产负债表数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            indicator=indicator
        )
        return self.extractor.get_stock_balance_sheet(params)
    
    def get_stock_income_statement(self,
                                  symbols: Symbols,
                                  indicator: Optional[str] = None,
                                  date: Optional[str] = None) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取利润表
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
            indicator: 财务指标类型，如 "benefit" 等
            date: 指定日期，格式 "2023-01-01"
        
        Returns:
            利润表数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            indicator=indicator,
            date=date
        )
        return self.extractor.get_stock_income_statement(params)
    
    def get_stock_cash_flow(self,
                           symbols: Symbols,
                           indicator: Optional[str] = None,
                           date: Optional[str] = None) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取现金流量表
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
            indicator: 财务指标类型，如 "cash" 等
            date: 指定日期，格式 "2023-01-01"
        
        Returns:
            现金流量表数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            indicator=indicator,
            date=date
        )
        return self.extractor.get_stock_cash_flow(params)
    
    def get_stock_dividend(self,
                          symbols: Symbols,
                          indicator: Optional[str] = None,
                          date: Optional[str] = None) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取分红数据
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
            indicator: 财务指标类型，如 "dividend" 等
            date: 指定日期，格式 "2023-01-01"
        
        Returns:
            分红数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            indicator=indicator,
            date=date
        )
        return self.extractor.get_stock_dividend(params)
    
    # ==================== 股票持仓数据 ====================
    
    def get_stock_institutional_holdings(self,
                                        symbols: Symbols,
                                        date: Optional[str] = None) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取机构持仓数据
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
            date: 指定日期，格式 "2023-01-01"
        
        Returns:
            机构持仓数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            date=date
        )
        return self.extractor.get_stock_institutional_holdings(params)
    
    def get_stock_hsgt_holdings(self,
                               symbols: Symbols,
                               start_date: Optional[DateRange] = None,
                               end_date: Optional[DateRange] = None,
                               market: Optional[str] = None,
                               indicator: Optional[str] = None) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取沪深港通持仓数据
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
            start_date: 开始日期，格式 "2023-01-01"
            end_date: 结束日期，格式 "2023-01-01"
            market: 市场代码，如 "SZ", "SH" 等
            indicator: 指标类型，如 "hold" 等
        
        Returns:
            沪深港通持仓数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            market=market,
            indicator=indicator
        )
        return self.extractor.get_stock_hsgt_holdings(params)
    
    # ==================== 股票研究分析数据 ====================
    
    def get_stock_research_reports(self,
                                  symbols: Symbols,
                                  indicator: Optional[str] = None,
                                  year: Optional[str] = None) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取研报数据
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
            indicator: 指标类型，如 "rating" 等
            year: 年份，如 "2023"
        
        Returns:
            研报数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            indicator=indicator,
            year=year
        )
        return self.extractor.get_stock_research_reports(params)
    
    def get_stock_forecast_consensus(self,
                                    symbols: Symbols,
                                    indicator: Optional[str] = None,
                                    date: Optional[str] = None) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取预测共识数据
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
            indicator: 指标类型，如 "profit" 等
            date: 指定日期，格式 "2023-01-01"
        
        Returns:
            预测共识数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            indicator=indicator,
            date=date
        )
        return self.extractor.get_stock_forecast_consensus(params)
    
    # ==================== 股票技术分析 ====================
    
    def get_stock_innovation_high_ranking(self,
                                   symbols: Symbols) -> ExtractionResult:
        """
        获取创新高股票排名
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
        
        Returns:
            创新高股票排名数据
        """
        params = self._build_standard_params(symbols=symbols)
        return self.extractor.get_stock_innovation_high_ranking(params)
    
    def get_stock_innovation_low_ranking(self,
                                  symbols: Symbols) -> ExtractionResult:
        """
        获取创新低股票排名
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
        
        Returns:
            创新低股票排名数据
        """
        params = self._build_standard_params(symbols=symbols)
        return self.extractor.get_stock_innovation_low_ranking(params)
    
    def get_stock_volume_price_rise_ranking(self,
                                     symbols: Symbols) -> ExtractionResult:
        """
        获取量价齐升股票排名
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
        
        Returns:
            量价齐升股票排名数据
        """
        params = self._build_standard_params(symbols=symbols)
        return self.extractor.get_stock_volume_price_rise_ranking(params)
    
    def get_stock_continuous_rise_ranking(self,
                                   symbols: Symbols) -> ExtractionResult:
        """
        获取连续上涨股票排名
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
        
        Returns:
            连续上涨股票排名数据
        """
        params = self._build_standard_params(symbols=symbols)
        return self.extractor.get_stock_continuous_rise_ranking(params)
    
    def get_stock_volume_price_fall_ranking(self,
                                     symbols: Symbols) -> ExtractionResult:
        """
        获取量价齐跌股票排名
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
        
        Returns:
            量价齐跌股票排名数据
        """
        params = self._build_standard_params(symbols=symbols)
        return self.extractor.get_stock_volume_price_fall_ranking(params)
    
    def get_stock_volume_shrink_ranking(self,
                                       symbols: Symbols) -> ExtractionResult:
        """
        获取创新缩量股票排名
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
        
        Returns:
            创新缩量股票排名数据
        """
        params = self._build_standard_params(symbols=symbols)
        return self.extractor.get_stock_volume_shrink_ranking(params)
    
    def get_stock_valuation(self,
                           symbols: Symbols) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取个股估值数据
        
        Args:
            symbols: 股票代码
        
        Returns:
            个股估值数据
        """
        params = self._build_standard_params(symbols=symbols)
        return self.extractor.get_stock_valuation(params)
    
    # ==================== 股票ESG数据 ====================
    
    def get_stock_esg_rating(self,
                            symbols: Symbols) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取股票ESG评级数据
        
        Args:
            symbols: 股票代码
        
        Returns:
            股票ESG评级数据
        """
        params = self._build_standard_params(symbols=symbols)
        return self.extractor.get_stock_esg_rating(params)
    
    # ==================== 股票事件数据 ====================
    
    def get_stock_major_contracts(self,
                                 symbols: Symbols,
                                 start_date: Optional[DateRange] = None,
                                 end_date: Optional[DateRange] = None) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取重大合同事件数据
        
        Args:
            symbols: 股票代码，标准格式如 "000001.SZ" 或 ["000001.SZ", "600519.SH"]
            start_date: 开始日期，格式 "2023-01-01"
            end_date: 结束日期，格式 "2023-01-01"
        
        Returns:
            重大合同事件数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date
        )
        return self.extractor.get_stock_major_contracts(params)
    
    def get_stock_suspension(self,
                            symbols: Symbols) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取停牌事件数据
        
        Args:
            symbols: 股票代码
        
        Returns:
            停牌事件数据
        """
        params = self._build_standard_params(symbols=symbols)
        return self.extractor.get_stock_suspension(params)
    
    # ==================== 股票新股数据 ====================
    
    def get_stock_ipo_data(self,
                          symbols: Symbols) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取新股发行数据
        
        Args:
            symbols: 股票代码
        
        Returns:
            新股发行数据
        """
        params = self._build_standard_params(symbols=symbols)
        return self.extractor.get_stock_ipo_data(params)
    
    def get_stock_ipo_performance(self,
                                 symbols: Symbols) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取新股表现数据
        
        Args:
            symbols: 股票代码
        
        Returns:
            新股表现数据
        """
        params = self._build_standard_params(symbols=symbols)
        return self.extractor.get_stock_ipo_performance(params)
    
    # ==================== 股票回购数据 ====================
    
    def get_stock_repurchase_plan(self,
                                 symbols: Symbols) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取回购计划数据
        
        Args:
            symbols: 股票代码
        
        Returns:
            回购计划数据
        """
        params = self._build_standard_params(symbols=symbols)
        return self.extractor.get_stock_repurchase_plan(params)
    
    def get_stock_repurchase_progress(self,
                                     symbols: Symbols) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取回购进度数据
        
        Args:
            symbols: 股票代码
        
        Returns:
            回购进度数据
        """
        params = self._build_standard_params(symbols=symbols)
        return self.extractor.get_stock_repurchase_progress(params)
    
    # ==================== 股票大宗交易数据 ====================
    
    def get_stock_block_trading(self,
                               symbols: Symbols,
                               start_date: Optional[DateRange] = None,
                               end_date: Optional[DateRange] = None) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        获取个股大宗交易数据
        
        Args:
            symbols: 股票代码
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            个股大宗交易数据
        """
        params = self._build_standard_params(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date
        )
        return self.extractor.get_stock_block_trading(params)
    
    # ==================== 市场数据 ====================
    
    def get_stock_list(self) -> ExtractionResult:
        """
        获取市场股票列表
        
        Returns:
            市场股票列表数据
        """
        params = self._build_standard_params()
        return self.extractor.get_stock_list(params)
    
    def get_market_overview(self) -> ExtractionResult:
        """
        获取市场概览数据
        
        Returns:
            市场概览数据
        """
        params = self._build_standard_params()
        return self.extractor.get_market_overview(params)
    
    def get_market_indices(self) -> ExtractionResult:
        """
        获取市场指数数据
        
        Returns:
            市场指数数据
        """
        params = self._build_standard_params()
        return self.extractor.get_market_indices(params)
    
    def get_market_activity(self) -> ExtractionResult:
        """
        获取市场活跃度数据
        
        Returns:
            市场活跃度数据
        """
        params = self._build_standard_params()
        return self.extractor.get_market_activity(params)
    
    def get_market_sentiment(self) -> ExtractionResult:
        """
        获取市场情绪数据
        
        Returns:
            市场情绪数据
        """
        params = self._build_standard_params()
        return self.extractor.get_market_sentiment(params)
    
    # ==================== 市场资金流向数据 ====================
    
    def get_market_fund_flow(self) -> ExtractionResult:
        """
        获取市场级别资金流向数据
        
        Returns:
            市场级别资金流向数据
        """
        params = self._build_standard_params()
        return self.extractor.get_market_fund_flow(params)
    
    def get_hsgt_fund_flow(self) -> ExtractionResult:
        """
        获取沪深港通资金流向数据
        
        Returns:
            沪深港通资金流向数据
        """
        params = self._build_standard_params()
        return self.extractor.get_hsgt_fund_flow(params)
    
    def get_big_deal_tracking(self) -> ExtractionResult:
        """
        获取大单追踪数据
        
        Returns:
            大单追踪数据
        """
        params = self._build_standard_params()
        return self.extractor.get_big_deal_tracking(params)
    
    # ==================== 市场大宗交易数据 ====================
    
    def get_market_block_trading(self) -> ExtractionResult:
        """
        获取市场大宗交易统计数据
        
        Returns:
            市场大宗交易统计数据
        """
        params = self._build_standard_params()
        return self.extractor.get_market_block_trading(params)
    
    # ==================== 市场板块数据 ====================
    
    def get_sector_quote(self) -> ExtractionResult:
        """
        获取行业板块行情数据
        
        Returns:
            行业板块行情数据
        """
        params = self._build_standard_params()
        return self.extractor.get_sector_quote(params)
    
    def get_sector_constituent_quotes(self) -> ExtractionResult:
        """
        获取行业板块成分股行情数据
        
        Returns:
            行业板块成分股行情数据
        """
        params = self._build_standard_params()
        return self.extractor.get_sector_constituent_quotes(params)
    
    def get_sector_fund_flow(self) -> ExtractionResult:
        """
        获取行业板块资金流向数据
        
        Returns:
            行业板块资金流向数据
        """
        params = self._build_standard_params()
        return self.extractor.get_sector_fund_flow(params)
    
    # ==================== 市场概念数据 ====================
    
    def get_concept_quote(self) -> ExtractionResult:
        """
        获取概念板块行情数据
        
        Returns:
            概念板块行情数据
        """
        params = self._build_standard_params()
        return self.extractor.get_concept_quote(params)
    
    def get_concept_constituent_quotes(self) -> ExtractionResult:
        """
        获取概念板块成分股行情数据
        
        Returns:
            概念板块成分股行情数据
        """
        params = self._build_standard_params()
        return self.extractor.get_concept_constituent_quotes(params)
    
    def get_concept_fund_flow(self) -> ExtractionResult:
        """
        获取概念板块资金流向数据
        
        Returns:
            概念板块资金流向数据
        """
        params = self._build_standard_params()
        return self.extractor.get_concept_fund_flow(params)
    
    # ==================== 查询和管理方法 ====================
    
    def get_available_data_types(self) -> Dict[str, List[str]]:
        """
        获取所有可用的数据类型
        
        Returns:
            数据分类和数据类型的映射
        """
        return self.extractor.get_available_data_types()
    
    def get_standard_fields(self, category: str, data_type: str) -> List[str]:
        """
        获取标准字段列表
        
        Args:
            category: 数据分类
            data_type: 数据类型
        
        Returns:
            标准字段列表
        """
        return self.extractor.get_standard_fields(category, data_type)
    
    def reload_config(self) -> None:
        """
        重新加载配置
        
        Returns:
            None
        """
        self.extractor.reload_config()
        logger.info("数据服务配置已重新加载")
