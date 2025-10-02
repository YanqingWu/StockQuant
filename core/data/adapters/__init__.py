"""
参数适配器模块
提供统一的参数转换、映射和验证功能
"""

from .base import TransformContext, ParameterTransformer, ParameterValidator
from .akshare_adapter import AkshareStockParamAdapter
from .standard_params import StandardParams
from .stock_symbol import StockSymbol
from .utils import to_standard_params, adapt_params_for_interface
from .conversion_rules import ConversionRules
from .param_normalizer import ParamNormalizer
from .exceptions import (
    AdapterError, ParameterValidationError, FormatConversionError,
    RequiredParameterError, InterfaceMappingError
)

__all__ = [
    'TransformContext',
    'ParameterTransformer', 
    'ParameterValidator',
    'AkshareStockParamAdapter',
    'StandardParams',
    'StockSymbol',
    'to_standard_params',
    'adapt_params_for_interface',
    'ConversionRules',
    'ParamNormalizer',
    'AdapterError',
    'ParameterValidationError',
    'FormatConversionError',
    'RequiredParameterError',
    'InterfaceMappingError'
]
