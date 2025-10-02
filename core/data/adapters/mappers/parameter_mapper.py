"""
参数映射器
"""

from typing import Any, Dict, Optional
from core.logging import get_logger

logger = get_logger(__name__)


class ParameterMapper:
    """参数映射器"""
    
    def __init__(self, config_loader=None):
        self.config_loader = config_loader
        self.mappings = {}
        if config_loader:
            try:
                # 从配置加载器中加载映射配置
                config = config_loader.load_config()
                self.mappings = config.parameter_mappings
            except Exception as e:
                logger.warning(f"加载参数映射配置失败: {e}")
    
    def map_parameters(self, interface_name: str, params: Dict[str, Any]) -> tuple:
        """映射参数到目标接口"""
        mapping_config = self.mappings.get(interface_name)
        if not mapping_config:
            raise ValueError(f"未找到接口映射配置: {interface_name}")
        
        # 新的配置格式：直接使用接口名作为目标接口
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
    
    def _apply_special_handling(self, interface_name: str, mapped_params: Dict[str, Any], original_params: Dict[str, Any]) -> None:
        """应用特殊处理逻辑 - 基于参数特征智能处理，避免硬编码接口名称"""
        
        # 1. 处理年份参数的特殊逻辑（基于参数特征检测）
        self._handle_year_parameters(mapped_params)
        
        # 2. 处理股票代码格式转换（基于示例参数智能检测）
        self._handle_symbol_format_conversion(interface_name, mapped_params)
        
        # 3. 处理日期格式转换（基于参数特征检测）
        self._handle_date_format_conversion(interface_name, mapped_params)
    
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
    
    def _handle_symbol_format_conversion(self, interface_name: str, mapped_params: Dict[str, Any]) -> None:
        """处理股票代码格式转换 - 基于示例参数智能检测"""
        if "symbol" not in mapped_params:
            return
            
        symbol_value = mapped_params["symbol"]
        if not hasattr(symbol_value, 'market'):  # 不是StockSymbol对象
            return
        
        # 通过接口元数据获取示例参数来智能检测格式
        target_format = self._detect_symbol_format_from_metadata(interface_name)
        
        if target_format == "lowercase_prefix":
            market_lower = symbol_value.market.lower()
            mapped_params["symbol"] = f"{market_lower}{symbol_value.code}"
            logger.debug(f"{interface_name}: 转换股票代码为小写前缀格式: {mapped_params['symbol']}")
        elif target_format == "code":
            mapped_params["symbol"] = symbol_value.code
            logger.debug(f"{interface_name}: 转换股票代码为纯代码格式: {mapped_params['symbol']}")
        elif target_format == "us_prefix":
            mapped_params["symbol"] = f"105.{symbol_value.code}"
            logger.debug(f"{interface_name}: 转换股票代码为105.前缀格式: {mapped_params['symbol']}")
        else:
            mapped_params["symbol"] = symbol_value.to_dot()
            logger.debug(f"{interface_name}: 保持股票代码为点格式: {mapped_params['symbol']}")
    
    def _handle_date_format_conversion(self, interface_name: str, mapped_params: Dict[str, Any]) -> None:
        """处理日期格式转换 - 基于参数特征智能检测"""
        # 检测需要紧凑日期格式的接口（通过示例参数特征判断）
        if self._needs_compact_date_format(interface_name):
            for date_key in ["start_date", "end_date"]:
                if date_key in mapped_params and mapped_params[date_key]:
                    converted_date = self._convert_date(mapped_params[date_key], "compact")
                    mapped_params[date_key] = converted_date
                    logger.debug(f"{interface_name}: 转换{date_key}为紧凑格式: {converted_date}")
    
    def _detect_symbol_format_from_metadata(self, interface_name: str) -> str:
        """从接口元数据中检测股票代码格式"""
        # 这里应该通过接口元数据获取示例参数，然后分析格式
        # 暂时返回默认格式，实际实现需要访问接口元数据
        return "dot"
    
    def _needs_compact_date_format(self, interface_name: str) -> bool:
        """检测接口是否需要紧凑日期格式"""
        # 这里应该通过接口元数据获取示例参数，然后分析日期格式
        # 暂时返回False，实际实现需要访问接口元数据
        return False
    
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
    
    def _convert_date(self, date_value: str, target_format: str) -> str:
        """转换日期格式"""
        if target_format == "compact":
            # 移除连字符
            return date_value.replace("-", "")
        return date_value
