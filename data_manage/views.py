# data_manage/views.py
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import DataSet
from .serializers import DataSetSerializer


class DataSetViewSet(viewsets.ModelViewSet):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer
    pagination_class = LimitOffsetPagination  # 显式指定分页类（如果你想自定义分页行为）

    def get_queryset(self):
        request = self.request
        queryset = DataSet.objects.filter(creator=request.user.id)

        name = request.query_params.get('name', None)
        data_type = request.query_params.get('type', None)

        if name:
            queryset = queryset.filter(name__icontains=name)  # `icontains` 是忽略大小写的模糊查询

        # 根据类型进行查询
        if data_type:
            queryset = queryset.filter(type=data_type)

        return queryset
