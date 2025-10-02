"""
适配器基础抽象类
定义转换上下文和基础接口
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, Set
from dataclasses import dataclass


@dataclass
class TransformContext:
    """转换上下文
    
    Attributes:
        interface_name: 接口名称
        source_params: 源参数字典
        target_params: 目标参数字典
        accepted_keys: 接受的参数键集合
        metadata: 可选的元数据
    """
    interface_name: str
    source_params: Dict[str, Any]
    target_params: Dict[str, Any]
    accepted_keys: Set[str]
    metadata: Optional[Any] = None
    
    def get_source_value(self, key: str, default: Any = None) -> Any:
        """获取源参数值"""
        return self.source_params.get(key, default)
    
    def set_target_value(self, key: str, value: Any) -> None:
        """设置目标参数值"""
        if key in self.accepted_keys:
            self.target_params[key] = value
    
    def has_source_key(self, key: str) -> bool:
        """检查源参数是否包含指定键"""
        return key in self.source_params
    
    def has_target_key(self, key: str) -> bool:
        """检查目标参数是否包含指定键"""
        return key in self.target_params


class ParameterTransformer(ABC):
    """参数转换器基类"""
    
    @abstractmethod
    def can_transform(self, context: TransformContext) -> bool:
        """判断是否可以转换"""
        pass
    
    @abstractmethod
    def transform(self, context: TransformContext) -> TransformContext:
        """执行转换"""
        pass


class ParameterValidator(ABC):
    """参数验证器基类"""
    
    @abstractmethod
    def can_validate(self, context: TransformContext) -> bool:
        """判断是否可以验证"""
        pass
    
    @abstractmethod
    def validate(self, context: TransformContext) -> bool:
        """执行验证"""
        pass


class TransformChain:
    """转换链"""
    
    def __init__(self, transformers: List[ParameterTransformer]):
        self.transformers = transformers
    
    def transform(self, context: TransformContext) -> TransformContext:
        """执行转换链"""
        for transformer in self.transformers:
            if transformer.can_transform(context):
                context = transformer.transform(context)
        return context


class ValidationChain:
    """验证链"""
    
    def __init__(self, validators: List[ParameterValidator]):
        self.validators = validators
    
    def validate(self, context: TransformContext) -> bool:
        """执行验证链"""
        for validator in self.validators:
            if validator.can_validate(context):
                if not validator.validate(context):
                    return False
        return True
