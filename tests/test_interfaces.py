#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面接口测试方案 - 适配新架构
利用新的执行器架构，提供详细的接口测试和问题检测功能
"""

import logging
import time
import sys
import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# 测试配置
TEST_CONFIG = {
    "default_timeout": 1.0,
    "max_retries": 1,
    "log_level": "INFO",
    "results_file": "interface_test_results.json",
    "show_progress": True
}

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入必要的模块
from core.data.interfaces.executor import InterfaceExecutor, CallResult, ExecutorConfig, RetryConfig
from core.data.interfaces.base import APIProviderManager, InterfaceMetadata, FunctionCategory
from core.data.interfaces.akshare import akshare_provider


@dataclass
class InterfaceTestResult:
    """测试结果记录"""
    interface_name: str
    test_type: str  # 'single'
    success: bool
    execution_time: float
    data_size: int = 0
    error_message: Optional[str] = None
    generated_params: Dict[str, Any] = None
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'interface_name': self.interface_name,
            'test_type': self.test_type,
            'success': self.success,
            'execution_time': self.execution_time,
            'data_size': self.data_size,
            'error_message': self.error_message,
            'generated_params': self.generated_params,
            'metadata': self.metadata or {}
        }





class EnhancedParameterGenerator:
    """增强的参数生成器 - 适配新的接口元数据"""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        

    
    def generate_params_for_interface(self, interface: InterfaceMetadata) -> Dict[str, Any]:
        """为特定接口获取参数"""
        # 直接使用接口的示例参数，如果没有则返回空字典
        return interface.example_params or {}
    



class ComprehensiveInterfaceTester:
    """全面的接口测试器"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.provider_manager = self._setup_provider_manager()
        self.executor = self._setup_executor()
        self.parameter_generator = EnhancedParameterGenerator(self.logger)
        self.test_results = []
        
        # 获取所有接口
        self.interfaces = self._get_all_interfaces()
        self.logger.info(f"发现 {len(self.interfaces)} 个接口")
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logging.basicConfig(
            level=getattr(logging, TEST_CONFIG["log_level"]),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('interface_test.log', encoding='utf-8')
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
        retry_config = RetryConfig(max_retries=TEST_CONFIG["max_retries"])
        config = ExecutorConfig(
            default_timeout=TEST_CONFIG["default_timeout"],
            retry_config=retry_config
        )
        return InterfaceExecutor(self.provider_manager, config)
    
    def _get_all_interfaces(self) -> List[InterfaceMetadata]:
        """获取所有接口"""
        all_interfaces = []
        for provider in self.provider_manager._providers.values():
            all_interfaces.extend(provider.registry._interfaces.values())
        return all_interfaces
    
    def test_single_interface(self, interface: InterfaceMetadata) -> InterfaceTestResult:
        """测试单个接口"""
        start_time = time.time()
        
        try:
            # 生成参数
            params = self.parameter_generator.generate_params_for_interface(interface)
            
            # 执行调用
            result = self.executor.execute_single(interface.name, params)
            
            # 计算数据大小
            data_size = self._calculate_data_size(result.data)
            
            test_result = InterfaceTestResult(
                interface_name=interface.name,
                test_type='single',
                success=result.success,
                execution_time=time.time() - start_time,
                data_size=data_size,
                error_message=str(result.error) if result.error else None,
                generated_params=params,
                metadata={
                    'description': interface.description,
                    'category': interface.function_category.value,
                    'data_source': interface.data_source.value,
                    'required_params': interface.required_params,
                    'optional_params': interface.optional_params
                }
            )
            
            return test_result
            
        except Exception as e:
            return InterfaceTestResult(
                interface_name=interface.name,
                test_type='single',
                success=False,
                execution_time=time.time() - start_time,
                error_message=str(e),
                generated_params=params if 'params' in locals() else {},
                metadata={'description': interface.description}
            )
    

    
    def _calculate_data_size(self, data: Any) -> int:
        """计算数据大小"""
        if data is None:
            return 0
        
        try:
            if hasattr(data, '__len__'):
                return len(data)
            elif hasattr(data, 'shape'):  # pandas DataFrame/Series
                return data.shape[0] if len(data.shape) > 0 else 0
            else:
                return 1
        except:
            return 0
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """运行全面测试 - 测试所有接口"""
        self.logger.info(f"开始全面接口测试，共 {len(self.interfaces)} 个接口")
        start_time = time.time()
        
        # 测试所有接口
        total_interfaces = len(self.interfaces)
        batch_size = 50  # 每批处理50个接口
        
        for i in range(0, total_interfaces, batch_size):
            batch_end = min(i + batch_size, total_interfaces)
            current_batch = self.interfaces[i:batch_end]
            
            self.logger.info(f"正在测试第 {i+1}-{batch_end} 个接口 ({len(current_batch)} 个)")
            
            # 单接口测试
            for j, interface in enumerate(current_batch, 1):
                current_index = i + j
                try:
                    # 显示开始测试的信息
                    if TEST_CONFIG["show_progress"]:
                        print(f"\r正在测试 [{current_index}/{total_interfaces}] {interface.name}...", end="", flush=True)
                    
                    result = self.test_single_interface(interface)
                    self.test_results.append(result)
                    
                    status = "✓" if result.success else "✗"
                    progress = f"[{current_index}/{total_interfaces}]"
                    error_info = f" - {result.error_message[:80]}" if result.error_message else ""
                    
                    # 清除进度行并打印结果
                    if TEST_CONFIG["show_progress"]:
                        print(f"\r{progress} {status} {interface.name} ({result.execution_time:.3f}s){error_info}")
                    else:
                        self.logger.info(f"{progress} {status} {interface.name} ({result.execution_time:.3f}s){error_info}")
                    
                    # 每测试10个接口保存一次结果
                    if current_index % 10 == 0:
                        self._save_test_results()
                        success_count = sum(1 for r in self.test_results if r.success)
                        success_rate = success_count / len(self.test_results) * 100
                        print(f"\n=== 进度报告 [{current_index}/{total_interfaces}] 成功率: {success_rate:.1f}% ({success_count}/{len(self.test_results)}) ===")
                        
                except Exception as e:
                    self.logger.error(f"测试接口 {interface.name} 时发生异常: {str(e)}")
                    # 创建失败结果记录
                    failed_result = InterfaceTestResult(
                        interface_name=interface.name,
                        test_type='single',
                        success=False,
                        execution_time=0.0,
                        error_message=f"测试异常: {str(e)}",
                        metadata={'description': interface.description}
                    )
                    self.test_results.append(failed_result)
        
        # 生成测试报告
        total_time = time.time() - start_time
        report = self._generate_test_report(total_time)
        
        # 保存最终结果
        self._save_test_results()
        self._save_detailed_report(report)
        
        self.logger.info(f"全面测试完成，总耗时: {total_time:.2f}s")
        return report
    
    def _generate_test_report(self, total_time: float) -> Dict[str, Any]:
        """生成测试报告"""
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r.success)
        failed_tests = total_tests - successful_tests
        
        # 按测试类型分组
        by_type = {}
        for result in self.test_results:
            test_type = result.test_type
            if test_type not in by_type:
                by_type[test_type] = {'total': 0, 'success': 0, 'failed': 0}
            
            by_type[test_type]['total'] += 1
            if result.success:
                by_type[test_type]['success'] += 1
            else:
                by_type[test_type]['failed'] += 1
        
        # 按功能分类分组
        by_category = {}
        for result in self.test_results:
            category = result.metadata.get('category', 'unknown') if result.metadata else 'unknown'
            if category not in by_category:
                by_category[category] = {'total': 0, 'success': 0, 'failed': 0}
            
            by_category[category]['total'] += 1
            if result.success:
                by_category[category]['success'] += 1
            else:
                by_category[category]['failed'] += 1
        
        # 失败接口详情
        failed_interfaces = [
            {
                'name': r.interface_name,
                'type': r.test_type,
                'error': r.error_message,
                'execution_time': r.execution_time
            }
            for r in self.test_results if not r.success
        ]
        
        report = {
            'summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'failed_tests': failed_tests,
                'success_rate': successful_tests / total_tests if total_tests > 0 else 0,
                'total_execution_time': total_time,
                'average_execution_time': sum(r.execution_time for r in self.test_results) / total_tests if total_tests > 0 else 0
            },
            'by_test_type': by_type,
            'by_category': by_category,
            'failed_interfaces': failed_interfaces,
            'top_performers': sorted(
                [r for r in self.test_results if r.success],
                key=lambda x: x.execution_time
            )[:5],
            'slowest_interfaces': sorted(
                self.test_results,
                key=lambda x: x.execution_time,
                reverse=True
            )[:5]
        }
        
        return report
    
    def _save_test_results(self):
        """保存测试结果"""
        results_data = {
            'timestamp': time.time(),
            'config': TEST_CONFIG,
            'results': [r.to_dict() for r in self.test_results]
        }
        
        with open(TEST_CONFIG["results_file"], 'w', encoding='utf-8') as f:
            json.dump(results_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"测试结果已保存到: {TEST_CONFIG['results_file']}")
    
    def _save_detailed_report(self, report: Dict[str, Any]):
        """保存详细报告"""
        # 保存详细的测试报告
        detailed_report_file = 'detailed_interface_test_report.json'
        with open(detailed_report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 保存失败接口的详细信息
        failed_interfaces_file = 'failed_interfaces_report.txt'
        with open(failed_interfaces_file, 'w', encoding='utf-8') as f:
            f.write("失败接口详细报告\n")
            f.write("=" * 80 + "\n\n")
            
            failed_results = [r for r in self.test_results if not r.success]
            for result in failed_results:
                f.write(f"接口名称: {result.interface_name}\n")
                f.write(f"测试类型: {result.test_type}\n")
                f.write(f"执行时间: {result.execution_time:.3f}s\n")
                f.write(f"错误信息: {result.error_message or 'N/A'}\n")
                f.write(f"生成参数: {result.generated_params}\n")
                if result.metadata:
                    f.write(f"接口描述: {result.metadata.get('description', 'N/A')}\n")
                    f.write(f"功能分类: {result.metadata.get('category', 'N/A')}\n")
                    f.write(f"必需参数: {result.metadata.get('required_params', [])}\n")
                    f.write(f"可选参数: {result.metadata.get('optional_params', [])}\n")
                f.write("-" * 80 + "\n\n")
        
        # 保存成功接口的统计信息
        success_interfaces_file = 'success_interfaces_report.txt'
        with open(success_interfaces_file, 'w', encoding='utf-8') as f:
            f.write("成功接口统计报告\n")
            f.write("=" * 80 + "\n\n")
            
            success_results = [r for r in self.test_results if r.success]
            for result in success_results:
                f.write(f"接口名称: {result.interface_name}\n")
                f.write(f"执行时间: {result.execution_time:.3f}s\n")
                f.write(f"数据大小: {result.data_size}\n")
                f.write(f"生成参数: {result.generated_params}\n")
                if result.metadata:
                    f.write(f"接口描述: {result.metadata.get('description', 'N/A')}\n")
                    f.write(f"功能分类: {result.metadata.get('category', 'N/A')}\n")
                f.write("-" * 40 + "\n\n")
        
        self.logger.info(f"详细报告已保存到: {detailed_report_file}")
        self.logger.info(f"失败接口报告已保存到: {failed_interfaces_file}")
        self.logger.info(f"成功接口报告已保存到: {success_interfaces_file}")


def run_interface_tests():
    """运行接口测试"""
    try:
        tester = ComprehensiveInterfaceTester()
        report = tester.run_comprehensive_test()
        
        # 打印测试报告
        print("\n" + "=" * 80)
        print("接口测试报告")
        print("=" * 80)
        
        summary = report['summary']
        print(f"总测试数: {summary['total_tests']}")
        print(f"成功: {summary['successful_tests']}")
        print(f"失败: {summary['failed_tests']}")
        print(f"成功率: {summary['success_rate']:.2%}")
        print(f"总耗时: {summary['total_execution_time']:.2f}s")
        print(f"平均耗时: {summary['average_execution_time']:.3f}s")
        
        # 按功能分类统计
        print("\n按功能分类统计:")
        for category, stats in report['by_category'].items():
            print(f"  {category}: {stats['success']}/{stats['total']} ({stats['success']/stats['total']:.1%})")
        
        # 失败接口
        if report['failed_interfaces']:
            print("\n失败接口:")
            for failed in report['failed_interfaces'][:10]:  # 只显示前10个
                print(f"  ✗ {failed['name']} - {failed['error'][:100]}...")
        
        print("=" * 80)
        
        return summary['success_rate'] > 0.1
        
    except Exception as e:
        print(f"测试运行失败: {e}")
        return False


if __name__ == "__main__":
    success = run_interface_tests()
    exit(0 if success else 1)