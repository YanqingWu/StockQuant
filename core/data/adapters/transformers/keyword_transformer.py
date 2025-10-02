"""
关键词转换器
"""

from typing import Any, Dict, Optional
from .base import BaseTransformer
from ..base import TransformContext


class KeywordTransformer(BaseTransformer):
    """关键词转换器"""
    
    KEYWORD_KEYS = ["keyword", "name"]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.max_length = self._get_config_value('max_length', 100)
        self.strip_whitespace = self._get_config_value('strip_whitespace', True)
    
    def can_transform(self, context: TransformContext) -> bool:
        """检查有关键词需要转换"""
        return any(key in context.source_params for key in self.KEYWORD_KEYS)
    
    def transform(self, context: TransformContext) -> TransformContext:
        """执行关键词转换"""
        for key in self.KEYWORD_KEYS:
            if context.has_source_key(key):
                value = context.source_params[key]
                if value is not None:
                    converted_value = self._convert_keyword(value)
                    context.set_target_value(key, converted_value)
        
        return context
    
    def _convert_keyword(self, value: Any) -> Any:
        """转换关键词格式"""
        def convert_one(v: Any) -> Any:
            if not isinstance(v, str):
                return v
            
            if self.strip_whitespace:
                v = v.strip()
            
            if len(v) > self.max_length:
                v = v[:self.max_length]
            
            return v
        
        return self._apply_to_value(value, convert_one)
