#!/usr/bin/env python3
"""
字段映射分析工具

该工具用于分析extraction_config.yaml中配置的接口，找出哪些返回字段没有被映射。
支持以下功能：
1. 根据给定的数据类型（如stock.profile）找到注册的接口
2. 从dump/interface_analysis_results.json中提取接口的返回字段
3. 对比field_mappings配置，找出未映射的字段
4. 如果没有指定接口，列出可选的接口类型

使用示例：
python field_mapping_analyzer.py stock.profile
python field_mapping_analyzer.py stock.daily_market.quote
python field_mapping_analyzer.py --list-types
"""

import json
import yaml
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict


class FieldMappingAnalyzer:
    def __init__(self):
        """
        初始化字段映射分析器
        """
        # 获取当前脚本所在目录的父目录（项目根目录）
        project_root = Path(__file__).parent.parent
        self.config_path = project_root / 'core' / 'data' / 'extractor' / 'extraction_config.yaml'
        self.analysis_path = project_root / 'dump' / 'interface_analysis_results.json'
        
        # 加载配置文件
        self.config_data = self._load_yaml_config()
        self.analysis_data = self._load_json_analysis()
        
        # 提取field_mappings
        self.field_mappings = self.config_data.get('field_mappings', {})
        
        # 构建接口分析数据的索引
        self.interface_analysis_index = self._build_interface_index()
    
    def _load_yaml_config(self) -> Dict:
        """加载YAML配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"错误：无法加载配置文件 {self.config_path}: {e}")
            sys.exit(1)
    
    def _load_json_analysis(self) -> Dict:
        """加载JSON分析文件"""
        try:
            with open(self.analysis_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"错误：无法加载分析文件 {self.analysis_path}: {e}")
            sys.exit(1)
    
    def _build_interface_index(self) -> Dict[str, Dict]:
        """构建接口分析数据的索引，以接口名为键"""
        index = {}
        for interface_data in self.analysis_data.get('interfaces', []):
            interface_name = interface_data.get('interface_name')
            if interface_name:
                index[interface_name] = interface_data
        return index
    
    def list_available_data_types(self) -> List[str]:
        """列出所有可用的数据类型"""
        data_types = []
        interfaces_config = self.config_data.get('interfaces_config', {})
        
        for category, category_data in interfaces_config.items():
            for data_type, type_data in category_data.items():
                if isinstance(type_data, dict):
                    # 检查是否有嵌套的数据类型（如daily_market.quote）
                    if 'interfaces' in type_data:
                        data_types.append(f"{category}.{data_type}")
                    else:
                        # 检查嵌套结构
                        for sub_type, sub_data in type_data.items():
                            if isinstance(sub_data, dict) and 'interfaces' in sub_data:
                                data_types.append(f"{category}.{data_type}.{sub_type}")
        
        return sorted(data_types)
    
    def get_interfaces_for_data_type(self, data_type: str) -> List[Dict]:
        """
        根据数据类型获取配置的接口列表
        
        Args:
            data_type: 数据类型，如 "stock.profile" 或 "stock.daily_market.quote"
        
        Returns:
            接口配置列表
        """
        parts = data_type.split('.')
        if len(parts) < 2:
            return []
        
        interfaces_config = self.config_data.get('interfaces_config', {})
        current_level = interfaces_config
        
        # 逐级深入到指定的数据类型
        for part in parts:
            if part in current_level:
                current_level = current_level[part]
            else:
                return []
        
        # 获取接口列表
        if isinstance(current_level, dict) and 'interfaces' in current_level:
            return current_level['interfaces']
        
        return []
    
    def get_interface_fields(self, interface_name: str) -> Tuple[List[str], bool]:
        """
        从分析结果中获取接口的返回字段
        
        Args:
            interface_name: 接口名称
        
        Returns:
            (字段列表, 是否成功获取)
        """
        interface_data = self.interface_analysis_index.get(interface_name)
        if not interface_data:
            return [], False
        
        # 检查接口是否成功执行
        if not interface_data.get('success', False):
            return [], False
        
        # 获取字段列表
        columns = interface_data.get('columns', [])
        return columns, True
    
    def find_unmapped_fields(self, interface_name: str, fields: List[str]) -> List[str]:
        """
        找出未映射的字段
        
        Args:
            interface_name: 接口名称
            fields: 字段列表
        
        Returns:
            未映射的字段列表
        """
        unmapped_fields = []
        
        for field in fields:
            # 检查字段是否在field_mappings中
            if field not in self.field_mappings:
                unmapped_fields.append(field)
        
        return unmapped_fields
    
    def analyze_data_type(self, data_type: str) -> Dict:
        """
        分析指定数据类型的字段映射情况
        
        Args:
            data_type: 数据类型
        
        Returns:
            分析结果字典
        """
        result = {
            'data_type': data_type,
            'interfaces': [],
            'total_interfaces': 0,
            'successful_interfaces': 0,
            'total_unmapped_fields': 0,
            'summary': {}
        }
        
        # 获取接口列表
        interfaces = self.get_interfaces_for_data_type(data_type)
        result['total_interfaces'] = len(interfaces)
        
        if not interfaces:
            result['error'] = f"未找到数据类型 '{data_type}' 的接口配置"
            return result
        
        # 分析每个接口
        for interface_config in interfaces:
            interface_name = interface_config.get('name')
            if not interface_name:
                continue
            
            interface_result = {
                'name': interface_name,
                'enabled': interface_config.get('enabled', False),
                'priority': interface_config.get('priority', 0),
                'markets': interface_config.get('markets', []),
                'fields': [],
                'unmapped_fields': [],
                'success': False,
                'error': None
            }
            
            # 获取接口字段
            fields, success = self.get_interface_fields(interface_name)
            interface_result['success'] = success
            interface_result['fields'] = fields
            
            if success:
                result['successful_interfaces'] += 1
                # 找出未映射的字段
                unmapped_fields = self.find_unmapped_fields(interface_name, fields)
                interface_result['unmapped_fields'] = unmapped_fields
                result['total_unmapped_fields'] += len(unmapped_fields)
            else:
                interface_result['error'] = "接口分析数据不可用或执行失败"
            
            result['interfaces'].append(interface_result)
        
        # 生成汇总信息
        result['summary'] = self._generate_summary(result)
        
        return result
    
    def _generate_summary(self, result: Dict) -> Dict:
        """生成分析结果的汇总信息"""
        summary = {
            'total_fields': 0,
            'unique_unmapped_fields': set(),
            'interfaces_with_unmapped_fields': 0,
            'most_common_unmapped_fields': {}
        }
        
        unmapped_field_count = defaultdict(int)
        
        for interface in result['interfaces']:
            if interface['success']:
                summary['total_fields'] += len(interface['fields'])
                
                if interface['unmapped_fields']:
                    summary['interfaces_with_unmapped_fields'] += 1
                    
                    for field in interface['unmapped_fields']:
                        summary['unique_unmapped_fields'].add(field)
                        unmapped_field_count[field] += 1
        
        # 转换set为list以便JSON序列化
        summary['unique_unmapped_fields'] = sorted(list(summary['unique_unmapped_fields']))
        
        # 找出最常见的未映射字段
        if unmapped_field_count:
            sorted_fields = sorted(unmapped_field_count.items(), key=lambda x: x[1], reverse=True)
            summary['most_common_unmapped_fields'] = dict(sorted_fields[:10])  # 取前10个
        
        return summary
    
    def print_analysis_result(self, result: Dict, output_format: str = 'text'):
        """打印分析结果"""
        if output_format == 'json':
            # 转换set为list以便JSON序列化
            result_copy = json.loads(json.dumps(result, default=str))
            print(json.dumps(result_copy, ensure_ascii=False, indent=2))
            return
        
        print(f"\n=== 字段映射分析结果：{result['data_type']} ===")
        
        if 'error' in result:
            print(f"错误：{result['error']}")
            return
        
        print(f"总接口数：{result['total_interfaces']}")
        print(f"成功分析的接口数：{result['successful_interfaces']}")
        print(f"总未映射字段数：{result['total_unmapped_fields']}")
        
        # 打印汇总信息
        summary = result['summary']
        print(f"\n--- 未映射字段汇总 ---")
        print(f"唯一未映射字段数：{len(summary['unique_unmapped_fields'])}")
        print(f"有未映射字段的接口数：{summary['interfaces_with_unmapped_fields']}")
        
        # 打印所有未映射字段
        if summary['unique_unmapped_fields']:
            print(f"\n--- 所有未映射字段列表 ---")
            for field in summary['unique_unmapped_fields']:
                count = summary['most_common_unmapped_fields'].get(field, 1)
                print(f"  {field} (出现在{count}个接口中)")
        else:
            print(f"\n✓ 所有字段都已映射")
    
    def generate_mapping_suggestions(self, result: Dict) -> Dict[str, str]:
        """
        为未映射的字段生成映射建议
        
        Args:
            result: 分析结果
        
        Returns:
            字段映射建议字典
        """
        suggestions = {}
        
        # 常见字段映射规则
        common_mappings = {
            # 英文字段
            'date': 'date',
            'open': 'open', 
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume',
            'amount': 'amount',
            'name': 'name',
            'code': 'symbol',
            'symbol': 'symbol',
            'item': 'field_name',  # 对于item-value格式
            'value': 'field_value',  # 对于item-value格式
            
            # 中文字段
            '板块': 'sector',
            '地区': 'region',
            '公司全称': 'full_name',
            '曾用简称': 'former_name',
            'B股代码': 'b_share_code',
            'B股简称': 'b_share_name',
            'H股代码': 'h_share_code', 
            'H股简称': 'h_share_name',
            '成立日期': 'establish_date',
            '传真': 'fax',
            '邮政编码': 'postal_code',
            '机构简介': 'company_profile',
            'A股上市日期': 'a_share_list_date',
            'A股总股本': 'a_share_total',
            'A股流通股本': 'a_share_outstanding',
        }
        
        # 收集所有未映射字段
        all_unmapped_fields = set()
        for interface in result.get('interfaces', []):
            all_unmapped_fields.update(interface.get('unmapped_fields', []))
        
        # 生成建议
        for field in all_unmapped_fields:
            if field in common_mappings:
                suggestions[field] = common_mappings[field]
            else:
                # 基于字段名生成建议
                field_lower = field.lower()
                if '日期' in field or 'date' in field_lower:
                    suggestions[field] = f"{field.replace('日期', '').replace('Date', '').lower()}_date"
                elif '代码' in field or 'code' in field_lower:
                    suggestions[field] = f"{field.replace('代码', '').replace('Code', '').lower()}_code"
                elif '名称' in field or 'name' in field_lower:
                    suggestions[field] = f"{field.replace('名称', '').replace('Name', '').lower()}_name"
                elif '金额' in field or 'amount' in field_lower:
                    suggestions[field] = f"{field.replace('金额', '').replace('Amount', '').lower()}_amount"
                else:
                    # 默认建议：转换为小写并替换特殊字符
                    suggested_name = field.lower().replace(' ', '_').replace('-', '_')
                    suggestions[field] = suggested_name
        
        return suggestions


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='分析字段映射配置')
    parser.add_argument('data_type', nargs='?', help='要分析的数据类型（如：stock.profile）')
    parser.add_argument('--list-types', action='store_true', help='列出所有可用的数据类型')
    parser.add_argument('--json', action='store_true', help='以JSON格式输出结果')
    
    args = parser.parse_args()
    
    analyzer = FieldMappingAnalyzer()
    
    if args.list_types:
        types = analyzer.list_available_data_types()
        print("可用的数据类型：")
        for data_type in sorted(types):
            print(f"  {data_type}")
        return
    
    if not args.data_type:
        print("请指定要分析的数据类型，或使用 --list-types 查看可用类型")
        return
    
    # 分析指定的数据类型
    result = analyzer.analyze_data_type(args.data_type)
    
    # 输出结果
    output_format = 'json' if args.json else 'text'
    analyzer.print_analysis_result(result, output_format)


if __name__ == '__main__':
    main()