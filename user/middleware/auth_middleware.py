from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse

from user.models import User

no_auth_url = [
    '/user/user_login'
]


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("AuthenticationMiddleware start")
        if request.path not in no_auth_url:
            if not request.session.get('user', None) or not User.objects.filter(id=request.session['user'].id).exists():
                return JsonResponse({'code': 1, 'msg': "请先登录再执行操作"})

        response = self.get_response(request)

        return response
