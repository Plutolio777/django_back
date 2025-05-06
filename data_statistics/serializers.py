from rest_framework import serializers

class DataSizeSerializer(serializers.Serializer):
    total_data_size_current = serializers.FloatField()  # 当前总数据大小（字节）
    total_data_size_current_human_readable = serializers.CharField()  # 格式化后的当前数据大小
    total_data_size_this_week = serializers.FloatField()  # 本周新增数据大小（字节）
    total_data_size_this_week_human_readable = serializers.CharField()  # 格式化后的本周数据大小
    total_data_size_last_week = serializers.FloatField()  # 上周新增数据大小（字节）
    total_data_size_last_week_human_readable = serializers.CharField()  # 格式化后的上周数据大小
    size_change_percentage = serializers.CharField()  # 变化百分比
    size_change_type = serializers.CharField()  # 变化类型（上升/下降/没有变化）
