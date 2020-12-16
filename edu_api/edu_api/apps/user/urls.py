from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from user import views

urlpatterns = [
    path("sign_up/", obtain_jwt_token),  # 登录
    path("token/", verify_jwt_token),
    path("users/", views.UserAPIView.as_view()),  # 注册
    path("captcha/", views.CaptchaAPIView.as_view()),#极验验证码
    path("message/", views.SendMessageAPIView.as_view()),#短信验证码
    re_path("login_phone/", views.PhoneModelViewSet.as_view({'post': 'login_phone'})),  # 短信登录
    re_path("phone_code/", views.PhModelViewSet.as_view({'post': 'phone_code'})),#登录检测手机号
    re_path(r'phone/', views.PhoneViewSet.as_view({'post': 'phone'}))#注册验证手机号是否存在
]
