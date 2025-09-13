#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细接口测试方案
为每个接口输出详细的测试记录，包括期望参数、实际参数、调用结果等
"""

import asyncio
import logging
import time
import unittest
import sys
import os
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# 测试配置
TEST_CONFIG = {
    # 超时配置
    "default_timeout": 3.0,  # 默认超时3秒
    "interface_timeouts": {
        "stock_zh_a_hist": 8.0,  # 历史数据接口8秒
        "stock_financial_analysis_indicator_em": 6.0,  # 财务分析接口6秒
        "stock_zh_a_hist_min_em": 6.0,  # 分钟数据接口6秒
    },
    
    # 重试配置
    "max_retries": 2,  # 重试2次
    "base_delay": 0.2,  # 基础延迟
    "max_delay": 2.0,  # 最大延迟
    
    # 并发配置
    "max_workers": 5,  # 减少并发数，避免网络问题
    
    # 频率限制配置
    "rate_limits": {
        "stock_zh_a_spot": {"max_calls": 5, "time_window": 60.0},
        "stock_zh_a_spot_em": {"max_calls": 10, "time_window": 60.0},
    },
    
    # 缓存配置
    "cache_enabled": True,
    "cache_ttl": 300,  # 5分钟缓存
    "cache_max_size": 200,
    
    # 日志配置
    "log_level": "DEBUG",
    "log_file": "test_interfaces_detailed.log",
    "results_file": "test_results_detailed.txt",
    "debug_file": "test_debug_detailed.json",  # 新增调试文件
}

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入必要的模块
from core.data.interfaces.executor import (
    InterfaceExecutor, CallTask, CallResult, BatchResult, 
    ExecutionContext, ExecutorConfig, RateLimit, CacheConfig, 
    RetryConfig, BatchCallManager, TaskQueue, ResultCollector
)
from core.data.interfaces.base import APIProviderManager, InterfaceMetadata, DataSource, FunctionCategory
from core.data.interfaces.akshare import akshare_provider


@dataclass
class InterfaceTestRecord:
    """接口测试记录"""
    interface_name: str
    description: str
    data_source: str
    function_category: str
    required_params: List[str]
    generated_params: Dict[str, Any]
    call_success: bool
    data_valid: bool
    error_type: Optional[str]
    error_message: Optional[str]
    execution_time: float
    retry_count: int
    from_cache: bool
    raw_result: Optional[Any] = None
    fix_suggestions: List[str] = None


class SmartParameterGenerator:
    """智能参数生成器"""
    
    def __init__(self):
        # 基于接口名称和参数类型的参数模板
        self.parameter_templates = {
            # 股票代码相关
            'stock_codes': {
                'a_stock': ['000001', '000002', '600000', '600036', '000858'],
                'hk_stock': ['00700', '00941', '01299', '00388'],
                'us_stock': ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN'],
                'kcb': ['688001', '688002', '688003'],
                'cy': ['300001', '300002', '300003'],
                'bj': ['830001', '830002', '830003']
            },
            # 日期相关
            'date_formats': {
                'start_date': ['2024-01-01', '20240101', '2024-01-01 00:00:00'],
                'end_date': ['2024-12-31', '20241231', '2024-12-31 23:59:59'],
                'date': ['2024-09-13', '20240913', '2024-09-13 00:00:00'],
                'period': ['daily', 'weekly', 'monthly', '1d', '1w', '1m']
            },
            # 其他常用参数
            'common_params': {
                'symbol': '000001',
                'indicator': 'pe',
                'market': 'A股',
                'adjust': 'qfq',
                'timeout': 10,
                'token': 'test_token',
                'stock': '000001',
                'code': '000001',
                'name': '平安银行',
                'type': 'A股',
                'category': '股票',
                'status': 'active',
                'level': 1,
                'page': 1,
                'size': 100,
                'limit': 100,
                'offset': 0
            }
        }
    
    def generate_params(self, interface: InterfaceMetadata) -> Dict[str, Any]:
        """根据接口元数据生成合适的参数"""
        params = {}
        
        if not interface.required_params:
            return params
        
        # 根据接口名称和参数生成测试数据
        for param in interface.required_params:
            param_lower = param.lower()
            
            # 股票代码相关
            if any(keyword in param_lower for keyword in ['code', 'symbol', 'stock']):
                params[param] = self._get_stock_code(interface.name, param)
            
            # 日期相关
            elif any(keyword in param_lower for keyword in ['date', 'time', 'period']):
                params[param] = self._get_date_param(param)
            
            # 其他参数
            else:
                params[param] = self._get_common_param(param)
        
        return params
    
    def _get_stock_code(self, interface_name: str, param_name: str) -> str:
        """根据接口名称获取合适的股票代码"""
        interface_lower = interface_name.lower()
        
        if 'hk' in interface_lower:
            return self.parameter_templates['stock_codes']['hk_stock'][0]
        elif 'us' in interface_lower:
            return self.parameter_templates['stock_codes']['us_stock'][0]
        elif 'kcb' in interface_lower or 'kc' in interface_lower:
            return self.parameter_templates['stock_codes']['kcb'][0]
        elif 'cy' in interface_lower:
            return self.parameter_templates['stock_codes']['cy'][0]
        elif 'bj' in interface_lower:
            return self.parameter_templates['stock_codes']['bj'][0]
        else:
            return self.parameter_templates['stock_codes']['a_stock'][0]
    
    def _get_date_param(self, param_name: str) -> str:
        """根据参数名称获取合适的日期格式"""
        param_lower = param_name.lower()
        
        if 'start' in param_lower:
            return self.parameter_templates['date_formats']['start_date'][0]
        elif 'end' in param_lower:
            return self.parameter_templates['date_formats']['end_date'][0]
        elif 'period' in param_lower:
            return self.parameter_templates['date_formats']['period'][0]
        else:
            return self.parameter_templates['date_formats']['date'][0]
    
    def _get_common_param(self, param_name: str) -> Any:
        """获取通用参数值"""
        param_lower = param_name.lower()
        
        # 根据参数名称匹配
        for key, value in self.parameter_templates['common_params'].items():
            if key in param_lower:
                return value
        
        # 默认值
        return "test_value"


class DetailedInterfaceTester:
    """详细接口测试器"""
    
    def __init__(self, executor: InterfaceExecutor, logger: logging.Logger):
        self.executor = executor
        self.logger = logger
        self.parameter_generator = SmartParameterGenerator()
        self.test_records: List[InterfaceTestRecord] = []
        self.debug_data = {
            "test_start_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "interfaces_tested": 0,
            "interfaces_successful": 0,
            "interfaces_failed": 0,
            "error_analysis": {},
            "interface_records": []
        }
    
    def test_interface_detailed(self, interface: InterfaceMetadata) -> InterfaceTestRecord:
        """详细测试单个接口"""
        self.logger.info("=" * 100)
        self.logger.info(f"测试接口: {interface.name}")
        self.logger.info("=" * 100)
        
        # 1. 输出接口基本信息
        self.logger.info(f"接口描述: {interface.description}")
        self.logger.info(f"数据源: {interface.data_source.value}")
        self.logger.info(f"功能分类: {interface.function_category.value}")
        self.logger.info(f"必需参数: {interface.required_params}")
        
        # 2. 生成测试参数
        generated_params = self.parameter_generator.generate_params(interface)
        self.logger.info(f"生成参数: {json.dumps(generated_params, ensure_ascii=False, indent=2)}")
        
        # 3. 执行调用
        start_time = time.time()
        try:
            result = self.executor.execute_single(interface.name, generated_params)
            execution_time = time.time() - start_time
        except Exception as e:
            execution_time = time.time() - start_time
            # 创建失败结果
            result = CallResult(
                task_id=f"test_{interface.name}",
                interface_name=interface.name,
                success=False,
                data=None,
                error=str(e),
                execution_time=execution_time,
                metadata={'total_attempts': 1, 'from_cache': False}
            )
        
        # 4. 分析结果
        call_success = result.success
        data_valid = self._is_data_valid(result)
        error_type = type(result.error).__name__ if result.error else None
        error_message = str(result.error) if result.error else None
        retry_count = result.metadata.get('total_attempts', 1)
        from_cache = result.metadata.get('from_cache', False)
        
        # 5. 输出详细结果
        self.logger.info("-" * 80)
        self.logger.info("调用结果分析:")
        self.logger.info(f"  调用成功: {'✅' if call_success else '❌'}")
        self.logger.info(f"  数据有效: {'✅' if data_valid else '❌'}")
        self.logger.info(f"  执行时间: {execution_time:.3f}s")
        self.logger.info(f"  重试次数: {retry_count}")
        self.logger.info(f"  来自缓存: {'✅' if from_cache else '❌'}")
        
        if result.error:
            self.logger.error(f"  错误类型: {error_type}")
            self.logger.error(f"  错误信息: {error_message}")
        
        if result.data is not None:
            if hasattr(result.data, '__len__'):
                self.logger.info(f"  返回数据: {type(result.data).__name__}, 长度: {len(result.data)}")
            else:
                self.logger.info(f"  返回数据: {type(result.data).__name__}")
        
        # 6. 生成修复建议
        fix_suggestions = self._generate_fix_suggestions(
            interface, generated_params, result, call_success, data_valid
        )
        
        if fix_suggestions:
            self.logger.info("修复建议:")
            for i, suggestion in enumerate(fix_suggestions, 1):
                self.logger.info(f"  {i}. {suggestion}")
        
        # 7. 创建测试记录
        record = InterfaceTestRecord(
            interface_name=interface.name,
            description=interface.description,
            data_source=interface.data_source.value,
            function_category=interface.function_category.value,
            required_params=interface.required_params,
            generated_params=generated_params,
            call_success=call_success,
            data_valid=data_valid,
            error_type=error_type,
            error_message=error_message,
            execution_time=execution_time,
            retry_count=retry_count,
            from_cache=from_cache,
            raw_result=result.data,
            fix_suggestions=fix_suggestions
        )
        
        # 8. 更新调试数据
        self.debug_data["interfaces_tested"] += 1
        if call_success and data_valid:
            self.debug_data["interfaces_successful"] += 1
        else:
            self.debug_data["interfaces_failed"] += 1
        
        # 记录错误分析
        if error_type:
            if error_type not in self.debug_data["error_analysis"]:
                self.debug_data["error_analysis"][error_type] = 0
            self.debug_data["error_analysis"][error_type] += 1
        
        # 记录接口详情
        self.debug_data["interface_records"].append({
            "interface_name": interface.name,
            "call_success": call_success,
            "data_valid": data_valid,
            "error_type": error_type,
            "execution_time": execution_time,
            "generated_params": generated_params,
            "fix_suggestions": fix_suggestions
        })
        
        self.test_records.append(record)
        return record
    
    def _is_data_valid(self, result: CallResult) -> bool:
        """检查数据是否有效"""
        if not result.success or result.data is None:
            return False
        
        # 检查数据是否为空
        if hasattr(result.data, '__len__') and len(result.data) == 0:
            return False
        
        # 检查数据类型
        if isinstance(result.data, str) and result.data.strip() == "":
            return False
        
        return True
    
    def _generate_fix_suggestions(self, interface: InterfaceMetadata, params: Dict[str, Any], 
                                 result: CallResult, call_success: bool, data_valid: bool) -> List[str]:
        """生成修复建议"""
        suggestions = []
        
        if not call_success and result.error:
            error_str = str(result.error)
            
            # KeyError - 缺少参数
            if "KeyError" in error_str:
                missing_key = error_str.split("'")[1] if "'" in error_str else "未知参数"
                suggestions.append(f"缺少必需参数 '{missing_key}'，请检查接口文档")
            
            # TypeError - 数据类型错误
            elif "TypeError" in error_str:
                suggestions.append("数据类型不匹配，请检查参数类型和格式")
            
            # ValueError - 参数值错误
            elif "ValueError" in error_str:
                suggestions.append("参数值无效，请检查参数值的范围和格式")
            
            # 网络相关错误
            elif any(keyword in error_str for keyword in ["Connection", "ProxyError", "Read timed out"]):
                suggestions.append("网络连接问题，请检查网络连接或代理设置")
            
            # 超时错误
            elif "timed out" in error_str:
                suggestions.append("请求超时，请增加超时时间或检查网络状况")
            
            # 其他错误
            else:
                suggestions.append(f"未知错误类型: {type(result.error).__name__}")
        
        elif call_success and not data_valid:
            suggestions.append("接口调用成功但返回数据无效，可能是参数值不正确")
        
        # 基于接口名称的特殊建议
        if "em" in interface.name.lower():
            suggestions.append("东方财富接口可能需要特定的参数格式，请参考官方文档")
        
        if "sina" in interface.name.lower():
            suggestions.append("新浪接口可能需要特定的股票代码格式")
        
        if "ths" in interface.name.lower():
            suggestions.append("同花顺接口可能需要特定的参数值")
        
        return suggestions
    
    def save_debug_data(self, filename: str):
        """保存调试数据到JSON文件"""
        self.debug_data["test_end_time"] = time.strftime('%Y-%m-%d %H:%M:%S')
        self.debug_data["total_execution_time"] = sum(record.execution_time for record in self.test_records)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.debug_data, f, ensure_ascii=False, indent=2, default=str)
        
        self.logger.info(f"调试数据已保存到: {filename}")


class TestInterfaceExecutorDetailed(unittest.TestCase):
    """详细接口执行器测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 设置详细的日志配置
        log_level = getattr(logging, TEST_CONFIG["log_level"])
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),  # 控制台输出
                logging.FileHandler(TEST_CONFIG["log_file"], mode='w', encoding='utf-8')  # 文件输出
            ]
        )
        
        # 设置akshare和executor的日志级别
        logging.getLogger('akshare').setLevel(logging.WARNING)
        logging.getLogger('core.data.interfaces.executor').setLevel(logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        
        # 创建API提供者管理器
        self.provider_manager = APIProviderManager()
        self.provider_manager.register_provider(akshare_provider)
        
        # 创建执行器配置
        rate_limits = {}
        for interface, limits in TEST_CONFIG["rate_limits"].items():
            rate_limits[interface] = RateLimit(
                max_calls=limits["max_calls"], 
                time_window=limits["time_window"]
            )
        
        self.config = ExecutorConfig(
            rate_limits=rate_limits,
            cache_config=CacheConfig(
                enabled=TEST_CONFIG["cache_enabled"], 
                ttl=TEST_CONFIG["cache_ttl"], 
                max_size=TEST_CONFIG["cache_max_size"]
            ),
            retry_config=RetryConfig(
                max_retries=TEST_CONFIG["max_retries"],
                base_delay=TEST_CONFIG["base_delay"],
                max_delay=TEST_CONFIG["max_delay"]
            ),
            default_timeout=TEST_CONFIG["default_timeout"],
            max_workers=TEST_CONFIG["max_workers"],
            interface_timeouts=TEST_CONFIG["interface_timeouts"]
        )
        
        # 创建执行器
        self.executor = InterfaceExecutor(self.provider_manager, self.config)
        
        # 获取所有注册的接口
        self.registered_interfaces = self._get_all_registered_interfaces()
        
        # 创建详细测试器
        self.detailed_tester = DetailedInterfaceTester(self.executor, self.logger)
        
        self.logger.info(f"Found {len(self.registered_interfaces)} registered interfaces")
    
    def _get_all_registered_interfaces(self) -> List[InterfaceMetadata]:
        """获取所有注册的接口"""
        all_interfaces = []
        for provider in self.provider_manager._providers.values():
            all_interfaces.extend(provider.registry._interfaces.values())
        return all_interfaces
    
    def test_all_interfaces_detailed(self):
        """详细测试所有接口"""
        self.logger.info(f"开始详细测试所有 {len(self.registered_interfaces)} 个接口...")
        
        # 测试所有接口
        for i, interface in enumerate(self.registered_interfaces, 1):
            self.logger.info(f"\n进度: {i}/{len(self.registered_interfaces)}")
            
            try:
                record = self.detailed_tester.test_interface_detailed(interface)
                
                # 每10个接口保存一次调试数据
                if i % 10 == 0:
                    self.detailed_tester.save_debug_data(TEST_CONFIG["debug_file"])
                    
            except Exception as e:
                self.logger.error(f"测试接口 {interface.name} 时发生异常: {e}")
                continue
        
        # 保存最终调试数据
        self.detailed_tester.save_debug_data(TEST_CONFIG["debug_file"])
        
        # 输出测试总结
        self._output_test_summary()
        
        # 至少应该有一些接口成功
        self.assertGreater(self.detailed_tester.debug_data["interfaces_successful"], 0, "No interfaces succeeded")
    
    def _output_test_summary(self):
        """输出测试总结"""
        debug_data = self.detailed_tester.debug_data
        
        self.logger.info("\n" + "=" * 100)
        self.logger.info("测试总结")
        self.logger.info("=" * 100)
        self.logger.info(f"总测试接口数: {debug_data['interfaces_tested']}")
        self.logger.info(f"成功接口数: {debug_data['interfaces_successful']}")
        self.logger.info(f"失败接口数: {debug_data['interfaces_failed']}")
        self.logger.info(f"成功率: {debug_data['interfaces_successful']/debug_data['interfaces_tested']*100:.1f}%")
        self.logger.info(f"总执行时间: {debug_data['total_execution_time']:.2f}s")
        
        # 错误分析
        if debug_data['error_analysis']:
            self.logger.info("\n错误类型分析:")
            for error_type, count in debug_data['error_analysis'].items():
                self.logger.info(f"  {error_type}: {count} 个接口")
        
        # 保存到文件
        with open(TEST_CONFIG["results_file"], 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write("详细接口测试结果\n")
            f.write("=" * 100 + "\n")
            f.write(f"测试开始时间: {debug_data['test_start_time']}\n")
            f.write(f"测试结束时间: {debug_data['test_end_time']}\n")
            f.write(f"总测试接口数: {debug_data['interfaces_tested']}\n")
            f.write(f"成功接口数: {debug_data['interfaces_successful']}\n")
            f.write(f"失败接口数: {debug_data['interfaces_failed']}\n")
            f.write(f"成功率: {debug_data['interfaces_successful']/debug_data['interfaces_tested']*100:.1f}%\n")
            f.write(f"总执行时间: {debug_data['total_execution_time']:.2f}s\n")
            
            if debug_data['error_analysis']:
                f.write("\n错误类型分析:\n")
                for error_type, count in debug_data['error_analysis'].items():
                    f.write(f"  {error_type}: {count} 个接口\n")
            
            f.write("\n详细接口记录:\n")
            for record in debug_data['interface_records']:
                f.write(f"\n接口: {record['interface_name']}\n")
                f.write(f"  调用成功: {record['call_success']}\n")
                f.write(f"  数据有效: {record['data_valid']}\n")
                f.write(f"  错误类型: {record['error_type']}\n")
                f.write(f"  执行时间: {record['execution_time']:.3f}s\n")
                f.write(f"  生成参数: {json.dumps(record['generated_params'], ensure_ascii=False)}\n")
                if record['fix_suggestions']:
                    f.write(f"  修复建议: {', '.join(record['fix_suggestions'])}\n")


def run_detailed_test():
    """运行详细测试"""
    print("=" * 100)
    print("开始运行详细接口测试")
    print("=" * 100)
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestInterfaceExecutorDetailed('test_all_interfaces_detailed'))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("\n" + "=" * 100)
    print("测试完成")
    print("=" * 100)
    print(f"详细日志: {TEST_CONFIG['log_file']}")
    print(f"测试结果: {TEST_CONFIG['results_file']}")
    print(f"调试数据: {TEST_CONFIG['debug_file']}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_detailed_test()
    exit(0 if success else 1)