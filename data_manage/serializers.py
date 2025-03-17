import pytz
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .models import DataSet
import os
import pandas as pd
beijing_tz = pytz.timezone('Asia/Shanghai')

class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = '__all__'
        read_only_fields = ['creator']
        extra_kwargs = {
            'data_set_path': {'required': False}  # 允许 PATCH/PUT 时不传文件
        }
        # 标记

    def validate(self, data):
        # 获取请求对象
        request = self.context.get('request', None)

        # 如果请求对象存在且是创建操作
        if request and request.method == 'POST':  # 创建操作时
            return super().validate(data)

        # 如果是更新操作（PATCH 或 PUT）
        elif request and request.method in ['PUT', 'PATCH']:  # 更新操作时
            if 'data_set_path' in data:  # 如果没有提供新的文件
                raise ValidationError('file cannot be modified')
        return data

    def create(self, validated_data):
        """
        重写 create 方法，在数据保存之前自动设置 `type` 字段
        """
        request = self.context.get("request", None)
        # 确保用户已经登录
        if request is None or not request.user.is_authenticated:
            raise AuthenticationFailed("用户未登录，无法创建数据集")

        validated_data['creator'] = request.user.id
        file = validated_data.get('data_set_path', None)
        validated_data['origin_path'] = file
        if file:
            # 获取文件扩展名
            file_extension = os.path.splitext(file.name)[1].lower()

            # 判断文件类型并设置 type 字段
            if file_extension == '.csv':
                validated_data['type'] = 'csv'
            elif file_extension in ['.xls', '.xlsx']:
                validated_data['type'] = 'excel'
            else:
                validated_data['type'] = 'unknown'

        # 创建数据集实例
        return super().create(validated_data)

    def to_representation(self, instance):
        # 获取默认的序列化数据
        representation = super().to_representation(instance)
        # 处理日期格式
        if 'create_time' in representation:
            representation['create_time'] = instance.create_time.astimezone(beijing_tz).strftime(settings.DATETIME_FORMAT)
        if 'update_time' in representation:
            representation['update_time'] = instance.update_time.astimezone(beijing_tz).strftime(settings.DATETIME_FORMAT)
        # 拼接绝对路径
        if 'data_set_path' in representation:
            # 拼接完整 URL，基于 MEDIA_URL
            representation['path'] = "/api/static/upload" + representation['data_set_path']

        return representation

    def update(self, instance, validated_data):
        """
        重写更新方法，允许不提供 `data_set_path` 文件时保留原文件。
        """
        # 更新其他字段
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        # 保存并返回更新后的实例
        instance.save()
        return instance