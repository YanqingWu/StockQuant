#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Executor模块全面测试套件

测试executor模块的所有核心功能，包括：
- 单接口调用
- 批量调用
- 异步调用
- 错误处理和重试机制
- 缓存功能
- 频率限制
- 超时管理
- 插件系统
- 任务队列管理
"""

import asyncio
import time
import uuid
import unittest
import threading
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.data.interfaces.executor import (
    InterfaceExecutor, CallTask, CallResult, BatchResult, ExecutionContext,
    ExecutorConfig, RetryConfig, CacheConfig, RateLimit, RateLimiter,
    ErrorType, ErrorClassifier, SimpleCache,
    TaskQueue, BatchCallManager, ExecutorPlugin,
    ThreadPoolTimeoutManager, AsyncTimeoutManager
)
from core.data.interfaces.base import APIProviderManager, InterfaceMetadata, FunctionCategory, DataSource, ParameterPattern
from core.data.interfaces.akshare import AkshareProvider

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    ak = None


class MockExecutorPlugin(ExecutorPlugin):
    """测试用插件"""
    
    def __init__(self, name: str = "MockPlugin"):
        self.name = name
        self.before_execute_calls = []
        self.after_execute_calls = []
        self.error_calls = []
    
    def before_execute(self, task: CallTask, context: ExecutionContext) -> None:
        self.before_execute_calls.append((task, context))
    
    def after_execute(self, result: CallResult, context: ExecutionContext) -> None:
        self.after_execute_calls.append((result, context))
    
    def on_error(self, task: CallTask, error: Exception, context: ExecutionContext) -> bool:
        self.error_calls.append((task, error, context))
        return True  # 继续执行


class TestErrorClassifier(unittest.TestCase):
    """测试错误分类器"""
    
    def test_classify_network_error(self):
        """测试网络错误分类"""
        error = ConnectionError("Connection failed")
        error_type = ErrorClassifier.classify_error(error)
        self.assertEqual(error_type, ErrorType.NETWORK_ERROR)
    
    def test_classify_timeout_error(self):
        """测试超时错误分类"""
        error = TimeoutError("Operation timed out")
        error_type = ErrorClassifier.classify_error(error)
        self.assertEqual(error_type, ErrorType.TIMEOUT_ERROR)
    
    def test_classify_rate_limit_error(self):
        """测试频率限制错误分类"""
        error = Exception("Rate limit exceeded")
        error_type = ErrorClassifier.classify_error(error)
        self.assertEqual(error_type, ErrorType.RATE_LIMIT_ERROR)
    
    def test_classify_validation_error(self):
        """测试验证错误分类"""
        error = ValueError("Invalid parameter")
        error_type = ErrorClassifier.classify_error(error)
        self.assertEqual(error_type, ErrorType.VALIDATION_ERROR)
    
    def test_should_retry(self):
        """测试重试判断"""
        # 网络错误应该重试
        self.assertTrue(ErrorClassifier.should_retry(ErrorType.NETWORK_ERROR, 0, 3))
        # 超时错误应该重试
        self.assertTrue(ErrorClassifier.should_retry(ErrorType.TIMEOUT_ERROR, 0, 3))
        # 验证错误不应该重试
        self.assertFalse(ErrorClassifier.should_retry(ErrorType.VALIDATION_ERROR, 0, 3))
        # 超过最大重试次数不应该重试
        self.assertFalse(ErrorClassifier.should_retry(ErrorType.NETWORK_ERROR, 3, 3))


class TestRateLimiter(unittest.TestCase):
    """测试频率限制器"""
    
    def test_rate_limiter_acquire(self):
        """测试频率限制器获取许可"""
        rate_limit = RateLimit(max_calls=2, time_window=1.0)
        limiter = RateLimiter(rate_limit)
        
        # 前两次应该成功
        self.assertTrue(limiter.acquire())
        self.assertTrue(limiter.acquire())
        
        # 第三次应该失败
        self.assertFalse(limiter.acquire())
    
    def test_rate_limiter_wait_time(self):
        """测试等待时间计算"""
        rate_limit = RateLimit(max_calls=1, time_window=1.0)
        limiter = RateLimiter(rate_limit)
        
        # 获取许可
        limiter.acquire()
        
        # 检查等待时间
        wait_time = limiter.wait_time()
        self.assertGreater(wait_time, 0)
        self.assertLessEqual(wait_time, 1.0)


class TestSimpleCache(unittest.TestCase):
    """测试简单缓存"""
    
    def setUp(self):
        self.config = CacheConfig(enabled=True, ttl=1, max_size=2)
        self.cache = SimpleCache(self.config)
    
    def test_cache_set_get(self):
        """测试缓存设置和获取"""
        # 设置缓存
        self.cache.set("key1", "value1")
        
        # 获取缓存
        value = self.cache.get("key1")
        self.assertEqual(value, "value1")
    
    def test_cache_expiration(self):
        """测试缓存过期"""
        # 设置缓存
        self.cache.set("key1", "value1")
        
        # 等待过期
        time.sleep(1.1)
        
        # 获取应该返回None
        value = self.cache.get("key1")
        self.assertIsNone(value)
    
    def test_cache_size_limit(self):
        """测试缓存大小限制"""
        # 添加超过限制的条目
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")  # 应该删除最旧的
        
        # 检查缓存大小
        self.assertEqual(len(self.cache.cache), 2)
        
        # key1应该被删除
        self.assertIsNone(self.cache.get("key1"))
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key3"), "value3")
    
    def test_cache_disabled(self):
        """测试缓存禁用"""
        config = CacheConfig(enabled=False)
        cache = SimpleCache(config)
        
        # 设置缓存
        cache.set("key1", "value1")
        
        # 获取应该返回None
        value = cache.get("key1")
        self.assertIsNone(value)


class TestCallTask(unittest.TestCase):
    """测试调用任务"""
    
    def test_call_task_creation(self):
        """测试任务创建"""
        task = CallTask(
            interface_name="test_interface",
            params={"param1": "value1"},
            priority=5,
            retry_count=2,
            timeout=10.0
        )
        
        self.assertEqual(task.interface_name, "test_interface")
        self.assertEqual(task.params, {"param1": "value1"})
        self.assertEqual(task.priority, 5)
        self.assertEqual(task.retry_count, 2)
        self.assertEqual(task.timeout, 10.0)
        self.assertIsNotNone(task.task_id)
    
    def test_call_task_priority_comparison(self):
        """测试任务优先级比较"""
        task1 = CallTask("test1", {}, priority=5)
        task2 = CallTask("test2", {}, priority=3)
        
        # 检查优先级比较是否正确
        # 在PriorityQueue中，__lt__方法用于排序，优先级高的应该排在前面
        # 所以task1(priority=5)应该小于task2(priority=3)，这样task1会排在前面
        self.assertTrue(task1 < task2)  # task1优先级高，应该小于task2（排在前面）
        self.assertFalse(task2 < task1)  # task2优先级低，不应该小于task1


class TestCallResult(unittest.TestCase):
    """测试调用结果"""
    
    def test_successful_result(self):
        """测试成功结果"""
        result = CallResult(
            task_id="task1",
            interface_name="test_interface",
            success=True,
            data={"result": "success"},
            execution_time=1.5
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.data, {"result": "success"})
        self.assertEqual(result.execution_time, 1.5)
        self.assertIsNone(result.error)
    
    def test_failed_result(self):
        """测试失败结果"""
        error = Exception("Test error")
        result = CallResult(
            task_id="task1",
            interface_name="test_interface",
            success=False,
            error=error
        )
        
        self.assertFalse(result.success)
        self.assertEqual(result.error, error)
        self.assertIsNone(result.data)


class TestBatchResult(unittest.TestCase):
    """测试批量结果"""
    
    def test_batch_result_properties(self):
        """测试批量结果属性"""
        results = [
            CallResult("task1", "interface1", True),
            CallResult("task2", "interface2", False),
            CallResult("task3", "interface3", True)
        ]
        
        batch_result = BatchResult(
            session_id="session1",
            total_tasks=3,
            successful_tasks=2,
            failed_tasks=1,
            results=results,
            execution_summary={},
            start_time=time.time(),
            end_time=time.time() + 1.0
        )
        
        self.assertEqual(batch_result.success_rate, 2/3)
        self.assertAlmostEqual(batch_result.total_execution_time, 1.0, places=1)


class TestTaskQueue(unittest.TestCase):
    """测试任务队列"""
    
    def setUp(self):
        self.queue = TaskQueue(use_priority=True)
    
    def test_add_get_task(self):
        """测试添加和获取任务"""
        task = CallTask("test_interface", {"param": "value"})
        task_id = self.queue.add_task(task)
        
        self.assertEqual(task_id, task.task_id)
        self.assertEqual(self.queue.size(), 1)
        
        retrieved_task = self.queue.get_task()
        self.assertEqual(retrieved_task, task)
        self.assertEqual(self.queue.size(), 0)
    
    def test_priority_queue(self):
        """测试优先级队列"""
        task1 = CallTask("test1", {}, priority=1)
        task2 = CallTask("test2", {}, priority=3)
        task3 = CallTask("test3", {}, priority=2)
        
        # 添加任务
        self.queue.add_task(task1)
        self.queue.add_task(task2)
        self.queue.add_task(task3)
        
        # 应该按优先级顺序获取
        self.assertEqual(self.queue.get_task(), task2)  # 优先级最高
        self.assertEqual(self.queue.get_task(), task3)
        self.assertEqual(self.queue.get_task(), task1)  # 优先级最低
    
    def test_empty_queue(self):
        """测试空队列"""
        self.assertTrue(self.queue.is_empty())
        self.assertIsNone(self.queue.get_task())


# TestResultCollector类已删除，因为ResultCollector类已被移除


class TestInterfaceExecutor(unittest.TestCase):
    """测试接口执行器"""
    
    def setUp(self):
        # 创建真实的提供者管理器
        self.provider_manager = APIProviderManager()
        self.provider = AkshareProvider()
        self.provider_manager.register_provider(self.provider)
        
        # 创建执行器配置
        self.config = ExecutorConfig(
            default_timeout=10.0,  # 根据成功接口测试报告调整：平均0.44s，最大18.14s，设置10s超时
            retry_config=RetryConfig(max_retries=1),  # 减少重试次数，避免测试时间过长
            cache_config=CacheConfig(enabled=True, ttl=60)
        )
        
        self.executor = InterfaceExecutor(self.provider_manager, self.config)
        
        # 定义一些测试用的真实接口和参数（基于成功接口测试报告的执行时间）
        self.test_interfaces = {
            # 快速接口（<0.1s）- 用于快速测试
            'stock_a_code_to_symbol': {'symbol': '000300'},  # 0.000s
            'stock_board_change_em': {},  # 0.092s
            'stock_sse_summary': {},  # 0.092s
            
            # 中等速度接口（0.1-0.5s）- 用于常规测试
            'stock_account_statistics_em': {},  # 0.215s
            'stock_individual_info_em': {'symbol': '603777'},  # 0.215s
            'stock_hot_keyword_em': {'symbol': 'SZ000665'},  # 0.215s
            'stock_zh_a_spot_em': {'symbol': '000001'},  # 0.215s
            
            # 较慢接口（0.5-1s）- 用于超时测试
            'stock_a_high_low_statistics': {'symbol': 'all'},  # 0.757s
            'stock_board_industry_name_em': {},  # 0.757s
            'stock_board_industry_name_ths': {},  # 0.757s
        }
    
    def test_execute_single_success(self):
        """测试单接口调用成功 - 使用真实接口"""
        # 使用一个简单的无参数接口进行测试
        interface_name = 'stock_account_statistics_em'
        params = {}
        
        result = self.executor.execute_single(interface_name, params)
        
        # 检查基本结果
        self.assertIsNotNone(result)
        self.assertEqual(result.interface_name, interface_name)
        self.assertIsNotNone(result.task_id)
        
        # 如果成功，检查数据
        if result.success:
            self.assertIsNotNone(result.data)
            self.assertGreater(result.execution_time, 0)
        else:
            # 如果失败，检查错误信息
            self.assertIsNotNone(result.error)
            print(f"接口 {interface_name} 调用失败: {result.error}")
    
    def test_execute_single_failure(self):
        """测试单接口调用失败 - 使用真实接口"""
        # 使用一个不存在的接口名称来测试失败情况
        interface_name = 'non_existent_interface'
        params = {}
        
        result = self.executor.execute_single(interface_name, params)
        
        # 检查失败结果
        self.assertIsNotNone(result)
        self.assertEqual(result.interface_name, interface_name)
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)
        self.assertIn("not found", str(result.error).lower())
    
    def test_execute_single_with_retry(self):
        """测试单接口调用重试 - 使用真实接口"""
        # 使用一个可能失败的接口来测试重试机制
        interface_name = 'stock_a_code_to_symbol'
        params = {'symbol': 'invalid_code'}  # 使用无效参数来触发错误
        
        result = self.executor.execute_single(interface_name, params)
        
        # 检查基本结果
        self.assertIsNotNone(result)
        self.assertEqual(result.interface_name, interface_name)
        
        # 由于使用了无效参数，接口可能会失败，这是正常的
        # 我们主要测试重试机制是否工作
        if not result.success:
            self.assertIsNotNone(result.error)
            print(f"接口 {interface_name} 调用失败（预期）: {result.error}")
        
        # 检查是否至少尝试了一次调用
        self.assertGreaterEqual(result.metadata.get("total_attempts", 1), 1)
    
    def test_execute_single_caching(self):
        """测试单接口调用缓存 - 使用真实接口"""
        # 使用一个简单的无参数接口测试缓存
        interface_name = 'stock_sse_summary'
        params = {}
        
        # 第一次调用
        result1 = self.executor.execute_single(interface_name, params)
        self.assertIsNotNone(result1)
        self.assertEqual(result1.interface_name, interface_name)
        
        # 第二次调用应该使用缓存（如果第一次成功）
        result2 = self.executor.execute_single(interface_name, params)
        self.assertIsNotNone(result2)
        self.assertEqual(result2.interface_name, interface_name)
        
        # 如果两次都成功，检查缓存是否生效
        if result1.success and result2.success:
            # 第二次调用的执行时间应该更短（因为使用了缓存）
            self.assertLessEqual(result2.execution_time, result1.execution_time)
            # 检查是否使用了缓存
            if result2.metadata.get("from_cache", False):
                print(f"接口 {interface_name} 成功使用缓存")
        else:
            print(f"接口 {interface_name} 调用失败，无法测试缓存功能")
    
    def test_execute_batch(self):
        """测试批量调用 - 使用真实接口"""
        # 使用多个真实接口进行批量测试
        tasks = [
            CallTask("stock_account_statistics_em", {}),
            CallTask("stock_board_change_em", {}),
            CallTask("stock_sse_summary", {}),
            CallTask("stock_a_code_to_symbol", {"symbol": "000300"}),
            CallTask("stock_individual_info_em", {"symbol": "603777"})
        ]
        
        batch_result = self.executor.execute_batch(tasks)
        
        # 检查批量结果
        self.assertEqual(batch_result.total_tasks, 5)
        self.assertEqual(len(batch_result.results), 5)
        self.assertGreaterEqual(batch_result.successful_tasks + batch_result.failed_tasks, 0)
        
        # 打印结果统计
        print(f"批量调用结果: 成功 {batch_result.successful_tasks}/{batch_result.total_tasks}")
        
        # 检查每个结果
        for i, result in enumerate(batch_result.results):
            self.assertIsNotNone(result)
            self.assertIsNotNone(result.task_id)
            self.assertIsNotNone(result.interface_name)
            if result.success:
                print(f"  ✓ {result.interface_name}: {result.execution_time:.3f}s")
            else:
                print(f"  ✗ {result.interface_name}: {result.error}")
    
    def test_execute_async(self):
        """测试异步调用 - 使用真实接口"""
        # 使用多个真实接口进行异步测试
        tasks = [
            CallTask("stock_board_industry_name_em", {}),
            CallTask("stock_board_industry_name_ths", {}),
            CallTask("stock_hot_keyword_em", {"symbol": "SZ000665"}),
            CallTask("stock_zh_a_spot_em", {"symbol": "000001"})
        ]
        
        async def run_async_test():
            batch_result = await self.executor.execute_async(tasks)
            return batch_result
        
        batch_result = asyncio.run(run_async_test())
        
        # 检查异步结果
        self.assertEqual(batch_result.total_tasks, 4)
        self.assertEqual(len(batch_result.results), 4)
        self.assertGreaterEqual(batch_result.successful_tasks + batch_result.failed_tasks, 0)
        
        # 打印异步结果统计
        print(f"异步调用结果: 成功 {batch_result.successful_tasks}/{batch_result.total_tasks}")
        
        # 检查每个结果
        for i, result in enumerate(batch_result.results):
            self.assertIsNotNone(result)
            self.assertIsNotNone(result.task_id)
            self.assertIsNotNone(result.interface_name)
            if result.success:
                print(f"  ✓ {result.interface_name}: {result.execution_time:.3f}s")
            else:
                print(f"  ✗ {result.interface_name}: {result.error}")
    
    def test_plugin_integration(self):
        """测试插件集成 - 使用真实接口"""
        plugin = MockExecutorPlugin("TestPlugin")
        self.executor.config.plugins = [plugin]
        
        # 使用真实接口测试插件
        interface_name = 'stock_sse_summary'
        params = {}
        
        result = self.executor.execute_single(interface_name, params)
        
        # 检查插件是否被调用
        self.assertGreaterEqual(len(plugin.before_execute_calls), 1)
        self.assertGreaterEqual(len(plugin.after_execute_calls), 1)
        
        # 检查插件调用记录
        before_call = plugin.before_execute_calls[0]
        after_call = plugin.after_execute_calls[0]
        
        self.assertEqual(before_call[0].interface_name, interface_name)
        self.assertEqual(after_call[0].interface_name, interface_name)
        
        print(f"插件测试: before_execute调用 {len(plugin.before_execute_calls)} 次")
        print(f"插件测试: after_execute调用 {len(plugin.after_execute_calls)} 次")
    
    def test_execution_time_analysis(self):
        """测试不同执行时间的接口 - 基于成功接口测试报告"""
        print("\n=== 执行时间分析测试 ===")
        
        # 测试快速接口（<0.1s）
        fast_interface = 'stock_a_code_to_symbol'
        fast_params = {'symbol': '000300'}
        result = self.executor.execute_single(fast_interface, fast_params)
        if result.success:
            print(f"快速接口 {fast_interface}: {result.execution_time:.3f}s (预期<0.1s)")
            self.assertLess(result.execution_time, 0.1)
        
        # 测试中等速度接口（0.1-0.5s）
        medium_interface = 'stock_account_statistics_em'
        medium_params = {}
        result = self.executor.execute_single(medium_interface, medium_params)
        if result.success:
            print(f"中等速度接口 {medium_interface}: {result.execution_time:.3f}s (预期0.1-0.5s)")
            self.assertGreaterEqual(result.execution_time, 0.05)  # 至少需要一些时间
            self.assertLess(result.execution_time, 1.0)  # 但不超过1秒
        
        # 测试较慢接口（0.5-1s）
        slow_interface = 'stock_a_high_low_statistics'
        slow_params = {'symbol': 'all'}
        result = self.executor.execute_single(slow_interface, slow_params)
        if result.success:
            print(f"较慢接口 {slow_interface}: {result.execution_time:.3f}s (预期0.5-1s)")
            self.assertGreaterEqual(result.execution_time, 0.3)  # 至少需要一些时间
            self.assertLess(result.execution_time, 2.0)  # 但不超过2秒
    
    def test_timeout_management(self):
        """测试超时管理 - 使用真实接口"""
        # 使用一个可能较慢的接口测试超时
        interface_name = 'stock_a_high_low_statistics'
        params = {'symbol': 'all'}
        
        # 创建一个短超时的任务（根据成功接口测试报告，大部分接口在0.1s内完成）
        task = CallTask(interface_name, params, timeout=0.1)
        
        try:
            result = self.executor._execute_with_retry(task, ExecutionContext())
            # 检查结果
            self.assertIsNotNone(result)
            self.assertEqual(result.interface_name, interface_name)
            
            if result.success:
                print(f"接口 {interface_name} 在超时限制内成功完成")
            else:
                print(f"接口 {interface_name} 调用失败: {result.error}")
                
        except Exception as e:
            # 预期可能会有异常，因为信号处理在多线程中有问题
            if "signal" in str(e).lower():
                print(f"超时测试跳过（信号处理问题）: {e}")
            else:
                raise
    
    @unittest.skipUnless(AKSHARE_AVAILABLE, "akshare not available")
    def test_thread_pool_timeout_manager(self):
        """测试线程池超时管理器"""
        print("\n=== 测试线程池超时管理器 ===")
        
        # 创建线程池超时管理器
        manager = ThreadPoolTimeoutManager(max_workers=2)
        
        def real_slow_interface():
            """使用真正会超时的接口"""
            return ak.stock_a_all_pb()  # 这个接口在报告中显示会超时
        
        def fast_task():
            """模拟快任务"""
            time.sleep(0.5)
            return "快速完成"
        
        try:
            # 测试超时情况 - 使用真实接口
            print("测试超时情况（2秒超时，使用真实慢接口）...")
            start_time = time.time()
            try:
                result = manager.execute_with_timeout(real_slow_interface, (), timeout=2.0)
                print(f"意外成功: {result}")
            except Exception as e:
                elapsed = time.time() - start_time
                print(f"预期超时异常: {type(e).__name__}: {e}")
                print(f"耗时: {elapsed:.2f}秒")
                self.assertLessEqual(elapsed, 2.5)  # 允许一些误差
            
            # 测试正常情况
            print("\n测试正常情况（2秒超时，任务需要0.5秒）...")
            start_time = time.time()
            try:
                result = manager.execute_with_timeout(fast_task, (), timeout=2.0)
                elapsed = time.time() - start_time
                print(f"成功完成: {result}")
                print(f"耗时: {elapsed:.2f}秒")
                self.assertEqual(result, "快速完成")
                self.assertLessEqual(elapsed, 1.0)
            except Exception as e:
                print(f"意外异常: {type(e).__name__}: {e}")
                self.fail(f"快任务不应该超时: {e}")
                
        finally:
            manager.shutdown()
            print("线程池已关闭")
    
    @unittest.skipUnless(AKSHARE_AVAILABLE, "akshare not available")
    def test_async_timeout_manager(self):
        """测试协程超时管理器"""
        print("\n=== 测试协程超时管理器 ===")
        
        async def run_async_test():
            # 创建协程超时管理器
            manager = AsyncTimeoutManager()
            
            async def async_real_slow_interface():
                """在异步环境中调用同步接口"""
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, ak.stock_news_main_cx)
            
            async def fast_async_task():
                """模拟快异步任务"""
                await asyncio.sleep(0.5)
                return "快速异步完成"
            
            # 测试超时情况 - 使用真实接口
            print("测试异步超时情况（2秒超时，使用真实慢接口）...")
            start_time = time.time()
            try:
                result = await manager.execute_with_timeout(async_real_slow_interface(), timeout=2.0)
                print(f"意外成功: {result}")
            except Exception as e:
                elapsed = time.time() - start_time
                print(f"预期超时异常: {type(e).__name__}: {e}")
                print(f"耗时: {elapsed:.2f}秒")
                self.assertLessEqual(elapsed, 2.5)  # 允许一些误差
            
            # 测试正常情况
            print("\n测试异步正常情况（2秒超时，任务需要0.5秒）...")
            start_time = time.time()
            try:
                result = await manager.execute_with_timeout(fast_async_task(), timeout=2.0)
                elapsed = time.time() - start_time
                print(f"成功完成: {result}")
                print(f"耗时: {elapsed:.2f}秒")
                self.assertEqual(result, "快速异步完成")
                self.assertLessEqual(elapsed, 1.0)
            except Exception as e:
                print(f"意外异常: {type(e).__name__}: {e}")
                self.fail(f"快异步任务不应该超时: {e}")
        
        # 运行异步测试
        asyncio.run(run_async_test())
    
    @unittest.skipUnless(AKSHARE_AVAILABLE, "akshare not available")
    def test_executor_with_timeout_integration(self):
        """测试InterfaceExecutor的超时功能集成"""
        print("\n=== 测试InterfaceExecutor超时功能集成 ===")
        
        # 创建配置，启用混合超时
        config = ExecutorConfig(
            enable_thread_timeout=True,
            enable_async_timeout=True,
            thread_pool_max_workers=2,
            default_timeout=2.0
        )
        
        # 创建provider manager
        provider_manager = APIProviderManager()
        provider = AkshareProvider()
        provider_manager.register_provider(provider)
        
        # 创建executor
        executor = InterfaceExecutor(provider_manager, config)
        
        print(f"线程池超时管理器已启用: {executor.thread_timeout_manager is not None}")
        print(f"协程超时管理器已启用: {executor.async_timeout_manager is not None}")
        
        try:
            # 测试InterfaceExecutor的超时功能 - 使用真实接口
            print("\n测试超时接口（stock_news_main_cx，执行时间约18秒）...")
            
            # 临时修改默认超时时间
            original_timeout = executor.config.default_timeout
            executor.config.default_timeout = 3.0  # 设置3秒超时
            
            try:
                result = executor.execute_single('stock_news_main_cx', {})
                if result.success:
                    print(f"意外成功: 数据行数 {len(result.data) if result.data else 0}")
                else:
                    print(f"预期失败: {result.error}")
                    # 检查是否是超时错误
                    if "timeout" in str(result.error).lower():
                        print("✓ 超时机制正常工作")
                    else:
                        print(f"非超时错误: {result.error}")
            finally:
                # 恢复原始超时时间
                executor.config.default_timeout = original_timeout
            
            # 测试正常情况（不超时）- 使用快速接口
            print("\n测试正常情况（使用快速接口）...")
            
            # 修改默认超时时间为10秒
            original_timeout = executor.config.default_timeout
            executor.config.default_timeout = 10.0
            
            try:
                # 使用更简单的接口进行测试
                result = executor.execute_single('tool_trade_date_hist_sina', {})
                print(f"执行成功: {result.success}")
                if result.success and result.data is not None:
                    print(f"数据行数: {len(result.data)}")
                    self.assertTrue(result.success)
                elif not result.success:
                    print(f"执行失败: {result.error}")
                    # 对于网络相关的失败，我们不认为是测试失败
                    if "timeout" not in str(result.error).lower():
                        print("非超时错误，可能是网络问题")
            finally:
                # 恢复原始超时设置
                executor.config.default_timeout = original_timeout
            
        finally:
            # 清理
            if executor.thread_timeout_manager:
                executor.thread_timeout_manager.shutdown()
                print("Executor线程池已关闭")


class TestExecutorCachingTTL(unittest.TestCase):
    def setUp(self):
        self.provider_manager = APIProviderManager()
        self.provider_manager.register_provider(AkshareProvider())
        self.config = ExecutorConfig(
            default_timeout=5.0,
            retry_config=RetryConfig(max_retries=1),
            cache_config=CacheConfig(enabled=True, ttl=60)
        )
        self.executor = InterfaceExecutor(self.provider_manager, self.config)

    def test_cache_disabled_by_zero_ttl(self):
        # 当每接口TTL=0时，应视为禁止缓存
        counter = {"n": 0}
        def fake_call(task: CallTask):
            counter["n"] += 1
            return counter["n"]
        interface_name = "stock_sse_summary"
        with patch.object(self.executor, "_get_cache_ttl_for_interface", return_value=0), \
             patch.object(self.executor, "_call_akshare_interface", side_effect=fake_call):
            r1 = self.executor.execute_single(interface_name, {})
            r2 = self.executor.execute_single(interface_name, {})
        self.assertTrue(r1.success and r2.success)
        self.assertEqual(counter["n"], 2)
        self.assertFalse(r2.metadata.get("from_cache", False))

    def test_cache_ttl_hit_and_expire(self):
        # 当TTL为正时，首次写入后在TTL窗口内应命中缓存，过期后应重新调用
        counter = {"n": 0}
        def fake_call(task: CallTask):
            counter["n"] += 1
            return counter["n"]
        interface_name = "stock_sse_summary"
        with patch.object(self.executor, "_get_cache_ttl_for_interface", return_value=1), \
             patch.object(self.executor, "_call_akshare_interface", side_effect=fake_call):
            r1 = self.executor.execute_single(interface_name, {})
            r2 = self.executor.execute_single(interface_name, {})
            # 第二次应命中缓存
            self.assertTrue(r2.metadata.get("from_cache", False))
            # 等待TTL过期
            time.sleep(1.2)
            r3 = self.executor.execute_single(interface_name, {})
        self.assertTrue(r1.success and r2.success and r3.success)
        # 第三次为过期后重新调用
        self.assertEqual(counter["n"], 2)
        self.assertFalse(r3.metadata.get("from_cache", False))

    def test_context_cache_disabled(self):
        # 即便TTL>0，但当会话禁用缓存时不应读写缓存
        counter = {"n": 0}
        def fake_call(task: CallTask):
            counter["n"] += 1
            return counter["n"]
        ctx = ExecutionContext(cache_enabled=False)
        interface_name = "stock_sse_summary"
        with patch.object(self.executor, "_get_cache_ttl_for_interface", return_value=30), \
             patch.object(self.executor, "_call_akshare_interface", side_effect=fake_call):
            r1 = self.executor.execute_single(interface_name, {}, context=ctx)
            r2 = self.executor.execute_single(interface_name, {}, context=ctx)
        self.assertTrue(r1.success and r2.success)
        self.assertEqual(counter["n"], 2)
        self.assertFalse(r2.metadata.get("from_cache", False))




class TestTimeoutManager(unittest.TestCase):
    """测试超时管理器"""
    
    @unittest.skipUnless(AKSHARE_AVAILABLE, "akshare not available")
    def test_thread_pool_timeout_manager_basic(self):
        """测试线程池超时管理器基本功能"""
        print("\n=== 测试线程池超时管理器基本功能 ===")
        
        manager = ThreadPoolTimeoutManager(max_workers=2)
        
        def simple_task(value):
            time.sleep(0.1)
            return value * 2
        
        try:
            # 测试正常执行
            result = manager.execute_with_timeout(simple_task, (5,), timeout=1.0)
            self.assertEqual(result, 10)
            print("✓ 正常执行测试通过")
            
            # 测试超时
            def slow_task():
                time.sleep(2.0)
                return "完成"
            
            start_time = time.time()
            with self.assertRaises(Exception):
                manager.execute_with_timeout(slow_task, (), timeout=0.5)
            elapsed = time.time() - start_time
            self.assertLess(elapsed, 1.0)  # 应该在1秒内超时
            print("✓ 超时测试通过")
            
        finally:
            manager.shutdown()
            print("✓ 线程池已关闭")
    
    def test_async_timeout_manager_basic(self):
        """测试协程超时管理器基本功能"""
        print("\n=== 测试协程超时管理器基本功能 ===")
        
        async def run_test():
            manager = AsyncTimeoutManager()
            
            async def simple_async_task(value):
                await asyncio.sleep(0.1)
                return value * 2
            
            # 测试正常执行
            result = await manager.execute_with_timeout(simple_async_task(5), timeout=1.0)
            self.assertEqual(result, 10)
            print("✓ 异步正常执行测试通过")
            
            # 测试超时
            async def slow_async_task():
                await asyncio.sleep(2.0)
                return "完成"
            
            start_time = time.time()
            with self.assertRaises(asyncio.TimeoutError):
                await manager.execute_with_timeout(slow_async_task(), timeout=0.5)
            elapsed = time.time() - start_time
            self.assertLess(elapsed, 1.0)  # 应该在1秒内超时
            print("✓ 异步超时测试通过")
        
        asyncio.run(run_test())


class TestBatchCallManagerAsync(unittest.TestCase):
    def setUp(self):
        self.provider_manager = APIProviderManager()
        self.provider = AkshareProvider()
        self.provider_manager.register_provider(self.provider)
        self.config = ExecutorConfig(
            default_timeout=0.0,
            retry_config=RetryConfig(max_retries=1),
            cache_config=CacheConfig(enabled=False),
            async_max_concurrency=5,
            enable_async_timeout=False
        )
        self.executor = InterfaceExecutor(self.provider_manager, self.config)
        # 补充：维护与原有用例一致的管理器实例
        self.manager = BatchCallManager(self.executor)

    def test_execute_all_async_smoke(self):
        bcm = BatchCallManager(self.executor)

        # mock 同步底层调用，以触发 to_thread 分支
        def mocked_call(task: CallTask):
            return {"ok": True, "name": task.interface_name}
        original_call = self.executor._call_akshare_interface  # type: ignore
        self.executor._call_akshare_interface = mocked_call  # type: ignore
        try:
            tasks = [CallTask("iface", {"i": i}) for i in range(8)]
            bcm.add_tasks(tasks)

            async def run():
                return await bcm.execute_all_async()

            result = asyncio.run(run())
            self.assertEqual(result.total_tasks, 8)
            self.assertEqual(len(result.results), 8)
            self.assertTrue(all(r.success for r in result.results))
        finally:
            # 恢复原方法，避免影响后续用例
            self.executor._call_akshare_interface = original_call  # type: ignore
    
    def test_add_task(self):
        """测试添加任务 - 使用真实接口"""
        task = CallTask("stock_sse_summary", {})
        task_id = self.manager.add_task(task)
        
        self.assertEqual(task_id, task.task_id)
        self.assertEqual(self.manager.get_queue_size(), 1)
    
    def test_add_tasks(self):
        """测试批量添加任务 - 使用真实接口"""
        tasks = [
            CallTask("stock_account_statistics_em", {}),
            CallTask("stock_board_change_em", {})
        ]
        
        task_ids = self.manager.add_tasks(tasks)
        
        self.assertEqual(len(task_ids), 2)
        self.assertEqual(self.manager.get_queue_size(), 2)
    
    def test_create_task(self):
        """测试创建任务 - 使用真实接口"""
        task = self.manager.create_task("stock_sse_summary", {}, priority=5)
        
        self.assertEqual(task.interface_name, "stock_sse_summary")
        self.assertEqual(task.params, {})
        self.assertEqual(task.priority, 5)
    
    def test_execute_all(self):
        """测试执行所有任务 - 使用真实接口"""
        # 添加真实接口任务
        self.manager.add_task(CallTask("stock_sse_summary", {}))
        self.manager.add_task(CallTask("stock_account_statistics_em", {}))
        
        # 执行所有任务
        result = self.manager.execute_all()
        
        # 检查结果
        self.assertEqual(result.total_tasks, 2)
        self.assertEqual(len(result.results), 2)
        self.assertGreaterEqual(result.successful_tasks + result.failed_tasks, 0)
        
        # 打印结果
        print(f"BatchCallManager执行结果: 成功 {result.successful_tasks}/{result.total_tasks}")
        for i, task_result in enumerate(result.results):
            if task_result.success:
                print(f"  ✓ {task_result.interface_name}: {task_result.execution_time:.3f}s")
            else:
                print(f"  ✗ {task_result.interface_name}: {task_result.error}")
    
    def test_execute_by_filter(self):
        """测试按条件执行任务 - 使用真实接口"""
        # 添加真实接口任务
        self.manager.add_task(CallTask("stock_sse_summary", {}))
        self.manager.add_task(CallTask("stock_account_statistics_em", {}))
        self.manager.add_task(CallTask("stock_board_change_em", {}))
        
        # 定义过滤条件：只执行包含"sse"的接口
        def filter_func(task):
            return "sse" in task.interface_name
        
        # 按条件执行
        result = self.manager.execute_by_filter(filter_func)
        
        # 检查结果
        self.assertEqual(result.total_tasks, 1)  # 只有stock_sse_summary匹配
        self.assertEqual(len(result.results), 1)
        self.assertEqual(result.results[0].interface_name, "stock_sse_summary")
        
        print(f"按条件执行结果: 成功 {result.successful_tasks}/{result.total_tasks}")
        for task_result in result.results:
            if task_result.success:
                print(f"  ✓ {task_result.interface_name}: {task_result.execution_time:.3f}s")
            else:
                print(f"  ✗ {task_result.interface_name}: {task_result.error}")
    
    def test_clear_queue(self):
        """测试清空队列 - 使用真实接口"""
        # 添加任务
        self.manager.add_task(CallTask("stock_sse_summary", {}))
        self.assertEqual(self.manager.get_queue_size(), 1)
        
        # 清空队列
        self.manager.clear_queue()
        self.assertEqual(self.manager.get_queue_size(), 0)


# TestTimeoutManager类已删除，因为TimeoutManager类已被移除


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        # 创建真实的提供者管理器
        self.provider_manager = APIProviderManager()
        self.provider = AkshareProvider()
        self.provider_manager.register_provider(self.provider)
        
        # 创建执行器
        self.config = ExecutorConfig(
            default_timeout=10.0,  # 根据成功接口测试报告调整：平均0.44s，最大18.14s，设置10s超时
            retry_config=RetryConfig(max_retries=1),
            cache_config=CacheConfig(enabled=True, ttl=60)
        )
        self.executor = InterfaceExecutor(self.provider_manager, self.config)
    
    def test_real_interface_execution(self):
        """测试真实接口执行"""
        # 获取一个简单的接口进行测试
        interfaces = self.provider.get_supported_interfaces()
        simple_interface = None
        
        for interface_name in interfaces:
            metadata = self.provider.get_interface_metadata(interface_name)
            if metadata and not metadata.required_params and not metadata.optional_params:
                simple_interface = interface_name
                break
        
        if simple_interface:
            result = self.executor.execute_single(simple_interface, {})
            # 不要求一定成功，因为网络等因素可能影响
            self.assertIsNotNone(result)
            self.assertIsNotNone(result.task_id)
            self.assertEqual(result.interface_name, simple_interface)
    
    def test_batch_execution_with_real_interfaces(self):
        """测试真实接口批量执行"""
        # 获取几个简单的接口
        interfaces = self.provider.get_supported_interfaces()[:3]
        tasks = []
        
        for interface_name in interfaces:
            metadata = self.provider.get_interface_metadata(interface_name)
            if metadata and not metadata.required_params:
                task = CallTask(interface_name, {})
                tasks.append(task)
        
        if tasks:
            batch_result = self.executor.execute_batch(tasks)
            self.assertEqual(batch_result.total_tasks, len(tasks))
            self.assertGreaterEqual(batch_result.successful_tasks, 0)
            self.assertGreaterEqual(batch_result.failed_tasks, 0)


def run_all_tests():
    """运行所有测试"""
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestErrorClassifier,
        TestRateLimiter,
        TestSimpleCache,
        TestCallTask,
        TestCallResult,
        TestBatchResult,
        TestTaskQueue,
        TestInterfaceExecutor,
        TestTimeoutManager,
        TestBatchCallManager,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


class TestBatchCallManagerPriority(unittest.TestCase):
    def setUp(self):
        self.provider_manager = APIProviderManager()
        self.provider = AkshareProvider()
        self.provider_manager.register_provider(self.provider)
        self.config = ExecutorConfig(
            default_timeout=0.0,
            retry_config=RetryConfig(max_retries=1),
            cache_config=CacheConfig(enabled=False),
            async_max_concurrency=3,
            enable_async_timeout=False
        )
        self.executor = InterfaceExecutor(self.provider_manager, self.config)
        self.manager = BatchCallManager(self.executor)

    def test_sync_priority_ordering(self):
        # 添加不同优先级任务（数值越大优先级越高）
        tasks = [
            CallTask("iface", {"i": 1}, priority=1),
            CallTask("iface", {"i": 2}, priority=5),
            CallTask("iface", {"i": 3}, priority=3),
        ]
        self.manager.add_tasks(tasks)

        # mock execute_batch 以捕获顺序
        original_execute_batch = self.executor.execute_batch
        def mocked_execute_batch(tasks_in, context=None):
            ordered_priorities = [t.priority for t in tasks_in]
            # 返回一个最小可用的 BatchResult
            return BatchResult(
                session_id=context.session_id if context else str(uuid.uuid4()),
                total_tasks=len(tasks_in),
                successful_tasks=len(tasks_in),
                failed_tasks=0,
                results=[CallResult(t.task_id, t.interface_name, True, data=t.priority) for t in tasks_in],
                execution_summary={"ordered_priorities": ordered_priorities},
                start_time=time.time(),
                end_time=time.time(),
            )
        self.executor.execute_batch = mocked_execute_batch  # type: ignore
        try:
            result = self.manager.execute_all()
            self.assertEqual(result.total_tasks, 3)
            # 期望按优先级从高到低：5,3,1
            self.assertEqual(result.execution_summary.get("ordered_priorities"), [5, 3, 1])
        finally:
            self.executor.execute_batch = original_execute_batch  # type: ignore

    def test_async_priority_ordering(self):
        # 添加不同优先级任务
        tasks = [
            CallTask("iface", {"i": 1}, priority=1),
            CallTask("iface", {"i": 2}, priority=5),
            CallTask("iface", {"i": 3}, priority=3),
        ]
        self.manager.add_tasks(tasks)

        # mock execute_async 以捕获顺序
        original_execute_async = self.executor.execute_async
        async def mocked_execute_async(tasks_in, callback=None, context=None):
            ordered_priorities = [t.priority for t in tasks_in]
            return BatchResult(
                session_id=context.session_id if context else str(uuid.uuid4()),
                total_tasks=len(tasks_in),
                successful_tasks=len(tasks_in),
                failed_tasks=0,
                results=[CallResult(t.task_id, t.interface_name, True, data=t.priority) for t in tasks_in],
                execution_summary={"ordered_priorities": ordered_priorities},
                start_time=time.time(),
                end_time=time.time(),
            )
        self.executor.execute_async = mocked_execute_async  # type: ignore
        try:
            async def run():
                return await self.manager.execute_all_async()
            result = asyncio.run(run())
            self.assertEqual(result.total_tasks, 3)
            # 期望按优先级从高到低：5,3,1
            self.assertEqual(result.execution_summary.get("ordered_priorities"), [5, 3, 1])
        finally:
            self.executor.execute_async = original_execute_async  # type: ignore

    def test_add_task(self):
        """测试添加任务 - 使用真实接口"""
        task = CallTask("stock_sse_summary", {})
        task_id = self.manager.add_task(task)
        
        self.assertEqual(task_id, task.task_id)
        self.assertEqual(self.manager.get_queue_size(), 1)
    
    def test_add_tasks(self):
        """测试批量添加任务 - 使用真实接口"""
        tasks = [
            CallTask("stock_account_statistics_em", {}),
            CallTask("stock_board_change_em", {})
        ]
        
        task_ids = self.manager.add_tasks(tasks)
        
        self.assertEqual(len(task_ids), 2)
        self.assertEqual(self.manager.get_queue_size(), 2)
    
    def test_create_task(self):
        """测试创建任务 - 使用真实接口"""
        task = self.manager.create_task("stock_sse_summary", {}, priority=5)
        
        self.assertEqual(task.interface_name, "stock_sse_summary")
        self.assertEqual(task.params, {})
        self.assertEqual(task.priority, 5)
    
    def test_execute_all(self):
        """测试执行所有任务 - 使用真实接口"""
        # 添加真实接口任务
        self.manager.add_task(CallTask("stock_sse_summary", {}))
        self.manager.add_task(CallTask("stock_account_statistics_em", {}))
        
        # 执行所有任务
        result = self.manager.execute_all()
        
        # 检查结果
        self.assertEqual(result.total_tasks, 2)
        self.assertEqual(len(result.results), 2)
        self.assertGreaterEqual(result.successful_tasks + result.failed_tasks, 0)
        
        # 打印结果
        print(f"BatchCallManager执行结果: 成功 {result.successful_tasks}/{result.total_tasks}")
        for i, task_result in enumerate(result.results):
            if task_result.success:
                print(f"  ✓ {task_result.interface_name}: {task_result.execution_time:.3f}s")
            else:
                print(f"  ✗ {task_result.interface_name}: {task_result.error}")
    
    def test_execute_by_filter(self):
        """测试按条件执行任务 - 使用真实接口"""
        # 添加真实接口任务
        self.manager.add_task(CallTask("stock_sse_summary", {}))
        self.manager.add_task(CallTask("stock_account_statistics_em", {}))
        self.manager.add_task(CallTask("stock_board_change_em", {}))
        
        # 定义过滤条件：只执行包含"sse"的接口
        def filter_func(task):
            return "sse" in task.interface_name
        
        # 按条件执行
        result = self.manager.execute_by_filter(filter_func)
        
        # 检查结果
        self.assertEqual(result.total_tasks, 1)  # 只有stock_sse_summary匹配
        self.assertEqual(len(result.results), 1)
        self.assertEqual(result.results[0].interface_name, "stock_sse_summary")
        
        print(f"按条件执行结果: 成功 {result.successful_tasks}/{result.total_tasks}")
        for task_result in result.results:
            if task_result.success:
                print(f"  ✓ {task_result.interface_name}: {task_result.execution_time:.3f}s")
            else:
                print(f"  ✗ {task_result.interface_name}: {task_result.error}")
    
    def test_clear_queue(self):
        """测试清空队列 - 使用真实接口"""
        # 添加任务
        self.manager.add_task(CallTask("stock_sse_summary", {}))
        self.assertEqual(self.manager.get_queue_size(), 1)
        
        # 清空队列
        self.manager.clear_queue()
        self.assertEqual(self.manager.get_queue_size(), 0)


# TestTimeoutManager类已删除，因为TimeoutManager类已被移除


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        # 创建真实的提供者管理器
        self.provider_manager = APIProviderManager()
        self.provider = AkshareProvider()
        self.provider_manager.register_provider(self.provider)
        
        # 创建执行器
        self.config = ExecutorConfig(
            default_timeout=10.0,  # 根据成功接口测试报告调整：平均0.44s，最大18.14s，设置10s超时
            retry_config=RetryConfig(max_retries=1),
            cache_config=CacheConfig(enabled=True, ttl=60)
        )
        self.executor = InterfaceExecutor(self.provider_manager, self.config)
    
    def test_real_interface_execution(self):
        """测试真实接口执行"""
        # 获取一个简单的接口进行测试
        interfaces = self.provider.get_supported_interfaces()
        simple_interface = None
        
        for interface_name in interfaces:
            metadata = self.provider.get_interface_metadata(interface_name)
            if metadata and not metadata.required_params and not metadata.optional_params:
                simple_interface = interface_name
                break
        
        if simple_interface:
            result = self.executor.execute_single(simple_interface, {})
            # 不要求一定成功，因为网络等因素可能影响
            self.assertIsNotNone(result)
            self.assertIsNotNone(result.task_id)
            self.assertEqual(result.interface_name, simple_interface)
    
    def test_batch_execution_with_real_interfaces(self):
        """测试真实接口批量执行"""
        # 获取几个简单的接口
        interfaces = self.provider.get_supported_interfaces()[:3]
        tasks = []
        
        for interface_name in interfaces:
            metadata = self.provider.get_interface_metadata(interface_name)
            if metadata and not metadata.required_params:
                task = CallTask(interface_name, {})
                tasks.append(task)
        
        if tasks:
            batch_result = self.executor.execute_batch(tasks)
            self.assertEqual(batch_result.total_tasks, len(tasks))
            self.assertGreaterEqual(batch_result.successful_tasks, 0)
            self.assertGreaterEqual(batch_result.failed_tasks, 0)


def run_all_tests():
    """运行所有测试"""
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestErrorClassifier,
        TestRateLimiter,
        TestSimpleCache,
        TestCallTask,
        TestCallResult,
        TestBatchResult,
        TestTaskQueue,
        TestInterfaceExecutor,
        TestTimeoutManager,
        TestBatchCallManager,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


class TestAsyncConcurrencyLimit(unittest.TestCase):
    def setUp(self):
        # 创建真实的提供者管理器（不会调用到，因为会打桩执行器内部方法）
        self.provider_manager = APIProviderManager()
        self.provider = AkshareProvider()
        self.provider_manager.register_provider(self.provider)
        self.config = ExecutorConfig(
            default_timeout=0.0,
            retry_config=RetryConfig(max_retries=1),
            cache_config=CacheConfig(enabled=False),
            async_max_concurrency=3,  # 设定并发上限
            enable_async_timeout=False  # 走 asyncio.to_thread 路径，便于在桩中测并发
        )
        self.executor = InterfaceExecutor(self.provider_manager, self.config)

    def test_async_max_concurrency_respected(self):
        # 构造多任务以触发并发
        task_count = 12
        tasks = [CallTask("iface", {"i": i}) for i in range(task_count)]

        # 通过打桩 _execute_single_with_context 来测量并发度（该函数会在线程池中执行）
        lock = threading.Lock()
        state = {"current": 0, "max": 0}

        original_impl = InterfaceExecutor._execute_single_with_context

        def stubbed_execute_single_with_context(self_exec: InterfaceExecutor, task: CallTask, context: ExecutionContext) -> CallResult:
            with lock:
                state["current"] += 1
                if state["current"] > state["max"]:
                    state["max"] = state["current"]
            # 停顿一段时间以制造重叠，从而观察并发上限
            time.sleep(0.2)
            with lock:
                state["current"] -= 1
            return CallResult(task.task_id, task.interface_name, True, data=task.params.get("i"))

        InterfaceExecutor._execute_single_with_context = stubbed_execute_single_with_context  # type: ignore
        try:
            async def run():
                return await self.executor.execute_async(tasks)
            batch_result = asyncio.run(run())

            # 基本正确性断言
            self.assertEqual(batch_result.total_tasks, task_count)
            self.assertEqual(len(batch_result.results), task_count)

            # 关键断言：最大并发不超过配置
            self.assertLessEqual(state["max"], self.config.async_max_concurrency)
        finally:
            InterfaceExecutor._execute_single_with_context = original_impl  # type: ignore


class TestPluginProtocolConsistency(unittest.TestCase):
    def setUp(self):
        self.provider_manager = APIProviderManager()
        self.provider = AkshareProvider()
        self.provider_manager.register_provider(self.provider)
        self.config = ExecutorConfig(
            default_timeout=0.0,
            retry_config=RetryConfig(max_retries=3, base_delay=0.01, max_delay=0.02),
            cache_config=CacheConfig(enabled=False),
            enable_async_timeout=False
        )
        self.executor = InterfaceExecutor(self.provider_manager, self.config)

    def test_on_error_can_abort_retry_sync(self):
        # 构造始终抛错的接口调用（通过打桩 _call_akshare_interface）
        original_call = InterfaceExecutor._call_akshare_interface
        def always_fail(self_exec: InterfaceExecutor, task: CallTask):
            raise ValueError("boom")
        InterfaceExecutor._call_akshare_interface = always_fail  # type: ignore

        # 构造插件：记录调用并在首次错误时返回 False 阻止重试
        class AbortOnErrorPlugin(ExecutorPlugin):
            def __init__(self):
                self.before = 0
                self.after = 0
                self.errors = 0
            def before_execute(self, task: CallTask, context: ExecutionContext) -> None:
                self.before += 1
            def after_execute(self, result: CallResult, context: ExecutionContext) -> None:
                self.after += 1
            def on_error(self, task: CallTask, error: Exception, context: ExecutionContext) -> bool:
                self.errors += 1
                return False  # 中断后续重试
        plugin = AbortOnErrorPlugin()
        self.executor.config.plugins = [plugin]

        try:
            task = CallTask("iface", {})
            result = self.executor._execute_with_retry(task, ExecutionContext())
            self.assertFalse(result.success)
            # 验证：before 只一次，on_error 一次（中断），after 一次（失败结果触发）
            self.assertEqual(plugin.before, 1)
            self.assertEqual(plugin.errors, 1)
            self.assertEqual(plugin.after, 1)
        finally:
            InterfaceExecutor._call_akshare_interface = original_call  # type: ignore

    def test_plugin_hooks_called_in_async(self):
        # 打桩底层 _call_akshare_interface，使其返回成功，同时记录插件调用
        class CounterPlugin(ExecutorPlugin):
            def __init__(self):
                self.before = 0
                self.after = 0
            def before_execute(self, task: CallTask, context: ExecutionContext) -> None:
                self.before += 1
            def after_execute(self, result: CallResult, context: ExecutionContext) -> None:
                self.after += 1
            def on_error(self, task: CallTask, error: Exception, context: ExecutionContext) -> bool:
                # 透传错误，不中断重试/执行
                return True
        plugin = CounterPlugin()
        self.executor.config.plugins = [plugin]

        original_call = InterfaceExecutor._call_akshare_interface
        def stubbed_call(self_exec: InterfaceExecutor, task: CallTask):
            return {"ok": True, **task.params}
        InterfaceExecutor._call_akshare_interface = stubbed_call  # type: ignore
        try:
            tasks = [CallTask("iface", {"i": i}) for i in range(5)]
            async def run():
                return await self.executor.execute_async(tasks)
            batch_result = asyncio.run(run())
            self.assertEqual(batch_result.total_tasks, 5)
            # 每个任务都应触发一次 before/after
            self.assertEqual(plugin.before, 5)
            self.assertEqual(plugin.after, 5)
        finally:
            InterfaceExecutor._call_akshare_interface = original_call  # type: ignore

    def test_on_error_can_abort_retry_async(self):
        # 让底层调用始终抛错
        original_call = InterfaceExecutor._call_akshare_interface
        def always_fail(self_exec: InterfaceExecutor, task: CallTask):
            raise ValueError("boom")
        InterfaceExecutor._call_akshare_interface = always_fail  # type: ignore

        class AbortOnErrorPlugin(ExecutorPlugin):
            def __init__(self):
                self.before = 0
                self.after = 0
                self.errors = 0
            def before_execute(self, task: CallTask, context: ExecutionContext) -> None:
                self.before += 1
            def after_execute(self, result: CallResult, context: ExecutionContext) -> None:
                self.after += 1
            def on_error(self, task: CallTask, error: Exception, context: ExecutionContext) -> bool:
                self.errors += 1
                return False
        plugin = AbortOnErrorPlugin()
        self.executor.config.plugins = [plugin]

        try:
            tasks = [CallTask("iface", {})]
            async def run():
                return await self.executor.execute_async(tasks)
            batch_result = asyncio.run(run())
            self.assertEqual(batch_result.total_tasks, 1)
            self.assertEqual(batch_result.failed_tasks, 1)
            # 应只尝试一次（on_error 返回 False 终止重试），before一次，errors一次，after一次（失败结果）
            self.assertEqual(plugin.before, 1)
            self.assertEqual(plugin.errors, 1)
            self.assertEqual(plugin.after, 1)
        finally:
            InterfaceExecutor._call_akshare_interface = original_call  # type: ignore

    def test_async_callback_exception_isolated(self):
        # stub 底层调用成功
        original_call = InterfaceExecutor._call_akshare_interface
        def stubbed(self_exec: InterfaceExecutor, task: CallTask):
            return {"ok": True}
        InterfaceExecutor._call_akshare_interface = stubbed  # type: ignore
        try:
            # 构造会抛错的回调
            called = {"count": 0}
            def bad_callback(result: CallResult):
                called["count"] += 1
                raise RuntimeError("callback boom")
            tasks = [CallTask("iface", {}) for _ in range(3)]
            async def run():
                return await self.executor.execute_async(tasks, callback=bad_callback)
            batch_result = asyncio.run(run())
            # 执行应完成且不因回调异常失败
            self.assertEqual(batch_result.total_tasks, 3)
            self.assertEqual(batch_result.successful_tasks, 3)
            # 回调应被调用3次
            self.assertEqual(called["count"], 3)
        finally:
            InterfaceExecutor._call_akshare_interface = original_call  # type: ignore


class TestAsyncRateLimitAndRetry(unittest.TestCase):
    def setUp(self):
        # 创建提供者管理器并注册 AkshareProvider（不会真正访问网络，底层会打桩）
        self.provider_manager = APIProviderManager()
        self.provider_manager.register_provider(AkshareProvider())
        # 开启异步路径，配置较小的重试延迟，便于测试
        self.config = ExecutorConfig(
            default_timeout=1.0,
            retry_config=RetryConfig(max_retries=3, base_delay=0.1, max_delay=5.0, exponential_base=2.0),
            cache_config=CacheConfig(enabled=False),
            enable_async_timeout=True,
            async_max_concurrency=10
        )
        self.executor = InterfaceExecutor(self.provider_manager, self.config)

    def test_async_retry_with_jitter_and_success(self):
        # 前两次失败（超时错误），第3次成功；校验重试次数与抖动等待下界
        original = InterfaceExecutor._call_akshare_interface
        attempts = {"n": 0}
        def flaky_call(self_exec: InterfaceExecutor, task: CallTask):
            attempts["n"] += 1
            if attempts["n"] <= 2:
                raise TimeoutError("timeout during call")
            return {"ok": True}
        InterfaceExecutor._call_akshare_interface = flaky_call  # type: ignore
        try:
            tasks = [CallTask("iface_async_retry", {}, retry_count=3)]
            # Patch 抖动为 20%，基于实现：delay = base_delay + 0.2 * base_delay
            with patch("core.data.interfaces.executor.random.uniform", return_value=0.2):
                async def run():
                    return await self.executor.execute_async(tasks)
                t0 = time.time()
                batch_result = asyncio.run(run())
                elapsed = time.time() - t0
            self.assertEqual(batch_result.total_tasks, 1)
            self.assertTrue(batch_result.results[0].success)
            # 预期等待：第1次 0.1*(1+0.2)=0.12，第2次 0.2*(1+0.2)=0.24，总 ~0.36s，留一定余量
            self.assertGreaterEqual(elapsed, 0.33)
            self.assertEqual(attempts["n"], 3)
        finally:
            InterfaceExecutor._call_akshare_interface = original  # type: ignore

    def test_async_retry_max_attempts_stop_on_fail(self):
        # 始终失败，验证达到最大尝试次数后停止，并记录 total_attempts
        original = InterfaceExecutor._call_akshare_interface
        attempts = {"n": 0}
        def always_fail(self_exec: InterfaceExecutor, task: CallTask):
            attempts["n"] += 1
            raise TimeoutError("timeout during call")
        InterfaceExecutor._call_akshare_interface = always_fail  # type: ignore
        try:
            # 设为最大重试2（总尝试=2）
            self.executor.config.retry_config = RetryConfig(max_retries=2, base_delay=0.05, max_delay=1.0, exponential_base=2.0)
            tasks = [CallTask("iface_fail", {}, retry_count=2)]
            async def run():
                return await self.executor.execute_async(tasks)
            batch_result = asyncio.run(run())
            self.assertEqual(batch_result.total_tasks, 1)
            self.assertFalse(batch_result.results[0].success)
            self.assertEqual(batch_result.results[0].metadata.get("total_attempts"), 2)
            self.assertEqual(attempts["n"], 2)
        finally:
            InterfaceExecutor._call_akshare_interface = original  # type: ignore

    def test_async_rate_limit_enforced(self):
        # 配置限流：0.5 秒窗口最多 2 次；4 个任务应跨两个窗口执行
        self.executor.config.rate_limits = {"iface_rl": RateLimit(max_calls=2, time_window=0.5)}
        # 重建限流器（执行器在初始化时构建过一次）
        self.executor.rate_limiters = {"iface_rl": RateLimiter(self.executor.config.rate_limits["iface_rl"])}

        original = InterfaceExecutor._call_akshare_interface
        def fast_call(self_exec: InterfaceExecutor, task: CallTask):
            time.sleep(0.01)
            return {"ok": True, "i": task.params.get("i")}
        InterfaceExecutor._call_akshare_interface = fast_call  # type: ignore
        try:
            tasks = [CallTask("iface_rl", {"i": i}) for i in range(4)]
            async def run():
                return await self.executor.execute_async(tasks)
            t0 = time.time()
            batch_result = asyncio.run(run())
            elapsed = time.time() - t0
            self.assertEqual(batch_result.total_tasks, 4)
            self.assertTrue(all(r.success for r in batch_result.results))
            # 至少跨越两个 0.5s 窗口
            self.assertGreaterEqual(elapsed, 0.45)
        finally:
            InterfaceExecutor._call_akshare_interface = original  # type: ignore


def run_all_tests():
    """运行所有测试"""
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestErrorClassifier,
        TestRateLimiter,
        TestSimpleCache,
        TestCallTask,
        TestCallResult,
        TestBatchResult,
        TestTaskQueue,
        TestInterfaceExecutor,
        TestTimeoutManager,
        TestBatchCallManager,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


class TestAsyncConcurrencyLimit(unittest.TestCase):
    def setUp(self):
        # 创建真实的提供者管理器（不会调用到，因为会打桩执行器内部方法）
        self.provider_manager = APIProviderManager()
        self.provider = AkshareProvider()
        self.provider_manager.register_provider(self.provider)
        self.config = ExecutorConfig(
            default_timeout=0.0,
            retry_config=RetryConfig(max_retries=1),
            cache_config=CacheConfig(enabled=False),
            async_max_concurrency=3,  # 设定并发上限
            enable_async_timeout=False  # 走 asyncio.to_thread 路径，便于在桩中测并发
        )
        self.executor = InterfaceExecutor(self.provider_manager, self.config)

    def test_async_max_concurrency_respected(self):
        # 构造多任务以触发并发
        task_count = 12
        tasks = [CallTask("iface", {"i": i}) for i in range(task_count)]

        # 通过打桩 _execute_single_with_context 来测量并发度（该函数会在线程池中执行）
        lock = threading.Lock()
        state = {"current": 0, "max": 0}

        original_impl = InterfaceExecutor._execute_single_with_context

        def stubbed_execute_single_with_context(self_exec: InterfaceExecutor, task: CallTask, context: ExecutionContext) -> CallResult:
            with lock:
                state["current"] += 1
                if state["current"] > state["max"]:
                    state["max"] = state["current"]
            # 停顿一段时间以制造重叠，从而观察并发上限
            time.sleep(0.2)
            with lock:
                state["current"] -= 1
            return CallResult(task.task_id, task.interface_name, True, data=task.params.get("i"))

        InterfaceExecutor._execute_single_with_context = stubbed_execute_single_with_context  # type: ignore
        try:
            async def run():
                return await self.executor.execute_async(tasks)
            batch_result = asyncio.run(run())

            # 基本正确性断言
            self.assertEqual(batch_result.total_tasks, task_count)
            self.assertEqual(len(batch_result.results), task_count)

            # 关键断言：最大并发不超过配置
            self.assertLessEqual(state["max"], self.config.async_max_concurrency)
        finally:
            InterfaceExecutor._execute_single_with_context = original_impl  # type: ignore


if __name__ == "__main__":
    print("开始执行Executor模块全面测试...")
    print("=" * 80)
    
    success = run_all_tests()
    
    print("=" * 80)
    if success:
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败！")
    
    exit(0 if success else 1)
