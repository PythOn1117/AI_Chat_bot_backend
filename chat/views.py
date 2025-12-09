import json
import logging
import traceback

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from chat.service import LlmClient
from utils.response_utils import set_response, set_error



# Create your views here.

logger = logging.getLogger(__name__)


class QuestionView(View):
    def get(self, request: WSGIRequest):
        return set_response({"message": "success"})

    def post(self, request: WSGIRequest):
        params = json.loads(request.body)
        question = params.get('question')
        if not question:
            return set_error("问题不能为空")
        stream = params.get('stream', False)

        user = request.session.get("user")
        try:
            content = LlmClient().chat_completion(user, question, stream=stream)
        except Exception as e:
            logger.error(traceback.format_exc())
            return set_error("请求失败")

        return set_response({"data": content})



