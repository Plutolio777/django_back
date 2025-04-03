# data_manage/views.py
import os.path
import shutil

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import JSONParser, MultiPartParser

from utils import tools
from .models import DataSet
from .serializers import DataSetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import DataSet
import pandas as pd
from rest_framework.permissions import IsAuthenticated


class DataSetViewSet(viewsets.ModelViewSet):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer
    pagination_class = LimitOffsetPagination  # 显式指定分页类（如果你想自定义分页行为）
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser]

    def get_queryset(self):
        request = self.request
        queryset = DataSet.objects.filter(creator=request.user.id)

        name = request.query_params.get('name', None)
        data_type = request.query_params.get('type', None)

        if name:
            queryset = queryset.filter(name__icontains=name)  # `icontains` 是忽略大小写的模糊查询

        # 根据类型进行查询
        if data_type:
            queryset = queryset.filter(type__in=data_type.split(','))

        return queryset.order_by("-update_time")

    # 新增一个删除方法，支持根据查询参数删除
    @action(detail=False, methods=['delete'], url_path='')
    def delete_by_query(self, request, *args, **kwargs):
        # 获取查询参数中的 id
        dataset_id = request.query_params.get('id', None)

        if not dataset_id:
            return Response({"error": "请提供数据集 ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 获取指定 ID 的 DataSet
            dataset = DataSet.objects.get(pk=dataset_id)
        except DataSet.DoesNotExist:
            raise NotFound("指定的 DataSet 未找到")

        # 确保用户只能删除自己创建的数据集
        if dataset.creator != request.user.id:
            raise PermissionDenied("你不能删除其他用户的数据集")

        dataset.delete()
        return Response({"message": "数据集已成功删除"}, status=status.HTTP_204_NO_CONTENT)


class DataSetFileByIdView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser]

    def get(self, request):
        # 获取查询参数中的 id、limit 和 offset
        dataset_id = request.query_params.get('id', None)
        limit = int(request.query_params.get('limit', 10))  # 默认每次返回10条
        offset = int(request.query_params.get('offset', 0))  # 默认从第0条开始

        if not dataset_id:
            return Response({"error": "请提供数据集 ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 获取指定 ID 的 DataSet
            dataset = DataSet.objects.get(pk=dataset_id)
        except DataSet.DoesNotExist:
            raise NotFound("指定的 DataSet 未找到")

        # 获取文件路径
        file_path = os.path.normpath(dataset.data_set_path.path)

        # 读取 CSV 或 Excel 文件
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)  # 默认第一行作为表头
            elif file_path.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path)  # 默认第一行作为表头
            elif file_path.endswith(('.zip', '.tar', '.gz', '.bz2')):
                # 尝试解压文件
                from django_back.settings import MEDIA_ROOT
                input_dir = os.path.join(MEDIA_ROOT, "data_sets", "unzip", dataset_id)
                if not os.path.exists(input_dir):
                    os.makedirs(input_dir)
                    shutil.copy2(file_path, input_dir)
                    tools.try_unzip_files(input_dir)
                datas = []
                for file in os.listdir(input_dir):
                    if file.endswith(('.zip', '.tar', '.gz', '.bz2')):
                        continue
                    final_path = os.path.join(input_dir, file)
                    media_url = tools.media_path_to_url(final_path)
                    datas.append({
                        "文件名称": file,
                        "file_path": media_url
                    })
                return Response({
                    "id": dataset.id,
                    "name": dataset.name,
                    "headers": ["文件名称"],  # 返回表头
                    "data": datas,  # 返回分页后的数据
                    "total_rows": len(datas),  # 总行数，便于前端分页
                    "limit": limit,
                    "offset": offset,
                    "type": "files"
                })
            else:
                return Response({"error": "文件类型不支持"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"文件读取失败: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 获取表头
        headers = list(df.columns)

        # 应用分页（避免一次性返回所有数据）
        paginated_data = df.iloc[offset:offset + limit].to_dict(orient='records')

        return Response({
            "id": dataset.id,
            "name": dataset.name,
            "headers": headers,  # 返回表头
            "data": paginated_data,  # 返回分页后的数据
            "total_rows": len(df),  # 总行数，便于前端分页
            "limit": limit,
            "offset": offset,
            "type": "file"
        })
