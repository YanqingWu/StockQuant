#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
接口分析工具 - 全面分析所有Akshare接口
分析接口参数、返回数据格式、性能表现等，为配置优化提供数据支持
"""

import logging
import time
import sys
import os
import json
import pandas as pd
import asyncio
import threading
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入必要的模块
from core.data.interfaces.executor import InterfaceExecutor, CallResult, ExecutorConfig, RetryConfig, TaskManager, CallTask, ExecutionContext
from core.data.interfaces.base import APIProviderManager, InterfaceMetadata, FunctionCategory
from core.data.interfaces.akshare import akshare_provider
from core.data.extractor.adapter import (
    StandardParams,
    to_standard_params,
    adapt_params_for_interface,
)
from core.data.extractor.config_loader import ConfigLoader


@dataclass
class InterfaceAnalysisResult:
    """接口分析结果"""
    interface_name: str
    success: bool
    execution_time: float
    error_message: Optional[str] = None
    
    # 参数信息
    input_params: Dict[str, Any] = None
    adapted_params: Dict[str, Any] = None
    
    # 返回数据信息
    data_type: str = None
    data_shape: Tuple[int, int] = None
    columns: List[str] = None
    sample_data: Any = None
    data_size: int = 0
    
    # 接口元数据
    description: str = None
    category: str = None
    data_source: str = None
    required_params: List[str] = None
    optional_params: List[str] = None
    
    # 配置信息
    priority: int = None
    enabled: bool = None
    used_in_config: bool = False
    config_category: str = None
    config_data_type: str = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        result = asdict(self)
        # 处理不可序列化的数据
        if isinstance(result.get('sample_data'), (pd.DataFrame, pd.Series)):
            result['sample_data'] = result['sample_data'].to_dict('records') if hasattr(result['sample_data'], 'to_dict') else str(result['sample_data'])
        
        # 处理其他不可序列化的对象
        def convert_to_serializable(obj):
            if isinstance(obj, (pd.DataFrame, pd.Series)):
                return obj.to_dict('records') if hasattr(obj, 'to_dict') else str(obj)
            elif hasattr(obj, 'isoformat'):  # datetime, date等
                return obj.isoformat()
            elif isinstance(obj, (set, frozenset)):
                return list(obj)
            elif hasattr(obj, '__dict__'):
                return str(obj)
            else:
                return obj
        
        # 递归处理所有值
        def recursive_convert(d):
            if isinstance(d, dict):
                return {k: recursive_convert(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [recursive_convert(item) for item in d]
            else:
                return convert_to_serializable(d)
        
        result = recursive_convert(result)
        return result


class InterfaceAnalyzer:
    """接口分析器"""
    
    def __init__(self, results_file: str = "interface_analysis_results.json", save_interval: int = 30):
        self.logger = self._setup_logger()
        self.provider_manager = self._setup_provider_manager()
        self.executor = self._setup_executor()
        self.task_manager = TaskManager(self.executor)
        self.config_loader = ConfigLoader()
        self.results_file = results_file
        self.save_interval = save_interval  # 保存间隔（秒）
        self.analysis_results = []
        
        # 线程安全锁
        self._results_lock = threading.Lock()
        self._save_lock = threading.Lock()
        
        # 定期保存任务
        self._save_task = None
        self._stop_save_task = threading.Event()
        
        # 获取所有接口
        self.interfaces = self._get_all_interfaces()
        self.logger.info(f"发现 {len(self.interfaces)} 个接口")
        
        # 获取配置中使用的接口
        self.config_interfaces = self._get_config_interfaces()
        self.logger.info(f"配置中使用了 {len(self.config_interfaces)} 个接口")
        
        # 加载已分析的结果
        self._load_existing_results()
    
    def _load_existing_results(self):
        """加载已分析的结果（仅支持新格式）"""
        self.analysis_results = []
        if not os.path.exists(self.results_file):
            return
        try:
            with open(self.results_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not (isinstance(data, dict) and 'interfaces' in data and isinstance(data['interfaces'], list)):
                self.logger.info("结果文件格式不兼容，忽略加载")
                return
            interface_dicts = data['interfaces']
            for interface_dict in interface_dicts:
                result = InterfaceAnalysisResult(
                    interface_name=interface_dict.get('interface_name', ''),
                    success=interface_dict.get('success', False),
                    execution_time=interface_dict.get('execution_time', 0.0),
                    error_message=interface_dict.get('error_message'),
                    input_params=interface_dict.get('input_params'),
                    adapted_params=interface_dict.get('adapted_params'),
                    data_type=interface_dict.get('data_type'),
                    data_shape=tuple(interface_dict.get('data_shape', (0, 0))) if interface_dict.get('data_shape') else None,
                    columns=interface_dict.get('columns'),
                    sample_data=interface_dict.get('sample_data'),
                    data_size=interface_dict.get('data_size', 0),
                    description=interface_dict.get('description'),
                    category=interface_dict.get('category'),
                    data_source=interface_dict.get('data_source'),
                    required_params=interface_dict.get('required_params'),
                    optional_params=interface_dict.get('optional_params'),
                    priority=interface_dict.get('priority'),
                    enabled=interface_dict.get('enabled'),
                    used_in_config=interface_dict.get('used_in_config', False),
                    config_category=interface_dict.get('config_category'),
                    config_data_type=interface_dict.get('config_data_type')
                )
                self.analysis_results.append(result)
            self.logger.info(f"加载了 {len(self.analysis_results)} 个已分析的结果")
        except Exception as e:
            self.logger.warning(f"加载已分析结果失败: {e}")
            self.analysis_results = []
    
    def _get_analyzed_interface_names(self) -> set:
        """获取已分析的接口名称集合"""
        with self._results_lock:
            return {result.interface_name for result in self.analysis_results if result.interface_name}
    
    def _start_periodic_save(self):
        """启动定期保存任务"""
        def save_worker():
            while not self._stop_save_task.is_set():
                if self._stop_save_task.wait(self.save_interval):
                    break  # 收到停止信号
                
                # 执行保存
                try:
                    # 获取当前结果数量（线程安全）
                    with self._results_lock:
                        current_count = len(self.analysis_results)
                    
                    self._save_analysis_results_thread_safe()
                    self.logger.info(f"定期保存完成，当前已分析 {current_count} 个接口")
                except Exception as e:
                    self.logger.error(f"定期保存失败: {e}")
        
        self._save_task = threading.Thread(target=save_worker, daemon=True)
        self._save_task.start()
        self.logger.info(f"启动定期保存任务，间隔 {self.save_interval} 秒")
    
    def _stop_periodic_save(self):
        """停止定期保存任务"""
        if self._save_task and self._save_task.is_alive():
            self._stop_save_task.set()
            self._save_task.join(timeout=5)  # 等待最多5秒
            self.logger.info("定期保存任务已停止")
    
    def _add_analysis_result(self, result: InterfaceAnalysisResult):
        """线程安全地添加分析结果"""
        with self._results_lock:
            self.analysis_results.append(result)

    def _clear_failed_analysis_results(self):
        """清除之前失败的接口分析结果"""
        with self._results_lock:
            initial_count = len(self.analysis_results)
            self.analysis_results = [
                result for result in self.analysis_results if result.success
            ]
            cleared_count = initial_count - len(self.analysis_results)
            if cleared_count > 0:
                self.logger.info(f"已清除 {cleared_count} 个之前失败的接口分析结果。")

    def _save_analysis_results_thread_safe(self):
        """线程安全地保存分析结果"""
        with self._save_lock:
            # 复制当前结果，避免长时间持有锁
            with self._results_lock:
                results_copy = self.analysis_results.copy()
            
            results_data = {
                'analysis_timestamp': datetime.now().isoformat(),
                'total_interfaces': len(results_copy),
                'interfaces': [r.to_dict() for r in results_copy]
            }
            
            # 写入临时文件，然后原子性重命名
            temp_file = f"{self.results_file}.tmp"
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(results_data, f, ensure_ascii=False, indent=2, default=str)
            
            # 原子性重命名
            os.rename(temp_file, self.results_file)
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('interface_analysis.log', encoding='utf-8')
            ]
        )
        return logging.getLogger(__name__)
    
    def _setup_provider_manager(self) -> APIProviderManager:
        """设置提供者管理器"""
        manager = APIProviderManager()
        manager.register_provider(akshare_provider)
        return manager
    
    def _setup_executor(self) -> InterfaceExecutor:
        """设置执行器"""
        retry_config = RetryConfig(max_retries=3)
        config = ExecutorConfig(
            default_timeout=0,  # 无超时限制
            retry_config=retry_config
        )
        return InterfaceExecutor(self.provider_manager, config)
    
    def _get_all_interfaces(self) -> List[InterfaceMetadata]:
        """获取所有接口"""
        all_interfaces = []
        for provider in self.provider_manager._providers.values():
            all_interfaces.extend(provider.registry._interfaces.values())
        return all_interfaces
    
    def _get_config_interfaces(self) -> Dict[str, Dict[str, Any]]:
        """获取配置中使用的接口信息"""
        config_interfaces = {}
        
        # 加载配置文件
        config = self.config_loader.load_from_file('core/data/extractor/extraction_config.yaml')
        
        for category_name, category_config in config.data_categories.items():
            for data_type_name, data_type_config in category_config.data_types.items():
                for interface_config in data_type_config.interfaces:
                    interface_name = interface_config.name
                    config_interfaces[interface_name] = {
                        'category': category_name,
                        'data_type': data_type_name,
                        'priority': interface_config.priority,
                        'enabled': interface_config.enabled
                    }
        
        return config_interfaces
    
    def _generate_params_for_interface(self, interface: InterfaceMetadata) -> StandardParams:
        """为接口生成参数"""
        base = interface.example_params or {}
        try:
            return to_standard_params(base)
        except Exception as e:
            self.logger.debug(f"to_standard_params 失败，返回空标准参数: {e}")
            return StandardParams()
    
    def _analyze_data_structure(self, data: Any) -> Dict[str, Any]:
        """分析数据结构"""
        if data is None:
            return {
                'data_type': 'None',
                'data_shape': (0, 0),
                'columns': [],
                'sample_data': None,
                'data_size': 0
            }
        
        try:
            if isinstance(data, pd.DataFrame):
                return {
                    'data_type': 'DataFrame',
                    'data_shape': data.shape,
                    'columns': list(data.columns),
                    'sample_data': data.head(3).to_dict('records') if not data.empty else [],
                    'data_size': len(data)
                }
            elif isinstance(data, pd.Series):
                return {
                    'data_type': 'Series',
                    'data_shape': (len(data), 1),
                    'columns': [data.name] if data.name else ['value'],
                    'sample_data': data.head(3).to_dict() if not data.empty else {},
                    'data_size': len(data)
                }
            elif isinstance(data, list):
                return {
                    'data_type': 'list',
                    'data_shape': (len(data), 1),
                    'columns': ['item'],
                    'sample_data': data[:3] if data else [],
                    'data_size': len(data)
                }
            elif isinstance(data, dict):
                return {
                    'data_type': 'dict',
                    'data_shape': (1, len(data)),
                    'columns': list(data.keys()),
                    'sample_data': data,
                    'data_size': 1
                }
            else:
                return {
                    'data_type': type(data).__name__,
                    'data_shape': (1, 1),
                    'columns': ['value'],
                    'sample_data': str(data)[:200],  # 限制长度
                    'data_size': 1
                }
        except Exception as e:
            self.logger.debug(f"分析数据结构失败: {e}")
            return {
                'data_type': 'unknown',
                'data_shape': (0, 0),
                'columns': [],
                'sample_data': str(data)[:200],
                'data_size': 0
            }
    
    def _calculate_data_info(self, data: Any) -> Dict[str, Any]:
        """计算数据信息（与_analyze_data_structure相同，保持兼容性）"""
        return self._analyze_data_structure(data)
    
    def analyze_single_interface(self, interface: InterfaceMetadata) -> InterfaceAnalysisResult:
        """分析单个接口"""
        start_time = time.time()
        
        try:
            # 生成标准参数
            std_params = self._generate_params_for_interface(interface)
            input_params = std_params.to_dict()
            
            # 适配参数
            adapted_params = adapt_params_for_interface(interface.name, std_params)
            
            # 执行调用
            result = self.executor.execute_single(interface.name, adapted_params)
            
            # 分析数据结构
            data_info = self._analyze_data_structure(result.data)
            
            # 获取配置信息
            config_info = self.config_interfaces.get(interface.name, {})
            
            analysis_result = InterfaceAnalysisResult(
                interface_name=interface.name,
                success=result.success,
                execution_time=time.time() - start_time,
                error_message=str(result.error) if result.error else None,
                input_params=input_params,
                adapted_params=adapted_params,
                data_type=data_info['data_type'],
                data_shape=data_info['data_shape'],
                columns=data_info['columns'],
                sample_data=data_info['sample_data'],
                data_size=data_info['data_size'],
                description=interface.description,
                category=interface.function_category.value,
                data_source=interface.data_source.value,
                required_params=interface.required_params,
                optional_params=interface.optional_params,
                priority=config_info.get('priority'),
                enabled=config_info.get('enabled'),
                used_in_config=interface.name in self.config_interfaces,
                config_category=config_info.get('category'),
                config_data_type=config_info.get('data_type')
            )
            
            return analysis_result
            
        except Exception as e:
            return InterfaceAnalysisResult(
                interface_name=interface.name,
                success=False,
                execution_time=time.time() - start_time,
                error_message=f"分析异常: {str(e)}",
                input_params=std_params.to_dict() if 'std_params' in locals() else {},
                adapted_params=adapted_params if 'adapted_params' in locals() else {},
                description=interface.description,
                category=interface.function_category.value,
                data_source=interface.data_source.value,
                required_params=interface.required_params,
                optional_params=interface.optional_params,
                used_in_config=interface.name in self.config_interfaces
            )
    
    async def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """运行全面分析（异步批量执行）"""
        # 在每次运行前清除之前失败的分析结果
        self._clear_failed_analysis_results()

        # 获取已分析的接口
        analyzed_names = self._get_analyzed_interface_names()
        
        # 筛选需要分析的接口
        interfaces_to_analyze = [
            interface for interface in self.interfaces 
            if interface.name not in analyzed_names
        ]
        
        if not interfaces_to_analyze:
            self.logger.info("所有接口都已分析过，无需重新分析")
            return self._generate_analysis_report(0)
        
        self.logger.info(f"开始分析 {len(interfaces_to_analyze)} 个新接口（跳过 {len(analyzed_names)} 个已分析接口）")
        start_time = time.time()
        
        # 启动定期保存任务
        self._start_periodic_save()
        
        try:
            # 创建批量任务
            tasks = []
            params_map: Dict[str, Dict[str, Any]] = {}
            for interface in interfaces_to_analyze:
                try:
                    # 生成参数
                    params = self._generate_params_for_interface(interface)
                    adapted_params = adapt_params_for_interface(interface.name, params)
                    
                    # 创建任务
                    task = self.task_manager.create_task(
                        interface_name=interface.name,
                        params=adapted_params,
                        priority=1,
                        timeout=0,  # 无超时限制
                        metadata={
                            'analysis': True,
                            'interface_metadata': {
                                'description': interface.description,
                                'category': interface.function_category.value,
                                'data_source': interface.data_source.value,
                                'required_params': interface.required_params,
                                'optional_params': interface.optional_params,
                            }
                        }
                    )
                    # 记录参数（按 task_id 追踪）
                    params_map[task.task_id] = {
                        'input_params': params.to_dict() if isinstance(params, StandardParams) else dict(params or {}),
                        'adapted_params': adapted_params,
                    }
                    tasks.append(task)
                    
                except Exception as e:
                    self.logger.error(f"为接口 {interface.name} 创建任务失败: {str(e)}")
                    # 创建失败结果记录
                    failed_result = InterfaceAnalysisResult(
                        interface_name=interface.name,
                        success=False,
                        execution_time=0.0,
                        error_message=f"任务创建失败: {str(e)}",
                        description=interface.description,
                        category=interface.function_category.value,
                        data_source=interface.data_source.value,
                        used_in_config=interface.name in self.config_interfaces
                    )
                    self._add_analysis_result(failed_result)
            
            if not tasks:
                self.logger.warning("没有可执行的任务")
                return self._generate_analysis_report(0)
            
            # 批量添加任务
            self.task_manager.add_tasks(tasks)
            
            # 异步批量执行
            self.logger.info(f"开始异步批量执行 {len(tasks)} 个任务")
            
            # 创建接口名称到接口对象的映射
            interface_map = {interface.name: interface for interface in interfaces_to_analyze}
            
            # 定义结果回调函数
            def result_callback(result: CallResult):
                interface_name = result.interface_name
                interface = interface_map.get(interface_name)
                
                if interface:
                    config_info = self.config_interfaces.get(interface_name, {})
                    param_rec = params_map.get(result.task_id, {})
                    input_params = param_rec.get('input_params', {})
                    adapted_params_rec = param_rec.get('adapted_params', {})
                    if result.success:
                        # 计算数据信息
                        data_info = self._calculate_data_info(result.data)
                        
                        # 创建分析结果
                        analysis_result = InterfaceAnalysisResult(
                            interface_name=interface_name,
                            success=True,
                            execution_time=result.execution_time,
                            input_params=input_params,
                            adapted_params=adapted_params_rec,
                            data_type=data_info['data_type'],
                            data_shape=data_info['data_shape'],
                            columns=data_info['columns'],
                            sample_data=data_info['sample_data'],
                            data_size=data_info['data_size'],
                            description=interface.description,
                            category=interface.function_category.value,
                            data_source=interface.data_source.value,
                            required_params=interface.required_params,
                            optional_params=interface.optional_params,
                            priority=config_info.get('priority'),
                            enabled=config_info.get('enabled'),
                            used_in_config=interface_name in self.config_interfaces,
                            config_category=config_info.get('category'),
                            config_data_type=config_info.get('data_type')
                        )
                        self._add_analysis_result(analysis_result)
                    else:
                        # 处理失败的结果
                        failed_result = InterfaceAnalysisResult(
                            interface_name=interface_name,
                            success=False,
                            execution_time=result.execution_time,
                            error_message=str(result.error) if result.error else None,
                            input_params=input_params,
                            adapted_params=adapted_params_rec,
                            description=interface.description,
                            category=interface.function_category.value,
                            data_source=interface.data_source.value,
                            priority=config_info.get('priority'),
                            enabled=config_info.get('enabled'),
                            used_in_config=interface_name in self.config_interfaces,
                            config_category=config_info.get('category'),
                            config_data_type=config_info.get('data_type')
                        )
                        self._add_analysis_result(failed_result)
            
            # 使用流式执行：通过 ExecutionContext.post_execute_hook 注入回调
            context = ExecutionContext()
            context.post_execute_hook = result_callback
            
            batch_result = await self.task_manager.execute_all_async(context=context)
            
            self.logger.info(f"流式执行完成，处理了 {batch_result.total_tasks} 个任务")
            
            # 生成分析报告
            total_time = time.time() - start_time
            report = self._generate_analysis_report(total_time)
            
            # 最终保存
            self._save_analysis_results_thread_safe()
            self._save_detailed_reports(report)
            
            self.logger.info(f"批量分析完成，总耗时: {total_time:.2f}s")
            return report
            
        finally:
            # 停止定期保存任务
            self._stop_periodic_save()
    
    def _process_batch_results(self, batch_result, interfaces_to_analyze):
        """处理批量执行结果"""
        # 创建接口名称到接口对象的映射
        interface_map = {interface.name: interface for interface in interfaces_to_analyze}
        
        # 处理成功的结果
        for result in batch_result.results:
            if result.success:
                interface_name = result.interface_name
                interface = interface_map.get(interface_name)
                
                if interface:
                    # 计算数据信息
                    data_info = self._calculate_data_info(result.data)
                    config_info = self.config_interfaces.get(interface_name, {})
                    
                    # 创建分析结果（无法从 CallResult 恢复原始参数，置空）
                    analysis_result = InterfaceAnalysisResult(
                        interface_name=interface_name,
                        success=True,
                        execution_time=result.execution_time,
                        input_params={},
                        adapted_params={},
                        data_type=data_info['data_type'],
                        data_shape=data_info['data_shape'],
                        columns=data_info['columns'],
                        sample_data=data_info['sample_data'],
                        data_size=data_info['data_size'],
                        description=interface.description,
                        category=interface.function_category.value,
                        data_source=interface.data_source.value,
                        required_params=interface.required_params,
                        optional_params=interface.optional_params,
                        priority=config_info.get('priority'),
                        enabled=config_info.get('enabled'),
                        used_in_config=interface_name in self.config_interfaces,
                        config_category=config_info.get('category'),
                        config_data_type=config_info.get('data_type')
                    )
                    self._add_analysis_result(analysis_result)
            else:
                # 处理失败的结果
                interface_name = result.interface_name
                interface = interface_map.get(interface_name)
                
                if interface:
                    config_info = self.config_interfaces.get(interface_name, {})
                    failed_result = InterfaceAnalysisResult(
                        interface_name=interface_name,
                        success=False,
                        execution_time=result.execution_time,
                        error_message=str(result.error) if result.error else None,
                        description=interface.description,
                        category=interface.function_category.value,
                        data_source=interface.data_source.value,
                        priority=config_info.get('priority'),
                        enabled=config_info.get('enabled'),
                        used_in_config=interface_name in self.config_interfaces,
                        config_category=config_info.get('category'),
                        config_data_type=config_info.get('data_type')
                    )
                    self._add_analysis_result(failed_result)
        
        self.logger.info(f"处理了 {len(batch_result.results)} 个批量执行结果")
    
    def _generate_analysis_report(self, total_time: float) -> Dict[str, Any]:
        """生成分析报告"""
        with self._results_lock:
            total_interfaces = len(self.analysis_results)
            successful_interfaces = sum(1 for r in self.analysis_results if r.success)
            failed_interfaces = total_interfaces - successful_interfaces
        
        # 按功能分类统计
        by_category = {}
        with self._results_lock:
            for result in self.analysis_results:
                category = result.category or 'unknown'
                if category not in by_category:
                    by_category[category] = {'total': 0, 'success': 0, 'failed': 0}
                
                by_category[category]['total'] += 1
                if result.success:
                    by_category[category]['success'] += 1
                else:
                    by_category[category]['failed'] += 1
        
        # 按数据源统计
        by_data_source = {}
        with self._results_lock:
            for result in self.analysis_results:
                source = result.data_source or 'unknown'
                if source not in by_data_source:
                    by_data_source[source] = {'total': 0, 'success': 0, 'failed': 0}
                
                by_data_source[source]['total'] += 1
                if result.success:
                    by_data_source[source]['success'] += 1
                else:
                    by_data_source[source]['failed'] += 1
        
        # 配置使用情况
        with self._results_lock:
            used_in_config = sum(1 for r in self.analysis_results if r.used_in_config)
            unused_interfaces = [r for r in self.analysis_results if not r.used_in_config]
        
        # 失败接口详情
        with self._results_lock:
            failed_interfaces = [
                {
                    'name': r.interface_name,
                    'error': r.error_message,
                    'execution_time': r.execution_time,
                    'category': r.category,
                    'used_in_config': r.used_in_config
                }
                for r in self.analysis_results if not r.success
            ]
        
        # 性能统计
        with self._results_lock:
            successful_results = [r for r in self.analysis_results if r.success]
            if successful_results:
                avg_execution_time = sum(r.execution_time for r in successful_results) / len(successful_results)
                fastest_interfaces = sorted(successful_results, key=lambda x: x.execution_time)[:5]
                slowest_interfaces = sorted(successful_results, key=lambda x: x.execution_time, reverse=True)[:5]
            else:
                avg_execution_time = 0
                fastest_interfaces = []
                slowest_interfaces = []
        
        # 数据格式统计
        data_types = {}
        with self._results_lock:
            for result in self.analysis_results:
                if result.success and result.data_type:
                    data_type = result.data_type
                    if data_type not in data_types:
                        data_types[data_type] = 0
                    data_types[data_type] += 1
        
        report = {
            'summary': {
                'total_interfaces': total_interfaces,
                'successful_interfaces': successful_interfaces,
                'failed_interfaces': failed_interfaces,
                'success_rate': successful_interfaces / total_interfaces if total_interfaces > 0 else 0,
                'total_analysis_time': total_time,
                'average_execution_time': avg_execution_time,
                'used_in_config': used_in_config,
                'unused_interfaces': len(unused_interfaces)
            },
            'by_category': by_category,
            'by_data_source': by_data_source,
            'data_types': data_types,
            'failed_interfaces': failed_interfaces,
            'unused_interfaces': [{'name': r.interface_name, 'category': r.category} for r in unused_interfaces],
            'fastest_interfaces': [{'name': r.interface_name, 'execution_time': r.execution_time} for r in fastest_interfaces],
            'slowest_interfaces': [{'name': r.interface_name, 'execution_time': r.execution_time} for r in slowest_interfaces]
        }
        
        return report
    
    def _save_analysis_results(self):
        """保存分析结果（统一委托线程安全方法）"""
        self._save_analysis_results_thread_safe()
        self.logger.info(f"分析结果已保存到: {self.results_file}")
    
    def _save_detailed_reports(self, report: Dict[str, Any]):
        """保存详细报告"""
        # 保存摘要报告
        with open('interface_analysis_summary.txt', 'w', encoding='utf-8') as f:
            f.write("接口分析摘要报告\n")
            f.write("=" * 80 + "\n\n")
            
            summary = report['summary']
            f.write(f"总接口数: {summary['total_interfaces']}\n")
            f.write(f"成功接口: {summary['successful_interfaces']}\n")
            f.write(f"失败接口: {summary['failed_interfaces']}\n")
            f.write(f"成功率: {summary['success_rate']:.2%}\n")
            f.write(f"总耗时: {summary['total_analysis_time']:.2f}s\n")
            f.write(f"平均耗时: {summary['average_execution_time']:.3f}s\n")
            f.write(f"配置中使用: {summary['used_in_config']}\n")
            f.write(f"未使用接口: {summary['unused_interfaces']}\n\n")
            
            # 按分类统计
            f.write("按功能分类统计:\n")
            f.write("-" * 40 + "\n")
            for category, stats in report['by_category'].items():
                success_rate = stats['success'] / stats['total'] if stats['total'] > 0 else 0
                f.write(f"{category}: {stats['success']}/{stats['total']} ({success_rate:.1%})\n")
            
            f.write("\n按数据源统计:\n")
            f.write("-" * 40 + "\n")
            for source, stats in report['by_data_source'].items():
                success_rate = stats['success'] / stats['total'] if stats['total'] > 0 else 0
                f.write(f"{source}: {stats['success']}/{stats['total']} ({success_rate:.1%})\n")
            
            f.write("\n数据格式统计:\n")
            f.write("-" * 40 + "\n")
            for data_type, count in report['data_types'].items():
                f.write(f"{data_type}: {count}\n")
        
        # 保存失败接口报告
        with open('failed_interfaces_report.txt', 'w', encoding='utf-8') as f:
            f.write("失败接口详细报告\n")
            f.write("=" * 80 + "\n\n")
            
            for failed in report['failed_interfaces']:
                f.write(f"接口名称: {failed['name']}\n")
                f.write(f"错误信息: {failed['error']}\n")
                f.write(f"执行时间: {failed['execution_time']:.3f}s\n")
                f.write(f"功能分类: {failed['category']}\n")
                f.write(f"配置中使用: {failed['used_in_config']}\n")
                f.write("-" * 80 + "\n\n")
        
        # 保存未使用接口报告
        with open('unused_interfaces_report.txt', 'w', encoding='utf-8') as f:
            f.write("未在配置中使用的接口\n")
            f.write("=" * 80 + "\n\n")
            
            for unused in report['unused_interfaces']:
                f.write(f"接口名称: {unused['name']}\n")
                f.write(f"功能分类: {unused['category']}\n")
                f.write("-" * 40 + "\n")
        
        # 保存数据样本
        with open('interface_data_samples.json', 'w', encoding='utf-8') as f:
            samples = {}
            for result in self.analysis_results:
                if result.success and result.sample_data:
                    samples[result.interface_name] = {
                        'data_type': result.data_type,
                        'data_shape': result.data_shape,
                        'columns': result.columns,
                        'sample_data': result.sample_data
                    }
            json.dump(samples, f, ensure_ascii=False, indent=2)
        
        self.logger.info("详细报告已保存")
        self.logger.info("- interface_analysis_summary.txt")
        self.logger.info("- failed_interfaces_report.txt") 
        self.logger.info("- unused_interfaces_report.txt")
        self.logger.info("- interface_data_samples.json")


async def run_interface_analysis():
    """运行接口分析（异步版本）"""
    try:
        analyzer = InterfaceAnalyzer()
        report = await analyzer.run_comprehensive_analysis()
        
        # 打印分析报告
        print("\n" + "=" * 80)
        print("接口分析报告")
        print("=" * 80)
        
        summary = report['summary']
        print(f"总接口数: {summary['total_interfaces']}")
        print(f"成功接口: {summary['successful_interfaces']}")
        print(f"失败接口: {summary['failed_interfaces']}")
        print(f"成功率: {summary['success_rate']:.2%}")
        print(f"总耗时: {summary['total_analysis_time']:.2f}s")
        print(f"平均耗时: {summary['average_execution_time']:.3f}s")
        print(f"配置中使用: {summary['used_in_config']}")
        print(f"未使用接口: {summary['unused_interfaces']}")
        
        # 按功能分类统计
        print("\n按功能分类统计:")
        for category, stats in report['by_category'].items():
            success_rate = stats['success'] / stats['total'] if stats['total'] > 0 else 0
            print(f"  {category}: {stats['success']}/{stats['total']} ({success_rate:.1%})")
        
        # 失败接口
        if report['failed_interfaces']:
            print(f"\n失败接口 ({len(report['failed_interfaces'])} 个):")
            for failed in report['failed_interfaces'][:10]:  # 只显示前10个
                print(f"  ✗ {failed['name']} - {failed['error'][:100]}...")
        
        print("=" * 80)
        
        return summary['success_rate'] > 0.1
        
    except Exception as e:
        print(f"分析运行失败: {e}")
        return False


def main():
    """主函数"""
    success = asyncio.run(run_interface_analysis())
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
