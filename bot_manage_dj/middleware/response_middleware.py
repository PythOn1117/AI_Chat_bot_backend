from django.http import JsonResponse, StreamingHttpResponse


class APIResponseMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if isinstance(response, dict):
            content_type = response.get('Content-Type', "json")
            if content_type == "json":
                return JsonResponse({"code": response.get("code"), "message": response.get("message"), "data": response.get("data", {})})
            elif content_type == "stream":
                return StreamingHttpResponse(response.get("data"), content_type=content_type)
            else:
                return JsonResponse({"code": 1, "message": "处理接口响应失败"})
        else:
            return response
