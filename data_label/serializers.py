import pytz
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from data_manage.serializers import DataSetSerializer
from .models import DataSet, TimeFrequencyLabelTask, UnsupervisedLabelTask, CleanedData
import os
import pandas as pd
beijing_tz = pytz.timezone('Asia/Shanghai')


class LabelTaskBaseSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        status_map = {
            0: "未执行",
            1: "执行中",
            2: "执行失败",
            3: "已执行"
        }
        # 获取默认的序列化数据
        representation = super().to_representation(instance)
        # 处理日期格式

        if 'label_create_time' in representation:
            representation['label_create_time'] = instance.label_create_time.astimezone(beijing_tz).strftime(settings.DATETIME_FORMAT)
        if 'task_execute_time' in representation and representation['task_execute_time']:
            representation['task_execute_time'] = instance.task_execute_time.astimezone(beijing_tz).strftime(settings.DATETIME_FORMAT)
        representation["status"] = status_map.get(instance.status)
        representation["progress"] = 45
        return representation



class TimeFrequencyLabelTaskSerializer(LabelTaskBaseSerializer):
    dataset = DataSetSerializer(read_only=True)
    class Meta:
        model = TimeFrequencyLabelTask
        fields = '__all__'


class UnsupervisedLabelTaskSerializer(LabelTaskBaseSerializer):
    dataset = DataSetSerializer(read_only=True)
    class Meta:
        model = UnsupervisedLabelTask
        fields = '__all__'

class CleanedDataSerializer(serializers.ModelSerializer):
    dataset = DataSetSerializer(read_only=True)
    class Meta:
        model = CleanedData
        fields = '__all__'

    def to_representation(self, instance):
        # 获取默认的序列化数据
        representation = super().to_representation(instance)
        # 处理日期格式

        if 'label_create_time' in representation:
            representation['label_create_time'] = instance.label_create_time.astimezone(beijing_tz).strftime(settings.DATETIME_FORMAT)
        if 'task_execute_time' in representation and representation['task_execute_time']:
            representation['task_execute_time'] = instance.task_execute_time.astimezone(beijing_tz).strftime(settings.DATETIME_FORMAT)
        return representation