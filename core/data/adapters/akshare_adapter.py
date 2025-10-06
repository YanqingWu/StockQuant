"""
Akshare适配器实现
重构后的主适配器类，保持对外接口不变
"""

from typing import Any, Dict, Optional
from .base import TransformContext, TransformChain, ValidationChain
from .transformers import (
    ValueMapper, SymbolTransformer, DateTransformer, 
    TimeTransformer, PeriodTransformer, AdjustTransformer, 
    MarketTransformer, KeywordTransformer, SpecialHandler,
    ParameterMapper
)
from .validators import RequiredValidator, FormatValidator, RangeValidator
from .exceptions import InterfaceMappingError, RequiredParameterError
from core.logging import get_logger

logger = get_logger(__name__)


class AkshareStockParamAdapter:
    """
    Akshare 参数适配器
    """
    
    def __init__(self, interface_mappings: Optional[Dict[str, Any]] = None) -> None:
        """初始化适配器，可选传入接口映射配置"""
        # 初始化参数映射器
        if interface_mappings:
            self.parameter_mapper = ParameterMapper(interface_mappings)
        else:
            self.parameter_mapper = ParameterMapper()
        
        # 添加简单的参数缓存
        self._param_cache = {}
        self._cache_max_size = 100
        
        # 初始化所有transformer实例
        self._value_mapper = ValueMapper()
        self._symbol_transformer = SymbolTransformer()
        self._date_transformer = DateTransformer()
        self._time_transformer = TimeTransformer()
        self._period_transformer = PeriodTransformer()
        self._adjust_transformer = AdjustTransformer()
        self._market_transformer = MarketTransformer()
        self._keyword_transformer = KeywordTransformer()
        self._special_handler = SpecialHandler()
        
        # 初始化转换链
        self.transform_chain = TransformChain([
            self._value_mapper,
            self._symbol_transformer,
            self._date_transformer,
            self._time_transformer,
            self._period_transformer,
            self._adjust_transformer,
            self._market_transformer,
            self._keyword_transformer,
            self._special_handler,
        ])
        
        # 初始化验证链
        self.validation_chain = ValidationChain([
            RequiredValidator(),
            FormatValidator(),
            RangeValidator(),
        ])
    
    def adapt(self, interface_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """适配参数（带缓存）"""
        # 生成简单的缓存键
        cache_key = self._generate_cache_key(interface_name, params)
        
        # 检查缓存
        if cache_key in self._param_cache:
            logger.debug(f"使用缓存的参数: {interface_name}")
            return self._param_cache[cache_key]
        
        # 执行参数适配
        result = self._adapt_without_cache(interface_name, params)
        
        # 缓存结果（限制缓存大小）
        self._cache_result(cache_key, result)
        
        return result
    
    def _adapt_without_cache(self, interface_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """不带缓存的参数适配"""
        # 1. 检查是否为映射接口
        if self.parameter_mapper and self.parameter_mapper.is_mapping_interface(interface_name):
            return self._handle_mapping_interface(interface_name, params)
        
        # 2. 使用基础适配逻辑处理
        return self._adapt_base(interface_name, params)
    
    def _generate_cache_key(self, interface_name: str, params: Dict[str, Any]) -> str:
        """生成缓存键"""
        import hashlib
        import json
        
        # 创建参数的稳定表示
        stable_params = {k: v for k, v in sorted(params.items())}
        param_str = json.dumps(stable_params, sort_keys=True)
        
        # 生成哈希
        hash_obj = hashlib.md5(f"{interface_name}:{param_str}".encode())
        return hash_obj.hexdigest()
    
    def _cache_result(self, cache_key: str, result: Dict[str, Any]) -> None:
        """缓存结果"""
        # 限制缓存大小
        if len(self._param_cache) >= self._cache_max_size:
            # 移除最旧的缓存项
            oldest_key = next(iter(self._param_cache))
            del self._param_cache[oldest_key]
        
        self._param_cache[cache_key] = result
    
    def _handle_mapping_interface(self, interface_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理映射接口"""
        try:
            # 映射到目标接口
            target_interface, mapped_params = self.parameter_mapper.map_parameters(interface_name, params)
            # 参数映射完成
            
            # 使用基础适配器处理映射后的参数
            return self._adapt_base(target_interface, mapped_params)
        
        except Exception as e:
            logger.error(f"接口映射失败: {interface_name}, 错误: {e}")
            raise InterfaceMappingError(interface_name, str(e))
    
    def _adapt_base(self, interface_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """基础适配逻辑（重构版）"""
        from core.data.interfaces.base import get_interface_metadata
        
        try:
            # 1. 获取接口元数据
            metadata = get_interface_metadata(interface_name)
            if not metadata:
                logger.warning(f"未找到接口 {interface_name} 的元数据，使用原始参数")
                return params
            
            # 2. 创建转换上下文
            context = TransformContext(
                interface_name=interface_name,
                source_params=params,
                target_params={},
                accepted_keys=set((metadata.required_params or []) + (metadata.optional_params or [])),
                metadata=metadata
            )
            
            # 3. 执行参数转换（增强错误处理和详细日志）
            try:
                logger.debug(f"开始参数转换: {interface_name}")
                logger.debug(f"源参数: {context.source_params}")
                
                context = self._transform_with_logging(context)
                logger.debug(f"转换后参数: {context.target_params}")
                logger.debug(f"参数转换链执行成功: {interface_name}")
            except Exception as e:
                logger.error(f"参数转换链执行失败: {interface_name}, 错误: {e}")
                # 回退到原始参数
                context.target_params = context.source_params.copy()
            
            # 4. 执行参数验证（增强错误处理和详细日志）
            try:
                logger.debug(f"开始参数验证: {interface_name}")
                validation_result = self._validate_with_logging(context)
                
                if not validation_result:
                    logger.warning(f"参数验证失败: {interface_name}")
                    # 可以选择是否继续使用转换后的参数
                else:
                    logger.debug(f"参数验证通过: {interface_name}")
            except Exception as e:
                logger.error(f"参数验证异常: {interface_name}, 错误: {e}")
            
            return context.target_params
            
        except Exception as e:
            logger.error(f"参数适配失败: {interface_name}, 错误: {e}")
            return params  # 回退到原始参数
    
    def _transform_with_logging(self, context: TransformContext) -> TransformContext:
        """带详细日志的参数转换"""
        for i, transformer in enumerate(self.transform_chain.transformers):
            transformer_name = transformer.__class__.__name__
            
            if transformer.can_transform(context):
                logger.debug(f"  [{i+1}] 执行转换器: {transformer_name}")
                logger.debug(f"      转换前: {context.target_params}")
                
                try:
                    context = transformer.transform(context)
                    logger.debug(f"      转换后: {context.target_params}")
                except Exception as e:
                    logger.error(f"      转换器 {transformer_name} 执行失败: {e}")
                    # 继续执行下一个转换器
            else:
                logger.debug(f"  [{i+1}] 跳过转换器: {transformer_name} (不适用)")
        
        return context
    
    def _validate_with_logging(self, context: TransformContext) -> bool:
        """带详细日志的参数验证"""
        for i, validator in enumerate(self.validation_chain.validators):
            validator_name = validator.__class__.__name__
            
            if validator.can_validate(context):
                logger.debug(f"  [{i+1}] 执行验证器: {validator_name}")
                
                try:
                    result = validator.validate(context)
                    if result:
                        logger.debug(f"      验证通过: {validator_name}")
                    else:
                        logger.warning(f"      验证失败: {validator_name}")
                        return False
                except Exception as e:
                    logger.error(f"      验证器 {validator_name} 执行异常: {e}")
                    return False
            else:
                logger.debug(f"  [{i+1}] 跳过验证器: {validator_name} (不适用)")
        
        return True
