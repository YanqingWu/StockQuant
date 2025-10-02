"""
适配器异常类
提供统一的异常处理机制
"""

from typing import Any, Optional


class AdapterError(Exception):
    """适配器基础异常"""
    pass


class ParameterValidationError(AdapterError):
    """参数验证异常"""
    
    def __init__(self, field: str, value: Any, reason: str):
        self.field = field
        self.value = value
        self.reason = reason
        super().__init__(f"参数 {field} 验证失败: {reason} (值: {value})")


class FormatConversionError(AdapterError):
    """格式转换异常"""
    
    def __init__(self, field: str, value: Any, target_format: str, reason: str = ""):
        self.field = field
        self.value = value
        self.target_format = target_format
        self.reason = reason
        super().__init__(f"参数 {field} 格式转换失败: {value} -> {target_format} ({reason})")


class RequiredParameterError(AdapterError):
    """必填参数缺失异常"""
    
    def __init__(self, missing_fields: list):
        self.missing_fields = missing_fields
        super().__init__(f"缺少必填参数: {', '.join(missing_fields)}")


class InterfaceMappingError(AdapterError):
    """接口映射异常"""
    
    def __init__(self, interface_name: str, reason: str):
        self.interface_name = interface_name
        self.reason = reason
        super().__init__(f"接口 {interface_name} 映射失败: {reason}")
