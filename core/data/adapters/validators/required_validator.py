"""
必填参数验证器
"""

from typing import Any, Dict, Optional
from .base import BaseValidator
from ..base import TransformContext
from ..exceptions import RequiredParameterError


class RequiredValidator(BaseValidator):
    """必填参数验证器"""
    
    def __init__(self):
        super().__init__()
        self.required_fields = []
    
    def can_validate(self, context: TransformContext) -> bool:
        """检查是否可以验证"""
        return bool(self.required_fields) or (context.metadata and context.metadata.required_params)
    
    def validate(self, context: TransformContext) -> bool:
        """执行必填参数验证"""
        # 获取必填字段列表
        required_fields = self.required_fields
        if context.metadata and context.metadata.required_params:
            required_fields = list(set(required_fields + context.metadata.required_params))
        
        # 检查必填字段
        missing_fields = []
        for field in required_fields:
            if field not in context.target_params or self._is_empty_value(context.target_params.get(field)):
                missing_fields.append(field)
        
        if missing_fields:
            raise RequiredParameterError(missing_fields)
        
        return True
