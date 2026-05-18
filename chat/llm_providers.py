from openai import OpenAI
import logging

logger = logging.getLogger(__name__)


class LlmProviderFactory:
    """大语言模型提供商工厂类"""

    @staticmethod
    def create_client(config):
        """
        根据配置创建 OpenAI 客户端

        Args:
            config: ModelConfig 实例

        Returns:
            OpenAI 客户端实例
        """
        return OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout,
            max_retries=config.max_retries
        )