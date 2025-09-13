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
        
        # 如果映射表中没有找到，使用更新后的分类逻辑
        name_lower = func_name.lower()
        desc_lower = doc.lower()
        
        # 股票财务数据 - 优先级最高，先检查
        if any(keyword in name_lower or keyword in desc_lower for keyword in [
            'financial', '财务', 'balance_sheet', '资产负债表', 'cash_flow', '现金流量表',
            'profit_sheet', '利润表', 'abstract', '摘要', 'benefit', '收益', 'debt', '负债',
            'analysis_indicator', '分析指标', 'report', '报告', 'forecast', '预测',
            'yjbb', '业绩报表', 'yjkb', '业绩快报', 'yjyg', '业绩预告', 'quarterly', '季度',
            'yearly', '年度', 'delisted', '退市', 'kcb_report', '科创板报告'
        ]) or 'yjbb_em' in name_lower or 'yjkb_em' in name_lower or 'financial_hk_report' in name_lower or 'financial_us_report' in name_lower:
            # 排除非财务数据的接口
            if not any(exclude in name_lower for exclude in [
                'rank_forecast', 'disclosure_report'
            ]):
                return 'STOCK_FINANCIAL'
        
        # 股票基础信息 - 排除已被行情数据匹配的接口
        if (any(keyword in name_lower or keyword in desc_lower for keyword in [
            'info', 'name', 'code', 'basic', '基础', '信息', '名称', '代码', 'profile', '资料',
            'delist', '退市', 'st_em', 'new', '新股', 'ipo', '上市', 'gdhs', '股东户数',
            'allotment', '配股', 'repurchase', '回购', 'dividend', '分红', 'fhps', '分红送配',
            'share_change', '股本变动', 'restricted', '限售', 'pledge', '质押', 'gpzy',
            'hold_', '持股', 'gdfx', '股东', 'management', '高管', 'control', '控制',
            'statistics', '统计', 'pb', '市净率', 'ttm', '市盈率', 'below_net', '破净',
            'high_low', '新高新低', 'concept_cons', '概念成份', 'concept_name', '概念名称',
            'concept_info', '概念简介', 'industry_info', '行业简介', 'board_', '板块',
            'changes', '异动', 'comment', '千股千评', 'keyword', '关键词', 'search', '搜索',
            'xgsglb', '限购股', 'staq', 'register', '注册制', 'concept_summary', '概念摘要',
            'industry_summary', '行业摘要', 'industry_cons', '行业成份', 'board_concept_name', '板块概念名称',
            'board_industry_name', '板块行业名称', 'board_concept_info', '板块概念信息',
            'board_industry_info', '板块行业信息', 'concept_index', '概念指数', 'industry_index', '行业指数',
            'rank_forecast', 'disclosure_report'
        ]) and not any(hist_keyword in name_lower for hist_keyword in [
            'hist', 'daily', 'spot', 'minute', 'min_em', 'hot_rank_latest', 'hsgt_board_rank', 'sector_fund_flow_rank'
        ])):
            return 'STOCK_BASIC'
        
        # 股票行情数据 - 优先级第二，在基础信息之前检查
        if any(keyword in name_lower or keyword in desc_lower for keyword in [
            'spot', '实时', 'hist', '历史', 'daily', '日线', 'minute', '分钟', 'min_em',
            'quote', '行情', 'price', '价格', 'bid_ask', '买卖盘', 'intraday', '盘中',
            'tick', '逐笔', 'cdr_daily', 'ah_', 'b_', 'kcb_', 'cy_a', 'bj_a', 'sh_a', 'sz_a',
            'us_', 'hk_', 'zh_a', 'zh_b', 'famous_spot', '知名', 'pink_spot', 'main_board_spot',
            'hot_rank', '人气榜', 'hot_deal', '热门交易', 'hot_follow', '热门关注', 'hot_up', '热门上涨',
            'hsgt_', '沪深港通', 'individual_fund_flow', '个股资金流', 'lhb_', '龙虎榜',
            'margin_', '融资融券', 'qsjy', '券商交易', 'sse_deal', '上交所成交', 'tfp', '停复牌',
            'zt_pool', '涨停板', 'dzjy_mrmx', '大宗交易明细', 'dzjy_sctj', '大宗交易统计',
            'concept_hist', '概念历史', 'industry_hist', '行业历史', 'board_concept_hist', '板块概念历史',
            'board_industry_hist', '板块行业历史', 'sector_fund_flow_hist', '板块资金流历史',
            'inner_trade', '内幕交易', 'clf_hist', '分类历史', 'new_a_spot', '新A股现货',
            'sector_spot', '板块现货', 'industry_spot', '行业现货'
        ]):
            return 'STOCK_QUOTE'
        
        # 股票技术指标
        if any(keyword in name_lower or keyword in desc_lower for keyword in [
            'technical', '技术', 'indicator', '指标', 'analysis_indicator_em', 'hk_analysis_indicator',
            'us_analysis_indicator', 'hk_indicator', 'a_indicator', 'gxl', '股息率',
            'rank_', '排名', 'buffett_index', '巴菲特指标', 'hot_rank_latest', '人气榜最新',
            'board_rank', '板块排名', 'fund_flow_rank', '资金流排名', 'hsgt_board_rank', 'sector_fund_flow_rank'
        ]):
            return 'STOCK_TECHNICAL'
        
        # 市场指数
        if any(keyword in name_lower or keyword in desc_lower for keyword in [
            'index', '指数', 'buffett_index', '巴菲特指标', 'concept_index', '概念指数',
            'industry_index', '行业指数', 'csindex', '中证指数', 'value_csindex', '指数估值'
        ]):
            return 'MARKET_INDEX'
        
        # 市场概览
        if any(keyword in name_lower or keyword in desc_lower for keyword in [
            'market_activity', '市场活跃度', 'market_fund_flow', '市场资金流',
            'scrd_desire_em', '市场情绪', 'scrd_focus_em', '市场焦点'
        ]):
            return 'MARKET_OVERVIEW'
        
        # 行业数据 - 更精确的匹配
        if any(keyword in name_lower or keyword in desc_lower for keyword in [
            'yysj_em', '营业收入', 'fund_flow_industry', '行业资金流', 'gpzy_industry', '股权质押行业',
            'industry_category_cninfo', '行业分类', 'industry_change_cninfo', '行业变更'
        ]):
            return 'INDUSTRY_DATA'
        
        # 基金数据 - 更精确的匹配
        if any(keyword in name_lower or keyword in desc_lower for keyword in [
            'fund_flow_big_deal', '大单资金流', 'fund_flow_concept', '概念资金流', 
            'main_fund_flow', '主力资金流', 'fund_stock_holder', '基金持股',
            'report_fund_hold', '基金持有报告'
        ]):
            return 'FUND_DATA'
        
        # 其他分类的特殊情况 - 精简并重新组织
        if any(keyword in name_lower or keyword in desc_lower for keyword in [
            'cyq', '筹码', 'esg', '环境社会治理', 'valuation_baidu', '百度估值',
            'vote_baidu', '百度投票', 'js_weibo_nlp', '金十微博情感', 'classify_sina', '新浪分类',
            'congestion_lg', '拥挤度', 'ebs_lg', 'add_stock', '增发', 'dzjy_yybph', '大宗交易营业部排行',
            'gsrl_gsdt', '公司动态', 'hot_tweet_xq', '雪球热门', 'institute_recommend', '机构推荐',
            'jgdy_detail', '机构调研详情', 'sse_summary', '上交所摘要', 'sy_em', '首页',
            'sy_yq_em', '首页舆情', 'szse_area_summary', '深交所地区摘要', 'value_em', '估值',
            'yzxdr_em', '一字涨跌', 'zdhtmx_em', '重大合同明细', 'zygc_em', '重要公告',
            'zyjs_ths', '主要介绍'
        ]):
            return 'OTHER'
        
        # 股票特殊数据类型 - 归类到OTHER
        if any(keyword in name_lower or keyword in desc_lower for keyword in [
            'congestion', '拥挤度', 'add_stock', '增发', 'suspend', '停牌', 'resume', '复牌',
            'announcement', '公告', 'notice', '通知', 'news', '新闻', 'research', '研报',
            'rating', '评级', 'recommendation', '推荐', 'target_price', '目标价',
            'institutional', '机构', 'analyst', '分析师', 'coverage', '覆盖',
            'event', '事件', 'calendar', '日历', 'earnings_calendar', '财报日历'
        ]):
            return 'OTHER'
        
        # 市场监管和交易规则 - 归类到OTHER
        if any(keyword in name_lower or keyword in desc_lower for keyword in [
            'rule', '规则', 'regulation', '监管', 'policy', '政策', 'law', '法规',
            'compliance', '合规', 'audit', '审计', 'inspection', '检查',
            'violation', '违规', 'penalty', '处罚', 'warning', '警告'
        ]):
            return 'OTHER'
        
        # 默认分类
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