from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('user/user_manage', views.UserManageView.as_view(), name='user_manage'),
    path('user/user_login', views.UserLoginView.as_view(), name='login'),
    path('user/user_logout', views.UserLogoutView.as_view(), name='logout'),
]