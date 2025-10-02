"""
参数值映射转换器
"""

from typing import Any, Dict, Optional
from .base import BaseTransformer
from ..base import TransformContext


class ValueMapper(BaseTransformer):
    """参数值映射转换器"""
    
    def __init__(self):
        super().__init__()
        self.value_mappings = {}
    
    def can_transform(self, context: TransformContext) -> bool:
        """检查是否有需要映射的参数值"""
        return bool(self.value_mappings)
    
    def transform(self, context: TransformContext) -> TransformContext:
        """执行参数值映射"""
        for field, enum_map in self.value_mappings.items():
            if context.has_source_key(field):
                value = context.get_source_value(field)
                mapped_value = self._apply_to_value(value, lambda v: self._map_value(v, enum_map))
                context.set_target_value(field, mapped_value)
        
        return context
    
    def _map_value(self, value: Any, enum_map: Dict[str, Any]) -> Any:
        """映射单个值"""
        if isinstance(value, str):
            s = value.strip()
            # 枚举映射按大小写不敏感匹配
            lower_map = {str(k).lower(): enum_map[k] for k in enum_map}
            return lower_map.get(s.lower(), value)
        return value
