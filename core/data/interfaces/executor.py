"""接口执行器模块
"""

import asyncio
import logging
import time
import uuid
import random
import threading
from abc import ABC, abstractmethod
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from queue import PriorityQueue, Queue
from threading import Lock
import akshare as ak
from .base import APIProviderManager, InterfaceMetadata


logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """错误类型枚举"""
    NETWORK_ERROR = "network_error"
    TIMEOUT_ERROR = "timeout_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    VALIDATION_ERROR = "validation_error"
    CACHE_ERROR = "cache_error"
    UNKNOWN_ERROR = "unknown_error"


class ErrorClassifier:
    """错误分类器"""
    
    @staticmethod
    def classify_error(error: Exception) -> ErrorType:
        """分类错误"""
        error_name = error.__class__.__name__.lower()
        error_msg = str(error).lower()
        
        if 'timeout' in error_name or 'timeout' in error_msg:
            return ErrorType.TIMEOUT_ERROR
        elif 'rate' in error_name or 'limit' in error_msg or '429' in error_msg:
            return ErrorType.RATE_LIMIT_ERROR
        elif 'network' in error_name or 'connection' in error_msg or 'socket' in error_msg:
            return ErrorType.NETWORK_ERROR
        elif 'validation' in error_name or 'invalid' in error_msg or 'value' in error_msg:
            return ErrorType.VALIDATION_ERROR
        elif 'cache' in error_name or 'cache' in error_msg:
            return ErrorType.CACHE_ERROR
        else:
            return ErrorType.UNKNOWN_ERROR
    
    @staticmethod
    def should_retry(error_type: ErrorType, attempt: int, max_retries: int) -> bool:
        """判断是否应该重试"""
        if attempt >= max_retries - 1:
            return False
        
        # 这些错误类型应该重试
        retryable_errors = {
            ErrorType.NETWORK_ERROR,
            ErrorType.TIMEOUT_ERROR,
            ErrorType.RATE_LIMIT_ERROR
        }
        
        return error_type in retryable_errors


@dataclass
class CallTask:
    """调用任务 - 封装单个接口调用"""
    interface_name: str
    params: Dict[str, Any]
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    priority: int = 0
    retry_count: int = 3
    timeout: float = 30.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # 扩展字段，供其他模块使用
    symbol: Optional[str] = None  # 股票代码
    market: Optional[str] = None  # 市场信息
    tags: List[str] = field(default_factory=list)  # 标签
    
    def __lt__(self, other):
        """支持优先级队列排序"""
        return self.priority > other.priority  # 数值越大优先级越高


@dataclass
class CallResult:
    """调用结果"""
    task_id: str
    interface_name: str
    success: bool
    data: Any = None
    error: Optional[Exception] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass
class BatchResult:
    """批量调用结果"""
    session_id: str
    total_tasks: int
    successful_tasks: int
    failed_tasks: int
    results: List[CallResult]
    execution_summary: Dict[str, Any]
    start_time: float
    end_time: float
    
    @property
    def success_rate(self) -> float:
        """成功率"""
        return self.successful_tasks / self.total_tasks if self.total_tasks > 0 else 0.0
    
    @property
    def total_execution_time(self) -> float:
        """总执行时间"""
        return self.end_time - self.start_time


@dataclass
class RateLimit:
    """频率限制配置"""
    max_calls: int  # 最大调用次数
    time_window: float  # 时间窗口（秒）
    

class RateLimiter:
    """频率限制器"""
    
    def __init__(self, rate_limit: RateLimit):
        self.rate_limit = rate_limit
        self.calls = []
        self.lock = Lock()
    
    def acquire(self) -> bool:
        """获取调用许可"""
        with self.lock:
            now = time.time()
            # 清理过期的调用记录
            self.calls = [call_time for call_time in self.calls 
                         if now - call_time < self.rate_limit.time_window]
            
            if len(self.calls) < self.rate_limit.max_calls:
                self.calls.append(now)
                return True
            return False
    
    def wait_time(self) -> float:
        """获取需要等待的时间"""
        with self.lock:
            if not self.calls:
                return 0.0
            oldest_call = min(self.calls)
            return max(0.0, self.rate_limit.time_window - (time.time() - oldest_call))


@dataclass
class RetryConfig:
    """重试配置"""
    max_retries: int = 3
    base_delay: float = 1.0  # 基础延迟（秒）
    max_delay: float = 60.0  # 最大延迟（秒）
    exponential_base: float = 2.0  # 指数退避基数


@dataclass
class CacheConfig:
    """缓存配置"""
    enabled: bool = True
    ttl: int = 300  # 缓存时间（秒）
    max_size: int = 1000  # 最大缓存条目数


class ExecutorPlugin(ABC):
    """执行器插件接口"""
    
    @abstractmethod
    def before_execute(self, task: CallTask, context: 'ExecutionContext') -> None:
        """执行前回调"""
        pass
    
    @abstractmethod
    def after_execute(self, result: CallResult, context: 'ExecutionContext') -> None:
        """执行后回调"""
        pass
    
    @abstractmethod
    def on_error(self, task: CallTask, error: Exception, context: 'ExecutionContext') -> bool:
        """错误处理回调，返回True表示继续执行，False表示停止"""
        pass


@dataclass
class ExecutorConfig:
    """执行器配置"""
    plugins: List[ExecutorPlugin] = field(default_factory=list)
    rate_limits: Dict[str, RateLimit] = field(default_factory=dict)  # 接口名 -> 频率限制
    cache_config: Optional[CacheConfig] = None
    retry_config: RetryConfig = field(default_factory=RetryConfig)
    default_timeout: float = 0.0  # 0表示无超时，>0表示有超时
    max_workers: int = 10
    # 接口特定超时配置
    interface_timeouts: Dict[str, float] = field(default_factory=dict)
    
    # 混合超时机制配置
    enable_thread_timeout: bool = True  # 是否启用线程池超时（同步执行）
    enable_async_timeout: bool = True   # 是否启用协程超时（异步执行）
    thread_pool_max_workers: int = 10   # 线程池最大工作线程数
    async_timeout_check_interval: float = 0.1  # 异步超时检查间隔（秒）


@dataclass
class ExecutionContext:
    """执行上下文"""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    rate_limit: Optional[RateLimit] = None
    cache_enabled: bool = True
    
    # 超时控制（覆盖默认配置）
    timeout_override: Optional[float] = None  # 覆盖默认超时
    
    # 回调函数 - 供其他模块注入逻辑
    pre_execute_hook: Optional[Callable[[CallTask], None]] = None
    post_execute_hook: Optional[Callable[[CallResult], None]] = None
    error_handler: Optional[Callable[[CallTask, Exception], bool]] = None
    
    # 扩展属性
    user_data: Dict[str, Any] = field(default_factory=dict)


class SimpleCache:
    """简单缓存实现"""
    
    def __init__(self, config: CacheConfig):
        self.config = config
        self.cache = {}
        self.access_times = {}
        self.lock = Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if not self.config.enabled:
            return None
            
        with self.lock:
            if key in self.cache:
                # 检查是否过期
                if time.time() - self.access_times[key] < self.config.ttl:
                    return self.cache[key]
                else:
                    # 过期，删除
                    del self.cache[key]
                    del self.access_times[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """设置缓存"""
        if not self.config.enabled:
            return
            
        with self.lock:
            # 检查缓存大小限制
            if len(self.cache) >= self.config.max_size:
                # 删除最旧的条目
                oldest_key = min(self.access_times.keys(), key=self.access_times.get)
                del self.cache[oldest_key]
                del self.access_times[oldest_key]
            
            self.cache[key] = value
            self.access_times[key] = time.time()
    
    def clear(self) -> None:
        """清空缓存"""
        with self.lock:
            self.cache.clear()
            self.access_times.clear()


class ThreadPoolTimeoutManager:
    """线程池超时管理器 - 用于同步执行"""
    
    def __init__(self, max_workers: int = 10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.execution_history = defaultdict(list)
        self.stats_lock = threading.Lock()
    
    def get_timeout(self, interface_name: str, default_timeout: float) -> float:
        """获取接口超时时间"""
        with self.stats_lock:
            history = self.execution_history[interface_name]
            if len(history) >= 5:
                avg_time = sum(history[-10:]) / len(history[-10:])
                return max(avg_time * 2.5, default_timeout)
            return default_timeout
    
    def execute_with_timeout(self, func, args, timeout: float):
        """带超时的执行"""
        future = self.executor.submit(func, *args)
        try:
            result = future.result(timeout=timeout)
            return result
        except FutureTimeoutError:
            future.cancel()
            raise TimeoutError(f"Execution timed out after {timeout}s")
    
    def record_execution_time(self, interface_name: str, execution_time: float):
        """记录执行时间"""
        with self.stats_lock:
            self.execution_history[interface_name].append(execution_time)
            if len(self.execution_history[interface_name]) > 50:
                self.execution_history[interface_name] = self.execution_history[interface_name][-30:]
    
    def shutdown(self):
        """关闭线程池"""
        self.executor.shutdown(wait=True)


class AsyncTimeoutManager:
    """协程超时管理器 - 用于异步执行"""
    
    def __init__(self):
        self.execution_history = defaultdict(list)
        self.stats_lock = asyncio.Lock()
    
    async def get_timeout(self, interface_name: str, default_timeout: float) -> float:
        """获取接口超时时间"""
        async with self.stats_lock:
            history = self.execution_history[interface_name]
            if len(history) >= 5:
                avg_time = sum(history[-10:]) / len(history[-10:])
                return max(avg_time * 2.5, default_timeout)
            return default_timeout
    
    async def execute_with_timeout(self, coro, timeout: float):
        """带超时的协程执行"""
        try:
            result = await asyncio.wait_for(coro, timeout=timeout)
            return result
        except asyncio.TimeoutError:
            raise TimeoutError(f"Async execution timed out after {timeout}s")
    
    async def record_execution_time(self, interface_name: str, execution_time: float):
        """记录执行时间"""
        async with self.stats_lock:
            self.execution_history[interface_name].append(execution_time)
            if len(self.execution_history[interface_name]) > 50:
                self.execution_history[interface_name] = self.execution_history[interface_name][-30:]


class InterfaceExecutor:
    """接口执行器 - 专注于接口调用逻辑"""
    
    def __init__(self, 
                 provider_manager: APIProviderManager,
                 config: Optional[ExecutorConfig] = None):
        self.provider_manager = provider_manager
        self.config = config or ExecutorConfig()
        self.cache = SimpleCache(self.config.cache_config or CacheConfig())
        self.rate_limiters = {}
        
        # 初始化频率限制器
        for interface_name, rate_limit in self.config.rate_limits.items():
            self.rate_limiters[interface_name] = RateLimiter(rate_limit)
        
        # 初始化双超时管理器
        self.thread_timeout_manager = None
        self.async_timeout_manager = None
        
        if self.config.enable_thread_timeout:
            self.thread_timeout_manager = ThreadPoolTimeoutManager(
                max_workers=self.config.thread_pool_max_workers
            )
        
        if self.config.enable_async_timeout:
            self.async_timeout_manager = AsyncTimeoutManager()
    
    def _get_cache_key(self, interface_name: str, params: Dict[str, Any]) -> str:
        """生成缓存键"""
        import hashlib
        import json
        
        # 将参数排序后序列化，确保相同参数生成相同的键
        sorted_params = json.dumps(params, sort_keys=True, ensure_ascii=False)
        key_str = f"{interface_name}:{sorted_params}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _apply_rate_limit(self, interface_name: str) -> None:
        """应用频率限制"""
        if interface_name in self.rate_limiters:
            limiter = self.rate_limiters[interface_name]
            while not limiter.acquire():
                wait_time = limiter.wait_time()
                if wait_time > 0:
                    logger.debug(f"Rate limit reached for {interface_name}, waiting {wait_time:.2f}s")
                    time.sleep(wait_time)
    
    def _get_timeout_for_task(self, task: CallTask, context: ExecutionContext) -> float:
        """获取任务的超时时间"""
        # 1. 优先使用ExecutionContext中的超时覆盖
        if context.timeout_override is not None:
            return context.timeout_override
        
        # 2. 使用接口特定的超时配置
        if task.interface_name in self.config.interface_timeouts:
            return self.config.interface_timeouts[task.interface_name]
        
        # 3. 使用任务自身的超时设置
        if task.timeout > 0:
            return task.timeout
        
        # 4. 使用默认配置
        return self.config.default_timeout
    
    def _call_akshare_interface(self, task: CallTask) -> Any:
        """调用akshare接口"""
        if hasattr(ak, task.interface_name):
            func = getattr(ak, task.interface_name)
            return func(**task.params)
        else:
            raise AttributeError(f"Interface {task.interface_name} not found in akshare")
    
    def _call_akshare_interface_with_sync_timeout(self, task: CallTask, timeout: float) -> Any:
        """使用线程池超时管理器调用akshare接口（同步执行）"""
        if not self.thread_timeout_manager:
            # 如果没有启用线程池超时，回退到普通调用
            return self._call_akshare_interface(task)
        
        # 使用线程池超时管理器执行
        return self.thread_timeout_manager.execute_with_timeout(
            self._call_akshare_interface, 
            (task,), 
            timeout
        )
    
    def _execute_with_retry(self, task: CallTask, context: ExecutionContext) -> CallResult:
        """带重试的执行"""
        last_error = None
        total_attempts = 0
        
        # 确定超时时间
        timeout_seconds = self._get_timeout_for_task(task, context)
        
        # 执行插件的before_execute
        for plugin in self.config.plugins:
            try:
                plugin.before_execute(task, context)
            except Exception as e:
                logger.warning(f"Plugin {plugin.__class__.__name__} before_execute failed: {e}")
        
        for attempt in range(task.retry_count):
            total_attempts += 1
            try:
                # 应用频率限制
                self._apply_rate_limit(task.interface_name)
                
                # 检查缓存
                cache_key = self._get_cache_key(task.interface_name, task.params)
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache hit for {task.interface_name}")
                    result = CallResult(
                        task_id=task.task_id,
                        interface_name=task.interface_name,
                        success=True,
                        data=cached_result,
                        metadata={"from_cache": True}
                    )
                    
                    # 执行插件的after_execute
                    for plugin in self.config.plugins:
                        try:
                            plugin.after_execute(result, context)
                        except Exception as e:
                            logger.warning(f"Plugin {plugin.__class__.__name__} after_execute failed: {e}")
                    
                    return result
                
                # 执行接口调用（使用混合超时机制）
                start_time = time.time()
                
                # 根据配置选择超时机制
                if timeout_seconds > 0 and self.config.enable_thread_timeout and self.thread_timeout_manager:
                    # 使用线程池超时管理器（真正的超时中断）
                    data = self._call_akshare_interface_with_sync_timeout(task, timeout_seconds)
                    # 记录执行时间到超时管理器
                    execution_time = time.time() - start_time
                    self.thread_timeout_manager.record_execution_time(task.interface_name, execution_time)
                else:
                    # 使用简单的事后检查超时
                    data = self._call_akshare_interface(task)
                    execution_time = time.time() - start_time
                    
                    # 检查是否超时（事后检查）
                    if timeout_seconds > 0 and execution_time > timeout_seconds:
                        raise TimeoutError(f"Interface {task.interface_name} timed out after {execution_time:.2f}s (limit: {timeout_seconds}s)")
                
                # 缓存结果
                self.cache.set(cache_key, data)
                
                result = CallResult(
                    task_id=task.task_id,
                    interface_name=task.interface_name,
                    success=True,
                    data=data,
                    execution_time=execution_time,
                    metadata={"attempt": attempt + 1}
                )
                
                # 执行插件的after_execute
                for plugin in self.config.plugins:
                    try:
                        plugin.after_execute(result, context)
                    except Exception as e:
                        logger.warning(f"Plugin {plugin.__class__.__name__} after_execute failed: {e}")
                
                return result
                
            except Exception as e:
                last_error = e
                error_type = ErrorClassifier.classify_error(e)
                logger.warning(f"Attempt {attempt + 1} failed for {task.interface_name}: {e} (ErrorType: {error_type.value})")
                
                # 检查是否应该重试
                if not ErrorClassifier.should_retry(error_type, attempt, task.retry_count):
                    logger.info(f"Not retrying {task.interface_name} due to error type: {error_type.value}")
                    break
                
                if attempt < task.retry_count - 1:
                    # 计算退避延迟（增加jitter避免雷群效应）
                    base_delay = self.config.retry_config.base_delay * (self.config.retry_config.exponential_base ** attempt)
                    jitter = random.uniform(0.1, 0.3) * base_delay  # 添加10-30%的随机抖动
                    delay = min(base_delay + jitter, self.config.retry_config.max_delay)
                    
                    logger.debug(f"Retrying {task.interface_name} in {delay:.2f}s")
                    time.sleep(delay)
        
        # 所有重试都失败了
        error_type = ErrorClassifier.classify_error(last_error) if last_error else ErrorType.UNKNOWN_ERROR
        result = CallResult(
            task_id=task.task_id,
            interface_name=task.interface_name,
            success=False,
            error=last_error,
            metadata={
                "total_attempts": total_attempts,
                "error_type": error_type.value
            }
        )
        
        # 执行插件的after_execute
        for plugin in self.config.plugins:
            try:
                plugin.after_execute(result, context)
            except Exception as e:
                logger.warning(f"Plugin {plugin.__class__.__name__} after_execute failed: {e}")
        
        return result
    
    def execute_single(self, 
                      interface_name: str, 
                      params: Dict[str, Any],
                      context: Optional[ExecutionContext] = None) -> CallResult:
        """执行单个接口调用"""
        task = CallTask(
            interface_name=interface_name,
            params=params,
            timeout=self.config.default_timeout,
            retry_count=self.config.retry_config.max_retries
        )
        
        context = context or ExecutionContext()
        
        # 使用统一的执行方法，插件逻辑在_execute_with_retry中处理
        return self._execute_single_with_context(task, context)
    
    def execute_batch(self, 
                     tasks: List[CallTask],
                     context: Optional[ExecutionContext] = None) -> BatchResult:
        """执行批量接口调用 - 主线程串行执行避免信号冲突"""
        context = context or ExecutionContext()
        session_id = context.session_id
        start_time = time.time()
        
        results = []
        successful_tasks = 0
        failed_tasks = 0
        
        logger.info(f"Starting batch execution with {len(tasks)} tasks (session: {session_id})")
        
        # 主线程串行执行，避免信号处理冲突
        for task in tasks:
            try:
                result = self._execute_single_with_context(task, context)
                results.append(result)
                
                if result.success:
                    successful_tasks += 1
                else:
                    failed_tasks += 1
                    
            except Exception as e:
                logger.error(f"Unexpected error in task {task.task_id}: {e}")
                result = CallResult(
                    task_id=task.task_id,
                    interface_name=task.interface_name,
                    success=False,
                    error=e
                )
                results.append(result)
                failed_tasks += 1
        
        end_time = time.time()
        
        # 生成执行摘要
        execution_summary = {
            "total_execution_time": end_time - start_time,
            "average_execution_time": sum(r.execution_time for r in results if r.execution_time > 0) / len(results) if results else 0,
            "cache_hits": sum(1 for r in results if r.metadata.get("from_cache", False)),
            "interfaces_used": list(set(r.interface_name for r in results))
        }
        
        batch_result = BatchResult(
            session_id=session_id,
            total_tasks=len(tasks),
            successful_tasks=successful_tasks,
            failed_tasks=failed_tasks,
            results=results,
            execution_summary=execution_summary,
            start_time=start_time,
            end_time=end_time
        )
        
        logger.info(f"Batch execution completed: {successful_tasks}/{len(tasks)} successful (session: {session_id})")
        
        return batch_result
    
    def _execute_single_with_context(self, task: CallTask, context: ExecutionContext) -> CallResult:
        """在上下文中执行单个任务"""
        # 执行前回调
        if context.pre_execute_hook:
            context.pre_execute_hook(task)
        
        # 执行调用（插件逻辑在_execute_with_retry中统一处理）
        result = self._execute_with_retry(task, context)
        
        # 错误处理
        if not result.success and context.error_handler:
            should_continue = context.error_handler(task, result.error)
            if not should_continue:
                logger.info(f"Task {task.task_id} stopped by error handler")
        
        # 执行后回调
        if context.post_execute_hook:
            context.post_execute_hook(result)
        
        return result
    
    async def _execute_with_retry_async(self, task: CallTask, context: ExecutionContext) -> CallResult:
        """异步版本的带重试执行"""
        last_error = None
        total_attempts = 0
        
        # 确定超时时间
        timeout_seconds = self._get_timeout_for_task(task, context)
        
        # 执行插件的before_execute
        for plugin in self.config.plugins:
            try:
                plugin.before_execute(task, context)
            except Exception as e:
                logger.warning(f"Plugin {plugin.__class__.__name__} before_execute failed: {e}")
        
        for attempt in range(task.retry_count):
            total_attempts += 1
            try:
                # 应用频率限制
                self._apply_rate_limit(task.interface_name)
                
                # 检查缓存
                cache_key = self._get_cache_key(task.interface_name, task.params)
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache hit for {task.interface_name}")
                    result = CallResult(
                        task_id=task.task_id,
                        interface_name=task.interface_name,
                        success=True,
                        data=cached_result,
                        metadata={"from_cache": True}
                    )
                    
                    # 执行插件的after_execute
                    for plugin in self.config.plugins:
                        try:
                            plugin.after_execute(result, context)
                        except Exception as e:
                            logger.warning(f"Plugin {plugin.__class__.__name__} after_execute failed: {e}")
                    
                    return result
                
                # 异步执行接口调用
                start_time = time.time()
                
                # 在协程中执行同步调用
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, self._call_akshare_interface, task)
                
                execution_time = time.time() - start_time
                
                # 缓存结果
                self.cache.set(cache_key, data)
                
                result = CallResult(
                    task_id=task.task_id,
                    interface_name=task.interface_name,
                    success=True,
                    data=data,
                    execution_time=execution_time,
                    metadata={"attempt": attempt + 1}
                )
                
                # 执行插件的after_execute
                for plugin in self.config.plugins:
                    try:
                        plugin.after_execute(result, context)
                    except Exception as e:
                        logger.warning(f"Plugin {plugin.__class__.__name__} after_execute failed: {e}")
                
                return result
                
            except Exception as e:
                last_error = e
                error_type = ErrorClassifier.classify_error(e)
                logger.warning(f"Attempt {attempt + 1} failed for {task.interface_name}: {e} (ErrorType: {error_type.value})")
                
                # 检查是否应该重试
                if not ErrorClassifier.should_retry(error_type, attempt, task.retry_count):
                    logger.info(f"Not retrying {task.interface_name} due to error type: {error_type.value}")
                    break
                
                if attempt < task.retry_count - 1:
                    # 计算退避延迟（增加jitter避免雷群效应）
                    base_delay = self.config.retry_config.base_delay * (self.config.retry_config.exponential_base ** attempt)
                    jitter = random.uniform(0.1, 0.3) * base_delay  # 添加10-30%的随机抖动
                    delay = min(base_delay + jitter, self.config.retry_config.max_delay)
                    
                    logger.debug(f"Retrying {task.interface_name} in {delay:.2f}s")
                    await asyncio.sleep(delay)
        
        # 所有重试都失败了
        error_type = ErrorClassifier.classify_error(last_error) if last_error else ErrorType.UNKNOWN_ERROR
        result = CallResult(
            task_id=task.task_id,
            interface_name=task.interface_name,
            success=False,
            error=last_error,
            metadata={
                "total_attempts": total_attempts,
                "error_type": error_type.value
            }
        )
        
        # 执行插件的after_execute
        for plugin in self.config.plugins:
            try:
                plugin.after_execute(result, context)
            except Exception as e:
                logger.warning(f"Plugin {plugin.__class__.__name__} after_execute failed: {e}")
        
        return result
    
    async def _execute_single_with_context_async(self, task: CallTask, context: ExecutionContext) -> CallResult:
        """在上下文中异步执行单个任务（用于协程超时管理器）"""
        # 执行前回调
        if context.pre_execute_hook:
            context.pre_execute_hook(task)
        
        # 异步执行调用
        result = await self._execute_with_retry_async(task, context)
        
        # 错误处理
        if not result.success and context.error_handler:
            should_continue = context.error_handler(task, result.error)
            if not should_continue:
                logger.info(f"Task {task.task_id} stopped by error handler")
        
        # 执行后回调
        if context.post_execute_hook:
            context.post_execute_hook(result)
        
        return result
    
    async def execute_async(self, 
                           tasks: List[CallTask],
                           callback: Optional[Callable[[CallResult], None]] = None,
                           context: Optional[ExecutionContext] = None) -> BatchResult:
        """异步执行接口调用 - 协程调度+主线程执行避免信号冲突"""
        # 创建默认上下文
        context = context or ExecutionContext()
        session_id = context.session_id
        start_time = time.time()
        
        results = []
        successful_tasks = 0
        failed_tasks = 0
        
        logger.info(f"Starting async execution with {len(tasks)} tasks (session: {session_id})")
        
        # 创建异步任务 - 主线程执行+协程调度
        async def execute_task_async(task: CallTask) -> CallResult:
            # 让出控制权，允许其他协程执行
            await asyncio.sleep(0.001)
            
            # 获取超时时间
            timeout_seconds = self._get_timeout_for_task(task, context)
            
            # 根据配置选择执行方式
            if timeout_seconds > 0 and self.config.enable_async_timeout and self.async_timeout_manager:
                # 使用协程超时管理器
                coro = self._execute_single_with_context_async(task, context)
                result = await self.async_timeout_manager.execute_with_timeout(
                    coro, 
                    timeout_seconds
                )
                # 记录执行时间
                if result.execution_time > 0:
                    await self.async_timeout_manager.record_execution_time(task.interface_name, result.execution_time)
            else:
                # 在主线程中同步执行，避免信号冲突
                result = self._execute_single_with_context(task, context)
            
            if callback:
                callback(result)
            return result
        
        # 分批执行，避免创建过多协程
        batch_size = 50
        all_results = []
        
        for i in range(0, len(tasks), batch_size):
            batch_tasks = tasks[i:i + batch_size]
            batch_results = await asyncio.gather(
                *[execute_task_async(task) for task in batch_tasks],
                return_exceptions=True
            )
            all_results.extend(batch_results)
        
        completed_results = all_results
        
        # 处理结果
        for i, result in enumerate(completed_results):
            if isinstance(result, Exception):
                task = tasks[i]
                result = CallResult(
                    task_id=task.task_id,
                    interface_name=task.interface_name,
                    success=False,
                    error=result
                )
                failed_tasks += 1
            else:
                if result.success:
                    successful_tasks += 1
                else:
                    failed_tasks += 1
            
            results.append(result)
        
        end_time = time.time()
        
        execution_summary = {
            "total_execution_time": end_time - start_time,
            "average_execution_time": sum(r.execution_time for r in results if r.execution_time > 0) / len(results) if results else 0,
            "cache_hits": sum(1 for r in results if r.metadata.get("from_cache", False)),
            "interfaces_used": list(set(r.interface_name for r in results))
        }
        
        batch_result = BatchResult(
            session_id=session_id,
            total_tasks=len(tasks),
            successful_tasks=successful_tasks,
            failed_tasks=failed_tasks,
            results=results,
            execution_summary=execution_summary,
            start_time=start_time,
            end_time=end_time
        )
        
        logger.info(f"Async execution completed: {successful_tasks}/{len(tasks)} successful (session: {session_id})")
        
        return batch_result


class TaskQueue:
    """任务队列"""
    
    def __init__(self, use_priority: bool = True):
        self.use_priority = use_priority
        if use_priority:
            self.queue = PriorityQueue()
        else:
            self.queue = Queue()
        self.tasks = {}  # task_id -> task
    
    def add_task(self, task: CallTask) -> str:
        """添加任务"""
        self.tasks[task.task_id] = task
        if self.use_priority:
            self.queue.put(task)
        else:
            self.queue.put(task)
        return task.task_id
    
    def get_task(self) -> Optional[CallTask]:
        """获取任务"""
        if self.queue.empty():
            return None
        return self.queue.get()
    
    def size(self) -> int:
        """队列大小"""
        return self.queue.qsize()
    
    def is_empty(self) -> bool:
        """是否为空"""
        return self.queue.empty()


class BatchCallManager:
    """批量调用管理器 - 管理多接口批量执行"""
    
    def __init__(self, executor: InterfaceExecutor):
        self.executor = executor
        self.task_queue = TaskQueue()
        self.results = []  # 简单的结果列表，替代ResultCollector
    
    def add_task(self, task: CallTask) -> str:
        """添加任务到队列"""
        return self.task_queue.add_task(task)
    
    def add_tasks(self, tasks: List[CallTask]) -> List[str]:
        """批量添加任务"""
        task_ids = []
        for task in tasks:
            task_id = self.add_task(task)
            task_ids.append(task_id)
        return task_ids
    
    def create_task(self, 
                   interface_name: str, 
                   params: Dict[str, Any],
                   **kwargs) -> CallTask:
        """创建任务的便捷方法"""
        return CallTask(
            interface_name=interface_name,
            params=params,
            **kwargs
        )
    
    def execute_all(self, context: Optional[ExecutionContext] = None) -> BatchResult:
        """执行所有任务"""
        tasks = []
        while not self.task_queue.is_empty():
            task = self.task_queue.get_task()
            if task:
                tasks.append(task)
        
        if not tasks:
            logger.warning("No tasks to execute")
            return BatchResult(
                session_id=str(uuid.uuid4()),
                total_tasks=0,
                successful_tasks=0,
                failed_tasks=0,
                results=[],
                execution_summary={},
                start_time=time.time(),
                end_time=time.time()
            )
        
        return self.executor.execute_batch(tasks, context)
    
    def execute_by_filter(self, 
                         filter_func: Callable[[CallTask], bool],
                         context: Optional[ExecutionContext] = None) -> BatchResult:
        """按条件执行任务"""
        # 获取所有任务
        all_tasks = []
        while not self.task_queue.is_empty():
            task = self.task_queue.get_task()
            if task:
                all_tasks.append(task)
        
        # 筛选任务
        filtered_tasks = [task for task in all_tasks if filter_func(task)]
        
        # 将未筛选的任务放回队列
        unfiltered_tasks = [task for task in all_tasks if not filter_func(task)]
        for task in unfiltered_tasks:
            self.task_queue.add_task(task)
        
        if not filtered_tasks:
            logger.warning("No tasks match the filter criteria")
            return BatchResult(
                session_id=str(uuid.uuid4()),
                total_tasks=0,
                successful_tasks=0,
                failed_tasks=0,
                results=[],
                execution_summary={},
                start_time=time.time(),
                end_time=time.time()
            )
        
        return self.executor.execute_batch(filtered_tasks, context)
    
    def get_queue_size(self) -> int:
        """获取队列大小"""
        return self.task_queue.size()
    
    def clear_queue(self) -> None:
        """清空队列"""
        while not self.task_queue.is_empty():
            self.task_queue.get_task()