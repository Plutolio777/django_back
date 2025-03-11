from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .models import DataSet
import os
import pandas as pd


class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = '__all__'
        read_only_fields = ['creator']  # 标记

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

        # 拼接绝对路径
        if 'data_set_path' in representation:
            # 拼接完整 URL，基于 MEDIA_URL
            representation['path'] = "/api/static/upload" + representation['data_set_path']

        return representation
