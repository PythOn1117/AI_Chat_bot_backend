from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('api/user_manage', views.UserManageView.as_view(), name='user_manage'),
    path('api/user_login', views.UserLoginView.as_view(), name='login'),
    path('api/user_logout', views.UserLogoutView.as_view(), name='logout'),
]