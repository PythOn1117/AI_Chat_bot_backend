import hashlib
import json

from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views import View

from user.models import User


class UserManageView(View):

    def post(self, request):
        data = json.loads(request.body)
        if not data.get('username') or not data.get('password'):
            return JsonResponse({'code': 1, 'msg': "请输入用户名或密码"})
        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({'code': 1, 'msg': "用户名已存在"})
        data['password'] = hashlib.md5(data['password'].encode('utf-8')).hexdigest()
        User.objects.create(**data)
        return JsonResponse({'code': 0, 'msg': "success"})


class UserLoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not User.objects.filter(username=username).exists():
            return JsonResponse({'code': 1, 'msg': "用户不存在"})

        user = User.objects.get(username=username)
        if not user.check_password(password):
            return JsonResponse({'code': 1, 'msg': "密码错误"})

        request.session['user'] = user
        return JsonResponse({'code': 0, 'msg': "登录成功"})


class UserLogoutView(View):
    def post(self, request):
        if 'user' in request.session:
            del request.session['user']
        request.session.flush()
        return JsonResponse({'code': 0, 'msg': "登出成功"})

