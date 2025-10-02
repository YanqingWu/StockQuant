"""
后处理器模块
包含各种数据后处理函数，用于在数据提取后进行格式转换和处理
"""

import pandas as pd
from typing import Any
from core.logging import get_logger

logger = get_logger(__name__)


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