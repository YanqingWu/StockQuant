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