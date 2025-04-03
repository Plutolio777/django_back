import os.path
import random
from utils import tools
from django.db import transaction
import pandas as pd
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from data_label.models import TimeFrequencyLabelTask, UnsupervisedLabelTask, CleanedData
from data_label.serializers import TimeFrequencyLabelTaskSerializer, UnsupervisedLabelTaskSerializer, \
    CleanedDataSerializer
from data_label.tasks import time_data_label_execute, unsupervised_data_label_execute
from django_back import settings


class DataMarkTaskBaseViewSet(viewsets.ModelViewSet):
    model = None
    task = None

    def get_queryset(self):
        user = self.request.user
        return (
            self.model.objects.filter(dataset__creator=user.id)
            .select_related("dataset")
        )

    @action(detail=False, methods=['post'])
    def execute(self, request):
        """ 获取当前登录用户信息 """
        task_id = request.data.get("task_id", None)
        task = self.model.objects.filter(id=task_id).first()
        if task is None:
            return Response({"message": "获取任务失败"}, status=status.HTTP_400_BAD_REQUEST)
        # 更新状态为执行中
        if task.status == 1:
            return Response({"message": "任务正在执行中"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            task.status = 1
            task.task_execute_time = timezone.now()
            task.save()
        self.task.delay_on_commit(task_id)

        # 返回响应
        serializer = self.get_serializer(task)
        response_data = serializer.data
        response_data['progress'] = 0  # 初始进度设为0

        return Response(response_data)

    @action(detail=False, methods=['get'])
    def progress(self, request):
        task_id = request.query_params.get("task_id", None)
        print(task_id)
        task = self.model.objects.filter(id=task_id).first()
        if task is None:
            return Response({"message": "获取任务失败"}, status=status.HTTP_400_BAD_REQUEST)
        cost_time = (timezone.now() - task.task_execute_time).seconds
        time_out_time = task.time_out_time

        serializer = self.get_serializer(task)
        response_data = serializer.data
        response_data['progress'] = min(int((cost_time / time_out_time) * 100), 99)  # 初始进度设为0
        return Response(response_data)

    @action(detail=False, methods=['get'])
    def progress_detail(self, request):
        task_id = request.query_params.get("task_id", None)
        task = self.model.objects.filter(id=task_id).first()
        if task is None:
            return Response({"message": "获取任务失败"}, status=status.HTTP_400_BAD_REQUEST)
        # 获取任务输出目录主文件夹
        out_put_path = task.out_put_path
        if not os.path.exists(out_put_path):
            return Response({"message": "输出文件夹不存在"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(task)
        response_data = serializer.data
        response_data["pictures_walet"] = []
        response_data["result_file_content"] = []
        response_data["result_file"] = ""
        # 图片
        filter_map = {}
        pictures_walet_path = os.path.join(out_put_path, "pictures_walet")
        if os.path.exists(pictures_walet_path):
            for file in os.listdir(pictures_walet_path):
                file_path = os.path.join(pictures_walet_path, file)
                media_url = tools.media_path_to_url(file_path)
                response_data["pictures_walet"].append({"title": file, "url": media_url})
                filter_map[file] = media_url

        result_file_path = os.path.join(out_put_path, "classification_results_1.xlsx")
        if os.path.exists(result_file_path):
            df = pd.read_excel(result_file_path, header=0)
            datas = df.to_dict('records')
            for row in datas:
                file_path, label = row.get("FileName"), row.get("Label")
                filename = os.path.basename(file_path)
                if filename in filter_map:
                    response_data["result_file_content"].append(
                        {"FileName": filename, "FilePath": filter_map.get(filename), "Label": label})
            response_data["result_file"] = tools.media_path_to_url(result_file_path)
        response_data["result_file_size"] = len(response_data["result_file_content"])
        response_data["pictures_walet"] = response_data["pictures_walet"][:29]
        return Response(response_data)


# Create your views here.
class TimeDataMarkTaskViewSet(DataMarkTaskBaseViewSet):
    task = time_data_label_execute
    model = TimeFrequencyLabelTask
    queryset = TimeFrequencyLabelTask.objects.all()
    serializer_class = TimeFrequencyLabelTaskSerializer
    pagination_class = LimitOffsetPagination  # 显式指定分页类（如果你想自定义分页行为）
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser]


class UnsupervisedDataMarkTaskViewSet(DataMarkTaskBaseViewSet):
    task = unsupervised_data_label_execute
    model = UnsupervisedLabelTask
    queryset = UnsupervisedLabelTask.objects.all()
    serializer_class = UnsupervisedLabelTaskSerializer
    pagination_class = LimitOffsetPagination  # 显式指定分页类（如果你想自定义分页行为）
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser]


class CleanedDataList(viewsets.ModelViewSet):
    queryset = CleanedData.objects.all()
    serializer_class = CleanedDataSerializer
    pagination_class = LimitOffsetPagination  # 显式指定分页类（如果你想自定义分页行为）
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser]

    def get_queryset(self):
        user = self.request.user
        return (
            CleanedData.objects.filter(dataset__creator=user.id).filter(is_executed=True)
            .select_related("dataset")
        )

    @action(detail=False, methods=['get'])
    def data_detail(self, request):
        task_id = request.query_params.get("task_id", None)
        task = CleanedData.objects.filter(id=task_id).first()
        if task is None:
            return Response({"message": "获取任务失败"}, status=status.HTTP_400_BAD_REQUEST)
        # 获取任务输出目录主文件夹
        out_put_path = task.out_put_path
        if not os.path.exists(out_put_path):
            return Response({"message": "输出文件夹不存在"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(task)
        response_data = serializer.data
        response_data["result_file_content"] = []
        response_data["result_file"] = ""
        # 图片
        filter_map = {}
        pictures_walet_path = os.path.join(out_put_path, "pictures_walet")
        if os.path.exists(pictures_walet_path):
            for file in os.listdir(pictures_walet_path):
                file_path = os.path.join(pictures_walet_path, file)
                media_url = tools.media_path_to_url(file_path)
                filter_map[file] = media_url

        result_file_path = os.path.join(out_put_path, "classification_results_1.xlsx")
        if os.path.exists(result_file_path):
            df = pd.read_excel(result_file_path, header=0)
            datas = df.to_dict('records')
            for row in datas:
                file_path, label = row.get("FileName"), row.get("Label")
                filename = os.path.basename(file_path)
                if filename in filter_map and "正常" == label:
                    response_data["result_file_content"].append(
                        {"FileName": filename, "FilePath": filter_map.get(filename), "Label": label})
            response_data["result_file"] = tools.media_path_to_url(result_file_path)
        response_data["result_file_size"] = len(response_data["result_file_content"])
        return Response(response_data)
