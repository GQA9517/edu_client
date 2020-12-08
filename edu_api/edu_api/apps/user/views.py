import random

from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as http_status, status
from rest_framework.generics import CreateAPIView
from django_redis import get_redis_connection
from rest_framework.viewsets import ModelViewSet

from edu_api.libs.geetest import GeetestLib
from edu_api.settings import constants
from edu_api.utils.send_msg import Message
from user.models import UserInfo
from user.serializer import UserModelSerializer
from user.service import get_user_by_account

pc_geetest_id = "759d5436a6bfe1e0a94d222e9452097b"
pc_geetest_key = "2061a99f3c25e50989a0c04536132953"


class CaptchaAPIView(APIView):
    """极验验证码"""

    user_id = 1
    status = False

    def get(self, request):
        """获取验证码"""
        username = request.query_params.get("username")
        user = get_user_by_account(username)
        if user is None:
            return Response({"message": "该用户不存在"},
                            status=http_status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id

        # 通过极验类生成验证码对象
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        response_str = gt.get_response_str()
        return Response(response_str)

    def post(self, request):
        """验证验证码"""

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.data.get("geetest_challenge")
        validate = request.data.get("geetest_validate")
        seccode = request.data.get("geetest_seccode")
        # 判断用户是否存在
        if self.user_id:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        print(result)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)


class UserAPIView(CreateAPIView):
    """用户注册"""
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer


# class UserViewSet(ModelViewSet):
#     def sign_in(self, request, *args, **kwargs):
#         _ = self
#         username = request.data.get('username')
#         password = request.data.get('password')
#         phone = request.data.get('phone')
#         # print(username, password, 35)
#         user = UserInfo.objects.filter(username=username, password=password,phone=phone)
#         if user:
#             return Response({
#                 'message': '登录成功',
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({
#                 'message': '登录失败',
#             }, status=status.HTTP_400_BAD_REQUEST)
#
#     def sign_up(self, request, *args, **kwargs):
#         _ = self
#         username = request.data.get('username')
#         password = request.data.get('password')
#         phone = request.data.get('phone')
#         user = UserInfo.objects.filter(username=username,phone=phone)
#         print(99,username, password,phone)
#         if user:
#             return Response({
#                 'message': '用户名已存在',
#             }, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             UserInfo.objects.create(username=username, password=password, phone=phone)
#             return Response({
#                 'message': '注册成功'
#             }, status=status.HTTP_200_OK)


class SendMessageAPIView(APIView):

    def get(self, request, *args, **kwargs):
        # 获取redis连接
        redis_connection = get_redis_connection("sms_code")

        # 判断手机号在60s内是否发送过短信
        phone = request.query_params.get("phone")
        phone_code = redis_connection.get("sms_%s" % phone)
        if phone_code is not None:
            return Response({"message": "您已经在60s内发送过短信了~"}, status=http_status.HTTP_400_BAD_REQUEST)

        # 生成随机的短信验证码
        code = random.randint(100000, 999999)
        # 将验证码保存至redis
        redis_connection.setex("sms_%s" % phone, constants.SMS_EXPIRE_TIME, code)
        redis_connection.setex("mobile_%s" % phone, constants.PHONE_EXPIRE_TIME, code)

        # 调用方法  完成短信的发送
        try:
            msg = Message(constants.API_KEY)
            msg.send_message(phone, code)
        except:
            return Response({"message": "短信发送失败"}, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 将发送的结果响应回去
        return Response({"message": "短信发送成功"}, status=http_status.HTTP_200_OK)
