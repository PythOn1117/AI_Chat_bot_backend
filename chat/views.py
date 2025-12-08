import json

from django.shortcuts import render
from django.views import View

from chat.service import LlmClient
from utils.response_utils import set_response, set_error

from chat.prompt.completion_service import completion_msg


# Create your views here.

class QuestionView(View):
    def post(self, request):
        params = json.loads(request.body)
        question = params.get('question')
        if not question:
            return set_error("问题不能为空")
        stream = params.get('stream', False)
        try:
            content = LlmClient().chat_completion(completion_msg(question), stream=stream)
        except Exception as e:
            return set_error("请求失败")

        return set_response({"data": content})



