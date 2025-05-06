from rest_framework import serializers

class DataSizeSerializer(serializers.Serializer):
    total_data_size = serializers.IntegerField()  # 总数据大小（字节）
    total_data_size_human_readable = serializers.CharField()  # 格式化后的数据大小（例如 '20.5 MB'）
