"""
特殊处理转换器
"""

from typing import Any, Dict, Optional
from .base import BaseTransformer
from ..base import TransformContext


class SpecialHandler(BaseTransformer):
    """特殊处理转换器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.special_rules = self._get_config_value('special_rules', {})
    
    def can_transform(self, context: TransformContext) -> bool:
        """检查是否需要特殊处理"""
        return context.interface_name in self.special_rules
    
    def transform(self, context: TransformContext) -> TransformContext:
        """执行特殊处理"""
        interface_name = context.interface_name
        if interface_name in self.special_rules:
            rule = self.special_rules[interface_name]
            self._apply_special_rule(context, rule)
        
        return context
    
    def _apply_special_rule(self, context: TransformContext, rule: Dict[str, Any]) -> None:
        """应用特殊规则"""
        rule_type = rule.get('type')
        
        if rule_type == 'year_dependency':
            self._handle_year_dependency(context)
        elif rule_type == 'remove_unsupported_params':
            self._remove_unsupported_params(context, rule.get('unsupported_params', []))
        elif rule_type == 'add_default_params':
            self._add_default_params(context, rule.get('default_params', {}))
    
    def _handle_year_dependency(self, context: TransformContext) -> None:
        """处理年份参数依赖关系"""
        # 特殊处理：如果提供了start_year，必须同时提供end_year
        if context.has_source_key("start_year") and not context.has_source_key("end_year"):
            # 移除start_year参数
            if "start_year" in context.target_params:
                del context.target_params["start_year"]
        elif context.has_source_key("end_year") and not context.has_source_key("start_year"):
            # 移除end_year参数
            if "end_year" in context.target_params:
                del context.target_params["end_year"]
    
    def _remove_unsupported_params(self, context: TransformContext, unsupported_params: list) -> None:
        """移除不支持的参数"""
        for param in unsupported_params:
            if param in context.target_params:
                del context.target_params[param]
    
    def _add_default_params(self, context: TransformContext, default_params: Dict[str, Any]) -> None:
        """添加默认参数"""
        for param, value in default_params.items():
            if param in context.accepted_keys and param not in context.target_params:
                context.set_target_value(param, value)
