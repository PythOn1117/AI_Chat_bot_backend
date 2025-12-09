from django.urls import path

from chat import views


app_name = 'chat'

urlpatterns = [
    path('api/ask_question', views.QuestionView.as_view(), name='ask_question'),
]