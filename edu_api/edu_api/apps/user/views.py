from django.db import transaction
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as http_status, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from user.models import UserInfo

from edu_api.libs.geetest import GeetestLib
from user.serializers import UserModelSerializer
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


class UserGenericAPIView(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):

    def get_queryset(self):
        return UserInfo.objects.all()

    serializer_class = UserModelSerializer
    lookup_field = 'id'

    def sign_up(self, request, *args, **kwargs):
        _ = self
        with transaction.atomic():
            return self.create(request, *args, **kwargs)


class UserViewSet(ModelViewSet):
    def sign_in(self, request, *args, **kwargs):
        _ = self
        username = request.data.get('username')
        password = request.data.get('password')
        # print(username, password, 35)
        user = UserInfo.objects.filter(username=username, password=password)
        if user:
            return Response({
                'message': '登录成功',
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': '登录失败',
            }, status=status.HTTP_400_BAD_REQUEST)

    def sign_up(self, request, *args, **kwargs):
        _ = self
        username = request.data.get('username')
        name = request.data.get('name')
        password = request.data.get('password')
        gender = request.data.get('gender')
        user = UserInfo.objects.filter(username=username)
        print(54, gender, username, name, password)
        if user:
            return Response({
                'message': '用户名已存在',
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            UserInfo.objects.create(username=username, password=password, name=name, gender=gender)
            return Response({
                'message': '注册成功'
            }, status=status.HTTP_200_OK)
