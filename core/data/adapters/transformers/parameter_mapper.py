"""
接口映射器
"""

from typing import Any, Dict, Optional, Tuple
from core.logging import get_logger

logger = get_logger(__name__)


class ParameterMapper:
    """参数映射器"""
    
    def __init__(self, mappings: Optional[Dict[str, Any]] = None):
        self.mappings = mappings or {}
    
    def is_mapping_interface(self, interface_name: str) -> bool:
        """检查是否为映射接口"""
        return interface_name in self.mappings
    
    def map_parameters(self, interface_name: str, params: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """映射参数到目标接口"""
        if interface_name not in self.mappings:
            raise ValueError(f"接口 {interface_name} 没有映射配置")
        
        mapping_config = self.mappings[interface_name]
        if not mapping_config:
            raise ValueError(f"接口 {interface_name} 的映射配置为空")
        
        target_interface = interface_name
        parameter_mapping = mapping_config["parameter_mapping"]
        validation = mapping_config.get("validation", {})
        
        # 1. 验证参数
        self._validate_parameters(params, validation)
        
        # 2. 映射参数
        mapped_params = {}
        for source_param, target_param in parameter_mapping.items():
            if source_param in params:
                mapped_params[target_param] = params[source_param]
        
        # 3. 应用默认值
        self._apply_default_values(mapped_params, validation)
        
        # 4. 特殊处理逻辑
        self._apply_special_handling(interface_name, mapped_params, params)
        
        return target_interface, mapped_params
    
    def _validate_parameters(self, params: Dict[str, Any], validation: Dict[str, Any]) -> None:
        """验证参数"""
        for param_name, param_config in validation.items():
            if param_name not in params:
                continue
            
            value = params[param_name]
            
            # 检查必需参数
            if param_config.get("required", False) and value is None:
                raise ValueError(f"参数 {param_name} 是必需的")
            
            # 检查有效值
            valid_values = param_config.get("valid_values", [])
            if valid_values and value not in valid_values:
                raise ValueError(f"参数 {param_name} 的值 {value} 不在有效范围内: {valid_values}")
    
    def _apply_default_values(self, params: Dict[str, Any], validation: Dict[str, Any]) -> None:
        """应用默认值"""
        for param_name, param_config in validation.items():
            if param_name not in params and "default_value" in param_config:
                params[param_name] = param_config["default_value"]
    
    def _apply_special_handling(self, interface_name: str, mapped_params: Dict[str, Any], original_params: Dict[str, Any]) -> None:
        """应用特殊处理逻辑 - 基于参数特征智能处理，避免硬编码接口名称"""
        # 处理年份参数的特殊逻辑（基于参数特征检测）
        self._handle_year_parameters(mapped_params)
    
    def _handle_year_parameters(self, mapped_params: Dict[str, Any]) -> None:
        """处理年份参数的特殊逻辑"""
        # 检测需要成对出现的年份参数
        year_params = ["start_year", "end_year"]
        present_year_params = [p for p in year_params if p in mapped_params]
        
        if len(present_year_params) == 1:
            # 如果只有一个年份参数，移除它以避免接口调用失败
            param_to_remove = present_year_params[0]
            logger.warning(f"年份参数需要成对出现，移除孤立的{param_to_remove}参数")
            del mapped_params[param_to_remove]
