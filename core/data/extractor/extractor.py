"""数据提取器
为每种数据类型提供专门的提取接口，基于配置文件进行字段映射和过滤，集成标准参数和task manager
"""

from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path
from dataclasses import dataclass
import pandas as pd
from datetime import datetime, date
from .config_loader import ConfigLoader
from ..adapters import to_standard_params, StandardParams, AkshareStockParamAdapter, StockSymbol
from ..interfaces.executor import TaskManager, InterfaceExecutor, CallTask, ExecutionContext, ExecutorConfig, RetryConfig
from ..cache.persistent_cache import PersistentCacheConfig
from ..interfaces.base import get_api_provider_manager
from core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ExtractionResult:
    """提取结果"""
    success: bool
    data: Any
    error: Optional[str] = None
    interface_name: Optional[str] = None
    source_interface: Optional[str] = None
    extracted_fields: Optional[List[str]] = None


class Extractor:
    """
    数据提取器
    为每种数据类型提供专门的提取接口，基于配置文件进行字段映射和过滤
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化提取器
        
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
        
        # 初始化参数适配器
        self.param_adapter = AkshareStockParamAdapter(self.config_loader)
        
        # 初始化task manager和executor
        self.provider_manager = get_api_provider_manager()
        
        # 从全局配置注入执行器配置（缓存/重试/超时）
        global_cfg = self.config.global_config
        self.executor_config = ExecutorConfig(
            cache_config=PersistentCacheConfig(
                enabled=bool(global_cfg.enable_cache),
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
        
        logger.info(f"Extractor 初始化完成，配置版本: {self.config.version}")
    
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
        # 开始处理提取结果
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
            # 数据检查通过
            if df is None or df.empty:
                # 接口返回空数据
                return ExtractionResult(
                    success=False,
                    data=None,
                    interface_name=interface_name,
                    error="空数据",
                    source_interface=interface_name
                )
            
            # 原始数据形状: {df.shape}

            # 应用后处理器（在列名映射之前）
            df = self._apply_post_processor(df, category, data_type, interface_name)

            # 列名映射
            try:
                col_mapping = {col: self.config.get_field_mapping(col) for col in df.columns}
                df = df.rename(columns=col_mapping)
                
                # 检查并处理重复列名
                if len(df.columns) != len(set(df.columns)):
                    duplicate_cols = [col for col in df.columns if list(df.columns).count(col) > 1]
                    logger.warning(f"检测到重复列名: {duplicate_cols}")
                    
                    # 合并重复列的数据，优先保留非空值
                    for dup_col in set(duplicate_cols):
                        # 获取所有同名列的索引
                        dup_indices = [i for i, col in enumerate(df.columns) if col == dup_col]
                        if len(dup_indices) > 1:
                            # 合并这些列的数据
                            merged_series = df.iloc[:, dup_indices[0]].copy()
                            for idx in dup_indices[1:]:
                                # 用非空值填充（0值是有意义的，不应该被过滤）
                                mask = merged_series.isna() | (merged_series == '')
                                merged_series = merged_series.where(~mask, df.iloc[:, idx])
                            
                            # 删除重复列，保留第一列并更新其数据
                            df = df.drop(df.columns[dup_indices[1:]], axis=1)
                            df.iloc[:, dup_indices[0]] = merged_series
                            
                            logger.info(f"已合并重复列 '{dup_col}'，保留 {len(dup_indices)} 列中的最佳数据")
                            
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
                    
                    # 标准字段处理完成
            except Exception as _e:
                logger.debug(f"标准字段过滤失败，保留原列: {_e}")

            # 转换symbol字段为统一格式
            try:
                if 'symbol' in df.columns:
                    logger.info(f"开始转换symbol字段，原始类型: {type(df['symbol'].iloc[0])}, 原始值: {df['symbol'].iloc[0]}")
                    def convert_symbol_to_unified_format(symbol_value):
                        """将symbol字段转换为统一的StockSymbol格式"""
                        if pd.isna(symbol_value) or symbol_value is None:
                            # 对于个股历史数据接口，如果symbol为None，尝试从参数中获取
                            if hasattr(self, '_current_params') and self._current_params and hasattr(self._current_params, 'symbol'):
                                return self._current_params.symbol.to_dot()
                            return symbol_value
                        
                        # 如果已经是StockSymbol对象，直接转换为dot格式
                        if isinstance(symbol_value, StockSymbol):
                            return symbol_value.to_dot()
                        
                        # 如果是字符串，尝试解析为StockSymbol
                        if isinstance(symbol_value, str):
                            code = symbol_value.strip()
                            
                            # 获取市场提示
                            hint_market = None
                            if hasattr(self, '_current_params') and self._current_params:
                                if hasattr(self._current_params, 'market') and self._current_params.market:
                                    hint_market = self._current_params.market
                                elif hasattr(self._current_params, 'symbol') and self._current_params.symbol:
                                    hint_market = self._current_params.symbol.market
                            
                            try:
                                parsed_symbol = StockSymbol.parse(code, hint_market=hint_market)
                                if parsed_symbol:
                                    return parsed_symbol.to_dot()
                                else:
                                    # 如果无法解析，保持原值
                                    return code
                            except Exception as e:
                                # 对于B股代码等无法解析的情况，保持原值
                                return code
                        
                        # 其他类型，转换为字符串后尝试解析
                        try:
                            str_value = str(symbol_value).strip()
                            
                            # 获取市场提示
                            hint_market = None
                            if hasattr(self, '_current_params') and self._current_params:
                                if hasattr(self._current_params, 'market') and self._current_params.market:
                                    hint_market = self._current_params.market
                                elif hasattr(self._current_params, 'symbol') and self._current_params.symbol:
                                    hint_market = self._current_params.symbol.market
                            
                            parsed_symbol = StockSymbol.parse(str_value, hint_market=hint_market)
                            if parsed_symbol:
                                return parsed_symbol.to_dot()
                            else:
                                return str_value
                        except Exception:
                            return symbol_value
                    
                    # 应用转换函数到symbol列
                    df['symbol'] = df['symbol'].apply(convert_symbol_to_unified_format)
                    logger.info(f"已将symbol字段转换为统一格式，转换后类型: {type(df['symbol'].iloc[0])}, 转换后值: {df['symbol'].iloc[0]}")
                else:
                    logger.info(f"DataFrame中没有symbol列，当前列名: {list(df.columns)}")
            except Exception as _e:
                logger.error(f"symbol字段转换失败，保持原格式: {_e}")

            # 转换date字段为统一格式
            try:
                if 'date' in df.columns:
                    logger.info(f"开始转换date字段，原始类型: {type(df['date'].iloc[0])}, 原始值: {df['date'].iloc[0]}")
                    
                    def convert_date_to_unified_format(date_value):
                        """将date字段转换为统一的datetime.date格式"""
                        if pd.isna(date_value) or date_value is None:
                            return date_value
                        
                        # 如果已经是date对象，直接返回
                        if isinstance(date_value, date):
                            return date_value
                        
                        # 如果已经是datetime对象，转换为date
                        if isinstance(date_value, datetime):
                            return date_value.date()
                        
                        # 如果是字符串，尝试解析
                        if isinstance(date_value, str):
                            date_str = str(date_value).strip()
                            
                            # 处理各种日期格式
                            if len(date_str) == 8 and date_str.isdigit():  # 20230922 格式
                                try:
                                    return datetime.strptime(date_str, '%Y%m%d').date()
                                except ValueError:
                                    pass
                            
                            # 处理其他常见格式
                            for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d', '%m/%d/%Y', '%d/%m/%Y']:
                                try:
                                    return datetime.strptime(date_str, fmt).date()
                                except ValueError:
                                    continue
                            
                            # 尝试pandas自动解析
                            try:
                                parsed_date = pd.to_datetime(date_str)
                                return parsed_date.date()
                            except:
                                pass
                            
                            # 如果都无法解析，保持原值
                            return date_value
                        
                        # 其他类型，尝试转换为字符串后解析
                        try:
                            str_value = str(date_value).strip()
                            return convert_date_to_unified_format(str_value)
                        except Exception:
                            return date_value
                    
                    # 应用转换函数到date列
                    df['date'] = df['date'].apply(convert_date_to_unified_format)
                    logger.info(f"已将date字段转换为统一格式，转换后类型: {type(df['date'].iloc[0])}, 转换后值: {df['date'].iloc[0]}")
                else:
                    logger.info(f"DataFrame中没有date列，当前列名: {list(df.columns)}")
            except Exception as e:
                logger.error(f"date字段转换失败，保持原格式: {e}")

            # 若无数据（空 DataFrame），则判定失败；仅列不匹配不视为失败
            if df is None or df.empty:
                return ExtractionResult(
                    success=False,
                    data=None,
                    interface_name=interface_name,
                    error="空数据",
                    source_interface=interface_name
                )

            # 处理完成
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
        
        # 使用全局参数适配器
        param_adapter = self.param_adapter
        
        # 设置当前参数，用于symbol字段转换
        self._current_params = params
        
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
                    # 统一通过适配器执行参数适配，隐藏具体映射细节
                    # 进行参数适配
                    adapted_params = param_adapter.adapt(interface.name, params_dict)
                except Exception as _e:
                    # 参数适配失败，回退原始参数
                    adapted_params = params_dict
                task = CallTask(interface_name=interface.name, params=adapted_params)
                self.task_manager.add_task(task)
            except Exception as e:
                logger.error(f"构建接口 {interface.name} 任务时发生错误: {e}")
                continue

        # 批量执行
        logger.info(f"开始批量执行，接口数量: {len(interfaces)}")
        batch_result = self.task_manager.execute_all(context=context)
        logger.info(f"批量执行完成，成功: {batch_result.successful_tasks}/{batch_result.total_tasks}")

        # 收集所有成功的结果进行数据合并
        successful_results = []
        # 处理批量执行结果
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
        
        # 如果没有成功的结果，返回空的标准字段DataFrame
        if not successful_results:
            # 没有成功的结果，返回空的标准字段DataFrame
            empty_df = self._create_empty_standard_dataframe(category, data_type)
            return ExtractionResult(
                success=True,
                data=empty_df,
                interface_name=None,
                error=None
            )
        
        # 如果只有一个成功结果，应用日期过滤后直接返回
        if len(successful_results) == 1:
            logger.debug("=== 处理单个接口结果 ===")
            single_result = successful_results[0][1]
            logger.debug(f"单个接口结果处理: {single_result.interface_name}, 数据形状: {single_result.data.shape if single_result.data is not None else 'None'}")
            
            # 应用股票代码过滤
            if single_result.data is not None and not single_result.data.empty and 'symbol' in single_result.data.columns:
                target_symbol = standard_params.symbol
                if target_symbol:
                    logger.debug(f"应用股票代码过滤: {target_symbol.to_dot()}")
                    original_count = len(single_result.data)
                    single_result.data = single_result.data[single_result.data['symbol'] == target_symbol.to_dot()]
                    logger.debug(f"股票代码过滤结果: {original_count} -> {len(single_result.data)} 行")
                    if single_result.data.empty:
                        logger.debug("股票代码过滤后数据为空")
                        empty_df = self._create_empty_standard_dataframe(category, data_type)
                        return ExtractionResult(
                            success=True,
                            data=empty_df,
                            error=None,
                            interface_name=single_result.interface_name
                        )
            
            # 应用日期过滤
            if single_result.data is not None and not single_result.data.empty:
                logger.debug("开始应用日期过滤")
                merge_config = self._get_merge_strategy(category, data_type)
                filtered_data = self._apply_date_filter(single_result.data, standard_params, merge_config)
                if not filtered_data.empty:
                    single_result.data = filtered_data
                    logger.debug(f"日期过滤后数据形状: {single_result.data.shape}")
                else:
                    logger.debug("日期过滤后数据为空")
                    # 创建空的标准字段DataFrame而不是返回None
                    empty_df = self._create_empty_standard_dataframe(category, data_type)
                    return ExtractionResult(
                        success=True,  # 改为True，因为这是正常的空数据情况
                        data=empty_df,
                        error=None,
                        interface_name=single_result.interface_name
                    )
            logger.debug(f"单个接口结果处理完成，最终数据形状: {single_result.data.shape if single_result.data is not None else 'None'}")
            return single_result
        
        # 多个成功结果，进行数据合并
        logger.info(f"开始合并 {len(successful_results)} 个接口的数据")
        merged_result = self._merge_interface_results(successful_results, standard_params, category, data_type)
        
        return merged_result
    
    def _merge_interface_results(self, successful_results: List[Tuple[Any, ExtractionResult]], 
                                standard_params: StandardParams, category: str, data_type: str) -> ExtractionResult:
        """
        基于配置的智能合并策略
        
        Args:
            successful_results: 成功的接口结果列表，每个元素为(interface, extraction_result)
            standard_params: 标准化参数
            category: 数据分类
            data_type: 数据类型
            
        Returns:
            合并后的提取结果
        """
        try:
            # 检查是否有成功的结果
            if not successful_results:
                # 创建空的标准字段DataFrame而不是返回None
                empty_df = self._create_empty_standard_dataframe(category, data_type)
                return ExtractionResult(
                    success=True,
                    data=empty_df,
                    error=None,
                    interface_name=None,
                    source_interface=None
                )
            
            # 获取合并策略配置
            merge_config = self._get_merge_strategy(category, data_type)
            
            # 根据策略执行合并
            if merge_config["strategy"] == "date_based_merge":
                return self._merge_by_date(successful_results, standard_params, merge_config, category, data_type)
            elif merge_config["strategy"] == "symbol_based_merge":
                return self._merge_by_symbol(successful_results, standard_params, merge_config, category, data_type)
            elif merge_config["strategy"] == "symbol_report_merge":
                return self._merge_by_symbol_report(successful_results, standard_params, merge_config, category, data_type)
            else:
                return self._merge_default(successful_results, standard_params, category, data_type)
                
        except Exception as e:
            logger.error(f"数据合并过程中发生错误: {e}")
            # 合并失败时返回优先级最高的结果
            if successful_results:
                return successful_results[0][1]
            else:
                # 创建空的标准字段DataFrame而不是返回None
                empty_df = self._create_empty_standard_dataframe(category, data_type)
                return ExtractionResult(
                    success=True,
                    data=empty_df,
                    error=None,
                    interface_name=None,
                    source_interface=None
                )

    def _get_merge_strategy(self, category: str, data_type: str) -> Dict[str, Any]:
        """
        根据接口位置获取合并策略配置
        
        Args:
            category: 数据分类
            data_type: 数据类型
            
        Returns:
            合并策略配置字典
        """
        return self.config_loader.get_merge_strategy(category, data_type)

    def _merge_by_date(self, successful_results: List[Tuple[Any, ExtractionResult]], 
                      standard_params: StandardParams, merge_config: Dict[str, Any], 
                      category: str, data_type: str) -> ExtractionResult:
        """
        按日期合并数据（用于日行情等时间序列数据）
        
        Args:
            successful_results: 成功的接口结果列表
            standard_params: 标准化参数
            merge_config: 合并策略配置
            
        Returns:
            合并后的提取结果
        """
        # 1. 收集所有接口的数据
        all_data = []
        interface_names = []
        
        for interface, result in successful_results:
            if result.data is not None and not result.data.empty:
                # 注意：日期过滤已经在单个结果处理时完成，这里直接使用数据
                all_data.append(result.data)
                interface_names.append(interface.name)
        
        if not all_data:
            # 创建空的标准字段DataFrame而不是返回None
            empty_df = self._create_empty_standard_dataframe(category, data_type)
            return ExtractionResult(success=True, data=empty_df, error=None)
        
        # 2. 合并所有数据
        merged_data = pd.concat(all_data, ignore_index=True)
        
        # 3. 按配置的字段分组去重，使用数据质量优先级
        group_by = merge_config.get("group_by", ["symbol", "date"])
        if group_by and all(col in merged_data.columns for col in group_by):
            merged_data = self._apply_quality_priority_dedup(merged_data, group_by, merge_config)
        
        # 4. 按日期排序
        if "date" in merged_data.columns:
            merged_data = merged_data.sort_values("date")
        
        return ExtractionResult(
            success=True,
            data=merged_data,
            interface_name=f"merged({', '.join(interface_names)})",
            error=None
        )

    def _apply_quality_priority_dedup(self, data: pd.DataFrame, group_by: List[str], 
                                    merge_config: Dict[str, Any]) -> pd.DataFrame:
        """
        应用数据质量优先级去重
        
        Args:
            data: 要去重的数据
            group_by: 分组字段
            merge_config: 合并配置
            
        Returns:
            去重后的数据
        """
        merge_options = merge_config.get("merge_options", {})
        quality_priority = merge_options.get("data_quality_priority", "highest")
        
        if quality_priority == "highest":
            # 按接口优先级去重（保留最后一个，即优先级最高的）
            return data.drop_duplicates(subset=group_by, keep='last')
        
        elif quality_priority == "latest":
            # 按数据时间去重（需要数据中包含时间戳字段）
            if 'timestamp' in data.columns:
                return data.sort_values('timestamp').drop_duplicates(subset=group_by, keep='last')
            else:
                # 如果没有时间戳字段，回退到接口优先级
                logger.info("数据中没有timestamp字段，回退到接口优先级去重")
                return data.drop_duplicates(subset=group_by, keep='last')
        
        elif quality_priority == "most_complete":
            # 按数据完整性去重
            return self._dedup_by_completeness(data, group_by)
        
        else:
            # 未知策略，回退到接口优先级
            logger.info(f"未知的数据质量优先级策略: {quality_priority}，回退到接口优先级")
            return data.drop_duplicates(subset=group_by, keep='last')

    def _dedup_by_completeness(self, data: pd.DataFrame, group_by: List[str]) -> pd.DataFrame:
        """
        按数据完整性去重
        
        Args:
            data: 要去重的数据
            group_by: 分组字段
            
        Returns:
            去重后的数据
        """
        def calculate_completeness(row):
            """计算单行数据的完整性（排除元数据字段）"""
            # 排除元数据字段，只计算业务字段的完整性
            metadata_fields = {'source', '_completeness_score', 'timestamp'}
            business_fields = [col for col in row.index if col not in metadata_fields]
            
            if not business_fields:
                return 0
                
            non_null_count = sum(1 for col in business_fields if pd.notna(row[col]))
            total_count = len(business_fields)
            return non_null_count / total_count if total_count > 0 else 0
        
        # 为每行数据添加完整性得分
        data_with_score = data.copy()
        data_with_score['_completeness_score'] = data_with_score.apply(calculate_completeness, axis=1)
        
        # 按分组字段和完整性得分排序，保留完整性最高的
        data_sorted = data_with_score.sort_values(['_completeness_score'], ascending=False)
        result = data_sorted.drop_duplicates(subset=group_by, keep='first')
        
        # 移除临时列
        result = result.drop('_completeness_score', axis=1)
        
        return result

    def _merge_by_symbol(self, successful_results: List[Tuple[Any, ExtractionResult]], 
                        standard_params: StandardParams, merge_config: Dict[str, Any], 
                        category: str, data_type: str) -> ExtractionResult:
        """
        按股票合并数据（用于基础信息等非时间序列数据）
        
        Args:
            successful_results: 成功的接口结果列表
            standard_params: 标准化参数
            merge_config: 合并策略配置
            
        Returns:
            合并后的提取结果
        """
        target_symbol = standard_params.symbol
        if not target_symbol:
            return successful_results[0][1]
        
        # 1. 提取目标股票的单行数据
        merged_data = None
        interface_names = []
        
        for interface, result in successful_results:
            if result.data is not None and not result.data.empty:
                target_row = self._find_target_stock_data(result.data, target_symbol)
                if target_row is not None:
                    if merged_data is None:
                        merged_data = target_row.copy()
                        interface_names.append(interface.name)
                    else:
                        merged_data = self._merge_stock_data(merged_data, target_row, interface.name)
                        interface_names.append(interface.name)
        
        if merged_data is None:
            # 创建空的标准字段DataFrame而不是返回None
            empty_df = self._create_empty_standard_dataframe(category, data_type)
            return ExtractionResult(success=True, data=empty_df, error=None)
        
        return ExtractionResult(
            success=True,
            data=pd.DataFrame([merged_data]),
            interface_name=f"merged({', '.join(interface_names)})",
            error=None
        )

    def _merge_by_symbol_report(self, successful_results: List[Tuple[Any, ExtractionResult]], 
                               standard_params: StandardParams, merge_config: Dict[str, Any], 
                               category: str, data_type: str) -> ExtractionResult:
        """
        按股票和报告期合并数据（用于财务数据）
        
        Args:
            successful_results: 成功的接口结果列表
            standard_params: 标准化参数
            merge_config: 合并策略配置
            
        Returns:
            合并后的提取结果
        """
        target_symbol = standard_params.symbol
        if not target_symbol:
            return successful_results[0][1]
        
        # 1. 收集所有接口的数据
        all_data = []
        interface_names = []
        
        for interface, result in successful_results:
            if result.data is not None and not result.data.empty:
                # 过滤目标股票的数据
                if 'symbol' in result.data.columns:
                    target_data = result.data[result.data['symbol'] == target_symbol.to_dot()]
                else:
                    target_data = result.data
                
                if not target_data.empty:
                    all_data.append(target_data)
                    interface_names.append(interface.name)
        
        if not all_data:
            # 创建空的标准字段DataFrame而不是返回None
            empty_df = self._create_empty_standard_dataframe(category, data_type)
            return ExtractionResult(success=True, data=empty_df, error=None)
        
        # 2. 合并所有数据
        merged_data = pd.concat(all_data, ignore_index=True)
        
        # 3. 按股票和报告期去重，使用数据质量优先级
        group_by = merge_config.get("group_by", ["symbol", "report_date"])
        if group_by and all(col in merged_data.columns for col in group_by):
            merged_data = self._apply_quality_priority_dedup(merged_data, group_by, merge_config)
        
        # 4. 按报告期排序
        if "report_date" in merged_data.columns:
            merged_data = merged_data.sort_values("report_date")
        
        return ExtractionResult(
            success=True,
            data=merged_data,
            interface_name=f"merged({', '.join(interface_names)})",
            error=None
        )

    def _merge_default(self, successful_results: List[Tuple[Any, ExtractionResult]], 
                      standard_params: StandardParams, category: str, data_type: str) -> ExtractionResult:
        """
        默认合并策略（向后兼容）
        
        Args:
            successful_results: 成功的接口结果列表
            standard_params: 标准化参数
            
        Returns:
            合并后的提取结果
        """
        # 使用原来的合并逻辑作为默认策略
        target_symbol = standard_params.symbol
        if not target_symbol:
            return successful_results[0][1]
        
        # 设置当前参数，用于日期过滤
        self._current_params = standard_params
        
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
            # 创建空的标准字段DataFrame而不是返回None
            empty_df = self._create_empty_standard_dataframe(category, data_type)
            return ExtractionResult(
                success=True,
                data=empty_df,
                interface_name=None,
                error=None
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

    def _apply_date_filter(self, data: pd.DataFrame, standard_params: StandardParams, 
                          merge_config: Dict[str, Any]) -> pd.DataFrame:
        """
        应用日期过滤
        
        Args:
            data: 数据DataFrame
            standard_params: 标准化参数
            merge_config: 合并策略配置
            
        Returns:
            过滤后的DataFrame
        """
        if not standard_params.start_date and not standard_params.end_date:
            return data
        
        date_column = merge_config.get("date_column", "date")
        if date_column not in data.columns:
            return data
        
        try:
            import pandas as pd
            from datetime import datetime
            
            # 确保日期列是datetime类型
            if not pd.api.types.is_datetime64_any_dtype(data[date_column]):
                data = data.copy()  # 创建副本避免修改原数据
                data[date_column] = pd.to_datetime(data[date_column])
            
            # 过滤数据 - 直接使用字符串日期进行比较
            mask = pd.Series([True] * len(data), index=data.index)
            
            if standard_params.start_date:
                start_timestamp = pd.Timestamp(standard_params.start_date)
                mask &= (data[date_column] >= start_timestamp)
            
            if standard_params.end_date:
                end_timestamp = pd.Timestamp(standard_params.end_date)
                mask &= (data[date_column] <= end_timestamp)
            
            filtered_data = data[mask]
            logger.debug(f"日期过滤: 原始 {len(data)} 行 -> 过滤后 {len(filtered_data)} 行")
            
            return filtered_data
            
        except Exception as e:
            logger.warning(f"日期过滤失败: {e}，返回原数据")
            return data

    def _create_empty_standard_dataframe(self, category: str, data_type: str) -> pd.DataFrame:
        """
        创建包含标准字段的空DataFrame
        
        Args:
            category: 数据分类
            data_type: 数据类型
            
        Returns:
            包含标准字段的空DataFrame
        """
        try:
            # 从配置中获取标准字段
            standard_fields = self.config.get_standard_fields(category, data_type)
            
            if not standard_fields:
                logger.warning(f"未找到标准字段定义: {category}.{data_type}")
                return pd.DataFrame()
            
            # 创建空DataFrame，包含所有标准字段
            empty_df = pd.DataFrame(columns=standard_fields)
            logger.info(f"创建空标准字段DataFrame: {category}.{data_type}, 字段: {standard_fields}")
            
            return empty_df
            
        except Exception as e:
            logger.error(f"创建空标准字段DataFrame失败: {e}")
            return pd.DataFrame()

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
            logger.debug(f"数据为空，无法查找目标股票 {target_symbol}")
            return None
        
        # 使用标准的symbol格式和列名
        target_symbol_str = target_symbol.to_dot()  # 标准格式，如 "601727.SH"
        logger.debug(f"查找目标股票: {target_symbol_str}, 数据形状: {data.shape}")
        
        # 添加详细的debug信息
        if 'symbol' in data.columns:
            unique_symbols = data['symbol'].dropna().unique()
            logger.debug(f"数据中的symbol列包含 {len(unique_symbols)} 个唯一值: {list(unique_symbols[:10])}")  # 只显示前10个
        else:
            logger.debug(f"数据中没有symbol列，列名: {list(data.columns)}")
        
        # 检查标准的symbol列
        if 'symbol' in data.columns:
            # 检查symbol列是否全为None（个股历史数据接口的情况）
            if data['symbol'].isna().all():
                logger.debug(f"symbol列全为None，可能是个股历史数据接口")
                # 进行日期过滤
                if 'date' in data.columns and hasattr(self, '_current_params') and self._current_params:
                    filtered_data = self._filter_data_by_date(data, self._current_params)
                    if not filtered_data.empty:
                        logger.debug(f"根据日期范围过滤后找到 {len(filtered_data)} 行数据")
                        return filtered_data.iloc[0]  # 返回第一行（最新的数据）
                    else:
                        logger.debug(f"日期范围内没有数据，返回最新的一行")
                        return data.iloc[0]  # 如果没有匹配的日期，返回第一行
                else:
                    logger.debug(f"没有日期列或参数，返回第一行作为代表")
                    return data.iloc[0]
            else:
                # 正常的symbol列匹配
                logger.debug(f"开始匹配symbol列，目标: {target_symbol_str}")
                matched_rows = data[data['symbol'].astype(str) == target_symbol_str]
                if not matched_rows.empty:
                    logger.debug(f"在symbol列中找到匹配的股票 {target_symbol_str}，匹配行数: {len(matched_rows)}")
                    return matched_rows.iloc[0]
                else:
                    # 添加更详细的匹配失败信息
                    logger.debug(f"symbol列匹配失败，目标: {target_symbol_str}")
                    logger.debug(f"尝试其他格式匹配...")
                    
                    # 尝试不同的格式匹配
                    target_code = target_symbol.code  # 如 "600519"
                    target_market = target_symbol.market  # 如 "SH"
                    
                    # 尝试 "600519.SH" 格式
                    if f"{target_code}.{target_market}" in data['symbol'].astype(str).values:
                        logger.debug(f"找到格式 {target_code}.{target_market}")
                        matched_rows = data[data['symbol'].astype(str) == f"{target_code}.{target_market}"]
                        return matched_rows.iloc[0]
                    
                    # 尝试 "600519" 格式
                    if target_code in data['symbol'].astype(str).values:
                        logger.debug(f"找到格式 {target_code}")
                        matched_rows = data[data['symbol'].astype(str) == target_code]
                        return matched_rows.iloc[0]
                    
                    # 尝试 "SH600519" 格式
                    if f"{target_market}{target_code}" in data['symbol'].astype(str).values:
                        logger.debug(f"找到格式 {target_market}{target_code}")
                        matched_rows = data[data['symbol'].astype(str) == f"{target_market}{target_code}"]
                        return matched_rows.iloc[0]
                    
                    logger.debug(f"所有格式匹配都失败，目标: {target_symbol_str}, 可用格式: {list(data['symbol'].dropna().unique()[:5])}")
        
        # 如果DataFrame只有一行数据，可能是单股票查询结果
        if len(data) == 1:
            logger.debug(f"DataFrame只有一行数据，假设为目标股票数据")
            return data.iloc[0]
        
        # 如果没有symbol列且有多行数据，可能是个股历史数据接口
        if 'symbol' not in data.columns and len(data) > 1:
            logger.debug(f"没有symbol列且有多行数据，可能是个股历史数据")
            
            # 检查是否有日期列，如果有则进行日期过滤
            if 'date' in data.columns and hasattr(self, '_current_params') and self._current_params:
                filtered_data = self._filter_data_by_date(data, self._current_params)
                if not filtered_data.empty:
                    logger.debug(f"根据日期范围过滤后找到 {len(filtered_data)} 行数据")
                    return filtered_data.iloc[0]  # 返回第一行（最新的数据）
                else:
                    logger.debug(f"日期范围内没有数据，返回最新的一行")
                    return data.iloc[0]  # 如果没有匹配的日期，返回第一行
            else:
                logger.debug(f"没有日期列或参数，返回第一行作为代表")
                return data.iloc[0]
        
        logger.debug(f"未找到目标股票 {target_symbol_str} 的数据 - 这可能是正常的，因为某些接口只覆盖特定股票")
        return None
    
    def _filter_data_by_date(self, data: pd.DataFrame, params) -> pd.DataFrame:
        """
        根据参数中的日期范围过滤数据
        
        Args:
            data: 数据DataFrame
            params: 参数对象，包含start_date和end_date
            
        Returns:
            过滤后的DataFrame
        """
        if 'date' not in data.columns:
            return data
        
        try:
            from datetime import datetime
            
            # 获取日期范围
            start_date = None
            end_date = None
            
            if hasattr(params, 'start_date') and params.start_date:
                start_date = datetime.strptime(params.start_date, '%Y-%m-%d').date()
            
            if hasattr(params, 'end_date') and params.end_date:
                end_date = datetime.strptime(params.end_date, '%Y-%m-%d').date()
            
            # 如果没有指定日期范围，返回原数据
            if start_date is None and end_date is None:
                return data
            
            # 过滤数据
            mask = pd.Series([True] * len(data), index=data.index)
            
            # 将DataFrame中的日期列转换为date类型以便比较
            date_series = pd.to_datetime(data['date'])
            
            if start_date is not None:
                start_timestamp = pd.Timestamp(start_date)
                mask &= (date_series >= start_timestamp)
            
            if end_date is not None:
                end_timestamp = pd.Timestamp(end_date)
                mask &= (date_series <= end_timestamp)
            
            filtered_data = data[mask]
            logger.debug(f"日期过滤: 原始 {len(data)} 行 -> 过滤后 {len(filtered_data)} 行")
            
            return filtered_data
            
        except Exception as e:
            logger.warning(f"日期过滤失败: {e}，返回原数据")
            return data
    
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
    def get_stock_basic_indicators(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取基础财务指标"""
        return self._execute_interface("stock", "financials.basic_indicators", params)
    
    def get_stock_balance_sheet(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取资产负债表"""
        return self._execute_interface("stock", "financials.detailed_financials.balance_sheet", params)
    
    def get_stock_income_statement(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取利润表"""
        return self._execute_interface("stock", "financials.detailed_financials.income_statement", params)
    
    def get_stock_cash_flow(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取现金流量表"""
        return self._execute_interface("stock", "financials.detailed_financials.cash_flow", params)
    
    def get_stock_dividend(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取分红数据"""
        return self._execute_interface("stock", "financials.dividend", params)
    
    def get_stock_institutional_holdings(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取机构持仓数据（包含基金、保险、券商等大资金）"""
        return self._execute_interface("stock", "holdings.institutional_holdings", params)
    
    def get_stock_hsgt_holdings(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取沪深港通持仓数据"""
        return self._execute_interface("stock", "holdings.hsgt_holdings", params)
    
    # 研究分析数据
    def get_stock_research_reports(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取研报数据"""
        return self._execute_interface("stock", "research_and_analyst.research_reports", params)
    
    def get_stock_forecast_consensus(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取预测共识数据"""
        return self._execute_interface("stock", "research_and_analyst.forecast_consensus", params)
    
    def get_stock_opinions(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取机构观点数据"""
        return self._execute_interface("stock", "research_and_analyst.opinions", params)
    
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
    
    def get_market_sentiment(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取市场情绪数据"""
        return self._execute_interface("market", "market_sentiment", params)
    
    
    # 技术分析
    def get_innovation_high_ranking(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取创新高股票排名"""
        return self._execute_interface("stock", "technical_analysis.innovation_high", params)
    
    def get_innovation_low_ranking(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取创新低股票排名"""
        return self._execute_interface("stock", "technical_analysis.innovation_low", params)
    
    def get_volume_price_rise_ranking(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取量价齐升股票排名"""
        return self._execute_interface("stock", "technical_analysis.volume_price_rise", params)
    
    def get_continuous_rise_ranking(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取连续上涨股票排名"""
        return self._execute_interface("stock", "technical_analysis.continuous_rise", params)
    
    def get_volume_price_fall_ranking(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取量价齐跌股票排名"""
        return self._execute_interface("stock", "technical_analysis.volume_price_fall", params)
    
    def get_volume_shrink_ranking(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取创新缩量股票排名"""
        return self._execute_interface("stock", "technical_analysis.volume_shrink", params)

    def get_stock_valuation(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取个股估值数据"""
        return self._execute_interface("stock", "valuation", params)
    
    # ==================== 板块数据 ====================
    def get_sector_quote(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取行业板块行情数据"""
        return self._execute_interface("market", "sector_data.sector_quote", params)
    
    def get_sector_constituent_quotes(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取行业板块成分股行情数据"""
        return self._execute_interface("market", "sector_data.constituent_quotes", params)
    
    def get_sector_fund_flow(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取行业板块资金流向数据"""
        return self._execute_interface("market", "sector_data.sector_fund_flow", params)
    
    # ==================== 概念数据 ====================
    def get_concept_quote(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取概念板块行情数据"""
        return self._execute_interface("market", "concept_data.concept_quote", params)
    
    def get_concept_constituent_quotes(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取概念板块成分股行情数据"""
        return self._execute_interface("market", "concept_data.constituent_quotes", params)
    
    def get_concept_fund_flow(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取概念板块资金流向数据"""
        return self._execute_interface("market", "concept_data.concept_fund_flow", params)
    
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
    
    # ==================== 资金流向数据 ====================
    def get_market_fund_flow(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取市场级别资金流向数据"""
        return self._execute_interface("market", "fund_flow.market_level", params)
    
    def get_hsgt_fund_flow(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取沪深港通资金流向数据"""
        return self._execute_interface("market", "fund_flow.hsgt_flow", params)
    
    def get_big_deal_tracking(self, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """获取大单追踪数据"""
        return self._execute_interface("market", "fund_flow.big_deal_tracking", params)

    def reload_config(self) -> None:
        """重新加载配置文件"""
        self.config = self.config_loader.reload()
        logger.info("配置文件已重新加载")