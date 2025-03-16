# data_manage/urls.py
from django.urls import path, include
from .views import DataMarkRecord


urlpatterns = [
    path('', DataMarkRecord.as_view(), name='datasets'),
]


