#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动解析akshare_interfaces.md文档并生成接口注册代码的脚本
增强版：集成智能参数分析功能
"""

import re
import os
from typing import List, Dict, Any, Optional


class ParameterAnalyzer:
    """参数分析器 - 分析参数的类型、约束和生成策略"""
    
    def __init__(self):
        # 股票代码格式映射
        self.stock_code_patterns = {
            'symbol': {
                'em': '000001',  # 东方财富格式
                'sina': 'sh000001',  # 新浪格式
                'tx': 'sh000001',  # 腾讯格式
                'ths': '000001.SZ',  # 同花顺格式
                'default': '000001'
            },
            'ts_code': '000001.SZ',  # tushare格式
            'secucode': '000001.SZ',  # 通用证券代码
            'code': '000001',  # 简单代码
            'stock': '000001'  # 股票代码
        }
        
        # 日期格式映射
        self.date_patterns = {
            'start_date': '20230101',
            'end_date': '20231231',
            'date': '20231201'
        }
        
        # 常用参数默认值
        self.common_defaults = {
            'period': 'daily',
            'adjust': '',
            'timeout': None,
            'market': 'all',
            'exchange': 'SSE',
            'indicator': '按报告期'
        }
    
    def analyze_parameter(self, param_info: Dict[str, Any], interface_name: str) -> Dict[str, Any]:
        """分析单个参数，生成智能参数信息"""
        param_name = param_info['name']
        param_type = param_info['type']
        param_desc = param_info['description']
        choices = param_info.get('choices')
        default = param_info.get('default')
        
        analysis = {
            'name': param_name,
            'type': param_type,
            'description': param_desc,
            'choices': choices,
            'default': default,
            'generation_strategy': self._determine_generation_strategy(param_name, param_type, param_desc, choices, interface_name),
            'test_values': self._generate_test_values(param_name, param_type, param_desc, choices, interface_name)
        }
        
        return analysis
    
    def _determine_generation_strategy(self, param_name: str, param_type: str, param_desc: str, choices: Optional[List[str]], interface_name: str) -> str:
        """确定参数生成策略"""
        param_lower = param_name.lower()
        desc_lower = param_desc.lower()
        interface_lower = interface_name.lower()
        
        # 股票代码相关
        if any(keyword in param_lower for keyword in ['symbol', 'code', 'stock']):
            if 'ts_code' in param_lower:
                return 'ts_code'
            elif 'secucode' in param_lower:
                return 'secucode'
            elif any(source in interface_lower for source in ['em', '东方财富']):
                return 'em_symbol'
            elif any(source in interface_lower for source in ['sina', '新浪']):
                return 'sina_symbol'
            elif any(source in interface_lower for source in ['tx', '腾讯']):
                return 'tx_symbol'
            elif any(source in interface_lower for source in ['ths', '同花顺']):
                return 'ths_symbol'
            else:
                return 'default_symbol'
        
        # 日期相关
        elif any(keyword in param_lower for keyword in ['date', 'time']):
            return 'date_value'
        
        # 有选择项的参数
        elif choices:
            return 'choice_value'
        
        # 数值类型
        elif param_type in ['int', 'float']:
            return 'numeric_value'
        
        # 字符串类型
        elif param_type == 'str':
            return 'string_value'
        
        return 'default_value'
    
    def _generate_test_values(self, param_name: str, param_type: str, param_desc: str, choices: Optional[List[str]], interface_name: str) -> List[Any]:
        """生成测试值列表"""
        strategy = self._determine_generation_strategy(param_name, param_type, param_desc, choices, interface_name)
        param_lower = param_name.lower()
        interface_lower = interface_name.lower()
        
        if strategy == 'ts_code':
            return ['000001.SZ', '000002.SZ', '600000.SH']
        elif strategy == 'secucode':
            return ['000001.SZ', '000002.SZ', '600000.SH']
        elif strategy == 'em_symbol':
            # 东方财富接口的特殊处理
            if 'financial' in interface_lower:
                return ['000001.SZ', '000002.SZ', '600000.SH']
            else:
                return ['000001', '000002', '600000']
        elif strategy == 'sina_symbol':
            return ['sh000001', 'sz000002', 'sh600000']
        elif strategy == 'tx_symbol':
            return ['sh000001', 'sz000002', 'sh600000']
        elif strategy == 'ths_symbol':
            return ['000001.SZ', '000002.SZ', '600000.SH']
        elif strategy == 'default_symbol':
            # 根据接口名称推断格式
            if any(keyword in interface_lower for keyword in ['em', '东方财富']):
                return ['000001', '000002', '600000']
            else:
                return ['000001', 'sh000001', '000001.SZ']
        elif strategy == 'date_value':
            if 'start' in param_lower:
                return ['20230101', '20230301', '20230601']
            elif 'end' in param_lower:
                return ['20231231', '20230331', '20230630']
            else:
                return ['20231201', '20231101', '20231001']
        elif strategy == 'choice_value' and choices:
            return choices[:3] if len(choices) >= 3 else choices
        elif strategy == 'numeric_value':
            if param_type == 'int':
                return [1, 5, 10]
            else:
                return [1.0, 5.0, 10.0]
        elif strategy == 'string_value':
            # 根据参数名称生成合适的字符串值
            if 'market' in param_lower:
                return ['all', 'sh', 'sz']
            elif 'exchange' in param_lower:
                return ['SSE', 'SZSE', 'BSE']
            elif 'period' in param_lower:
                return ['daily', 'weekly', 'monthly']
            elif 'adjust' in param_lower:
                return ['', 'qfq', 'hfq']
            elif 'indicator' in param_lower:
                return ['按报告期', '按单季度', '按年度']
            else:
                return ['test', 'default', 'sample']
        
        return ['default']


class InterfaceParser:
    """接口解析器 - 增强版，集成智能参数分析"""
    
    def __init__(self, md_file_path: str):
        self.md_file_path = md_file_path
        self.interfaces = []
        self.analyzer = ParameterAnalyzer()
        
    def parse_interfaces(self) -> List[Dict[str, Any]]:
        """解析所有接口"""
        with open(self.md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 按接口分割内容
        interface_blocks = re.split(r'\n#### ', content)
        
        for block in interface_blocks[1:]:  # 跳过第一个空块
            interface_info = self._parse_single_interface(block)
            if interface_info:
                self.interfaces.append(interface_info)
                
        return self.interfaces
    
    def _parse_single_interface(self, block: str) -> Dict[str, Any]:
        """解析单个接口 - 增强版，集成智能参数分析"""
        lines = block.strip().split('\n')
        if not lines:
            return None
            
        # 解析接口名称和描述
        first_line = lines[0]
        if ' - ' in first_line:
            interface_name, description = first_line.split(' - ', 1)
        else:
            interface_name = first_line
            description = ""
            
        interface_info = {
            'name': interface_name.strip(),
            'description': description.strip(),
            'data_source': '',
            'function': '',
            'limit': '',
            'input_params': [],
            'return_fields': [],
            'enhanced_input_params': [],  # 新增智能分析结果
            'required_params': [],  # 必需参数
            'optional_params': [],  # 可选参数
            'return_type': 'DataFrame',  # 默认返回类型
            'keywords': [],  # 关键词
            'usage': ''
        }
        
        current_section = None
        
        for line_num, line in enumerate(lines, 1):
            original_line = line
            line = line.strip()
            

            if not line:
                continue
                
            # 识别各个字段
            if line.startswith('- **数据源**:'):
                interface_info['data_source'] = line.replace('- **数据源**:', '').strip()
            elif line.startswith('- **功能**:'):
                interface_info['function'] = line.replace('- **功能**:', '').strip()
            elif line.startswith('- **限量**:'):
                interface_info['limit'] = line.replace('- **限量**:', '').strip()
            elif line.startswith('- **输入参数**:'):
                current_section = 'input_params'

            elif line.startswith('- **返回字段**:'):
                current_section = 'return_fields'

            elif line.startswith('- **用途**:'):
                interface_info['usage'] = line.replace('- **用途**:', '').strip()
                current_section = None

            elif current_section and (line.startswith('  - `') or line.startswith('- `')):
                # 解析参数或字段
                param_match = re.match(r'- `([^`]+)` \(`([^`]+)`\): (.+)', line)
                if param_match:
                    param_name, param_type, param_desc = param_match.groups()
                    
                    # 跳过占位符参数（参数名为'-'的情况）
                    if param_name == '-':
                        continue
                        
                    # 解析参数的可选值
                    choices = None
                    default_value = None
                    
                    # 提取 choice of {...} 格式的可选值
                    choice_match = re.search(r'choice of \{([^}]+)\}', param_desc)
                    if choice_match:
                        choice_str = choice_match.group(1)
                        # 解析选项，处理引号
                        choices = []
                        for item in choice_str.split(','):
                            item = item.strip().strip('"').strip("'")
                            if item:
                                choices.append(item)
                    
                    # 提取默认值
                    default_match = re.search(r'默认[为是]?[：:]?\s*([^;，。]+)', param_desc)
                    if default_match:
                        default_value = default_match.group(1).strip()
                    
                    param_info = {
                        'name': param_name,
                        'type': param_type,
                        'description': param_desc,
                        'choices': choices,
                        'default': default_value
                    }
                    
                    if current_section == 'input_params':
                        interface_info['input_params'].append(param_info)
                        # 使用ParameterAnalyzer进行智能分析
                        enhanced_param = self.analyzer.analyze_parameter(param_info, interface_name)
                        interface_info['enhanced_input_params'].append(enhanced_param)
                        
                        # 区分必需参数和可选参数
                        if param_info.get('default') is not None or '可选' in param_desc or 'optional' in param_desc.lower():
                            interface_info['optional_params'].append(param_name)
                        else:
                            interface_info['required_params'].append(param_name)
                            
                    elif current_section == 'return_fields':
                        interface_info['return_fields'].append(param_info)
        
        # 生成关键词
        interface_info['keywords'] = self._generate_keywords(interface_info)
        
        # 推断返回类型
        interface_info['return_type'] = self._infer_return_type(interface_info)
                         
        return interface_info
    
    def _generate_keywords(self, interface_info: Dict[str, Any]) -> List[str]:
        """生成接口关键词"""
        keywords = set()
        
        # 从接口名称提取关键词
        name_parts = interface_info['name'].replace('_', ' ').split()
        keywords.update(name_parts)
        
        # 从描述提取关键词
        desc = interface_info.get('description', '')
        if desc:
            # 提取中文关键词
            chinese_keywords = ['股票', 'A股', 'B股', '指数', '基金', '债券', '期货', '新闻', '财务', '行业']
            for keyword in chinese_keywords:
                if keyword in desc:
                    keywords.add(keyword)
        
        # 从数据源提取关键词
        data_source = interface_info.get('data_source', '')
        if data_source:
            keywords.add(data_source)
            
        return list(keywords)[:10]  # 限制关键词数量
    
    def _infer_return_type(self, interface_info: Dict[str, Any]) -> str:
        """推断返回类型"""
        name = interface_info['name'].lower()
        desc = interface_info.get('description', '').lower()
        
        # 根据接口名称和描述推断返回类型
        if any(keyword in name for keyword in ['list', 'names', 'codes']):
            return 'List[str]'
        elif any(keyword in name for keyword in ['count', 'num', 'total']):
            return 'int'
        elif any(keyword in desc for keyword in ['列表', '清单', '名单']):
            return 'List[str]'
        elif any(keyword in desc for keyword in ['数量', '总数', '计数']):
            return 'int'
        else:
            return 'DataFrame'  # 默认返回DataFrame
    
    def categorize_interfaces(self) -> Dict[str, List[Dict[str, Any]]]:
        """按功能分类接口（与 FunctionCategory 对齐）"""
        # 使用功能分类作为分组键
        categories: Dict[str, List[Dict[str, Any]]] = {
            'stock_basic': [],
            'stock_quote': [],
            'stock_financial': [],
            'stock_technical': [],
            'market_index': [],
            'market_overview': [],
            'macro_economy': [],
            'industry_data': [],
            'fund_data': [],
            'bond_data': [],
            'forex_data': [],
            'futures_data': [],
            'other': []
        }
        
        # 复用生成器的分类逻辑，确保一致性
        generator = CodeGenerator(self.interfaces)
        for interface in self.interfaces:
            cat = generator._determine_category(interface)
            if cat not in categories:
                cat = 'other'
            categories[cat].append(interface)
        
        return categories
                
        return categories


class CodeGenerator:
    """代码生成器"""
    
    def __init__(self, interfaces: List[Dict[str, Any]]):
        self.interfaces = interfaces
        
    def generate_akshare_provider(self, output_file: str):
        """生成AkshareProvider类代码"""
        parser = InterfaceParser('')
        parser.interfaces = self.interfaces
        categories = parser.categorize_interfaces()
        
        code_lines = [
            '#!/usr/bin/env python3',
            '# -*- coding: utf-8 -*-',
            '"""',
            'AKShare数据接口提供者 - 自动生成',
            '"""',
            '',
            'from typing import List',
            'from .base import (',
            '    BaseAPIProvider, InterfaceMetadata, FunctionCategory, create_interface,',
            '    DataSource, ParameterPattern',
            ')',
            '',
            '',
            'class AkshareProvider(BaseAPIProvider):',
            '    """AKShare数据接口提供者"""',
            '    ',
            '    def __init__(self):',
            '        super().__init__("akshare", DataSource.AKSHARE)',
            '        ',
            '    def register_interfaces(self) -> None:',
            '        """注册所有接口"""',
            '        interfaces = []',
            '        ',
        ]
        
        # 为每个分类生成注册调用
        category_methods = {
            'stock_basic': '_register_stock_basic_interfaces',
            'stock_quote': '_register_stock_quote_interfaces',
            'stock_financial': '_register_stock_financial_interfaces',
            'stock_technical': '_register_stock_technical_interfaces',
            'market_index': '_register_market_index_interfaces',
            'market_overview': '_register_market_overview_interfaces',
            'macro_economy': '_register_macro_economy_interfaces',
            'industry_data': '_register_industry_data_interfaces',
            'fund_data': '_register_fund_data_interfaces',
            'bond_data': '_register_bond_data_interfaces',
            'forex_data': '_register_forex_data_interfaces',
            'futures_data': '_register_futures_data_interfaces',
            'other': '_register_other_interfaces'
        }
        
        for category, method_name in category_methods.items():
            if categories[category]:  # 只有该分类有接口时才添加
                code_lines.append(f'        interfaces.extend(self.{method_name}())')
                
        code_lines.extend([
            '        ',
            '        # 批量注册所有接口',
            '        self.registry.register_interfaces(interfaces)',
            ''
        ])
        
        # 生成各个分类的注册方法
        for category, method_name in category_methods.items():
            if not categories[category]:
                continue
                
            code_lines.extend([
                f'    def {method_name}(self) -> List[InterfaceMetadata]:',
                f'        """注册{self._get_category_name(category)}接口"""',
                '        return ['
            ])
            
            for interface in categories[category]:
                code_lines.append(self._generate_interface_code(interface))
                
            code_lines.extend([
                '        ]',
                ''
            ])
            
        # 创建提供者实例
        code_lines.extend([
            '',
            '# 创建提供者实例',
            'akshare_provider = AkshareProvider()'
        ])
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(code_lines))
            
    def _get_category_name(self, category: str) -> str:
        """获取分类中文名称（与 FunctionCategory 对齐）"""
        names = {
            'stock_basic': '股票基础',
            'stock_quote': '股票行情',
            'stock_financial': '财务数据',
            'stock_technical': '技术指标',
            'market_index': '市场指数',
            'market_overview': '市场概览',
            'macro_economy': '宏观经济',
            'industry_data': '行业数据',
            'fund_data': '基金',
            'bond_data': '债券',
            'forex_data': '外汇',
            'futures_data': '期货',
            'other': '其他'
        }
        return names.get(category, category)
        
    def _generate_interface_code(self, interface: Dict[str, Any]) -> str:
        """生成单个接口的注册代码 - 完整版，包含所有元数据字段"""
        name = interface['name']
        description = interface.get('description', '').replace('"', '\\"')  # 转义引号
        enhanced_parameters = interface.get('enhanced_input_params', [])
        
        # 确定分类
        category = self._determine_category(interface)
        
        # 获取参数信息
        required_params = interface.get('required_params', [])
        optional_params = interface.get('optional_params', [])
        return_type = interface.get('return_type', 'DataFrame')
        keywords = interface.get('keywords', [])
        
        # 生成示例参数
        example_params = {}
        smart_params_dict = {}
        
        for param in interface.get('input_params', []):
            # 查找对应的增强参数信息
            enhanced_param = next((ep for ep in enhanced_parameters if ep['name'] == param['name']), None)
            if enhanced_param and enhanced_param.get('test_values'):
                test_values = enhanced_param['test_values'][:3]  # 取前3个测试值
                smart_params_dict[param['name']] = test_values
                if test_values:
                    example_params[param['name']] = test_values[0]  # 第一个作为示例
        
        # 生成智能参数注释
        smart_params_comment = ""
        if smart_params_dict:
            smart_params_lines = []
            for param_name, test_values in smart_params_dict.items():
                values_str = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in test_values])
                smart_params_lines.append(f"            # {param_name}: [{values_str}]")
            if smart_params_lines:
                smart_params_comment = "\n" + "\n".join(smart_params_lines)
                
        # 生成完整的接口代码
        code = f'            # {name} - 完整元数据{smart_params_comment}\n'
        code += f'            create_interface("{name}")\\\n'
        code += f'                .with_source(DataSource.AKSHARE)\\\n'
        code += f'                .with_category(FunctionCategory.{category.upper()})\\\n'
        code += f'                .with_description("{description}")\\\n'
        
        # 添加必需参数
        if required_params:
            params_str = ', '.join([f'"{p}"' for p in required_params])
            code += f'                .with_required_params({params_str})\\\n'
        
        # 添加可选参数
        if optional_params:
            params_str = ', '.join([f'"{p}"' for p in optional_params])
            code += f'                .with_optional_params({params_str})\\\n'
        
        # 添加返回类型
        code += f'                .with_return_type("{return_type}")\\\n'
        
        # 添加关键词
        if keywords:
            keywords_str = ', '.join([f'"{k}"' for k in keywords[:5]])  # 限制关键词数量
            code += f'                .with_keywords({keywords_str})\\\n'
        
        # 添加示例参数
        if example_params:
            # 将示例参数转换为字符串格式，处理特殊字符
            params_items = []
            for k, v in example_params.items():
                if isinstance(v, str):
                    # 清理参数值中的特殊字符，避免JSON格式错误
                    clean_v = str(v).replace('"', '').replace("'", '').split(':')[0].strip()
                    params_items.append(f'"{k}": "{clean_v}"')
                else:
                    params_items.append(f'"{k}": {v}')
            params_dict_str = '{' + ', '.join(params_items) + '}'
            code += f'                .with_example_params({params_dict_str})\\\n'
        
        code += f'                .build(),'
        
        return code
        
    def _determine_category(self, interface: Dict[str, Any]) -> str:
        """确定接口分类 - 改进版本，提高分类准确性（与 FunctionCategory 对齐）"""
        name = interface['name'].lower()
        description = interface.get('description', '').lower()
        
        # 市场概览（在指数之前判断）
        if any(keyword in name for keyword in ['overview', 'market_overview', 'summary']) or any(k in description for k in ['概览', '全市场', '市场概览']):
            return 'market_overview'
        
        # 股票财务数据
        if any(keyword in name for keyword in ['financial', 'balance', 'profit', 'cash_flow', 'debt', 'benefit', 'abstract']):
            return 'stock_financial'
        
        # 股票行情数据
        elif any(keyword in name for keyword in ['daily', 'hist', 'minute', 'spot', 'real_time', 'quote', 'price']):
            if 'stock' in name:
                return 'stock_quote'
            elif any(keyword in name for keyword in ['index_', 'stock_index']):
                return 'market_index'
        
        # 股票技术指标
        elif any(keyword in name for keyword in ['technical', 'indicator', 'ma_', 'kdj', 'rsi', 'macd']):
            return 'stock_technical'
        
        # 股票基础信息
        elif any(keyword in name for keyword in ['stock_zh_a', 'stock_a_', 'stock_info', 'stock_basic', 'stock_list']):
            return 'stock_basic'
        
        # 市场指数
        elif any(keyword in name for keyword in ['index_', 'stock_index']):
            return 'market_index'
        
        # 宏观经济
        elif any(keyword in name for keyword in ['macro_', 'gdp', 'cpi', 'pmi', 'economy']):
            return 'macro_economy'
        
        # 基金数据
        elif any(keyword in name for keyword in ['fund_', 'etf_']):
            return 'fund_data'
        
        # 债券数据
        elif any(keyword in name for keyword in ['bond_', 'convertible_']):
            return 'bond_data'
        
        # 外汇数据
        elif any(keyword in name for keyword in ['forex_', 'currency_', 'exchange_rate']):
            return 'forex_data'
        
        # 期货数据
        elif any(keyword in name for keyword in ['futures_', 'option_']):
            return 'futures_data'
        
        # 行业数据 / 研报
        elif any(keyword in name for keyword in ['news_', 'report_', 'industry_', 'sector_']):
            return 'industry_data'
        
        # 其他股票相关（兜底）
        elif 'stock' in name:
            return 'stock_basic'
        
        else:
            return 'other'


def main():
    """主函数"""
    # 文件路径
    md_file = '/Users/wuyanqing/PycharmProjects/StockQuant/docs/akshare_interfaces.md'
    output_file = '/Users/wuyanqing/PycharmProjects/StockQuant/core/data/interfaces/akshare.py'
    
    print("开始解析akshare接口文档...")
    
    # 解析接口
    parser = InterfaceParser(md_file)
    interfaces = parser.parse_interfaces()
    
    print(f"共解析到 {len(interfaces)} 个接口")
    
    # 按分类统计
    categories = parser.categorize_interfaces()
    for category, interface_list in categories.items():
        if interface_list:
            print(f"  {category}: {len(interface_list)} 个接口")
    
    # 生成代码
    print("\n开始生成接口注册代码...")
    generator = CodeGenerator(interfaces)
    generator.generate_akshare_provider(output_file)
    
    print(f"代码已生成到: {output_file}")
    print("\n生成完成！")


if __name__ == '__main__':
    main()