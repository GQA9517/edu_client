import random
import re

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user.models import UserInfo
from user.service import get_user_by_account


class UserModelSerializer(ModelSerializer):

    token = serializers.CharField(max_length=1024, read_only=True, help_text="用户token")
    sms_code = serializers.CharField(max_length=1024, write_only=True)

    class Meta:
        model = UserInfo
        fields = ("phone", "password", "id", "username", "token", "sms_code")

        extra_kwargs = {
            "phone": {
                "write_only": True
            },
            "password": {
                "write_only": True
            },
            "id": {
                "read_only": True
            },
            "username": {
                "read_only": True
            },
        }

    def validate(self, attrs):
        """前端参数校验"""
        phone = attrs.get("phone")
        password = attrs.get("password")
        # 获取用户输入的验证码
        sms_code = attrs.get("sms_code")

        # 验证手机号
        if not re.match(r'^1(3[0-9]|4[01456879]|5[0-3,5-9]|6[2567]|7[0-8]|8[0-9]|9[0-3,5-9])\d{8}$', phone):
            raise serializers.ValidationError('手机号格式不正确')

        # 验证密码  最少8位 两到三种字符
        if not re.match(r'^(?![0-9]+$)(?![a-z]+$)(?![A-Z]+$)(?!([^(0-9a-zA-Z)])+$).{8,20}$', password):
            raise serializers.ValidationError('密码格式不正确,密码格式为包含数字, 英文, 字符中的两种以上，且长度为8-20')
        # 验证手机号是否已存在
        try:
            user = get_user_by_account(phone)
        except UserInfo.DoesNotExist:
            user = None

        if user:
            raise serializers.ValidationError("手机号已注册")

        # 验证手机号对应的验证码是否正确
        # 限制总共可以验证多少次 3次
        redis_connection = get_redis_connection("sms_code")
        phone_code = redis_connection.mget("mobile_%s" % phone)[0].decode('utf-8')
        if sms_code != phone_code:
            raise serializers.ValidationError("验证码错误")
        # 成功验证码后需要及时删除验证码

        return attrs

    def create(self, validated_data):
        """用户信息设置"""
        # 获取密码  对密码进行加密
        password = validated_data.get("password")
        hash_pwd = make_password(password)
        print(hash_pwd)

        # 处理用户名  设置默认值  随机生成字符串  手机号
        phone = validated_data.get("phone")

        # 随机生成名字
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        name = ''.join(random.sample(alphabet, 5))

        # 为用户添加数据
        user = UserInfo.objects.create(
            phone=phone,
            username=name,
            password=hash_pwd,
            email=phone + '@163.com'
        )

        # 为注册成功的用户生成token  完成自动登录
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        return user
