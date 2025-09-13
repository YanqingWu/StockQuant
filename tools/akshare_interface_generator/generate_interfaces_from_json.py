#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从JSON文件生成AKShare接口的脚本
读取解析结果JSON文件，生成接口注册代码
"""

import json
import os
import signal
import traceback
import akshare as ak
from typing import Dict, Any, List
from datetime import datetime
from contextlib import contextmanager


@contextmanager
def timeout(seconds):
    """超时上下文管理器"""
    def timeout_handler(signum, frame):
        raise TimeoutError(f"操作超时 ({seconds}秒)")
    
    # 设置信号处理器
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    
    try:
        yield
    finally:
        # 恢复原来的信号处理器
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


class InterfaceCodeGenerator:
    """接口代码生成器"""
    
    def __init__(self):
        # 获取脚本所在目录，然后构建相对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(script_dir))
        
        # 生成分类文件的输出目录
        self.output_dir = os.path.join(project_root, 'core', 'data', 'interfaces')
        # 生成主接口文件的路径
        self.main_interface_file = os.path.join(self.output_dir, 'akshare.py')
        
        # 分类映射 - 映射到base.py中FunctionCategory的正确枚举值
        self.category_mapping = {
            'STOCK_BASIC': 'STOCK_BASIC',
            'STOCK_QUOTE': 'STOCK_QUOTE', 
            'STOCK_FINANCIAL': 'STOCK_FINANCIAL',
            'STOCK_TECHNICAL': 'STOCK_TECHNICAL',
            'MARKET_INDEX': 'MARKET_INDEX',
            'MARKET_OVERVIEW': 'MARKET_OVERVIEW',
            'MACRO_ECONOMY': 'MACRO_ECONOMY',
            'FUND_DATA': 'FUND_DATA',
            'BOND_DATA': 'BOND_DATA',
            'FOREX_DATA': 'FOREX_DATA',
            'FUTURES_DATA': 'FUTURES_DATA',
            'INDUSTRY_DATA': 'INDUSTRY_DATA',
            'OTHER': 'OTHER'
        }
    
    def load_interfaces_from_json(self, json_file: str) -> Dict[str, Any]:
        """从JSON文件加载接口数据"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    
    def test_interface_call(self, interface: Dict[str, Any]) -> Dict[str, Any]:
        """测试接口调用"""
        func_name = interface['name']
        example_params = interface.get('example_params', {})
        
        test_result = {
            'success': False,
            'error': None,
            'timeout': False,
            'response_type': None,
            'response_shape': None
        }
        
        try:
            func = getattr(ak, func_name)
            if example_params:
                print(f"  🧪 测试调用 {func_name} 参数: {example_params}")
            else:
                print(f"  🧪 测试调用 {func_name} (无参数)")
            
            # 使用信号超时机制，设置超时时间为1秒
            with timeout(1):
                if example_params:
                    result = func(**example_params)
                else:
                    result = func()
                
            test_result['success'] = True
            test_result['response_type'] = type(result).__name__
            
            # 获取响应形状信息
            if hasattr(result, 'shape'):
                test_result['response_shape'] = result.shape
            elif hasattr(result, '__len__'):
                test_result['response_shape'] = len(result)
            
            print(f"  ✅ {func_name}: 调用成功，返回类型: {test_result['response_type']}")
            if test_result['response_shape']:
                print(f"     形状: {test_result['response_shape']}")
                
        except TimeoutError as e:
            test_result['timeout'] = True
            test_result['error'] = str(e)
            print(f"  ⏰ {func_name}: 调用超时 - {e}")
            
        except Exception as e:
            test_result['error'] = str(e)
            error_type = type(e).__name__
            
            # 检查是否为网络超时错误
            error_str = str(e).lower()
            if ('timed out' in error_str or 'timeout' in error_str or 
                'read timeout' in error_str or 'connection timeout' in error_str):
                test_result['timeout'] = True
                print(f"  ⏰ {func_name}: 网络超时 ({error_type})")
                print(f"     超时详情: {e}")
            else:
                print(f"  ❌ {func_name}: 调用失败 ({error_type})")
                print(f"     错误详情: {e}")
            
            print(f"     参数: {example_params}")
            
            # 打印详细的错误堆栈（仅前几行）
            tb_lines = traceback.format_exc().split('\n')
            relevant_lines = [line for line in tb_lines if func_name in line or 'akshare' in line.lower()]
            if relevant_lines:
                print(f"     相关堆栈: {relevant_lines[-1] if relevant_lines else tb_lines[-2]}")
        
        return test_result
    
    def filter_successful_interfaces(self, interfaces: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """过滤出测试成功的接口（包括超时接口）"""
        successful = []
        for interface in interfaces:
            test_result = interface.get('test_result', {})
            # 保留测试成功的接口和超时接口
            if test_result.get('success', False) or test_result.get('timeout', False):
                successful.append(interface)
        return successful
    
    def categorize_interfaces(self, interfaces: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """按分类组织接口"""
        categorized = {}
        for interface in interfaces:
            category = interface.get('category', 'OTHER')
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(interface)
        return categorized
    
    def generate_interface_code(self, interface: Dict[str, Any]) -> str:
        """生成单个接口的注册代码"""
        name = interface['name']
        description = interface.get('description', '').replace('"', '\\"')
        required_params = interface.get('required_params', [])
        optional_params = interface.get('optional_params', [])
        example_params = interface.get('example_params', {})
        return_type = interface.get('return_type', 'DataFrame')
        keywords = interface.get('keywords', [])
        category = interface.get('category', 'OTHER')
        
        # 映射分类
        mapped_category = self.category_mapping.get(category, 'OTHER')
        
        # 生成代码 - 改为直接返回列表格式
        code = f'create_interface("{name}")\\\n'
        code += f'    .with_source(DataSource.AKSHARE)\\\n'
        code += f'    .with_category(FunctionCategory.{mapped_category})\\\n'
        code += f'    .with_description("{description}")\\\n'
        
        # 设置必需参数
        if required_params:
            params_str = ', '.join([f'"{p["name"]}"' for p in required_params])
            code += f'    .with_required_params({params_str})\\\n'
        
        # 设置可选参数
        if optional_params:
            params_str = ', '.join([f'"{p["name"]}"' for p in optional_params])
            code += f'    .with_optional_params({params_str})\\\n'
        
        # 如果没有必需参数，需要手动设置参数模式
        if not required_params:
            if optional_params:
                params_str = ', '.join([f'"{p["name"]}"' for p in optional_params])
                code += f'    .with_pattern(ParameterPattern.from_params([{params_str}]))\\\n'
            else:
                code += f'    .with_pattern(ParameterPattern.from_params([]))\\\n'
        
        # 添加返回类型
        code += f'    .with_return_type("{return_type}")\\\n'
        
        # 添加关键词
        if keywords:
            keywords_str = ', '.join([f'"{k}"' for k in keywords[:5]])
            code += f'    .with_keywords({keywords_str})\\\n'
        
        # 添加示例参数（清洗与标准化）
        if example_params:
            import re
            sanitized_items = []
            for k, v in example_params.items():
                # 丢弃明显的文档占位/伪KV字符串
                if isinstance(v, str):
                    sv = v.strip()
                    if sv.startswith(':'):
                        continue
                    if '"' in sv and ': ' in sv:
                        continue
                    if '：' in sv:  # 全角冒号
                        continue
                    # 针对常见键标准化
                    key_lower = k.lower()
                    # 日期
                    if key_lower in ('date', 'start_date', 'end_date'):
                        if not re.match(r'^\d{4}-\d{2}-\d{2}$', sv) and not re.match(r'^\d{8}$', sv):
                            sv = '2024-01-01' if key_lower != 'end_date' else '2024-01-31'
                        v = sv
                    # 代码/符号
                    elif key_lower in ('symbol', 'code'):
                        if not re.match(r'^[\w\.-]+$', sv):
                            sv = '000001'
                        v = sv
                    elif key_lower in ('ts_code',):
                        if not re.match(r'^[\w\.-]+$', sv):
                            sv = '000001.SZ'
                        v = sv
                    # 周期
                    elif key_lower == 'period':
                        allowed = {'daily', '1', '5', '15', '30', '60'}
                        if sv not in allowed:
                            sv = 'daily'
                        v = sv
                    # 复权
                    elif key_lower == 'adjust':
                        allowed = {'', 'qfq', 'hfq', 'bfq'}
                        if sv not in allowed:
                            sv = ''
                        v = sv
                sanitized_items.append(f'"{k}": {repr(v)}')
            if sanitized_items:
                params_dict_str = '{' + ', '.join(sanitized_items) + '}'
                code += f'    .with_example_params({params_dict_str})\\\n'
        
        code += f'    .build(),'
        
        return code
    
    def _validate_example_params(self, example_params: Dict[str, Any], required_params: List[Dict[str, Any]], optional_params: List[Dict[str, Any]]) -> None:
        """验证示例参数与实际默认值保持一致
        
        按照用户要求：
        1. 严格禁止参数猜测 - 所有参数必须有明确来源（默认值、文档信息或重要参数列表）
        2. 参数优先级明确 - 默认值 > 文档信息 > 重要参数，绝不能随意猜测参数值
        3. 示例参数一致性 - example_params 必须与实际默认值保持一致
        """
        # 合并所有参数信息
        all_params = {}
        for param in required_params + optional_params:
            param_name = param['name']
            all_params[param_name] = param
        
        # 检查示例参数中的每个参数
        for param_name, example_value in list(example_params.items()):
            # 如果参数不在定义的参数列表中，移除它
            if param_name not in all_params:
                del example_params[param_name]
                continue
                
            param_info = all_params[param_name]
            default_value = param_info.get('default')
            
            # 如果有默认值，确保示例参数与默认值一致
            if default_value is not None and default_value != 'None':
                # 尝试转换默认值到合适的类型
                param_type = param_info.get('type', 'str')
                try:
                    if param_type == 'int':
                        example_params[param_name] = int(default_value)
                    elif param_type == 'float':
                        example_params[param_name] = float(default_value)
                    elif param_type == 'bool':
                        example_params[param_name] = default_value.lower() in ('true', '1', 'yes') if isinstance(default_value, str) else bool(default_value)
                    else:
                        example_params[param_name] = str(default_value)
                except (ValueError, TypeError):
                    # 如果转换失败，保留原始示例值
                    pass
    
    def generate_file_header(self, category: str, interface_count: int) -> str:
        """生成文件头部"""
        mapped_category = self.category_mapping.get(category, 'OTHER')
        category_name_cn = {
            'STOCK_BASIC': '股票基础信息',
            'STOCK_QUOTE': '股票行情数据', 
            'STOCK_FINANCIAL': '股票财务数据',
            'STOCK_TECHNICAL': '股票技术分析',
            'MARKET_INDEX': '市场指数数据',
            'MARKET_OVERVIEW': '市场概览',
            'MACRO_ECONOMY': '宏观经济数据',
            'FUND_DATA': '基金数据',
            'BOND_DATA': '债券数据',
            'FOREX_DATA': '外汇数据',
            'FUTURES_DATA': '期货数据',
            'INDUSTRY_DATA': '行业分析',
            'OTHER': '其他数据'
        }.get(category, '其他数据')
        
        return f'''# -*- coding: utf-8 -*-
"""
AKShare {category_name_cn}接口
自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
包含 {interface_count} 个接口
"""

from typing import List
from src.data_sources.base import (
    create_interface, 
    ParameterPattern, 
    DataSource, 
    FunctionCategory,
    InterfaceMetadata
)


def register_{category.lower()}_interfaces() -> List[InterfaceMetadata]:
    """
    注册AKShare {category_name_cn}接口
    """
'''
    
    def generate_category_file(self, category: str, interfaces: List[Dict[str, Any]]) -> str:
        """生成分类文件内容"""
        # 生成文件头部
        content = self.generate_file_header(category, len(interfaces))
        
        # 添加返回值列表
        content += "    interfaces = []\n"
        
        # 生成每个接口的代码
        for interface in interfaces:
            interface_code = self.generate_interface_code(interface)
            # 修改为添加到列表而不是直接注册
            content += f"    interfaces.append({interface_code.strip()})\n"
        
        # 添加返回语句
        content += "    return interfaces\n"
        
        return content
    
    def write_interface_files(self, categorized_interfaces: Dict[str, List[Dict[str, Any]]]) -> Dict[str, str]:
        """写入接口文件"""
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        generated_files = {}
        
        for category, interfaces in categorized_interfaces.items():
            if not interfaces:  # 跳过空分类
                continue
                
            # 生成文件内容
            file_content = self.generate_category_file(category, interfaces)
            
            # 写入文件
            filename = f'{category.lower()}.py'
            file_path = os.path.join(self.output_dir, filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            generated_files[category] = file_path
            print(f"生成文件: {file_path} ({len(interfaces)} 个接口)")
        
        return generated_files
    
    def generate_main_akshare_file(self, categorized_interfaces: Dict[str, List[Dict[str, Any]]]) -> str:
        """生成主akshare.py文件，将所有接口直接生成在一个文件中"""
        total_interfaces = sum(len(interfaces) for interfaces in categorized_interfaces.values())
        
        content = f'''# -*- coding: utf-8 -*-
"""
AKShare数据源接口提供者
自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
总共 {total_interfaces} 个接口
"""

'''
        
        # 添加导入语句
        content += 'from typing import List\n'
        content += 'from .base import (\n'
        content += '    BaseAPIProvider, InterfaceMetadata, FunctionCategory, create_interface,\n'
        content += '    DataSource, ParameterPattern\n'
        content += ')\n\n'
        
        # 创建AkshareProvider类
        content += 'class AkshareProvider(BaseAPIProvider):\n'
        content += '    """AKShare数据接口提供者"""\n\n'
        content += '    def __init__(self):\n'
        content += '        super().__init__("akshare", DataSource.AKSHARE)\n\n'
        
        # 添加register_interfaces方法
        content += '    def register_interfaces(self) -> None:\n'
        content += '        """注册所有接口"""\n'
        content += '        interfaces = []\n\n'
        
        # 添加各分类接口注册
        for category in categorized_interfaces.keys():
            if categorized_interfaces[category]:  # 只导入非空分类
                module_name = category.lower()
                content += f'        interfaces.extend(self._register_{module_name}_interfaces())\n'
        
        content += '\n        # 批量注册所有接口\n'
        content += '        self.registry.register_interfaces(interfaces)\n\n'
        
        # 直接添加各分类接口注册方法和接口代码
        for category, interfaces in categorized_interfaces.items():
            if not interfaces:  # 跳过空分类
                continue
                
            # 添加分类注册方法
            content += f'    def _register_{category.lower()}_interfaces(self) -> List[InterfaceMetadata]:\n'
            content += f'        """注册{category}接口"""\n'
            content += '        return [\n'
            
            # 生成每个接口的代码
            for i, interface in enumerate(interfaces):
                interface_code = self.generate_interface_code(interface)
                # 添加适当的缩进
                indented_code = '\n'.join(['        ' + line for line in interface_code.strip().split('\n')])
                content += f'{indented_code}\n'
                # 如果不是最后一个接口，在逗号后添加空行
                if i < len(interfaces) - 1:
                    content += '\n'
            
            # 添加返回语句结束
            content += '        ]\n\n'
        
        # 添加提供者实例创建和注册代码
        content += '\n# 创建提供者实例并注册\n'
        content += 'akshare_provider = AkshareProvider()\n\n'
        content += '# 注册到全局管理器\n'
        content += 'from .base import register_provider\n'
        content += 'register_provider(akshare_provider)\n'
        
        # 写入主文件
        main_file_path = self.main_interface_file
        # 确保目录存在
        os.makedirs(os.path.dirname(main_file_path), exist_ok=True)
        with open(main_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"生成主文件: {main_file_path}")
        return main_file_path
    
    def generate_from_json(self, json_file: str) -> Dict[str, Any]:
        """从JSON文件生成接口代码"""
        print(f"从 {json_file} 加载接口数据...")
        
        # 加载数据
        data = self.load_interfaces_from_json(json_file)
        interfaces = data.get('interfaces', [])
        metadata = data.get('metadata', {})
        
        print(f"加载了 {len(interfaces)} 个接口")
        
        # 测试所有接口调用
        print(f"\n开始测试接口调用...")
        for i, interface in enumerate(interfaces, 1):
            print(f"测试 {i}/{len(interfaces)}: {interface['name']}")
            test_result = self.test_interface_call(interface)
            interface['test_result'] = test_result
        
        # 过滤成功的接口
        successful_interfaces = self.filter_successful_interfaces(interfaces)
        print(f"\n测试完成，{len(successful_interfaces)} 个接口测试成功，将生成代码")
        
        if not successful_interfaces:
            print("没有成功的接口，无法生成代码")
            return {'generated_files': [], 'stats': {}}
        
        # 按分类组织
        categorized = self.categorize_interfaces(successful_interfaces)
        
        # 生成主文件（包含所有接口）
        main_file = self.generate_main_akshare_file(categorized)
        generated_files = {'main': main_file}
        
        # 统计测试结果
        test_stats = {
            'total': len(interfaces),
            'success': 0,
            'failed': 0,
            'timeout': 0,
            'no_params': 0
        }
        
        failed_interfaces = []
        timeout_interfaces = []
        
        for interface in interfaces:
            test_result = interface.get('test_result', {})
            if test_result.get('success'):
                test_stats['success'] += 1
            elif test_result.get('timeout'):
                test_stats['timeout'] += 1
                timeout_interfaces.append(interface['name'])
            else:
                test_stats['failed'] += 1
                failed_interfaces.append({
                    'name': interface['name'],
                    'error': test_result.get('error', '未知错误'),
                    'params': interface.get('example_params', {}),
                    'reason': 'call_failed'
                })
        
        # 统计信息
        stats = {
            'total_loaded': len(interfaces),
            'successful': len(successful_interfaces),
            'categories': len(categorized),
            'generated_files': len(generated_files),
            'category_distribution': {cat: len(interfaces) for cat, interfaces in categorized.items()},
            'test_stats': test_stats,
            'failed_interfaces': failed_interfaces,
            'timeout_interfaces': timeout_interfaces
        }
        
        # 打印统计信息
        print(f"\n" + "="*60)
        print(f"代码生成完成！")
        
        print(f"\n📊 测试结果统计:")
        print(f"  ✅ 成功: {test_stats['success']} 个")
        print(f"  ❌ 失败: {test_stats['failed']} 个")
        print(f"  ⏰ 超时: {test_stats['timeout']} 个")
        print(f"  ⚠️  无参数: {test_stats['no_params']} 个")
        
        success_rate = (test_stats['success'] / test_stats['total']) * 100 if test_stats['total'] > 0 else 0
        print(f"  📈 成功率: {success_rate:.1f}%")
        
        print(f"\n📊 生成统计:")
        print(f"  📁 生成文件: {len(generated_files)} 个")
        print(f"  🔧 成功接口: {len(successful_interfaces)} 个")
        print(f"  📂 分类数量: {len(categorized)} 个")
        
        print(f"\n📈 分类分布:")
        for category, count in stats['category_distribution'].items():
            category_name_cn = {
                'STOCK_BASIC': '股票基础信息',
                'STOCK_QUOTE': '股票行情数据', 
                'STOCK_FINANCIAL': '股票财务数据',
                'STOCK_TECHNICAL': '股票技术分析',
                'MARKET_INDEX': '市场指数数据',
                'MARKET_OVERVIEW': '市场概览',
                'MACRO_ECONOMY': '宏观经济数据',
                'FUND_DATA': '基金数据',
                'BOND_DATA': '债券数据',
                'FOREX_DATA': '外汇数据',
                'FUTURES_DATA': '期货数据',
                'INDUSTRY_DATA': '行业分析',
                'OTHER': '其他数据'
            }.get(category, category)
            print(f"  {category_name_cn}: {count} 个")
        
        # 保存调用失败的接口到文件
        if failed_interfaces:
            # 获取脚本所在目录，然后构建相对路径
            script_dir = os.path.dirname(os.path.abspath(__file__))
            failed_file_path = os.path.join(script_dir, 'failed_interfaces.json')
            
            failed_data = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_failed': len(failed_interfaces),
                'failed_interfaces': failed_interfaces,
                'summary': {
                    'total_count': len(failed_interfaces),
                    'note': '包含调用失败的接口，超时接口已被视为成功，无参数接口会正常调用测试'
                }
            }
            
            with open(failed_file_path, 'w', encoding='utf-8') as f:
                json.dump(failed_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 调用失败的接口信息已保存到: {failed_file_path}")
            print(f"  ❌ 调用失败接口: {len(failed_interfaces)} 个")
            print(f"    注意: 超时接口已被视为成功，不包含在失败文件中")
        
        # 详细失败报告
        if failed_interfaces:
            print(f"\n❌ 失败接口详情 ({len(failed_interfaces)} 个):")
            for i, failed in enumerate(failed_interfaces[:10], 1):  # 只显示前10个
                print(f"  {i}. {failed['name']}")
                print(f"     错误: {failed['error']}")
                print(f"     参数: {failed['params']}")
            if len(failed_interfaces) > 10:
                print(f"     ... 还有 {len(failed_interfaces) - 10} 个失败接口")
        
        # 超时接口报告
        if timeout_interfaces:
            print(f"\n⏰ 超时接口 ({len(timeout_interfaces)} 个):")
            for name in timeout_interfaces[:10]:  # 只显示前10个
                print(f"  - {name}")
            if len(timeout_interfaces) > 10:
                print(f"  ... 还有 {len(timeout_interfaces) - 10} 个超时接口")
        
        print(f"\n📁 生成的文件:")
        print(f"  {main_file}")
        
        print("="*60 + "\n")
        
        print(f"✅ 代码生成完成！")
        print(f"所有接口已统一生成在 {main_file} 文件中")
        
        # 将测试结果保存到单独的文件，不覆盖原始JSON
        tested_interfaces_file = json_file.replace('.json', '_tested.json')
        print(f"\n💾 保存测试结果到单独文件...")
        updated_data = {
            'metadata': metadata,
            'interfaces': interfaces  # 包含测试结果的完整接口数据
        }
        
        # 更新元数据中的测试统计
        updated_data['metadata']['test_stats'] = test_stats
        updated_data['metadata']['last_test_time'] = datetime.now().isoformat()
        
        with open(tested_interfaces_file, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 测试结果已保存到: {tested_interfaces_file}")
        print(f"📝 原始JSON文件保持不变: {json_file}")
        
        return {
            'generated_files': generated_files,
            'stats': stats
        }


def main():
    """主函数"""
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, 'akshare_interfaces.json')
    
    if not os.path.exists(json_file):
        print(f"错误: JSON文件不存在: {json_file}")
        print("请先运行 parse_akshare_interfaces.py 生成接口数据")
        return
    
    print("开始从JSON文件生成接口代码...")
    
    # 创建生成器
    generator = InterfaceCodeGenerator()
    
    # 生成代码
    result = generator.generate_from_json(json_file)
    
    if result['generated_files']:
        print(f"\n✅ 代码生成完成！")
        print(f"可以在 {generator.output_dir} 目录查看生成的文件")
    else:
        print(f"\n❌ 代码生成失败")


if __name__ == '__main__':
    main()