from django.urls import path,re_path
from rest_framework_jwt.views import obtain_jwt_token

from user import views

urlpatterns = [
    path("login/", obtain_jwt_token),
    path("captcha/", views.CaptchaAPIView.as_view()),
    path("phone_login/", views.CaozuoMessageAPIView.as_view({'post': 'login'})),
    path("register/", views.UserAPIView.as_view()),
    path("message/", views.SendMessageAPIView.as_view()),
    path("check/", views.CaozuoMessageAPIView.as_view({'patch': 'check_code'})),
    path("dele/", views.CaozuoMessageAPIView.as_view({'delete': 'delete_code'})),
    path("ifunique/", views.ifunique.as_view()),
]
