from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.


# data_manage/models.py
from django.db import models

from utils.validators import validate_filename, validate_no_executable_files


class DataSet(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False, verbose_name='数据集名称')
    description = models.TextField(null=True, blank=True, verbose_name='数据集描述')
    data_source_type = models.CharField(max_length=20, null=True, blank=True, verbose_name='电话号码', default="数据源")
    type = models.CharField(max_length=20, null=True, blank=True, verbose_name='电话号码')
    create_time = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='数据集创建时间')
    update_time = models.DateTimeField(auto_now=True, null=False, blank=False, verbose_name='数据集更新时间')
    origin_path = models.TextField(null=True, blank=True, verbose_name='原始文件名称')
    data_set_path = models.FileField(upload_to="data_sets/", verbose_name='数据集路径', validators=[
        FileExtensionValidator(allowed_extensions=['xlsx', "csv", "xls", "tar", "zip", "7z", "tar.gz", 'tar.bz2']),
        validate_filename,
        validate_no_executable_files,
    ])
    creator = models.IntegerField(null=False, blank=False, verbose_name='创建者')
    file_size = models.BigIntegerField(null=False, blank=False, verbose_name='创建者',default=0)

    def __str__(self):
        return self.name

    def formatted_create_time(self):
        return self.create_time.strftime("%Y-%m-%d %H:%M:%S")

    def formatted_update_time(self):
        return self.update_time.strftime("%Y-%m-%d %H:%M:%S")

