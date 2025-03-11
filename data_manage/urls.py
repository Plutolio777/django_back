# data_manage/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DataSetViewSet, DataSetFileByIdView

router = DefaultRouter()
router.register(r'datasets', DataSetViewSet)  # 将视图集注册到路由中

urlpatterns = [
    path('', include(router.urls)),  # 将路由集成到项目中
    path('data_detail/', DataSetFileByIdView.as_view(), name='datasets'),
]


