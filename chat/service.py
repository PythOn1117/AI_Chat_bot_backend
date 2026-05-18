import logging
import traceback
from typing import Optional

from django.conf import settings
from openai import OpenAI

from chat.prompt.completion_service import add_content_to_history
from chat.prompt.completion_service import completion_msg, get_history_content
from chat.models_config import ModelConfigLoader, ModelConfig
from chat.llm_providers import LlmProviderFactory

logger = logging.getLogger(__name__)


class LlmClient:
    """大语言模型客户端，支持多模型切换"""

    def __init__(self, model_provider: Optional[str] = None):
        """
        初始化 LLM 客户端

        Args:
            model_provider: 模型提供商 (deepseek/glm/minimax)，None 则使用默认模型
        """
        # 向后兼容：如果传入的 model_provider 不是我们支持的类型，可能是旧的模型名称
        if model_provider and model_provider not in ModelConfigLoader.SUPPORTED_PROVIDERS:
            # 如果是旧的模型名称（如 "deepseek-chat"），尝试推断提供商
            model_provider = self._infer_provider_from_model_name(model_provider)

        provider = model_provider or ModelConfigLoader.get_default_model()

        try:
            self.config = ModelConfigLoader.load_config(provider)
            self.client = LlmProviderFactory.create_client(self.config)
            logger.info(f"初始化 {provider} 模型客户端成功")
        except Exception as e:
            logger.error(f'模型初始化失败: {str(e)}')
            raise Exception(f"模型初始化有误: {str(e)}")

    def _infer_provider_from_model_name(self, model_name: str) -> str:
        """从模型名称推断提供商（用于向后兼容）"""
        if 'deepseek' in model_name.lower():
            return 'deepseek'
        elif 'glm' in model_name.lower():
            return 'glm'
        elif 'minimax' in model_name.lower() or 'abab' in model_name.lower():
            return 'minimax'
        else:
            # 无法推断，返回默认模型
            return ModelConfigLoader.get_default_model()

    def chat_completion(self, user, question, stream=False, model_provider: Optional[str] = None):
        """
        聊天补全

        Args:
            user: 用户对象
            question: 用户问题
            stream: 是否流式输出
            model_provider: 指定模型提供商（覆盖初始化时的设置）

        Returns:
            模型响应内容
        """
        try:
            # 如果指定了新的模型提供商，重新初始化客户端
            if model_provider and model_provider != self.config.provider:
                self.config = ModelConfigLoader.load_config(model_provider)
                self.client = LlmProviderFactory.create_client(self.config)

            history = get_history_content(user)
            message = completion_msg(history, question)

            response = self.client.chat.completions.create(
                messages=message,
                model=self.config.model,
                stream=stream,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
            )
            content = response.choices[0].message.content

            add_content_to_history(user, message, content)
            logger.info(f"{self.config.provider} API 请求成功，tokens: {response.usage.total_tokens}")
            return content
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e