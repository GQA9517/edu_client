# 定义jwt的返回值
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from user.models import UserInfo


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        "token": token,
        "username": user.username,
        "user_id": user.id,
        "email": user.email
    }


def get_user_by_account(account):
    try:
        user = UserInfo.objects.filter(Q(username=account) | Q(phone=account) | Q(email=account)).first()
    except UserInfo.DoesNotExist:
        return None
    else:
        return user


class UserAuthentication(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        根据账号来获取用户对象
        :param request: 请求对象
        :param username: 前端输入的登陆条件 手机号 用户名
        :param password:
        :param kwargs:
        :return:
        """
        user = get_user_by_account(username)
        if user and user.check_password(password) and user.is_authenticated:
            return user
        else:
            return None
