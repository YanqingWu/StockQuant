"""
参数名映射转换器
"""

from typing import Any, Dict, Optional
from .base import BaseTransformer
from ..base import TransformContext


class NameMapper(BaseTransformer):
    """参数名映射转换器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name_mappings = self._get_config_value('name_mappings', {})
    
    def can_transform(self, context: TransformContext) -> bool:
        """检查是否有需要映射的参数名"""
        return bool(self.name_mappings)
    
    def transform(self, context: TransformContext) -> TransformContext:
        """执行参数名映射"""
        for source_key, target_key in self.name_mappings.items():
            if context.has_source_key(source_key) and target_key in context.accepted_keys:
                # 如果目标键已存在，跳过映射
                if not context.has_target_key(target_key):
                    value = context.get_source_value(source_key)
                    context.set_target_value(target_key, value)
        
        return context
