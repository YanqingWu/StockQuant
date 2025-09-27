"""数据提取管理器
为每种数据类型提供专门的提取接口，基于配置文件进行字段映射和过滤，集成标准参数和task manager
"""

import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, date
import pandas as pd
from .config_loader import ConfigLoader, ExtractionConfig
from .adapter import to_standard_params, StandardParams, AkshareStockParamAdapter, StockSymbol
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
    
    def _apply_post_processor(self, data: Any, category: str, data_type: str, 
                             interface_name: str) -> Any:
        """
        应用后处理器函数
        
        Args:
            data: 原始数据
            category: 数据分类
            data_type: 数据类型
            interface_name: 接口名称
            
        Returns:
            处理后的数据
        """
        try:
            # 获取接口配置
            interface_config = self.config.get_interface_config(category, data_type, interface_name)
            if not interface_config or not interface_config.post_processor:
                logger.debug(f"接口 {interface_name} 未配置后处理器，跳过处理")
                return data
            
            # 动态导入并调用后处理器函数
            try:
                from . import post_processors
                processor_func = getattr(post_processors, interface_config.post_processor, None)
                if processor_func:
                    logger.debug(f"应用后处理器: {interface_config.post_processor}")
                    processed_data = processor_func(data)
                    logger.debug(f"后处理器 {interface_config.post_processor} 执行成功")
                    return processed_data
                else:
                    logger.warning(f"后处理器函数 {interface_config.post_processor} 不存在，跳过处理")
                    return data
            except ImportError as e:
                logger.error(f"导入后处理器模块失败: {e}")
                return data
                
        except Exception as e:
            logger.error(f"后处理器执行失败: {e}")
            return data  # 失败时返回原数据
    
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

            # 应用后处理器（在列名映射之前）
            df = self._apply_post_processor(df, category, data_type, interface_name)

            # 列名映射
            try:
                col_mapping = {col: self.config.get_field_mapping(col) for col in df.columns}
                df = df.rename(columns=col_mapping)
            except Exception as _e:
                logger.debug(f"列名映射失败，继续使用原列名: {_e}")

            # 列过滤（标准字段）
            try:
                # 标准字段过滤：确保所有标准字段都存在，即使数据为空也创建空列
                standard_fields = self.config.get_standard_fields(category, data_type)
                if standard_fields:
                    # 保留存在的标准字段
                    keep_cols = [c for c in df.columns if c in standard_fields]
                    if keep_cols:
                        df = df[keep_cols]
                    else:
                        # 如果没有匹配的列，创建一个空的DataFrame但保留原有行数
                        df = pd.DataFrame(index=df.index)
                    
                    # 为所有缺失的标准字段添加空列
                    missing_fields = [f for f in standard_fields if f not in df.columns]
                    for field in missing_fields:
                        df[field] = None  # 或者使用 pd.NA
                    
                    # 按标准字段顺序重新排列列
                    df = df[standard_fields]
                    
                    logger.debug(f"标准字段处理完成: {category}.{data_type}, 保留字段: {list(df.columns)}")
            except Exception as _e:
                logger.debug(f"标准字段过滤失败，保留原列: {_e}")

            # 转换symbol字段为统一格式
            try:
                if 'symbol' in df.columns:
                    def convert_symbol_to_unified_format(symbol_value):
                        """将symbol字段转换为统一的StockSymbol格式"""
                        if pd.isna(symbol_value) or symbol_value is None:
                            return symbol_value
                        
                        # 如果已经是StockSymbol对象，直接转换为dot格式
                        if isinstance(symbol_value, StockSymbol):
                            return symbol_value.to_dot()
                        
                        # 如果是字符串，尝试解析为StockSymbol
                        if isinstance(symbol_value, str):
                            parsed_symbol = StockSymbol.parse(symbol_value.strip())
                            if parsed_symbol:
                                return parsed_symbol.to_dot()
                            else:
                                # 如果无法解析，保持原值
                                return symbol_value
                        
                        # 其他类型，转换为字符串后尝试解析
                        try:
                            str_value = str(symbol_value).strip()
                            parsed_symbol = StockSymbol.parse(str_value)
                            if parsed_symbol:
                                return parsed_symbol.to_dot()
                            else:
                                return str_value
                        except Exception:
                            return symbol_value
                    
                    # 应用转换函数到symbol列
                    df['symbol'] = df['symbol'].apply(convert_symbol_to_unified_format)
                    logger.debug(f"已将symbol字段转换为统一格式")
            except Exception as _e:
                logger.debug(f"symbol字段转换失败，保持原格式: {_e}")

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
        执行指定数据类型的接口，使用标准参数和task manager，支持多接口数据合并
        
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

        # 收集所有成功的结果进行数据合并
        successful_results = []
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
                        successful_results.append((interface, extraction_result))
                    else:
                        logger.warning(f"接口 {interface.name} 数据处理失败: {extraction_result.error}")
                else:
                    logger.warning(f"接口 {interface.name} 执行失败: {result.error}")
        
        # 如果没有成功的结果，返回失败
        if not successful_results:
            return ExtractionResult(
                success=False,
                data=None,
                interface_name=None,
                error=f"所有接口执行失败: {category}.{data_type}"
            )
        
        # 如果只有一个成功结果，直接返回
        if len(successful_results) == 1:
            return successful_results[0][1]
        
        # 多个成功结果，进行数据合并
        logger.info(f"开始合并 {len(successful_results)} 个接口的数据")
        merged_result = self._merge_interface_results(successful_results, standard_params, category, data_type)
        
        return merged_result
    
    def _merge_interface_results(self, successful_results: List[Tuple[Any, ExtractionResult]], 
                                standard_params: StandardParams, category: str, data_type: str) -> ExtractionResult:
        """
        合并多个接口的数据结果
        
        Args:
            successful_results: 成功的接口结果列表，每个元素为(interface, extraction_result)
            standard_params: 标准化参数
            category: 数据分类
            data_type: 数据类型
            
        Returns:
            合并后的提取结果
        """
        try:
            # 获取目标股票symbol
            target_symbol = standard_params.symbol
            if not target_symbol:
                # 如果没有指定symbol，返回第一个成功结果
                return successful_results[0][1]
            
            # 按接口优先级排序
            successful_results.sort(key=lambda x: x[0].priority)
            
            # 初始化合并后的数据
            merged_data = None
            merged_interface_names = []
            
            for interface, extraction_result in successful_results:
                interface_data = extraction_result.data
                merged_interface_names.append(interface.name)
                
                if interface_data is None or interface_data.empty:
                    continue
                
                # 查找目标股票数据
                target_row = self._find_target_stock_data(interface_data, target_symbol)
                
                if target_row is not None:
                    if merged_data is None:
                        # 第一个有效数据作为基础
                        merged_data = target_row.copy()
                        logger.info(f"使用接口 {interface.name} 作为基础数据")
                    else:
                        # 合并数据，优先保留已有数据，补充缺失字段
                        merged_data = self._merge_stock_data(merged_data, target_row, interface.name)
                else:
                    logger.warning(f"接口 {interface.name} 中未找到目标股票 {target_symbol} 的数据")
            
            if merged_data is None:
                return ExtractionResult(
                    success=False,
                    data=None,
                    interface_name=None,
                    error=f"所有接口中都未找到目标股票 {target_symbol} 的数据"
                )
            
            # 将合并后的单行数据转换为DataFrame
            if isinstance(merged_data, pd.Series):
                merged_df = pd.DataFrame([merged_data])
            else:
                merged_df = merged_data
            
            logger.info(f"数据合并完成，使用了接口: {', '.join(merged_interface_names)}")
            
            return ExtractionResult(
                success=True,
                data=merged_df,
                interface_name=f"merged({', '.join(merged_interface_names)})",
                error=None
            )
            
        except Exception as e:
            logger.error(f"数据合并过程中发生错误: {e}")
            # 合并失败时返回优先级最高的结果
            return successful_results[0][1]
    
    def _find_target_stock_data(self, data: pd.DataFrame, target_symbol: StockSymbol) -> Optional[pd.Series]:
        """
        在DataFrame中查找目标股票的数据
        
        Args:
            data: 数据DataFrame
            target_symbol: 目标股票symbol
            
        Returns:
            目标股票的数据行，如果未找到返回None
        """
        if data is None or data.empty:
            return None
        
        # 使用标准的symbol格式和列名
        target_symbol_str = target_symbol.to_dot()  # 标准格式，如 "601727.SH"
        
        # 检查标准的symbol列
        if 'symbol' in data.columns:
            matched_rows = data[data['symbol'].astype(str) == target_symbol_str]
            if not matched_rows.empty:
                logger.debug(f"在symbol列中找到匹配的股票 {target_symbol_str}")
                return matched_rows.iloc[0]
        
        # 如果DataFrame只有一行数据，可能是单股票查询结果
        if len(data) == 1:
            logger.debug(f"DataFrame只有一行数据，假设为目标股票数据")
            return data.iloc[0]
        
        logger.warning(f"未找到目标股票 {target_symbol_str} 的数据")
        return None
    
    def _merge_stock_data(self, base_data: pd.Series, new_data: pd.Series, interface_name: str) -> pd.Series:
        """
        合并两个股票数据Series
        
        Args:
            base_data: 基础数据
            new_data: 新数据
            interface_name: 新数据来源接口名
            
        Returns:
            合并后的数据
        """
        merged = base_data.copy()
        
        # 统计补充的字段数量
        filled_count = 0
        
        for col in new_data.index:
            # 如果基础数据中该字段为空或不存在，则使用新数据补充
            if col not in merged.index or pd.isna(merged[col]) or merged[col] == '' or merged[col] == 0:
                if pd.notna(new_data[col]) and new_data[col] != '' and new_data[col] != 0:
                    merged[col] = new_data[col]
                    filled_count += 1
        
        if filled_count > 0:
            logger.info(f"从接口 {interface_name} 补充了 {filled_count} 个字段")
        
        return merged

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