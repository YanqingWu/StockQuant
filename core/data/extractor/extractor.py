"""数据提取器
为每种数据类型提供专门的提取接口，基于配置文件进行字段映射和过滤，集成标准参数和task manager
"""

from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path
import pandas as pd
from datetime import datetime, date
from .config_loader import ConfigLoader
from ..adapters import to_standard_params, StandardParams, AkshareStockParamAdapter, StockSymbol
from ..interfaces.executor import TaskManager, InterfaceExecutor, CallTask, ExecutionContext, ExecutorConfig, RetryConfig, BatchResult
from ..cache.persistent_cache import PersistentCacheConfig
from ..interfaces.base import get_api_provider_manager
from core.logging import get_logger
from .exceptions import ExtractionErrorHandler, DataValidator
from .types import ExtractionResult
from .constants import ExtractorConstants, get_default_config_path

logger = get_logger(__name__)


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
        # 确定配置文件路径
        if config_path is None:
            config_path = str(get_default_config_path())
        
        # 使用指定路径创建ConfigLoader
        self.config_loader = ConfigLoader(Path(config_path))
        self.config = self.config_loader.load_config()
        
        # 初始化参数适配器
        interface_mappings = self.config.get_parameter_mappings() if hasattr(self.config, 'get_parameter_mappings') else None
        self.param_adapter = AkshareStockParamAdapter(interface_mappings)
        
        # 初始化task manager和executor
        self.provider_manager = get_api_provider_manager()
        
        # 从全局配置注入执行器配置（缓存/重试/超时/异步执行）
        global_cfg = self.config.global_config
        self.executor_config = ExecutorConfig(
            cache_config=PersistentCacheConfig(
                enabled=bool(global_cfg.enable_cache),
            ),
            retry_config=RetryConfig(
                max_retries=int(global_cfg.retry_count)
            ),
            # 异步执行配置
            async_max_concurrency=int(getattr(global_cfg, 'async_max_concurrency', 10)),
        )
        # 仅在配置中提供了正数超时时才覆盖默认值
        try:
            _cfg_timeout = float(getattr(global_cfg, "timeout", 0))
            if _cfg_timeout > 0:
                self.executor_config.default_timeout = _cfg_timeout
                logger.info(f"设置超时时间: {_cfg_timeout}秒")
        except (ValueError, TypeError) as e:
            logger.warning(f"timeout配置无效: {e}，使用默认值")
        except Exception as e:
            logger.error(f"处理timeout配置时发生错误: {e}")
        # 验证关键组件是否成功初始化
        try:
            self.executor = InterfaceExecutor(self.provider_manager, self.executor_config)
            self.task_manager = TaskManager(self.executor)
            logger.debug("执行器和任务管理器初始化成功")
        except Exception as e:
            logger.error(f"组件初始化失败: {e}")
            raise
        
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
    
    # ==================== 数据处理子函数 ====================
    
    def _validate_raw_data(self, raw_data: Any, interface_name: str) -> ExtractionResult:
        """验证原始数据"""
        if DataValidator.is_empty_data(raw_data):
            return self._create_error_result(interface_name, "接口返回空数据")
        return self._create_success_result(None, interface_name)
    
    def _convert_to_dataframe(self, raw_data: Any, interface_name: str) -> Union[pd.DataFrame, ExtractionResult]:
        """将原始数据转换为DataFrame"""
        try:
            if isinstance(raw_data, pd.DataFrame):
                return raw_data.copy()
            elif isinstance(raw_data, list):
                return pd.DataFrame(raw_data)
            elif isinstance(raw_data, dict):
                return pd.DataFrame([raw_data])
            elif isinstance(raw_data, str):
                return self._convert_string_to_dataframe(raw_data)
            else:
                return self._create_error_result(interface_name, f"不支持的数据类型: {type(raw_data)}")
        except Exception as e:
            return self._create_error_result(interface_name, f"DataFrame转换失败: {e}")
    
    def _convert_string_to_dataframe(self, raw_data: str) -> pd.DataFrame:
        """将字符串转换为DataFrame"""
        if not raw_data or len(raw_data) < ExtractorConstants.MIN_SYMBOL_LENGTH:
            return pd.DataFrame([{"raw_value": raw_data}])
        
        # 尝试解析为股票代码格式
        if raw_data.startswith(ExtractorConstants.STOCK_CODE_PREFIXES):
            market = raw_data[:2].upper()
            code = raw_data[2:]
            return pd.DataFrame([{
                "symbol": f"{code}.{market}",
                "code": code,
                "market": market,
                "raw_value": raw_data
            }])
        else:
            return pd.DataFrame([{
                "symbol": raw_data,
                "raw_value": raw_data
            }])
    
    def _map_and_deduplicate_columns(self, df: pd.DataFrame, interface_name: str) -> pd.DataFrame:
        """列名映射和重复列处理"""
        try:
            # 列名映射
            col_mapping = {col: self.config.get_field_mapping(col) for col in df.columns}
            df = df.rename(columns=col_mapping)
            
            # 处理重复列名
            df = self._handle_duplicate_columns(df)
            
            return df
        except Exception as e:
            logger.debug(f"列名映射失败，继续使用原列名: {e}")
            return df
    
    def _handle_duplicate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """处理重复列名"""
        if len(df.columns) == len(set(df.columns)):
            return df
        
        duplicate_cols = [col for col in df.columns if list(df.columns).count(col) > 1]
        logger.warning(f"检测到重复列名: {duplicate_cols}")
        
        for dup_col in set(duplicate_cols):
            dup_indices = [i for i, col in enumerate(df.columns) if col == dup_col]
            if len(dup_indices) > 1:
                # 合并重复列的数据
                merged_series = df.iloc[:, dup_indices[0]].copy()
                for idx in dup_indices[1:]:
                    mask = merged_series.isna() | (merged_series == '')
                    merged_series = merged_series.where(~mask, df.iloc[:, idx])
                
                # 删除重复列，保留第一列并更新其数据
                df = df.drop(df.columns[dup_indices[1:]], axis=1)
                df.iloc[:, dup_indices[0]] = merged_series
                
                logger.info(f"已合并重复列 '{dup_col}'，保留 {len(dup_indices)} 列中的最佳数据")
        
        return df
    
    def _filter_standard_fields(self, df: pd.DataFrame, category: str, data_type: str, interface_name: str) -> pd.DataFrame:
        """标准字段过滤"""
        try:
            standard_fields = self.config.get_standard_fields(category, data_type)
            if not standard_fields:
                logger.warning(f"未找到 {category}.{data_type} 的标准字段定义")
                return df
            
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
                df[field] = None
            
            # 按标准字段顺序重新排列列
            df = df[standard_fields]
            
            return df
        except Exception as e:
            logger.debug(f"标准字段过滤失败，保留原列: {e}")
            return df
    
    def _convert_field_formats(self, df: pd.DataFrame, interface_name: str) -> pd.DataFrame:
        """转换字段格式"""
        if df is None or df.empty:
            return df
        
        # 转换symbol字段
        df = self._convert_symbol_field(df, interface_name)
        
        # 转换date字段
        df = self._convert_date_field(df, interface_name)
        
        return df
    
    def _convert_symbol_field(self, df: pd.DataFrame, interface_name: str) -> pd.DataFrame:
        """转换symbol字段为统一格式"""
        if 'symbol' not in df.columns:
            logger.info(f"DataFrame中没有symbol列，当前列名: {list(df.columns)}")
            return df
        
        try:
            logger.info(f"开始转换symbol字段，原始类型: {type(df['symbol'].iloc[0])}, 原始值: {df['symbol'].iloc[0]}")
            
            df['symbol'] = df['symbol'].apply(self._convert_single_symbol)
            
            logger.info(f"已将symbol字段转换为统一格式，转换后类型: {type(df['symbol'].iloc[0])}, 转换后值: {df['symbol'].iloc[0]}")
        except Exception as e:
            logger.error(f"symbol字段转换失败，保持原格式: {e}")
        
        return df
    
    def _convert_single_symbol(self, symbol_value) -> str:
        """转换单个symbol值"""
        if pd.isna(symbol_value) or symbol_value is None:
            return None
        
        # 如果已经是StockSymbol对象，直接转换为dot格式
        if isinstance(symbol_value, StockSymbol):
            return symbol_value.to_dot()
        
        # 如果是字符串，尝试解析为StockSymbol
        if isinstance(symbol_value, str):
            code = symbol_value.strip()
            try:
                parsed_symbol = StockSymbol.parse(code, hint_market=None)
                return parsed_symbol.to_dot() if parsed_symbol else code
            except Exception:
                return code
        
        # 其他类型，转换为字符串后尝试解析
        try:
            str_value = str(symbol_value).strip()
            parsed_symbol = StockSymbol.parse(str_value, hint_market=None)
            return parsed_symbol.to_dot() if parsed_symbol else str_value
        except Exception:
            return symbol_value
    
    def _convert_date_field(self, df: pd.DataFrame, interface_name: str) -> pd.DataFrame:
        """转换date字段为统一格式"""
        if 'date' not in df.columns:
            logger.info(f"DataFrame中没有date列，当前列名: {list(df.columns)}")
            return df
        
        try:
            logger.info(f"开始转换date字段，原始类型: {type(df['date'].iloc[0])}, 原始值: {df['date'].iloc[0]}")
            
            df['date'] = df['date'].apply(self._convert_single_date)
            
            logger.info(f"已将date字段转换为统一格式，转换后类型: {type(df['date'].iloc[0])}, 转换后值: {df['date'].iloc[0]}")
        except Exception as e:
            logger.error(f"date字段转换失败，保持原格式: {e}")
        
        return df
    
    def _convert_single_date(self, date_value) -> date:
        """转换单个date值"""
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
            return self._parse_date_string(str(date_value).strip())
        
        # 其他类型，尝试转换为字符串后解析
        try:
            str_value = str(date_value).strip()
            return self._parse_date_string(str_value)
        except Exception:
            return date_value
    
    def _parse_date_string(self, date_str: str) -> date:
        """解析日期字符串"""
        # 处理各种日期格式
        if len(date_str) == 8 and date_str.isdigit():  # 20230922 格式
            try:
                return datetime.strptime(date_str, '%Y%m%d').date()
            except ValueError:
                pass
        
        # 处理其他常见格式
        for fmt in ExtractorConstants.SUPPORTED_DATE_FORMATS:
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
        return date_str
    
    def _create_final_result(self, df: pd.DataFrame, interface_name: str) -> ExtractionResult:
        """创建最终结果"""
        if df is None or df.empty:
            return self._create_error_result(interface_name, "空数据")
        
        return self._create_success_result(df, interface_name)
    
    def _create_success_result(self, data: Optional[pd.DataFrame], interface_name: str, 
                              extracted_fields: List[str] = None) -> ExtractionResult:
        """创建成功结果"""
        return ExtractionResult(
            success=True,
            data=data,
            interface_name=interface_name,
            source_interface=interface_name,
            extracted_fields=extracted_fields or (list(data.columns) if data is not None else [])
        )
    
    def _create_error_result(self, interface_name: str, error: str) -> ExtractionResult:
        """创建错误结果"""
        return ExtractionResult(
            success=False,
            data=None,
            interface_name=interface_name,
            error=error,
            source_interface=interface_name
        )
    
    def _handle_processing_error(self, error: Exception, interface_name: str) -> ExtractionResult:
        """处理处理过程中的错误"""
        return ExtractionErrorHandler.handle_data_processing_error(error, interface_name)
    
    def _process_extraction_result(self, raw_data: Any, category: str, data_type: str, 
                                 interface_name: str) -> ExtractionResult:
        """
        处理提取结果，统一返回 pandas.DataFrame
        """
        try:
            # 1. 数据验证
            validation_result = self._validate_raw_data(raw_data, interface_name)
            if not validation_result.success:
                return validation_result

            # 2. 转换为DataFrame
            df = self._convert_to_dataframe(raw_data, interface_name)
            if isinstance(df, ExtractionResult):
                return df

            # 3. 应用后处理器
            df = self._apply_post_processor(df, category, data_type, interface_name)

            # 4. 列名映射和重复列处理
            df = self._map_and_deduplicate_columns(df, interface_name)

            # 5. 标准字段过滤
            df = self._filter_standard_fields(df, category, data_type, interface_name)

            # 6. 字段格式转换
            df = self._convert_field_formats(df, interface_name)

            # 7. 最终验证和返回
            return self._create_final_result(df, interface_name)
            
        except Exception as e:
            return self._handle_processing_error(e, interface_name)
    
    def _execute_interface_with_batch(self, category: str, data_type: str, 
                                     params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """
        支持批量执行的接口执行器
        
        Args:
            category: 数据分类
            data_type: 数据类型
            params: 接口参数（支持单个参数或参数列表）
            
        Returns:
            单个结果或结果列表
        """
        if isinstance(params, list):
            return self._execute_interface_batch(category, data_type, params)
        else:
            return self._execute_interface(category, data_type, params)
    
    def _execute_interface_batch(self, category: str, data_type: str, 
                                params_list: List[Union[StandardParams, Dict[str, Any]]]) -> List[ExtractionResult]:
        """
        批量执行接口
        
        Args:
            category: 数据分类
            data_type: 数据类型
            params_list: 参数列表
            
        Returns:
            结果列表，与输入参数顺序对应
        """
        try:
            if not params_list:
                logger.warning("批量执行参数列表为空")
                return []
            
            logger.info(f"开始批量执行 {category}.{data_type}，参数数量: {len(params_list)}")
            
            # 1. 批量参数标准化和验证
            standardized_params = []
            param_tasks = []
            call_mapping = {}  # task_id -> param_index 映射
            
            for i, params in enumerate(params_list):
                try:
                    # 标准化参数
                    standard_params, params_dict, market = self._prepare_execution_params(params)
                    standardized_params.append(standard_params)
                    
                    # 选择接口
                    interfaces = self._select_interfaces(category, data_type, market)
                    
                    # 构建任务
                    tasks = self._build_interface_tasks(interfaces, params_dict)
                    
                    # 为每个任务添加参数索引到metadata
                    for task in tasks:
                        task.metadata['param_index'] = i
                        task.metadata['standard_params'] = standard_params
                        call_mapping[task.task_id] = i
                        param_tasks.append(task)
                    
                except Exception as e:
                    logger.error(f"参数 {i} 标准化失败: {e}")
                    # 为失败的参数创建空结果
                    standardized_params.append(None)
            
            if not param_tasks:
                logger.warning("没有有效的任务可以执行")
                return [ExtractionResult(success=False, error="参数标准化失败") for _ in params_list]
            
            # 2. 执行批量任务
            context = ExecutionContext(
                cache_enabled=bool(self.config.global_config.enable_cache),
                user_data={"category": category, "data_type": data_type, "batch_mode": True}
            )
            
            # 清空任务队列并添加新任务
            self.task_manager.clear_queue()
            for task in param_tasks:
                self.task_manager.add_task(task)
            
            # 选择执行模式
            use_async = self._should_use_async_execution(len(param_tasks))
            execution_mode = "异步" if use_async else "同步"
            logger.info(f"批量执行使用{execution_mode}模式，任务数量: {len(param_tasks)}")
            
            # 执行任务
            if use_async:
                import asyncio
                batch_result = asyncio.run(self.task_manager.execute_all_async(context=context))
            else:
                batch_result = self.task_manager.execute_all(context=context)
            
            logger.info(f"批量执行完成，成功: {batch_result.successful_tasks}/{batch_result.total_tasks}")
            
            # 3. 处理批量结果
            return self._process_batch_results(batch_result, call_mapping, standardized_params, category, data_type)
            
        except Exception as e:
            logger.error(f"批量执行失败: {e}")
            return [ExtractionResult(success=False, error=f"批量执行失败: {e}") for _ in params_list]

    def _execute_interface(self, category: str, data_type: str, params: Union[StandardParams, Dict[str, Any]]) -> ExtractionResult:
        """
        执行指定数据类型的接口（重构版）
        
        Args:
            category: 数据分类
            data_type: 数据类型
            params: 接口参数（支持StandardParams或Dict）
            
        Returns:
            提取结果
        """
        try:
            # 1. 准备执行参数
            standard_params, params_dict, market = self._prepare_execution_params(params)
            
            # 2. 选择接口
            interfaces = self._select_interfaces(category, data_type, market)
            
            # 3. 构建任务
            tasks = self._build_interface_tasks(interfaces, params_dict)
            
            # 4. 执行任务
            context = ExecutionContext(
                cache_enabled=bool(self.config.global_config.enable_cache),
                user_data={"category": category, "data_type": data_type}
            )
            batch_result = self._execute_interface_tasks(tasks, context)
            
            # 5. 处理结果
            successful_results = self._process_execution_results(batch_result, interfaces, category, data_type)
            
            # 6. 合并结果
            return self._merge_execution_results(successful_results, standard_params, category, data_type)
            
        except Exception as e:
            logger.error(f"接口执行失败: {e}")
            return ExtractionResult(success=False, error=str(e))
    
    def _process_batch_results(self, batch_result: BatchResult, call_mapping: Dict[str, int], 
                              standardized_params: List[Optional[StandardParams]], 
                              category: str, data_type: str) -> List[ExtractionResult]:
        """处理批量执行结果
        
        Args:
            batch_result: 批量执行结果
            call_mapping: 任务ID -> 参数索引映射
            standardized_params: 标准化参数列表
            category: 数据分类
            data_type: 数据类型
            
        Returns:
            结果列表，与输入顺序对应
        """
        from collections import defaultdict
        
        # 按参数索引分组结果
        param_results = defaultdict(list)
        
        for result in batch_result.results:
            param_index = call_mapping.get(result.task_id)
            if param_index is not None and result.success:
                # 处理提取结果
                extraction_result = self._process_extraction_result(
                    result.data,
                    category,
                    data_type,
                    result.interface_name
                )
                if extraction_result.success:
                    param_results[param_index].append((None, extraction_result))
        
        # 为每个参数创建结果
        results = []
        for i, standard_params in enumerate(standardized_params):
            if i in param_results and param_results[i]:
                # 合并该参数的所有结果
                successful_results = param_results[i]
                if standard_params is not None:
                    merged_result = self._merge_execution_results(
                        successful_results,
                        standard_params,
                        category,
                        data_type
                    )
                    results.append(merged_result)
                else:
                    # 参数标准化失败的情况
                    results.append(ExtractionResult(
                        success=False,
                        error="参数标准化失败",
                        data=None
                    ))
            else:
                # 没有结果或参数标准化失败
                if standard_params is not None:
                    results.append(self._create_empty_result(category, data_type))
                else:
                    results.append(ExtractionResult(
                        success=False,
                        error="参数标准化失败",
                        data=None
                    ))
        
        return results
    
    def _extract_market_from_params(self, standard_params: StandardParams) -> Optional[str]:
        """从参数中提取市场信息"""
        try:
            if standard_params.symbol and hasattr(standard_params.symbol, 'market'):
                market = standard_params.symbol.market
                if market:
                    logger.debug(f"从symbol中提取市场: {market}")
                    return market
            
            if standard_params.market:
                logger.debug(f"使用直接指定的市场: {standard_params.market}")
                return standard_params.market
            
            logger.debug("未找到市场信息")
            return None
        except Exception as e:
            logger.error(f"提取市场信息失败: {e}")
            return None
    
    def _prepare_execution_params(self, params: Union[StandardParams, Dict[str, Any]]) -> Tuple[StandardParams, Dict[str, Any], Optional[str]]:
        """准备执行参数"""
        # 参数标准化
        try:
            standard_params = to_standard_params(params)
            params_dict = standard_params.to_dict()
            logger.debug(f"参数标准化成功")
        except Exception as e:
            logger.error(f"参数标准化失败: {e}")
            # 回退到原始参数
            if isinstance(params, dict):
                params_dict = params
            else:
                params_dict = {}
            # 创建默认的StandardParams对象
            standard_params = StandardParams()
        
        # 市场信息提取
        market = self._extract_market_from_params(standard_params)
        
        return standard_params, params_dict, market
    
    def _select_interfaces(self, category: str, data_type: str, market: Optional[str]) -> List[Any]:
        """选择启用的接口"""
        interfaces = self.config.get_enabled_interfaces(category, data_type, market)
        if not interfaces:
            market_info = f" (市场: {market})" if market else ""
            raise ValueError(f"未找到启用的接口: {category}.{data_type}{market_info}")
        
        logger.info(f"找到 {len(interfaces)} 个可用接口: {[i.name for i in interfaces]}")
        return interfaces
    
    def _build_interface_tasks(self, interfaces: List[Any], params_dict: Dict[str, Any]) -> List[CallTask]:
        """构建接口任务列表"""
        tasks = []
        param_adapter = self.param_adapter
        
        for interface in interfaces:
            try:
                logger.info(f"准备加入批量任务: {interface.name}")
                try:
                    # 统一通过适配器执行参数适配，隐藏具体映射细节
                    adapted_params = param_adapter.adapt(interface.name, params_dict)
                    logger.debug(f"参数适配成功: {interface.name}")
                except Exception as e:
                    # 参数适配失败，回退原始参数
                    logger.warning(f"参数适配失败: {interface.name}, 错误: {e}")
                    adapted_params = params_dict
                
                task = CallTask(interface_name=interface.name, params=adapted_params)
                tasks.append(task)
            except Exception as e:
                logger.error(f"构建接口 {interface.name} 任务时发生错误: {e}")
                continue
        
        return tasks
    
    def _execute_interface_tasks(self, tasks: List[CallTask], context: ExecutionContext) -> BatchResult:
        """执行接口任务"""
        # 添加到任务管理器
        for task in tasks:
            self.task_manager.add_task(task)
        
        # 选择执行模式
        use_async = self._should_use_async_execution(len(tasks))
        execution_mode = "异步" if use_async else "同步"
        logger.info(f"使用{execution_mode}执行模式，接口数量: {len(tasks)}")
        
        # 执行任务
        if use_async:
            import asyncio
            batch_result = asyncio.run(self.task_manager.execute_all_async(context=context))
        else:
            batch_result = self.task_manager.execute_all(context=context)
        
        logger.info(f"批量执行完成，成功: {batch_result.successful_tasks}/{batch_result.total_tasks}")
        return batch_result
    
    def _process_execution_results(self, batch_result: BatchResult, interfaces: List[Any], 
                                 category: str, data_type: str) -> List[Tuple[Any, ExtractionResult]]:
        """处理执行结果"""
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
        
        return successful_results
    
    def _create_empty_result(self, category: str, data_type: str) -> ExtractionResult:
        """创建空结果"""
        empty_df = self._create_empty_standard_dataframe(category, data_type)
        return ExtractionResult(
            success=True,
            data=empty_df,
            interface_name=None,
            error=None
        )
    
    def _process_single_result(self, single_result: ExtractionResult, standard_params: StandardParams, 
                             category: str, data_type: str) -> ExtractionResult:
        """处理单个接口结果"""
        logger.debug("=== 处理单个接口结果 ===")
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
                    return self._create_empty_result(category, data_type)
        
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
                return self._create_empty_result(category, data_type)
        
        logger.debug(f"单个接口结果处理完成，最终数据形状: {single_result.data.shape if single_result.data is not None else 'None'}")
        return single_result
    
    def _merge_execution_results(self, successful_results: List[Tuple[Any, ExtractionResult]], 
                               standard_params: StandardParams, category: str, data_type: str) -> ExtractionResult:
        """合并执行结果"""
        if not successful_results:
            return self._create_empty_result(category, data_type)
        
        if len(successful_results) == 1:
            return self._process_single_result(successful_results[0][1], standard_params, category, data_type)
        else:
            logger.info(f"开始合并 {len(successful_results)} 个接口的数据")
            return self._merge_interface_results(successful_results, standard_params, category, data_type)
    
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
                if interface is not None:
                    interface_names.append(interface.name)
                else:
                    interface_names.append(result.interface_name or "unknown")
        
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
                        if interface is not None:
                            interface_names.append(interface.name)
                        else:
                            interface_names.append(result.interface_name or "unknown")
                    else:
                        interface_name = interface.name if interface is not None else (result.interface_name or "unknown")
                        merged_data = self._merge_stock_data(merged_data, target_row, interface_name)
                        interface_names.append(interface_name)
        
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
                    if interface is not None:
                        interface_names.append(interface.name)
                    else:
                        interface_names.append(result.interface_name or "unknown")
        
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
        
        # 移除实例变量污染，使用参数传递
        
        # 按接口优先级排序
        successful_results.sort(key=lambda x: x[0].priority)
        
        # 初始化合并后的数据
        merged_data = None
        merged_interface_names = []
        
        for interface, extraction_result in successful_results:
            interface_data = extraction_result.data
            if interface is not None:
                merged_interface_names.append(interface.name)
            else:
                merged_interface_names.append(extraction_result.interface_name or "unknown")
            
            if interface_data is None or interface_data.empty:
                continue
            
            # 查找目标股票数据
            target_row = self._find_target_stock_data(interface_data, target_symbol)
            
            if target_row is not None:
                if merged_data is None:
                    # 第一个有效数据作为基础
                    merged_data = target_row.copy()
                    interface_name = interface.name if interface is not None else (extraction_result.interface_name or "unknown")
                    logger.info(f"使用接口 {interface_name} 作为基础数据")
                else:
                    # 合并数据，优先保留已有数据，补充缺失字段
                    interface_name = interface.name if interface is not None else (extraction_result.interface_name or "unknown")
                    merged_data = self._merge_stock_data(merged_data, target_row, interface_name)
            else:
                interface_name = interface.name if interface is not None else (extraction_result.interface_name or "unknown")
                logger.warning(f"接口 {interface_name} 中未找到目标股票 {target_symbol} 的数据")
        
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
                if 'date' in data.columns:
                    # 简化处理，直接返回第一行
                    logger.debug(f"没有参数信息，返回第一行作为代表")
                    return data.iloc[0]
                else:
                    logger.debug(f"没有日期列，返回第一行作为代表")
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
            if 'date' in data.columns:
                # 简化处理，直接返回第一行
                logger.debug(f"没有参数信息，返回第一行作为代表")
                return data.iloc[0]
            else:
                logger.debug(f"没有日期列，返回第一行作为代表")
                return data.iloc[0]
        
        logger.debug(f"未找到目标股票 {target_symbol_str} 的数据 - 这可能是正常的，因为某些接口只覆盖特定股票")
        return None
    
    def _filter_data_by_date(self, data: pd.DataFrame, standard_params: StandardParams) -> pd.DataFrame:
        """
        根据参数中的日期范围过滤数据
        
        Args:
            data: 数据DataFrame
            standard_params: 标准化参数对象，包含start_date和end_date
            
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
            
            if standard_params.start_date:
                start_date = datetime.strptime(standard_params.start_date, '%Y-%m-%d').date()
            
            if standard_params.end_date:
                end_date = datetime.strptime(standard_params.end_date, '%Y-%m-%d').date()
            
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

    # ==================== 个股相关接口 (STOCK) ====================
    
    # 股票基础信息
    def get_stock_profile(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取股票基础信息"""
        return self._execute_interface_with_batch("stock", "profile", params)
    
    # 股票行情数据
    def get_stock_daily_quote(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取股票日行情数据"""
        return self._execute_interface_with_batch("stock", "daily_market.quote", params)
    
    def get_stock_financing_data(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取融资融券数据"""
        return self._execute_interface_with_batch("stock", "daily_market.financing", params)
    
    def get_stock_cost_distribution(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取成本分布数据"""
        return self._execute_interface_with_batch("stock", "daily_market.cost_distribution", params)
    
    def get_stock_fund_flow(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取股票资金流向数据"""
        return self._execute_interface_with_batch("stock", "daily_market.fund_flow", params)
    
    def get_stock_dragon_tiger(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取龙虎榜数据"""
        return self._execute_interface_with_batch("stock", "daily_market.dragon_tiger", params)
    
    def get_stock_sentiment(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取股票情绪数据"""
        return self._execute_interface_with_batch("stock", "daily_market.sentiment", params)
    
    def get_stock_news(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取股票新闻数据"""
        return self._execute_interface_with_batch("stock", "daily_market.news", params)
    
    # 股票财务数据
    def get_stock_basic_indicators(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取基础财务指标"""
        return self._execute_interface_with_batch("stock", "financials.basic_indicators", params)
    
    def get_stock_balance_sheet(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取资产负债表"""
        return self._execute_interface_with_batch("stock", "financials.detailed_financials.balance_sheet", params)
    
    def get_stock_income_statement(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取利润表"""
        return self._execute_interface_with_batch("stock", "financials.detailed_financials.income_statement", params)
    
    def get_stock_cash_flow(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取现金流量表"""
        return self._execute_interface_with_batch("stock", "financials.detailed_financials.cash_flow", params)
    
    def get_stock_dividend(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取分红数据"""
        return self._execute_interface_with_batch("stock", "financials.dividend", params)
    
    # 股票持仓数据
    def get_stock_institutional_holdings(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取机构持仓数据（包含基金、保险、券商等大资金）"""
        return self._execute_interface_with_batch("stock", "holdings.institutional_holdings", params)
    
    def get_stock_hsgt_holdings(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取沪深港通持仓数据"""
        return self._execute_interface_with_batch("stock", "holdings.hsgt_holdings", params)
    
    # 股票研究分析数据
    def get_stock_research_reports(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取研报数据"""
        return self._execute_interface_with_batch("stock", "research_and_analyst.research_reports", params)
    
    def get_stock_forecast_consensus(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取预测共识数据"""
        return self._execute_interface_with_batch("stock", "research_and_analyst.forecast_consensus", params)
    
    def get_stock_opinions(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取机构观点数据"""
        return self._execute_interface_with_batch("stock", "research_and_analyst.opinions", params)
    
    # 股票技术分析
    def get_innovation_high_ranking(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取创新高股票排名"""
        return self._execute_interface_with_batch("stock", "technical_analysis.innovation_high", params)
    
    def get_innovation_low_ranking(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取创新低股票排名"""
        return self._execute_interface_with_batch("stock", "technical_analysis.innovation_low", params)
    
    def get_volume_price_rise_ranking(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取量价齐升股票排名"""
        return self._execute_interface_with_batch("stock", "technical_analysis.volume_price_rise", params)
    
    def get_continuous_rise_ranking(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取连续上涨股票排名"""
        return self._execute_interface_with_batch("stock", "technical_analysis.continuous_rise", params)
    
    def get_volume_price_fall_ranking(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取量价齐跌股票排名"""
        return self._execute_interface_with_batch("stock", "technical_analysis.volume_price_fall", params)
    
    def get_volume_shrink_ranking(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取创新缩量股票排名"""
        return self._execute_interface_with_batch("stock", "technical_analysis.volume_shrink", params)

    def get_stock_valuation(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取个股估值数据"""
        return self._execute_interface_with_batch("stock", "valuation", params)
    
    # 股票ESG数据
    def get_stock_esg_rating(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取股票ESG评级数据"""
        return self._execute_interface_with_batch("stock", "esg_data.esg_rating", params)
    
    # 股票事件数据
    def get_stock_major_contracts(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取重大合同事件数据"""
        return self._execute_interface_with_batch("stock", "events.major_contracts", params)
    
    def get_stock_suspension(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取停牌事件数据"""
        return self._execute_interface_with_batch("stock", "events.suspension", params)
    
    # 股票新股数据
    def get_stock_ipo_data(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取新股发行数据"""
        return self._execute_interface_with_batch("stock", "new_stock.ipo_data", params)
    
    def get_stock_ipo_performance(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取新股表现数据"""
        return self._execute_interface_with_batch("stock", "new_stock.performance", params)
    
    # 股票回购数据
    def get_stock_repurchase_plan(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取回购计划数据"""
        return self._execute_interface_with_batch("stock", "repurchase.repurchase_plan", params)
    
    def get_stock_repurchase_progress(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取回购进度数据"""
        return self._execute_interface_with_batch("stock", "repurchase.repurchase_progress", params)
    
    # 股票大宗交易数据
    def get_stock_block_trading(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取个股大宗交易数据"""
        return self._execute_interface_with_batch("stock", "block_trading", params)

    # ==================== 市场相关接口 (MARKET) ====================
    
    # 市场基础数据
    def get_stock_list(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取市场股票列表"""
        return self._execute_interface_with_batch("market", "stock_list", params)
    
    def get_market_overview(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取市场概览数据"""
        return self._execute_interface_with_batch("market", "market_overview", params)
    
    def get_market_indices(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取市场指数数据"""
        return self._execute_interface_with_batch("market", "market_indices", params)
    
    def get_market_activity(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取市场活跃度数据"""
        return self._execute_interface_with_batch("market", "market_activity", params)
    
    def get_market_sentiment(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取市场情绪数据"""
        return self._execute_interface_with_batch("market", "market_sentiment", params)
    
    # 市场资金流向数据
    def get_market_fund_flow(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取市场级别资金流向数据"""
        return self._execute_interface_with_batch("market", "fund_flow.market_level", params)
    
    def get_hsgt_fund_flow(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取沪深港通资金流向数据"""
        return self._execute_interface_with_batch("market", "fund_flow.hsgt_flow", params)
    
    def get_big_deal_tracking(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取大单追踪数据"""
        return self._execute_interface_with_batch("market", "fund_flow.big_deal_tracking", params)

    # 市场大宗交易数据
    def get_market_block_trading(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取市场大宗交易统计数据"""
        return self._execute_interface_with_batch("market", "block_trading", params)
    
    # 市场板块数据
    def get_sector_quote(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取行业板块行情数据"""
        return self._execute_interface_with_batch("market", "sector_data.sector_quote", params)
    
    def get_sector_constituent_quotes(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取行业板块成分股行情数据"""
        return self._execute_interface_with_batch("market", "sector_data.constituent_quotes", params)
    
    def get_sector_fund_flow(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取行业板块资金流向数据"""
        return self._execute_interface_with_batch("market", "sector_data.sector_fund_flow", params)
    
    # 市场概念数据
    def get_concept_quote(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取概念板块行情数据"""
        return self._execute_interface_with_batch("market", "concept_data.concept_quote", params)
    
    def get_concept_constituent_quotes(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取概念板块成分股行情数据"""
        return self._execute_interface_with_batch("market", "concept_data.constituent_quotes", params)
    
    def get_concept_fund_flow(self, params: Union[StandardParams, Dict[str, Any], List[Union[StandardParams, Dict[str, Any]]]]) -> Union[ExtractionResult, List[ExtractionResult]]:
        """获取概念板块资金流向数据"""
        return self._execute_interface_with_batch("market", "concept_data.concept_fund_flow", params)
    
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
    
    def _should_use_async_execution(self, interface_count: int) -> bool:
        """判断是否应该使用异步执行"""
        # 检查是否启用异步执行
        if not getattr(self.config.global_config, 'enable_async_execution', True):
            return False
        
        # 检查接口数量阈值
        async_threshold = getattr(self.config.global_config, 'async_execution_threshold', 2)
        if interface_count < async_threshold:
            return False
        
        # 检查最大并发数配置
        max_concurrency = getattr(self.config.global_config, 'async_max_concurrency', 10)
        if max_concurrency <= 0:
            return False
        
        return True