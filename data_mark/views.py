# Create your views here.


from django.core.files import File
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from data_manage.models import DataSet
from .models import TimeFrequencyMarkingRecord
from .serializers import TimeFrequencyMarkingRecordSerializer


class SaveDataSetToRecord(APIView):

    def post(self, request):
        # 获取前端传来的数据集ID
        data_set_id = request.data.get('data_set_id')

        if not data_set_id:
            return Response({"error": "DataSet ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取 DataSet 对象
        data_set = get_object_or_404(DataSet, id=data_set_id)

        # 获取 DataSet 中的文件路径
        file_path = data_set.data_set_path.path  # 获取本地文件路径

        try:
            # 以二进制模式打开文件
            with open(file_path, 'rb') as file:
                # 创建 File 对象
                django_file = File(file)

                # 创建并保存 TimeFrequencyMarkingRecord 实例
                record = TimeFrequencyMarkingRecord.objects.create(
                    data_set_id=data_set.id,  # 将对应的 DataSet ID 赋值
                    input_file=django_file  # 保存文件到 input_file
                )

            # 序列化并返回创建的 Record 实例
            serializer = TimeFrequencyMarkingRecordSerializer(record)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
