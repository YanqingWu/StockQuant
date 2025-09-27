"""数据提取管理器
为每种数据类型提供专门的提取接口，基于配置文件进行字段映射和过滤，集成标准参数和task manager
"""

import logging
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, date
import pandas as pd
from .config_loader import ConfigLoader, ExtractionConfig
from .adapter import to_standard_params, StandardParams, AkshareStockParamAdapter
from ..interfaces.executor import TaskManager, InterfaceExecutor, CallTask, ExecutionContext, ExecutorConfig, RetryConfig, CacheConfig
from ..interfaces.base import api_provider_manager

logger = logging.getLogger(__name__)


@dataclass
class ExtractionResult:
    """提取结果"""
    success: bool
    data: Any
    error: Optional[str] = None
    interface_name: Optional[str] = None  # 添加接口名称字段
    source_interface: Optional[str] = None
    extracted_fields: Optional[List[str]] = None


class ExtractorManager:
    """
    数据提取管理器
    为每种数据类型提供专门的提取接口，基于配置文件进行字段映射和过滤
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化提取管理器
        
        Args:
            config_path: 配置文件路径，如果不提供则使用默认路径
        """
        self.config_loader = ConfigLoader()
        
        # 加载配置文件
        if config_path is None:
            # 使用默认配置文件路径
            current_dir = Path(__file__).parent
            config_path = current_dir / "extraction_config.yaml"
        
        self.config = self.config_loader.load_config()
        
        # 初始化task manager和executor
        self.provider_manager = api_provider_manager
        
        # 从全局配置注入执行器配置（缓存/重试/超时）
        global_cfg = self.config.global_config
        self.executor_config = ExecutorConfig(
            cache_config=CacheConfig(
                enabled=bool(global_cfg.enable_cache),
                ttl=int(global_cfg.default_cache_duration),
            ),
            retry_config=RetryConfig(
                max_retries=int(global_cfg.retry_count)
            ),
        )
        # 仅在配置中提供了正数超时时才覆盖默认值
        try:
            _cfg_timeout = float(getattr(global_cfg, "timeout", 0))
            if _cfg_timeout > 0:
                self.executor_config.default_timeout = _cfg_timeout
        except Exception:
            pass
        self.executor = InterfaceExecutor(self.provider_manager, self.executor_config)
        self.task_manager = TaskManager(self.executor)
        
        logger.info(f"ExtractorManager 初始化完成，配置版本: {self.config.version}")
    
    def _apply_field_mapping(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        应用字段映射，将中文字段名转换为英文标准字段名
        
        Args:
            data: 原始数据字典
            
        Returns:
            映射后的数据字典
        """
        if not data:
            return data
            
        mapped_data = {}
        for key, value in data.items():
            # 查找字段映射
            mapped_key = self.config.get_field_mapping(key)
            mapped_data[mapped_key] = value
            
        return mapped_data
    
    def _filter_standard_fields(self, data: Dict[str, Any], category: str, data_type: str) -> Dict[str, Any]:
        """
        过滤标准字段，只保留配置文件中定义的字段
        
        Args:
            data: 数据字典
            category: 数据分类
            data_type: 数据类型
            
        Returns:
            过滤后的数据字典
        """
        if not data:
            return data
            
        standard_fields = self.config.get_standard_fields(category, data_type)
        if not standard_fields:
            logger.warning(f"未找到 {category}.{data_type} 的标准字段定义")
            return data
            
        filtered_data = {}
        for field in standard_fields:
            if field in data:
                filtered_data[field] = data[field]
            else:
                logger.debug(f"字段 '{field}' 在数据中不存在")
                
        return filtered_data
    
    def _process_extraction_result(self, raw_data: Any, category: str, data_type: str, 
                                 interface_name: str) -> ExtractionResult:
        """
        处理提取结果，统一返回 pandas.DataFrame：
        - 对列名应用字段映射
        - 按标准字段进行列过滤
        """
        try:
            if raw_data is None:
                return ExtractionResult(
                    success=False,
                    data=None,
                    interface_name=interface_name,
                    error="接口返回空数据",
                    source_interface=interface_name
                )

            # 统一转换为 DataFrame
            df: Optional[pd.DataFrame] = None
            if isinstance(raw_data, pd.DataFrame):
                df = raw_data.copy()
            elif isinstance(raw_data, list):
                try:
                    df = pd.DataFrame(raw_data)
                except Exception as _e:
                    return ExtractionResult(
                        success=False,
                        data=None,
                        interface_name=interface_name,
                        error=f"无法将列表数据转换为DataFrame: {_e}",
                        source_interface=interface_name
                    )
            elif isinstance(raw_data, dict):
                try:
                    df = pd.DataFrame([raw_data])
                except Exception as _e:
                    return ExtractionResult(
                        success=False,
                        data=None,
                        interface_name=interface_name,
                        error=f"无法将字典数据转换为DataFrame: {_e}",
                        source_interface=interface_name
                    )
            elif isinstance(raw_data, str):
                # 处理字符串类型数据，尝试解析为更有意义的结构
                try:
                    # 对于字符串，尝试解析为股票代码格式
                    if raw_data and len(raw_data) >= 6:
                        # 尝试解析为股票代码格式 (如 "sz000300")
                        if raw_data.startswith(('sz', 'sh', 'bj')):
                            market = raw_data[:2].upper()
                            code = raw_data[2:]
                            df = pd.DataFrame([{
                                "symbol": f"{code}.{market}",
                                "code": code,
                                "market": market,
                                "raw_value": raw_data
                            }])
                        else:
                            # 其他字符串，创建基本结构
                            df = pd.DataFrame([{
                                "symbol": raw_data,
                                "raw_value": raw_data
                            }])
                    else:
                        # 空字符串或太短的字符串
                        df = pd.DataFrame([{"raw_value": raw_data}])
                except Exception as _e:
                    return ExtractionResult(
                        success=False,
                        data=None,
                        interface_name=interface_name,
                        error=f"无法将字符串数据转换为DataFrame: {_e}",
                        source_interface=interface_name
                    )
            else:
                return ExtractionResult(
                    success=False,
                    data=None,
                    interface_name=interface_name,
                    error=f"不支持的数据类型: {type(raw_data)}",
                    source_interface=interface_name
                )

            # 判空
            if df is None or df.empty:
                return ExtractionResult(
                    success=False,
                    data=None,
                    interface_name=interface_name,
                    error="空数据",
                    source_interface=interface_name
                )

            # 列名映射
            try:
                col_mapping = {col: self.config.get_field_mapping(col) for col in df.columns}
                df = df.rename(columns=col_mapping)
            except Exception as _e:
                logger.debug(f"列名映射失败，继续使用原列名: {_e}")

            # 列过滤（标准字段）
            try:
                # 标准字段过滤：仅当配置存在且有匹配列时才进行裁剪；否则保持原列不动
                standard_fields = self.config.get_standard_fields(category, data_type)
                if standard_fields:
                    keep_cols = [c for c in df.columns if c in standard_fields]
                    if keep_cols:
                        df = df[keep_cols]
                    else:
                        logger.debug(
                            f"标准字段 {category}.{data_type} 配置为 {standard_fields}，但返回列 {list(df.columns)} 无匹配，跳过裁剪保留原列"
                        )
            except Exception as _e:
                logger.debug(f"标准字段过滤失败，保留原列: {_e}")

            # 若无数据（空 DataFrame），则判定失败；仅列不匹配不视为失败
            if df is None or df.empty:
                return ExtractionResult(
                    success=False,
                    data=None,
                    interface_name=interface_name,
                    error="空数据",
                    source_interface=interface_name
                )

            return ExtractionResult(
                success=True,
                data=df,
                interface_name=interface_name,
                source_interface=interface_name,
                extracted_fields=list(df.columns)
            )

        except Exception as e:
            logger.error(f"处理提取结果时发生错误: {e}")
            return ExtractionResult(
                success=False,
                data=None,
                interface_name=interface_name,
                error=str(e),
                source_interface=interface_name
            )
    
    def _execute_interface(self, category: str, data_type: str, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """
        执行指定数据类型的接口，使用标准参数和task manager
        
        Args:
            category: 数据分类
            data_type: 数据类型
            params: 接口参数（支持StandardParams或Dict）
            
        Returns:
            提取结果
        """
        # 标准化参数
        standard_params = to_standard_params(params)
        params_dict = standard_params.to_dict()
        
        # 从参数中提取市场信息用于接口筛选
        market = None
        if standard_params.symbol and hasattr(standard_params.symbol, 'market'):
            market = standard_params.symbol.market
        elif standard_params.market:
            market = standard_params.market
        
        # 获取启用的接口列表，根据市场进行筛选
        interfaces = self.config.get_enabled_interfaces(category, data_type, market)
        if not interfaces:
            market_info = f" (市场: {market})" if market else ""
            return ExtractionResult(
                success=False,
                data=None,
                error=f"未找到启用的接口: {category}.{data_type}{market_info}"
            )
        
        # 初始化参数适配器
        param_adapter = AkshareStockParamAdapter()
        
        # 构造执行上下文
        context = ExecutionContext(
            cache_enabled=bool(self.config.global_config.enable_cache),
            user_data={"category": category, "data_type": data_type}
        )
        
        # 使用全局 TaskManager 批量构建并执行任务（按接口优先级）
        # 先为每个接口构建任务并入队
        for interface in interfaces:
            try:
                logger.info(f"准备加入批量任务: {interface.name}")
                try:
                    adapted_params = param_adapter.adapt(interface.name, params_dict)
                except Exception as _e:
                    logger.debug(f"参数适配失败，回退原始参数: {interface.name}, err={_e}")
                    adapted_params = params_dict
                task = CallTask(interface_name=interface.name, params=adapted_params)
                self.task_manager.add_task(task)
            except Exception as e:
                logger.error(f"构建接口 {interface.name} 任务时发生错误: {e}")
                continue

        # 批量执行
        batch_result = self.task_manager.execute_all(context=context)

        # 按接口优先级选择第一个成功结果
        if batch_result and batch_result.results:
            for interface in interfaces:
                # 查找该接口的结果
                matched = [r for r in batch_result.results if r.interface_name == interface.name]
                if not matched:
                    logger.warning(f"接口 {interface.name} 未返回结果")
                    continue
                result = matched[0]
                if result.success:
                    extraction_result = self._process_extraction_result(result.data, category, data_type, interface.name)
                    if extraction_result.success:
                        logger.info(f"接口 {interface.name} 执行成功")
                        return extraction_result
                    else:
                        logger.warning(f"接口 {interface.name} 数据处理失败: {extraction_result.error}")
                else:
                    logger.warning(f"接口 {interface.name} 执行失败: {result.error}")
                
        # 返回失败结果
        return ExtractionResult(
            success=False,
            data=None,
            interface_name=None,
            error=f"所有接口执行失败: {category}.{data_type}"
        )
    
    # ==================== 股票相关接口 ====================
    
    # 股票基础信息
    def get_stock_profile(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取股票基础信息"""
        return self._execute_interface("stock", "profile", params)
    
    def get_stock_company_profile(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取公司详细信息"""
        return self._execute_interface("stock", "company_profile", params)
    
    # 股票行情数据
    def get_stock_daily_quote(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取股票日行情数据"""
        return self._execute_interface("stock", "daily_market.quote", params)
    
    def get_stock_financing_data(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取融资融券数据"""
        return self._execute_interface("stock", "daily_market.financing", params)
    
    def get_stock_cost_distribution(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取成本分布数据"""
        return self._execute_interface("stock", "daily_market.cost_distribution", params)
    
    def get_stock_fund_flow(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取股票资金流向数据"""
        return self._execute_interface("stock", "daily_market.fund_flow", params)
    
    def get_stock_dragon_tiger(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取龙虎榜数据"""
        return self._execute_interface("stock", "daily_market.dragon_tiger", params)
    
    def get_stock_sentiment(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取股票情绪数据"""
        return self._execute_interface("stock", "daily_market.sentiment", params)
    
    def get_stock_news(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取股票新闻数据"""
        return self._execute_interface("stock", "daily_market.news", params)
    
    # 股票财务数据
    def get_stock_balance_sheet(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取资产负债表"""
        return self._execute_interface("stock", "financials.balance_sheet", params)
    
    def get_stock_income_statement(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取利润表"""
        return self._execute_interface("stock", "financials.income_statement", params)
    
    def get_stock_cash_flow(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取现金流量表"""
        return self._execute_interface("stock", "financials.cash_flow", params)
    
    # ==================== 市场相关接口 ====================
    
    # 市场股票列表
    def get_stock_list(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取市场股票列表"""
        return self._execute_interface("market", "stock_list", params)
    
    # 市场概览
    def get_market_overview(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取市场概览数据"""
        return self._execute_interface("market", "market_overview", params)
    
    def get_market_indices(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取市场指数数据"""
        return self._execute_interface("market", "market_indices", params)
    
    def get_market_activity(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取市场活跃度数据"""
        return self._execute_interface("market", "market_activity", params)
    
    # 行业板块
    def get_industry_sector_metadata(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取行业板块元数据"""
        return self._execute_interface("market", "industry_sector.metadata", params)
    
    def get_industry_sector_quote(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取行业板块行情"""
        return self._execute_interface("market", "industry_sector.quote", params)
    
    def get_industry_sector_constituents(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取行业板块成分股"""
        return self._execute_interface("market", "industry_sector.constituents", params)
    
    # 概念板块
    def get_concept_sector_metadata(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取概念板块元数据"""
        return self._execute_interface("market", "concept_sector.metadata", params)
    
    def get_concept_sector_quote(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取概念板块行情"""
        return self._execute_interface("market", "concept_sector.quote", params)
    
    def get_concept_sector_constituents(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取概念板块成分股"""
        return self._execute_interface("market", "concept_sector.constituents", params)
    
    # 板块实时行情
    def get_sector_spot_data(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取板块实时行情"""
        return self._execute_interface("market", "sector_spot", params)
    
    # 技术分析
    def get_technical_indicators(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取技术指标数据"""
        return self._execute_interface("market", "technical_analysis.indicators", params)
    
    def get_technical_ranking(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取技术分析排名数据"""
        return self._execute_interface("market", "technical_analysis.ranking", params)
    
    # ==================== 工具方法 ====================
    
    def get_available_data_types(self) -> Dict[str, List[str]]:
        """
        获取所有可用的数据类型
        
        Returns:
            数据分类和数据类型的映射
        """
        result = {}
        for category_name, category_config in self.config.interfaces_config.items():
            enabled_types = list(category_config.get_enabled_data_types().keys())
            if enabled_types:
                result[category_name] = enabled_types
        return result
    
    def get_standard_fields(self, category: str, data_type: str) -> List[str]:
        """
        获取指定数据类型的标准字段列表
        
        Args:
            category: 数据分类
            data_type: 数据类型
            
        Returns:
            标准字段列表
        """
        return self.config.get_standard_fields(category, data_type)
    
    def reload_config(self) -> None:
        """重新加载配置文件"""
        self.config = self.config_loader.reload()
        logger.info("配置文件已重新加载")