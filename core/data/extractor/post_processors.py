"""
后处理器模块
包含各种数据后处理函数，用于在数据提取后进行格式转换和处理
"""

import pandas as pd
from typing import Any
from core.logging import get_logger

logger = get_logger(__name__)


def convert_market_summary_to_columns(data: Any) -> Any:
    """
    将市场概览的项目-数值格式转换为标准列格式
    
    适用于市场概览接口返回的项目-数值对格式，将其转换为标准列格式
    
    Args:
        data: 原始数据（通常是DataFrame）
        
    Returns:
        转换后的数据（保持相同类型）
    """
    # 如果不是DataFrame，直接返回原数据
    if not isinstance(data, pd.DataFrame):
        logger.debug("数据不是DataFrame类型，跳过市场概览转换")
        return data
    
    # 检查数据是否为空
    if data.empty:
        logger.debug("DataFrame为空，跳过转换")
        return data
    
    try:
        logger.debug(f"开始处理市场概览数据，原始数据形状: {data.shape}")
        logger.debug(f"原始数据列名: {data.columns.tolist()}")
        
        # 检查是否是市场概览格式（包含'项目'列）
        if '项目' not in data.columns:
            logger.debug("DataFrame不包含'项目'列，跳过市场概览转换")
            return data
        
        # 将项目-数值对转换为字典
        result_dict = {}
        
        # 处理每个项目
        for _, row in data.iterrows():
            item = row['项目']
            logger.debug(f"处理项目: {item}")
            if item in ['流通股本', '总市值', '成交金额', '上市公司', '上市股票', '流通市值', '报告时间']:
                # 优先获取股票列的值（全市场数据）
                if '股票' in row and pd.notna(row['股票']):
                    result_dict[item] = row['股票']
                    logger.debug(f"从股票列获取 {item}: {row['股票']}")
                # 如果没有股票列，获取主板列的值
                elif '主板' in row and pd.notna(row['主板']):
                    result_dict[item] = row['主板']
                    logger.debug(f"从主板列获取 {item}: {row['主板']}")
                # 最后获取科创板列的值
                elif '科创板' in row and pd.notna(row['科创板']):
                    result_dict[item] = row['科创板']
                    logger.debug(f"从科创板列获取 {item}: {row['科创板']}")
        
        # 添加交易所信息
        result_dict['exchange'] = 'SSE'
        
        # 处理日期信息
        if '报告时间' in result_dict:
            try:
                # 将20250930格式转换为日期
                date_str = str(result_dict['报告时间'])
                if len(date_str) == 8 and date_str.isdigit():
                    from datetime import datetime
                    date_obj = datetime.strptime(date_str, '%Y%m%d').date()
                    result_dict['date'] = date_obj
                    logger.debug(f"解析日期: {date_str} -> {date_obj}")
                else:
                    result_dict['date'] = None
            except Exception as e:
                logger.error(f"日期解析失败: {e}")
                result_dict['date'] = None
        else:
            result_dict['date'] = None
        
        # 删除临时的报告时间字段
        if '报告时间' in result_dict:
            del result_dict['报告时间']
        
        logger.debug(f"转换结果字典: {result_dict}")
        
        # 创建新的DataFrame，指定dtype避免pandas自动推断
        dtypes = {}
        if 'date' in result_dict and result_dict['date'] is not None:
            dtypes['date'] = 'object'
        
        result_df = pd.DataFrame([result_dict])
        
        # 确保date列保持为date类型
        if 'date' in result_df.columns and result_df['date'].iloc[0] is not None:
            # 强制转换为object类型，避免pandas自动转换为datetime64
            result_df['date'] = result_df['date'].astype('object')
        
        logger.debug(f"成功转换市场概览格式，原始行数: {len(data)}, 转换后列数: {len(result_df.columns)}")
        return result_df
        
    except Exception as e:
        logger.error(f"转换市场概览格式时出错: {e}")
        return data


def convert_item_value_to_columns(data: Any) -> Any:
    """
    将item-value格式转换为标准列格式
    
    适用于包含'item'和'value'列的DataFrame，将其转换为以item作为列名、value作为值的单行DataFrame
    
    Args:
        data: 原始数据（通常是DataFrame）
        
    Returns:
        转换后的数据（保持相同类型）
        
    Examples:
        输入DataFrame:
        | item    | value |
        |---------|-------|
        | 股票代码 | 000001 |
        | 股票名称 | 平安银行 |
        | 总市值   | 1000000 |
        
        输出DataFrame:
        | 股票代码 | 股票名称 | 总市值   |
        |---------|---------|---------|
        | 000001  | 平安银行 | 1000000 |
    """
    # 如果不是DataFrame，直接返回原数据
    if not isinstance(data, pd.DataFrame):
        logger.debug("数据不是DataFrame类型，跳过item-value转换")
        return data
    
    # 检查是否包含必要的列
    if 'item' not in data.columns or 'value' not in data.columns:
        logger.debug("DataFrame不包含'item'或'value'列，跳过转换")
        return data
    
    # 检查数据是否为空
    if data.empty:
        logger.debug("DataFrame为空，跳过转换")
        return data
    
    try:
        # 将item-value对转换为字典
        data_dict = dict(zip(data['item'], data['value']))
        
        # 创建新的DataFrame
        result_df = pd.DataFrame([data_dict])
        
        logger.debug(f"成功转换item-value格式，原始行数: {len(data)}, 转换后列数: {len(result_df.columns)}")
        return result_df
        
    except Exception as e:
        logger.error(f"item-value格式转换失败: {e}")
        return data  # 失败时返回原数据


def normalize_numeric_columns(data: Any) -> Any:
    """
    标准化数值列格式
    
    将字符串形式的数值转换为适当的数值类型
    
    Args:
        data: 原始数据（通常是DataFrame）
        
    Returns:
        转换后的数据
    """
    if not isinstance(data, pd.DataFrame):
        return data
    
    try:
        # 尝试将可能的数值列转换为数值类型
        for col in data.columns:
            if data[col].dtype == 'object':
                # 尝试转换为数值类型
                numeric_series = pd.to_numeric(data[col], errors='ignore')
                if not numeric_series.equals(data[col]):
                    data[col] = numeric_series
                    logger.debug(f"列 '{col}' 已转换为数值类型")
        
        return data
        
    except Exception as e:
        logger.error(f"数值列标准化失败: {e}")
        return data


def clean_whitespace(data: Any) -> Any:
    """
    清理字符串列中的空白字符
    
    Args:
        data: 原始数据（通常是DataFrame）
        
    Returns:
        清理后的数据
    """
    if not isinstance(data, pd.DataFrame):
        return data
    
    try:
        # 清理字符串列的空白字符
        for col in data.columns:
            if data[col].dtype == 'object':
                data[col] = data[col].astype(str).str.strip()
                logger.debug(f"列 '{col}' 已清理空白字符")
        
        return data
        
    except Exception as e:
        logger.error(f"空白字符清理失败: {e}")
        return data


def convert_market_sentiment_format(data: Any) -> Any:
    """
    转换市场情绪数据格式
    
    处理百度股市通投票数据的格式转换：
    1. 将百分比格式转换为数值
    2. 添加当前日期
    3. 处理数值格式（如"1.32万"）
    
    Args:
        data: 原始数据（通常是DataFrame）
        
    Returns:
        转换后的数据
    """
    if not isinstance(data, pd.DataFrame):
        logger.debug("数据不是DataFrame类型，跳过市场情绪转换")
        return data
    
    if data.empty:
        logger.debug("DataFrame为空，跳过转换")
        return data
    
    try:
        logger.debug(f"开始处理市场情绪数据，原始数据形状: {data.shape}")
        logger.debug(f"原始数据列名: {data.columns.tolist()}")
        
        # 检查是否是市场情绪格式
        if not all(col in data.columns for col in ['周期', '看涨', '看跌', '看涨比例', '看跌比例']):
            logger.debug("DataFrame不包含市场情绪字段，跳过转换")
            return data
        
        # 创建结果列表
        result_list = []
        
        # 获取当前日期
        from datetime import date
        current_date = date.today()
        
        # 处理每一行数据
        for _, row in data.iterrows():
            try:
                # 转换百分比格式
                bullish_ratio = row['看涨比例']
                bearish_ratio = row['看跌比例']
                
                if isinstance(bullish_ratio, str) and bullish_ratio.endswith('%'):
                    bullish_ratio = float(bullish_ratio.rstrip('%')) / 100
                elif isinstance(bullish_ratio, str):
                    bullish_ratio = float(bullish_ratio)
                
                if isinstance(bearish_ratio, str) and bearish_ratio.endswith('%'):
                    bearish_ratio = float(bearish_ratio.rstrip('%')) / 100
                elif isinstance(bearish_ratio, str):
                    bearish_ratio = float(bearish_ratio)
                
                # 处理数值格式（如"1.32万"）
                def parse_number(value):
                    if isinstance(value, str):
                        if '万' in value:
                            return float(value.replace('万', '')) * 10000
                        elif '千' in value:
                            return float(value.replace('千', '')) * 1000
                        else:
                            return float(value)
                    return value
                
                bullish_count = parse_number(row['看涨'])
                bearish_count = parse_number(row['看跌'])
                
                # 创建结果字典
                result_dict = {
                    'date': current_date,
                    'period': row['周期'],
                    'bullish_count': bullish_count,
                    'bearish_count': bearish_count,
                    'bullish_ratio': bullish_ratio,
                    'bearish_ratio': bearish_ratio
                }
                
                result_list.append(result_dict)
                logger.debug(f"处理周期 {row['周期']}: 看涨={bullish_count}, 看跌={bearish_count}, 看涨比例={bullish_ratio}, 看跌比例={bearish_ratio}")
                
            except Exception as e:
                logger.error(f"处理行数据时出错: {e}, 行数据: {row.to_dict()}")
                continue
        
        if not result_list:
            logger.warning("没有成功处理任何市场情绪数据")
            return data
        
        # 创建新的DataFrame
        result_df = pd.DataFrame(result_list)
        
        logger.debug(f"成功转换市场情绪格式，原始行数: {len(data)}, 转换后行数: {len(result_df)}")
        return result_df
        
    except Exception as e:
        logger.error(f"转换市场情绪格式时出错: {e}")
        return data


def convert_szse_summary_to_market_overview(data: Any) -> Any:
    """
    将深交所概览数据转换为市场概览格式
    
    Args:
        data: 原始数据（通常是DataFrame）
        
    Returns:
        转换后的数据（保持相同类型）
    """
    if not isinstance(data, pd.DataFrame):
        logger.debug("数据不是DataFrame类型，跳过深交所概览转换")
        return data
    
    if data.empty:
        logger.debug("DataFrame为空，跳过转换")
        return data
    
    try:
        logger.debug(f"开始处理深交所概览数据，原始数据形状: {data.shape}")
        logger.debug(f"原始数据列名: {data.columns.tolist()}")
        
        # 检查是否是深交所概览格式
        if '证券类别' not in data.columns:
            logger.debug("DataFrame不包含'证券类别'列，跳过深交所概览转换")
            return data
        
        # 获取股票类别的数据（全市场数据）
        stock_data = data[data['证券类别'] == '股票']
        if stock_data.empty:
            logger.debug("未找到股票类别数据")
            return data
        
        # 提取关键字段
        result_dict = {}
        row = stock_data.iloc[0]
        
        result_dict['exchange'] = 'SZSE'
        result_dict['stock_count'] = row.get('数量', None)
        result_dict['turnover_amount'] = row.get('成交金额', None)
        result_dict['total_market_cap'] = row.get('总市值', None)
        result_dict['circulating_market_cap'] = row.get('流通市值', None)
        
        # 设置日期为当前日期
        from datetime import date
        result_dict['date'] = date.today()
        
        # 创建新的DataFrame
        result_df = pd.DataFrame([result_dict])
        
        logger.debug(f"成功转换深交所概览格式，结果: {result_dict}")
        return result_df
        
    except Exception as e:
        logger.error(f"转换深交所概览格式时出错: {e}")
        return data


def convert_account_statistics_to_market_overview(data: Any) -> Any:
    """
    将投资者统计数据转换为市场概览格式
    
    Args:
        data: 原始数据（通常是DataFrame）
        
    Returns:
        转换后的数据（保持相同类型）
    """
    if not isinstance(data, pd.DataFrame):
        logger.debug("数据不是DataFrame类型，跳过投资者统计转换")
        return data
    
    if data.empty:
        logger.debug("DataFrame为空，跳过转换")
        return data
    
    try:
        logger.debug(f"开始处理投资者统计数据，原始数据形状: {data.shape}")
        logger.debug(f"原始数据列名: {data.columns.tolist()}")
        
        # 获取最新数据
        latest_data = data.iloc[-1]
        
        result_dict = {}
        result_dict['exchange'] = 'SH+SZ'  # 沪深两市
        result_dict['investor_count'] = latest_data.get('期末投资者-总量', None)
        result_dict['new_investor_count'] = latest_data.get('新增投资者-数量', None)
        result_dict['total_market_cap'] = latest_data.get('沪深总市值', None)
        
        # 计算投资者增长率
        if len(data) > 1:
            prev_investor_count = data.iloc[-2].get('期末投资者-总量', None)
            if prev_investor_count and result_dict['investor_count']:
                growth_rate = (result_dict['investor_count'] - prev_investor_count) / prev_investor_count * 100
                result_dict['investor_growth_rate'] = growth_rate
        
        # 处理日期
        date_str = latest_data.get('数据日期', '')
        if date_str:
            try:
                from datetime import datetime
                if len(date_str) == 7:  # 格式如 "2025-01"
                    date_obj = datetime.strptime(date_str + '-01', '%Y-%m-%d').date()
                else:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                result_dict['date'] = date_obj
            except Exception as e:
                logger.error(f"日期解析失败: {e}")
                result_dict['date'] = None
        
        # 创建新的DataFrame
        result_df = pd.DataFrame([result_dict])
        
        logger.debug(f"成功转换投资者统计格式，结果: {result_dict}")
        return result_df
        
    except Exception as e:
        logger.error(f"转换投资者统计格式时出错: {e}")
        return data


def convert_buffett_index_to_market_overview(data: Any) -> Any:
    """
    将巴菲特指数数据转换为市场概览格式
    
    Args:
        data: 原始数据（通常是DataFrame）
        
    Returns:
        转换后的数据（保持相同类型）
    """
    if not isinstance(data, pd.DataFrame):
        logger.debug("数据不是DataFrame类型，跳过巴菲特指数转换")
        return data
    
    if data.empty:
        logger.debug("DataFrame为空，跳过转换")
        return data
    
    try:
        logger.debug(f"开始处理巴菲特指数数据，原始数据形状: {data.shape}")
        logger.debug(f"原始数据列名: {data.columns.tolist()}")
        
        # 获取最新数据
        latest_data = data.iloc[-1]
        
        result_dict = {}
        result_dict['exchange'] = 'SH+SZ'  # 沪深两市
        result_dict['total_market_cap'] = latest_data.get('总市值', None)
        
        # 计算市值GDP比值
        gdp = latest_data.get('GDP', None)
        if result_dict['total_market_cap'] and gdp:
            result_dict['market_cap_to_gdp_ratio'] = result_dict['total_market_cap'] / gdp
        
        # 处理日期
        date_value = latest_data.get('日期', '')
        if date_value:
            try:
                from datetime import datetime
                if isinstance(date_value, str):
                    date_obj = datetime.strptime(date_value, '%Y-%m-%d').date()
                elif hasattr(date_value, 'date'):
                    date_obj = date_value.date()
                else:
                    date_obj = None
                result_dict['date'] = date_obj
            except Exception as e:
                logger.error(f"日期解析失败: {e}")
                result_dict['date'] = None
        
        # 创建新的DataFrame
        result_df = pd.DataFrame([result_dict])
        
        logger.debug(f"成功转换巴菲特指数格式，结果: {result_dict}")
        return result_df
        
    except Exception as e:
        logger.error(f"转换巴菲特指数格式时出错: {e}")
        return data


def convert_market_activity_to_market_overview(data: Any) -> Any:
    """
    将市场活跃度数据转换为市场概览格式
    
    Args:
        data: 原始数据（通常是DataFrame）
        
    Returns:
        转换后的数据（保持相同类型）
    """
    if not isinstance(data, pd.DataFrame):
        logger.debug("数据不是DataFrame类型，跳过市场活跃度转换")
        return data
    
    if data.empty:
        logger.debug("DataFrame为空，跳过转换")
        return data
    
    try:
        logger.debug(f"开始处理市场活跃度数据，原始数据形状: {data.shape}")
        logger.debug(f"原始数据列名: {data.columns.tolist()}")
        
        # 检查是否是市场活跃度格式
        if 'item' not in data.columns or 'value' not in data.columns:
            logger.debug("DataFrame不包含'item'或'value'列，跳过市场活跃度转换")
            return data
        
        result_dict = {}
        result_dict['exchange'] = 'SH+SZ'  # 沪深两市
        
        # 映射活跃度数据
        for _, row in data.iterrows():
            item = row['item']
            value = row['value']
            
            if item == '上涨':
                result_dict['rising_count'] = value
            elif item == '下跌':
                result_dict['falling_count'] = value
            elif item == '涨停':
                result_dict['limit_up_count'] = value
            elif item == '跌停':
                result_dict['limit_down_count'] = value
            elif item == '真实涨停':
                result_dict['real_limit_up_count'] = value
        
        # 设置日期为当前日期
        from datetime import date
        result_dict['date'] = date.today()
        
        # 创建新的DataFrame
        result_df = pd.DataFrame([result_dict])
        
        logger.debug(f"成功转换市场活跃度格式，结果: {result_dict}")
        return result_df
        
    except Exception as e:
        logger.error(f"转换市场活跃度格式时出错: {e}")
        return data


def convert_fund_flow_to_market_overview(data: Any) -> Any:
    """
    将资金流向数据转换为市场概览格式
    
    Args:
        data: 原始数据（通常是DataFrame）
        
    Returns:
        转换后的数据（保持相同类型）
    """
    if not isinstance(data, pd.DataFrame):
        logger.debug("数据不是DataFrame类型，跳过资金流向转换")
        return data
    
    if data.empty:
        logger.debug("DataFrame为空，跳过转换")
        return data
    
    try:
        logger.debug(f"开始处理资金流向数据，原始数据形状: {data.shape}")
        logger.debug(f"原始数据列名: {data.columns.tolist()}")
        
        # 获取最新数据
        latest_data = data.iloc[-1]
        
        result_dict = {}
        result_dict['exchange'] = 'SH+SZ'  # 沪深两市
        result_dict['main_net_inflow'] = latest_data.get('主力净流入-净额', None)
        result_dict['main_net_inflow_ratio'] = latest_data.get('主力净流入-净占比', None)
        result_dict['large_net_inflow'] = latest_data.get('超大单净流入-净额', None)
        result_dict['large_net_inflow_ratio'] = latest_data.get('超大单净流入-净占比', None)
        
        # 处理日期
        date_value = latest_data.get('日期', '')
        if date_value:
            try:
                from datetime import datetime
                if isinstance(date_value, str):
                    date_obj = datetime.strptime(date_value, '%Y-%m-%d').date()
                elif hasattr(date_value, 'date'):
                    date_obj = date_value.date()
                else:
                    date_obj = None
                result_dict['date'] = date_obj
            except Exception as e:
                logger.error(f"日期解析失败: {e}")
                result_dict['date'] = None
        
        # 创建新的DataFrame
        result_df = pd.DataFrame([result_dict])
        
        logger.debug(f"成功转换资金流向格式，结果: {result_dict}")
        return result_df
        
    except Exception as e:
        logger.error(f"转换资金流向格式时出错: {e}")
        return data