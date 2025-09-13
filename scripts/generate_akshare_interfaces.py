#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动解析akshare_interfaces.md文档并生成接口注册代码的脚本
"""

import re
import os
from typing import List, Dict, Any


class InterfaceParser:
    """接口解析器"""
    
    def __init__(self, md_file_path: str):
        self.md_file_path = md_file_path
        self.interfaces = []
        
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
        """解析单个接口"""
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
                        
                    param_info = {
                        'name': param_name,
                        'type': param_type,
                        'description': param_desc
                    }
                    if current_section == 'input_params':
                        interface_info['input_params'].append(param_info)
                    elif current_section == 'return_fields':
                        interface_info['return_fields'].append(param_info)
                         
        return interface_info
    
    def categorize_interfaces(self) -> Dict[str, List[Dict[str, Any]]]:
        """按功能分类接口"""
        categories = {
            'a_stock': [],
            'b_stock': [],
            'cdr': [],
            'market_index': [],
            'macro': [],
            'fund': [],
            'bond': [],
            'futures': [],
            'technical': [],
            'industry': [],
            'news': [],
            'hk_stock': [],
            'us_stock': [],
            'others': []
        }
        
        for interface in self.interfaces:
            name = interface['name'].lower()
            desc = interface['description'].lower()
            
            # 根据接口名称和描述进行分类
            if any(keyword in name for keyword in ['stock_zh_a', 'stock_a_', 'a股', 'stock_financial']):
                categories['a_stock'].append(interface)
            elif any(keyword in name for keyword in ['stock_zh_b', 'stock_b_', 'b股']):
                categories['b_stock'].append(interface)
            elif any(keyword in name for keyword in ['cdr', 'stock_zh_a_cdr']):
                categories['cdr'].append(interface)
            elif any(keyword in name for keyword in ['index_', 'stock_index', '指数']):
                categories['market_index'].append(interface)
            elif any(keyword in name for keyword in ['macro_', 'gdp', 'cpi', 'pmi', '宏观']):
                categories['macro'].append(interface)
            elif any(keyword in name for keyword in ['fund_', 'etf_', '基金']):
                categories['fund'].append(interface)
            elif any(keyword in name for keyword in ['bond_', 'convertible_', '债券']):
                categories['bond'].append(interface)
            elif any(keyword in name for keyword in ['futures_', 'option_', '期货', '期权']):
                categories['futures'].append(interface)
            elif any(keyword in name for keyword in ['tech_', 'ma_', 'rsi_', 'macd_', '技术']):
                categories['technical'].append(interface)
            elif any(keyword in name for keyword in ['industry_', 'sector_', '行业']):
                categories['industry'].append(interface)
            elif any(keyword in name for keyword in ['news_', 'report_', '新闻', '公告']):
                categories['news'].append(interface)
            elif any(keyword in name for keyword in ['stock_hk', 'hk_', '港股']):
                categories['hk_stock'].append(interface)
            elif any(keyword in name for keyword in ['stock_us', 'us_', '美股']):
                categories['us_stock'].append(interface)
            else:
                categories['others'].append(interface)
                
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
            'from app.collectors.sources.api.base import (',
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
            'a_stock': '_register_a_stock_interfaces',
            'b_stock': '_register_b_stock_interfaces', 
            'cdr': '_register_cdr_interfaces',
            'market_index': '_register_market_index_interfaces',
            'macro': '_register_macro_interfaces',
            'fund': '_register_fund_interfaces',
            'bond': '_register_bond_interfaces',
            'futures': '_register_futures_interfaces',
            'technical': '_register_technical_interfaces',
            'industry': '_register_industry_interfaces',
            'news': '_register_news_interfaces',
            'hk_stock': '_register_hk_stock_interfaces',
            'us_stock': '_register_us_stock_interfaces',
            'others': '_register_other_interfaces'
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
            
        # 添加自动注册逻辑
        code_lines.extend([
            '',
            '# 自动注册到全局管理器',
            'akshare_provider = AkshareProvider()',
            'from app.collectors.sources.api.base import api_provider_manager',
            'api_provider_manager.register_provider(akshare_provider)'
        ])
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(code_lines))
            
    def _get_category_name(self, category: str) -> str:
        """获取分类中文名称"""
        names = {
            'a_stock': 'A股',
            'b_stock': 'B股',
            'cdr': 'CDR',
            'market_index': '市场指数',
            'macro': '宏观经济',
            'fund': '基金',
            'bond': '债券',
            'futures': '期货',
            'technical': '技术指标',
            'industry': '行业数据',
            'news': '新闻资讯',
            'hk_stock': '港股',
            'us_stock': '美股',
            'others': '其他'
        }
        return names.get(category, category)
        
    def _generate_interface_code(self, interface: Dict[str, Any]) -> str:
        """生成单个接口的注册代码"""
        name = interface['name']
        description = interface.get('description', '').replace('"', '\\"')  # 转义引号
        
        # 确定分类
        category = self._determine_category(interface)
        
        # 提取必填参数（占位符参数已在解析阶段过滤）
        required_params = []
        for param in interface.get('input_params', []):
            required_params.append(f'"{param["name"]}"')
                
        # 生成接口代码，参数模式将由with_required_params自动生成
        code = f'            create_interface("{name}")\\\n'
        code += f'                .with_source(DataSource.AKSHARE)\\\n'
        code += f'                .with_category(FunctionCategory.{category.upper()})\\\n'
        code += f'                .with_description("{description}")\\\n'
        if required_params:
            params_str = ', '.join(required_params)
            code += f'                .with_required_params({params_str})\\\n'
        code += f'                .build(),'
        
        return code
        
    def _determine_category(self, interface: Dict[str, Any]) -> str:
        """确定接口分类"""
        name = interface['name'].lower()
        
        if any(keyword in name for keyword in ['stock_zh_a', 'stock_a_', 'a股']):
            return 'stock_basic'
        elif any(keyword in name for keyword in ['index_', 'stock_index']):
            return 'market_index'
        elif any(keyword in name for keyword in ['macro_', 'gdp', 'cpi']):
            return 'macro_economy'
        elif any(keyword in name for keyword in ['fund_', 'etf_']):
            return 'fund_data'
        elif any(keyword in name for keyword in ['bond_', 'convertible_']):
            return 'bond_data'
        elif any(keyword in name for keyword in ['futures_', 'option_']):
            return 'futures_data'
        elif any(keyword in name for keyword in ['news_', 'report_']):
            return 'industry_data'
        else:
            return 'other'


def main():
    """主函数"""
    # 文件路径
    md_file = '/Users/wuyanqing/PycharmProjects/OpenStockData/docs/akshare_interfaces.md'
    output_file = '/Users/wuyanqing/PycharmProjects/OpenStockData/app/collectors/sources/api/akshare_generated.py'
    
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