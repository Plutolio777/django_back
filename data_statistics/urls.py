# data_manage/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from data_statistics.views import CalculateUserDataSize, LabelDataSizeTrend, CleanedDataSizeTrend, \
    AbnormalLabelDataTrend

router = DefaultRouter()

urlpatterns = [
    path('data_size/', CalculateUserDataSize.as_view(), name='data_size'),
    path('label_size/', LabelDataSizeTrend.as_view(), name='label_size'),
    path('cleaned_size/', CleanedDataSizeTrend.as_view(), name='cleaned_size'),
    path('error_size/', AbnormalLabelDataTrend.as_view(), name='error_size'),
]


