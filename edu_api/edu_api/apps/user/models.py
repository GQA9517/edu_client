from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserInfo(AbstractUser):
    """用户模型"""
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, unique=True)
    user_head = models.ImageField(upload_to="user", verbose_name="用户头像", blank=True, null=True)

    class Meta:
        db_table = "bz_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username