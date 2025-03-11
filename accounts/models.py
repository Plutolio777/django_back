from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import Group


from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/%Y%m%d/', null=True, blank=True, verbose_name='头像')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='电话号码')

    # 解决 groups 和 user_permissions 冲突
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",  # 确保 related_name 唯一
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",  # 确保 related_name 唯一
        blank=True
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
