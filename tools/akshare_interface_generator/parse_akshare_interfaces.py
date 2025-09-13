#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析AKShare接口的脚本
直接从akshare库中提取函数签名和参数信息，输出到JSON文件
"""

import akshare as ak
import inspect
import re
import signal
import traceback
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
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


class AKShareInterfaceParser:
    """AKShare接口解析器"""
    
    def __init__(self):
        # 股票代码示例
        self.stock_codes = {
            'em': ['000001', '000002', '600000'],  # 东方财富格式
            'sina': ['sh000001', 'sz000002', 'sh600000'],  # 新浪格式
            'ts': ['000001.SZ', '000002.SZ', '600000.SH'],  # tushare格式
            'default': ['000001', '000002', '600000']
        }
        
        # 日期示例
        today = datetime.now()
        self.dates = {
            'recent': today.strftime('%Y%m%d'),
            'last_month': (today - timedelta(days=30)).strftime('%Y%m%d'),
            'start_of_year': today.strftime('%Y0101'),
            'end_of_year': today.strftime('%Y1231')
        }
        
        # 敏感参数（不生成示例值）
        self.sensitive_params = {'token', 'api_key', 'apikey', 'access_token', 'password'}
        
        # 加载接口分类映射表
        self.category_mapping = self._load_category_mapping()
    
    def discover_akshare_functions(self) -> List[str]:
        """发现所有AKShare函数"""
        functions = []
        for name in dir(ak):
            if not name.startswith('_'):
                obj = getattr(ak, name)
                if callable(obj) and not isinstance(obj, type):
                    # 只保留以stock开头的函数
                    if name.startswith('stock'):
                        functions.append(name)
        return sorted(functions)
    
    def parse_function(self, func_name: str) -> Optional[Dict[str, Any]]:
        """解析单个AKShare函数"""
        try:
            func = getattr(ak, func_name)
            signature = inspect.signature(func)
            doc = inspect.getdoc(func) or ""
            
            # 提取参数信息
            params_info = self._extract_parameters(signature, doc)
            
            # 生成示例参数
            example_params = self._generate_example_params(params_info, func_name)
            
            # 第一步不测试，只解析数据
            test_result = None
            
            # 推断返回类型
            return_type = self._infer_return_type(func_name, doc)
            
            # 生成关键词
            keywords = self._generate_keywords(func_name, doc)
            
            # 确定分类
            category = self._determine_category(func_name, doc)
            
            result = {
                'name': func_name,
                'description': self._extract_description(doc),
                'required_params': params_info['required'],
                'optional_params': params_info['optional'],
                'example_params': example_params,
                'return_type': return_type,
                'keywords': keywords,
                'data_source': self._infer_data_source(func_name, doc),
                'category': category,
                'function_doc': doc,
                'test_result': test_result  # 第一步为None，第二步会填充
            }
            
            return result
            
        except AttributeError:
            print(f"函数 {func_name} 不存在于akshare库中")
            return None
        except Exception as e:
            print(f"分析函数 {func_name} 时出错: {e}")
            return None
    
    def _test_function_call(self, func, func_name: str, example_params: Dict[str, Any]) -> Dict[str, Any]:
        """测试函数调用"""
        test_result = {
            'success': False,
            'error': None,
            'timeout': False,
            'response_type': None,
            'response_shape': None
        }
        
        if not example_params:
            print(f"  ⚠️  {func_name}: 无示例参数，跳过测试")
            test_result['error'] = '无示例参数'
            return test_result
        
        try:
            print(f"  🧪 测试调用 {func_name} 参数: {example_params}")
            
            with timeout(1):  # 1秒超时
                result = func(**example_params)
                
            test_result['success'] = True
            test_result['response_type'] = type(result).__name__
            
            # 获取响应形状信息
            if hasattr(result, 'shape'):
                test_result['response_shape'] = str(result.shape)
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
            print(f"  ❌ {func_name}: 调用失败 ({error_type})")
            print(f"     错误详情: {e}")
            print(f"     参数: {example_params}")
            
            # 打印详细的错误堆栈（仅前几行）
            tb_lines = traceback.format_exc().split('\n')
            relevant_lines = [line for line in tb_lines if func_name in line or 'akshare' in line.lower()]
            if relevant_lines:
                print(f"     相关堆栈: {relevant_lines[-1] if relevant_lines else tb_lines[-2]}")
        
        return test_result
    
    def _extract_parameters(self, signature: inspect.Signature, doc: str) -> Dict[str, List[Dict[str, Any]]]:
        """从函数签名和文档中提取参数信息"""
        required = []
        optional = []
        
        for param_name, param in signature.parameters.items():
            # 跳过 *args 和 **kwargs
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            
            # 获取参数类型
            param_type = self._get_param_type(param)
            
            # 从文档中提取参数描述
            param_desc = self._extract_param_description(param_name, doc)
            
            # 从文档中提取选择项
            choices = self._extract_param_choices(param_name, doc)
            
            param_info = {
                'name': param_name,
                'type': param_type,
                'description': param_desc,
                'choices': choices,
                'default': str(param.default) if param.default != inspect.Parameter.empty else None
            }
            
            # 判断是必需参数还是可选参数
            if param.default == inspect.Parameter.empty:
                required.append(param_info)
            else:
                optional.append(param_info)
        
        return {
            'required': required,
            'optional': optional
        }
    
    def _get_param_type(self, param: inspect.Parameter) -> str:
        """获取参数类型"""
        if param.annotation != inspect.Parameter.empty:
            if hasattr(param.annotation, '__name__'):
                return param.annotation.__name__
            else:
                return str(param.annotation)
        else:
            # 根据参数名推断类型
            param_name = param.name.lower()
            if any(keyword in param_name for keyword in ['date', 'time']):
                return 'str'
            elif any(keyword in param_name for keyword in ['count', 'num', 'size', 'limit']):
                return 'int'
            elif any(keyword in param_name for keyword in ['rate', 'price', 'amount']):
                return 'float'
            else:
                return 'str'  # 默认字符串类型
    
    def _extract_param_description(self, param_name: str, doc: str) -> str:
        """从文档中提取参数描述"""
        if not doc:
            return ""
        
        # 查找 :param param_name: 格式的描述
        pattern = r':param\s+' + re.escape(param_name) + r':\s*([^:]+?)(?=\n\s*:|\n\s*$|\n\s*\w)'
        match = re.search(pattern, doc, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        return ""
    
    def _extract_param_choices(self, param_name: str, doc: str) -> Optional[List[str]]:
        """从文档中提取参数选择项"""
        if not doc:
            return None
        
        # 查找 choice of {...} 格式的选择项
        pattern = r':param\s+' + re.escape(param_name) + r':[^;]*choice\s+of\s*\{([^}]+)\}'
        match = re.search(pattern, doc)
        if match:
            choices_str = match.group(1)
            # 解析选择项，处理引号
            choices = []
            for item in choices_str.split(','):
                item = item.strip().strip('"').strip("'")
                if item:
                    choices.append(item)
            return choices if choices else None
        
        return None
    
    def _generate_example_params(self, params_info: Dict[str, List[Dict[str, Any]]], func_name: str) -> Dict[str, Any]:
        """生成示例参数"""
        example_params = {}
        
        # 处理必需参数
        for param in params_info['required']:
            if param['name'].lower() not in self.sensitive_params:
                example_value = self._generate_example_value(param, func_name)
                if example_value is not None:
                    example_params[param['name']] = example_value
        
        # 处理可选参数：优先处理有默认值的参数，其次处理重要参数
        for param in params_info['optional']:
            if param['name'].lower() not in self.sensitive_params:
                # 如果参数有默认值，直接使用默认值
                if param.get('default') is not None and param.get('default') != 'None':
                    example_value = self._generate_example_value(param, func_name)
                    if example_value is not None:
                        example_params[param['name']] = example_value
                # 如果没有默认值，只处理重要的可选参数
                else:
                    important_optional = ['symbol', 'date', 'start_date', 'end_date', 'period', 'adjust']
                    if param['name'].lower() in important_optional:
                        example_value = self._generate_example_value(param, func_name)
                        if example_value is not None:
                            example_params[param['name']] = example_value
        
        return example_params
    
    def _generate_example_value(self, param: Dict[str, Any], func_name: str) -> Any:
        """为单个参数生成示例值"""
        param_name = param['name'].lower()
        param_type = param['type']
        choices = param.get('choices')
        default_value = param.get('default')
        param_desc = param.get('description', '')
        
        # 1. 严格禁止参数猜测 - 所有参数必须有明确来源
        # 2. 参数优先级明确 - 默认值 > 文档信息 > 重要参数列表
        
        # 优先级1: 使用函数签名中的默认值（如果不是None且不是'None'字符串）
        if default_value is not None and default_value != 'None':
            # 尝试转换default值到合适的类型
            try:
                if param_type == 'int':
                    return int(default_value)
                elif param_type == 'float':
                    return float(default_value)
                elif param_type == 'bool':
                    return default_value.lower() in ('true', '1', 'yes') if isinstance(default_value, str) else bool(default_value)
                else:
                    return str(default_value)
            except (ValueError, TypeError):
                # 如果转换失败，继续使用其他逻辑
                pass
        
        # 优先级2: 如果有选择项，使用第一个
        if choices:
            return choices[0]
        
        # 优先级3: 从参数描述中提取示例值
        # 查找URL中的示例值，如 https://example.com/xxx?symbol=sh600519
        if param_desc:
            # 尝试从URL中提取参数值
            url_pattern = r'https?://[^\s]+[?&]' + re.escape(param_name) + r'=([^&\s#]+)'
            url_match = re.search(url_pattern, param_desc)
            if url_match:
                return url_match.group(1)
            
            # 尝试从描述中提取示例值格式如 "例如: sh600519" 或 "示例: sh600519"
            example_pattern = r'[例示](?:如|例)[：:](\s*)([^\s,;，；]+)'
            example_match = re.search(example_pattern, param_desc)
            if example_match:
                return example_match.group(2)
        
        # 优先级4: 对于少数关键参数，如果没有其他来源，使用预定义的重要参数列表
        important_params = ['symbol', 'date', 'start_date', 'end_date', 'period', 'adjust']
        if param_name in important_params:
            if param_name == 'symbol':
                return self._get_stock_code_example(func_name)
            elif param_name in ['date', 'start_date']:
                return '20240101'
            elif param_name == 'end_date':
                return '20241231'
            elif param_name == 'period':
                return 'daily'
            elif param_name == 'adjust':
                return 'qfq'
        
        # 如果没有任何明确来源，返回None
        return None
    
    def _get_stock_code_example(self, func_name: str) -> str:
        """根据函数名推断股票代码格式"""
        func_lower = func_name.lower()
        if 'em' in func_lower or '东方财富' in func_lower:
            return self.stock_codes['em'][0]
        elif 'sina' in func_lower or '新浪' in func_lower:
            return self.stock_codes['sina'][0]
        elif 'ts' in func_lower or 'tushare' in func_lower:
            return self.stock_codes['ts'][0]
        else:
            return self.stock_codes['default'][0]
    
    def _infer_return_type(self, func_name: str, doc: str) -> str:
        """推断返回类型"""
        func_lower = func_name.lower()
        doc_lower = doc.lower()
        
        if any(keyword in func_lower for keyword in ['list', 'names', 'codes']):
            return 'List[str]'
        elif any(keyword in func_lower for keyword in ['count', 'num', 'total']):
            return 'int'
        elif any(keyword in doc_lower for keyword in ['列表', '清单', '名单']):
            return 'List[str]'
        elif any(keyword in doc_lower for keyword in ['数量', '总数', '计数']):
            return 'int'
        else:
            return 'DataFrame'
    
    def _generate_keywords(self, func_name: str, doc: str) -> List[str]:
        """生成关键词"""
        keywords = set()
        
        # 从函数名提取关键词
        name_parts = func_name.replace('_', ' ').split()
        keywords.update(name_parts)
        
        # 从描述提取关键词
        if doc:
            chinese_keywords = ['股票', 'A股', 'B股', '指数', '基金', '债券', '期货', '新闻', '财务', '行业']
            for keyword in chinese_keywords:
                if keyword in doc:
                    keywords.add(keyword)
        
        return list(keywords)[:10]
    
    def _extract_description(self, doc: str) -> str:
        """从文档中提取描述"""
        if not doc:
            return ""
        
        # 提取第一行作为描述
        lines = doc.strip().split('\n')
        first_line = lines[0].strip()
        
        # 移除常见的文档格式标记
        first_line = re.sub(r'^[:\s]*', '', first_line)
        
        return first_line[:100]  # 限制长度
    
    def _infer_data_source(self, func_name: str, doc: str) -> str:
        """推断数据源"""
        func_lower = func_name.lower()
        doc_lower = doc.lower()
        
        if 'em' in func_lower or '东方财富' in doc_lower:
            return '东方财富网'
        elif 'sina' in func_lower or '新浪' in doc_lower:
            return '新浪财经'
        elif 'tx' in func_lower or '腾讯' in doc_lower:
            return '腾讯财经'
        elif 'ths' in func_lower or '同花顺' in doc_lower:
            return '同花顺'
        else:
            return '未明确说明'
    
    def _load_category_mapping(self) -> Dict[str, str]:
        """加载接口分类映射表"""
        import os
        
        # 获取映射文件路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        mapping_file = os.path.join(current_dir, 'interface_category_mapping.json')
        
        try:
            with open(mapping_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('interface_category_mapping', {})
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"警告: 无法加载分类映射文件 {mapping_file}: {e}")
            return {}
    
    def _determine_category(self, func_name: str, doc: str) -> str:
        """确定接口分类"""
        # 优先从映射表中查找
        if func_name in self.category_mapping:
            return self.category_mapping[func_name]
        
        # 如果映射表中没有找到，使用原有的关键词匹配逻辑
        name = func_name.lower()
        description = doc.lower()
        
        # 技术指标（优先匹配，避免落入行情）
        technical_keywords = [
            'technical', 'indicator', 'macd', 'rsi', 'kdj', 'boll', 'ema', 'dma', 'sar', 'cci', 'wr', 'atr'
        ]
        if any(keyword in name for keyword in technical_keywords):
            return 'STOCK_TECHNICAL'
        
        # 股票财务数据
        if any(keyword in name for keyword in ['financial', 'balance', 'profit', 'cash_flow', 'fina', 'income']):
            return 'STOCK_FINANCIAL'
        
        # 股票行情数据
        elif any(keyword in name for keyword in ['daily', 'hist', 'minute', 'spot', 'real_time', 'kline']):
            return 'STOCK_QUOTE'
        
        # 股票基础信息
        elif any(keyword in name for keyword in ['stock_info', 'stock_basic', 'stock_list', 'info_']):
            return 'STOCK_BASIC'
        
        # 市场指数
        elif any(keyword in name for keyword in ['index_', 'stock_index']):
            return 'MARKET_INDEX'
        
        # 市场概览/总体
        elif any(keyword in name for keyword in ['market_overview', 'market_summary', 'overview']) or \
             any(kw in description for kw in ['市场概览', '市场总览', '全市场', '市场热度']):
            return 'MARKET_OVERVIEW'
        
        # 宏观经济
        elif any(keyword in name for keyword in ['macro_', 'macro', 'economy', 'gdp', 'cpi', 'ppi']) or \
             ('宏观' in description):
            return 'MACRO_ECONOMY'
        
        # 基金数据
        elif any(keyword in name for keyword in ['fund_', 'etf_']):
            return 'FUND_DATA'
        
        # 债券数据
        elif any(keyword in name for keyword in ['bond_', 'convertible_']):
            return 'BOND_DATA'
        
        # 外汇数据
        elif any(keyword in name for keyword in ['forex_', 'currency_', 'fx_', 'exchange_rate']):
            return 'FOREX_DATA'
        
        # 期货数据
        elif any(keyword in name for keyword in ['futures_', 'option_', 'fut_']):
            return 'FUTURES_DATA'
        
        # 行业/资讯/报告
        elif any(keyword in name for keyword in ['news_', 'report_', 'industry_']):
            return 'INDUSTRY_DATA'
        
        else:
            return 'OTHER'
    
    def parse_all_interfaces(self, output_file: str, max_interfaces: Optional[int] = None) -> Dict[str, Any]:
        """解析所有接口并保存到JSON文件"""
        print("发现AKShare函数...")
        functions = self.discover_akshare_functions()
        
        if max_interfaces:
            functions = functions[:max_interfaces]
        
        print(f"找到 {len(functions)} 个函数，开始解析...")
        
        # 解析所有函数
        interfaces = []
        for i, func_name in enumerate(functions, 1):
            print(f"解析 {i}/{len(functions)}: {func_name}")
            interface_info = self.parse_function(func_name)
            if interface_info:
                interfaces.append(interface_info)
        
        print(f"成功解析 {len(interfaces)} 个接口")
        
        # 第一步不进行测试，只统计基本信息
        basic_stats = {
            'total': len(interfaces),
            'with_params': sum(1 for i in interfaces if i.get('example_params')),
            'without_params': sum(1 for i in interfaces if not i.get('example_params'))
        }
        
        # 准备输出数据
        output_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_functions': len(functions),
                'parsed_interfaces': len(interfaces),
                'basic_stats': basic_stats
            },
            'interfaces': interfaces
        }
        
        # 保存到JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        # 打印统计信息
        print(f"\n" + "="*60)
        print(f"解析完成！")
        print(f"总共解析 {len(interfaces)} 个接口")
        print(f"\n📊 解析统计:")
        print(f"  📋 总接口数: {basic_stats['total']} 个")
        print(f"  ✅ 有参数: {basic_stats['with_params']} 个")
        print(f"  ⚠️  无参数: {basic_stats['without_params']} 个")
        
        # 按分类统计
        category_stats = {}
        for interface in interfaces:
            category = interface.get('category', 'OTHER')
            category_stats[category] = category_stats.get(category, 0) + 1
        
        print(f"\n📈 分类分布:")
        for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
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
        
        print(f"\n📁 解析结果已保存到: {output_file}")
        print(f"💡 下一步: 运行 generate_interfaces_from_json.py 来测试和生成接口代码")
        print("="*60)
        
        return output_data


def main():
    """主函数"""
    import os
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'akshare_interfaces.json')
    
    print("开始解析AKShare接口...")
    
    # 创建解析器
    parser = AKShareInterfaceParser()
    
    # 解析所有接口
    result = parser.parse_all_interfaces(output_file)
    
    print(f"\n解析完成！可以手动编辑 {output_file} 文件来修正失败的接口")
    print("然后运行 generate_interfaces_from_json.py 来生成接口代码")


if __name__ == '__main__':
    main()