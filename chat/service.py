import logging
from django.conf import settings
from typing import List, Dict
from openai import OpenAI

logger = logging.getLogger(__name__)


class LlmClient:
    def __init__(self):
        if not settings.DEEPSEEK_API_KEY:
            logger.error('DEEPSEEK_API_KEY为空')
            raise Exception("模型初始化有误")

        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
            timeout=30,
            max_retries=2,
        )

    def chat_completion(self, message: List[Dict], stream=False):
        try:
            response = self.client.chat.completions.create(
                messages=message,
                model="deepseek-chat",
                stream=stream,
                max_tokens=1024,
                temperature=0.7,
            )
            content = response.choices[0].message.content
            logger.info(f"DeepSeek API 请求成功， tokens: {response.usage.total_tokens}")
            return content
        except Exception as e:
            logger.error(e)
            raise e