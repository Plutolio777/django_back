from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from django.utils import timezone

from data_label.models import TimeFrequencyLabelTask, UnsupervisedLabelTask, CleanedData
from data_manage.models import DataSet
from data_statistics.serializers import DataSizeSerializer


class CalculateUserDataSize(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 获取当前登录用户的 ID
        user_id = request.user.id

        # 获取当前日期和一周前的日期
        today = timezone.now()
        one_week_ago = today - timedelta(weeks=1)

        # 获取所有的数据集
        datasets = DataSet.objects.filter(creator=user_id)

        # 计算当前总存储量
        total_size_current_bit = sum(dataset.file_size for dataset in datasets)
        total_size_current_byte = total_size_current_bit / 8  # 转换为字节 (byte)
        total_size_current_human_readable = self.convert_to_readable_size(total_size_current_byte)

        # 获取本周数据集（当前日期到一周前）
        datasets_this_week = DataSet.objects.filter(creator=user_id, create_time__gte=one_week_ago)
        total_size_this_week_bit = sum(dataset.file_size for dataset in datasets_this_week)
        total_size_this_week_byte = total_size_this_week_bit / 8
        total_size_this_week_human_readable = self.convert_to_readable_size(total_size_this_week_byte)

        # 获取上周数据集（一周前到两周前的日期）
        last_week_start = one_week_ago - timedelta(weeks=1)
        datasets_last_week = DataSet.objects.filter(creator=user_id, create_time__gte=last_week_start,
                                                    create_time__lt=one_week_ago)
        total_size_last_week_bit = sum(dataset.file_size for dataset in datasets_last_week)
        total_size_last_week_byte = total_size_last_week_bit / 8
        total_size_last_week_human_readable = self.convert_to_readable_size(total_size_last_week_byte)

        # 计算本周和上周存储量的上升/下降百分比
        if total_size_last_week_byte > 0:
            size_change_percentage = (
                                             abs(total_size_this_week_byte - total_size_last_week_byte) / total_size_last_week_byte) * 100
        else:
            size_change_percentage = 0 if total_size_this_week_byte == 0 else 100

        # 判断存储量是上升还是下降
        if size_change_percentage > 0:
            size_change_type = "上升"
        elif size_change_percentage < 0:
            size_change_type = "下降"
        else:
            size_change_type = "没有变化"

        # 返回最终的响应
        data = {
            'total_data_size_current': total_size_current_byte,
            'total_data_size_current_human_readable': total_size_current_human_readable,
            'total_data_size_this_week': total_size_this_week_byte,
            'total_data_size_this_week_human_readable': total_size_this_week_human_readable,
            'total_data_size_last_week': total_size_last_week_byte,
            'total_data_size_last_week_human_readable': total_size_last_week_human_readable,
            'size_change_percentage': f'{size_change_percentage:.2f}%',
            'size_change_type': size_change_type
        }

        # 返回序列化的结果
        serializer = DataSizeSerializer(data)
        return Response(serializer.data)

    @classmethod
    def convert_to_readable_size(cls, size_in_bytes):
        """
        将字节数转换为易读的格式（KB、MB、GB 等）
        """
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} B"
        elif size_in_bytes < 1024 ** 2:
            return f"{size_in_bytes / 1024:.2f} KB"
        elif size_in_bytes < 1024 ** 3:
            return f"{size_in_bytes / (1024 ** 2):.2f} MB"
        elif size_in_bytes < 1024 ** 4:
            return f"{size_in_bytes / (1024 ** 3):.2f} GB"
        else:
            return f"{size_in_bytes / (1024 ** 4):.2f} TB"


class LabelDataSizeTrend(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 获取当前登录用户的 ID
        user_id = request.user.id

        # 获取当前日期和一周前的日期
        today = timezone.now()
        one_week_ago = today - timedelta(weeks=1)

        # 获取当前所有已标注数据集总量
        total_label_data = TimeFrequencyLabelTask.objects.filter(dataset__creator=user_id).count() + \
                           UnsupervisedLabelTask.objects.filter(dataset__creator=user_id).count()

        # 计算已标注数据集本周总量
        label_data_this_week = TimeFrequencyLabelTask.objects.filter(dataset__creator=user_id,
                                                                     label_create_time__gte=one_week_ago)
        unsupervised_data_this_week = UnsupervisedLabelTask.objects.filter(dataset__creator=user_id,
                                                                           label_create_time__gte=one_week_ago)
        total_label_data_this_week = label_data_this_week.count() + unsupervised_data_this_week.count()

        # 获取上周已标注数据集总量
        last_week_start = one_week_ago - timedelta(weeks=1)
        label_data_last_week = TimeFrequencyLabelTask.objects.filter(dataset__creator=user_id,
                                                                     label_create_time__gte=last_week_start,
                                                                     label_create_time__lt=one_week_ago)
        unsupervised_data_last_week = UnsupervisedLabelTask.objects.filter(dataset__creator=user_id,
                                                                           label_create_time__gte=last_week_start,
                                                                           label_create_time__lt=one_week_ago)
        total_label_data_last_week = label_data_last_week.count() + unsupervised_data_last_week.count()

        # 计算上升/下降百分比
        if total_label_data_last_week > 0:
            size_change_percentage = ((
                                              total_label_data_this_week - total_label_data_last_week) / total_label_data_last_week) * 100
        else:
            size_change_percentage = 0 if total_label_data_this_week == 0 else 100

        # 判断存储量是上升还是下降
        if size_change_percentage > 0:
            size_change_type = "上升"
        elif size_change_percentage < 0:
            size_change_type = "下降"
        else:
            size_change_type = "没有变化"

        # 返回最终的响应
        data = {
            'total_label_data': total_label_data,
            'total_label_data_this_week': total_label_data_this_week,
            'total_label_data_last_week': total_label_data_last_week,
            'size_change_percentage': f'{size_change_percentage:.2f}%',
            'size_change_type': size_change_type
        }

        return Response(data)


class CleanedDataSizeTrend(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 获取当前登录用户的 ID
        user_id = request.user.id

        # 获取当前日期和一周前的日期
        today = timezone.now()
        one_week_ago = today - timedelta(weeks=1)

        # 获取当前所有清洗数据集总量
        total_cleaned_data = CleanedData.objects.filter(dataset__creator=user_id).count()

        # 计算清洗数据集本周总量
        cleaned_data_this_week = CleanedData.objects.filter(dataset__creator=user_id,
                                                            label_create_time__gte=one_week_ago)
        total_cleaned_data_this_week = cleaned_data_this_week.count()

        # 获取上周清洗数据集总量
        last_week_start = one_week_ago - timedelta(weeks=1)
        cleaned_data_last_week = CleanedData.objects.filter(dataset__creator=user_id,
                                                            label_create_time__gte=last_week_start,
                                                            label_create_time__lt=one_week_ago)
        total_cleaned_data_last_week = cleaned_data_last_week.count()

        # 计算上升/下降百分比
        if total_cleaned_data_last_week > 0:
            size_change_percentage = ((
                                              total_cleaned_data_this_week - total_cleaned_data_last_week) / total_cleaned_data_last_week) * 100
        else:
            size_change_percentage = 0 if total_cleaned_data_this_week == 0 else 100

        # 判断存储量是上升还是下降
        if size_change_percentage > 0:
            size_change_type = "上升"
        elif size_change_percentage < 0:
            size_change_type = "下降"
        else:
            size_change_type = "没有变化"

        # 返回最终的响应
        data = {
            'total_cleaned_data': total_cleaned_data,
            'total_cleaned_data_this_week': total_cleaned_data_this_week,
            'total_cleaned_data_last_week': total_cleaned_data_last_week,
            'size_change_percentage': f'{size_change_percentage:.2f}%',
            'size_change_type': size_change_type
        }

        return Response(data)


class AbnormalLabelDataTrend(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 获取当前登录用户的 ID
        user_id = request.user.id

        # 获取当前日期和一周前的日期
        today = timezone.now()
        one_week_ago = today - timedelta(weeks=1)

        # 获取当前所有异常标注数据（status=2）
        abnormal_label_data_current_time_freq = TimeFrequencyLabelTask.objects.filter(dataset__creator=user_id,
                                                                                      status=2)
        abnormal_label_data_current_unsupervised = UnsupervisedLabelTask.objects.filter(dataset__creator=user_id,
                                                                                        status=2)

        # 计算所有异常数据的总量
        total_abnormal_label_data_current = abnormal_label_data_current_time_freq.count() + abnormal_label_data_current_unsupervised.count()

        # 获取本周异常数据（status=2，当前日期到一周前）
        abnormal_label_data_this_week_time_freq = TimeFrequencyLabelTask.objects.filter(dataset__creator=user_id,
                                                                                        status=2,
                                                                                        label_create_time__gte=one_week_ago)
        abnormal_label_data_this_week_unsupervised = UnsupervisedLabelTask.objects.filter(dataset__creator=user_id,
                                                                                          status=2,
                                                                                          label_create_time__gte=one_week_ago)

        # 计算本周异常数据的总量
        total_abnormal_label_data_this_week = abnormal_label_data_this_week_time_freq.count() + abnormal_label_data_this_week_unsupervised.count()

        # 获取上周异常数据（status=2，过去一周的数据）
        last_week_start = one_week_ago - timedelta(weeks=1)
        abnormal_label_data_last_week_time_freq = TimeFrequencyLabelTask.objects.filter(dataset__creator=user_id,
                                                                                        status=2,
                                                                                        label_create_time__gte=last_week_start,
                                                                                        label_create_time__lt=one_week_ago)
        abnormal_label_data_last_week_unsupervised = UnsupervisedLabelTask.objects.filter(dataset__creator=user_id,
                                                                                          status=2,
                                                                                          label_create_time__gte=last_week_start,
                                                                                          label_create_time__lt=one_week_ago)

        # 计算上周异常数据的总量
        total_abnormal_label_data_last_week = abnormal_label_data_last_week_time_freq.count() + abnormal_label_data_last_week_unsupervised.count()

        # 计算环比变化百分比
        if total_abnormal_label_data_last_week > 0:
            size_change_percentage = ((
                                                  total_abnormal_label_data_this_week - total_abnormal_label_data_last_week) / total_abnormal_label_data_last_week) * 100
        else:
            size_change_percentage = 0 if total_abnormal_label_data_this_week == 0 else 100

        # 判断异常数据变化方向（上升或下降）
        if size_change_percentage > 0:
            size_change_type = "上升"
        elif size_change_percentage < 0:
            size_change_type = "下降"
        else:
            size_change_type = "没有变化"

        # 返回最终的响应
        data = {
            'total_abnormal_label_data_current': total_abnormal_label_data_current,
            'total_abnormal_label_data_this_week': total_abnormal_label_data_this_week,
            'total_abnormal_label_data_last_week': total_abnormal_label_data_last_week,
            'size_change_percentage': f'{size_change_percentage:.2f}%',
            'size_change_type': size_change_type
        }

        return Response(data)
