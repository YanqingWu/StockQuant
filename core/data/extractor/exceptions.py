"""
数据提取错误处理器
提供细粒度的异常处理，替代宽泛的Exception捕获
"""

import pandas as pd
from typing import Optional
from .types import ExtractionResult
from core.logging import get_logger

logger = get_logger(__name__)


class ExtractionErrorHandler:
    """数据提取错误处理器"""
    
    @staticmethod
    def handle_data_processing_error(e: Exception, interface_name: str) -> ExtractionResult:
        """处理数据转换过程中的异常"""
        if isinstance(e, pd.errors.EmptyDataError):
            logger.warning(f"接口 {interface_name} 返回空数据")
            return ExtractionResult(
                success=False, 
                data=None, 
                error="数据为空",
                interface_name=interface_name
            )
        elif isinstance(e, pd.errors.ParserError):
            logger.error(f"接口 {interface_name} 数据解析错误: {e}")
            return ExtractionResult(
                success=False, 
                data=None, 
                error=f"数据解析错误: {e}",
                interface_name=interface_name
            )
        elif isinstance(e, KeyError):
            logger.error(f"接口 {interface_name} 缺少必要字段: {e}")
            return ExtractionResult(
                success=False, 
                data=None, 
                error=f"缺少必要字段: {e}",
                interface_name=interface_name
            )
        elif isinstance(e, ValueError):
            logger.error(f"接口 {interface_name} 数据格式错误: {e}")
            return ExtractionResult(
                success=False, 
                data=None, 
                error=f"数据格式错误: {e}",
                interface_name=interface_name
            )
        elif isinstance(e, TypeError):
            logger.error(f"接口 {interface_name} 数据类型错误: {e}")
            return ExtractionResult(
                success=False, 
                data=None, 
                error=f"数据类型错误: {e}",
                interface_name=interface_name
            )
        elif isinstance(e, AttributeError):
            logger.error(f"接口 {interface_name} 属性访问错误: {e}")
            return ExtractionResult(
                success=False, 
                data=None, 
                error=f"属性访问错误: {e}",
                interface_name=interface_name
            )
        else:
            logger.error(f"接口 {interface_name} 未预期的错误: {e}", exc_info=True)
            return ExtractionResult(
                success=False, 
                data=None, 
                error=f"处理失败: {e}",
                interface_name=interface_name
            )
    
    @staticmethod
    def handle_interface_execution_error(e: Exception, interface_name: str) -> ExtractionResult:
        """处理接口执行过程中的异常"""
        if isinstance(e, ConnectionError):
            logger.error(f"接口 {interface_name} 连接错误: {e}")
            return ExtractionResult(
                success=False,
                data=None,
                error=f"网络连接错误: {e}",
                interface_name=interface_name
            )
        elif isinstance(e, TimeoutError):
            logger.error(f"接口 {interface_name} 超时: {e}")
            return ExtractionResult(
                success=False,
                data=None,
                error=f"请求超时: {e}",
                interface_name=interface_name
            )
        elif isinstance(e, PermissionError):
            logger.error(f"接口 {interface_name} 权限错误: {e}")
            return ExtractionResult(
                success=False,
                data=None,
                error=f"权限不足: {e}",
                interface_name=interface_name
            )
        else:
            logger.error(f"接口 {interface_name} 执行错误: {e}", exc_info=True)
            return ExtractionResult(
                success=False,
                data=None,
                error=f"接口执行失败: {e}",
                interface_name=interface_name
            )


class DataValidator:
    """数据验证器"""
    
    @staticmethod
    def is_empty_data(data) -> bool:
        """检查数据是否为空"""
        if data is None:
            return True
        if isinstance(data, (list, tuple)) and len(data) == 0:
            return True
        if isinstance(data, str) and not data.strip():
            return True
        if isinstance(data, pd.DataFrame) and data.empty:
            return True
        if isinstance(data, dict) and not data:
            return True
        return False
    
    @staticmethod
    def validate_dataframe_structure(df: pd.DataFrame, required_columns: Optional[list] = None) -> tuple[bool, str]:
        """验证DataFrame结构"""
        if df is None:
            return False, "DataFrame为None"
        
        if df.empty:
            return False, "DataFrame为空"
        
        if required_columns:
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return False, f"缺少必要列: {missing_columns}"
        
        return True, "验证通过"
