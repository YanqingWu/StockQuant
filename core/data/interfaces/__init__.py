"""接口模块"""

from .akshare import akshare_provider
from .base import get_api_provider_manager

# 导入日志系统
from core.logging import get_logger

# 模块级logger
logger = get_logger(__name__)

# 为了向后兼容，提供 api_provider_manager 属性
api_provider_manager = get_api_provider_manager()
