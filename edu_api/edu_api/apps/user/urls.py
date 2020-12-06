from django.urls import path,re_path
from rest_framework_jwt.views import obtain_jwt_token

from user import views

urlpatterns = [
    path("login/", obtain_jwt_token),
    path("captcha/", views.CaptchaAPIView.as_view()),
    re_path(r'^users/',views.UserViewSet.as_view({'post':'sign_in'})),#登录
    re_path(r'^user/',views.UserViewSet.as_view({'post':'sign_up'})),#注册
]
