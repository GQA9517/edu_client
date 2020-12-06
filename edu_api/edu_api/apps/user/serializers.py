from rest_framework import serializers
from user.models import UserInfo


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('username', 'password','email','phone','user_head')

        extra_kwargs = {
            'username': {
                'max_length': 20,
                'min_length': 2,
            },
            'password': {
                'max_length': 10,
                'min_length': 3,
            }
        }

