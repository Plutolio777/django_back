# data_manage/serializers.py
from rest_framework import serializers
from .models import TimeFrequencyMarkingRecord


class TimeFrequencyMarkingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeFrequencyMarkingRecord
        fields = ['id', 'data_set_id', 'input_file']
