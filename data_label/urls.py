# data_manage/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimeDataMarkTaskViewSet, UnsupervisedDataMarkTaskViewSet, CleanedDataList

router = DefaultRouter()
router.register(r'time', TimeDataMarkTaskViewSet)  # 将视图集注册到路由中
router.register(r'unsupervised', UnsupervisedDataMarkTaskViewSet)  # 将视图集注册到路由中

router.register(r'cleaned', CleanedDataList)
urlpatterns = [
    path('', include(router.urls)),  # 将路由集成到项目中
]


