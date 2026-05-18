from dataclasses import dataclass
from typing import Optional
from decouple import config
import logging

logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    """模型配置数据类"""
    provider: str  # deepseek, glm, minimax
    api_key: str
    base_url: str
    model: str
    max_tokens: int = 1024
    temperature: float = 0.7
    timeout: int = 30
    max_retries: int = 2


class ModelConfigLoader:
    """模型配置加载器"""

    # 支持的模型提供商
    SUPPORTED_PROVIDERS = ['deepseek', 'glm', 'minimax']

    @classmethod
    def get_default_model(cls) -> str:
        """获取默认模型"""
        return config('DEFAULT_MODEL', default='deepseek')

    @classmethod
    def load_config(cls, provider: str) -> ModelConfig:
        """加载指定模型的配置"""
        provider = provider.lower()

        if provider not in cls.SUPPORTED_PROVIDERS:
            raise ValueError(f"不支持的模型提供商: {provider}")

        prefix = provider.upper()

        try:
            return ModelConfig(
                provider=provider,
                api_key=config(f'{prefix}_API_KEY'),
                base_url=config(f'{prefix}_BASE_URL'),
                model=config(f'{prefix}_MODEL'),
                max_tokens=config(f'{prefix}_MAX_TOKENS', default=1024, cast=int),
                temperature=config(f'{prefix}_TEMPERATURE', default=0.7, cast=float),
                timeout=config(f'{prefix}_TIMEOUT', default=30, cast=int),
                max_retries=config(f'{prefix}_MAX_RETRIES', default=2, cast=int)
            )
        except Exception as e:
            logger.error(f"加载 {provider} 模型配置失败: {str(e)}")
            raise

    @classmethod
    def load_default_config(cls) -> ModelConfig:
        """加载默认模型配置"""
        default_model = cls.get_default_model()
        return cls.load_config(default_model)