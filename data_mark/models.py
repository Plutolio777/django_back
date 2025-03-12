from django.core.validators import FileExtensionValidator

from django.db import models

from utils.validators import validate_filename, validate_no_executable_files


class TimeFrequencyMarkingRecord(models.Model):
    data_set_id = models.IntegerField(null=False, blank=False, verbose_name='数据集id')

    input_file = models.FileField(upload_to="data_marks/", verbose_name='数据集路径', validators=[
        FileExtensionValidator(allowed_extensions=['xlsx', "csv", "xls"]),
        validate_filename,
        validate_no_executable_files,
    ])

    mark_type = models.IntegerField(null=False, blank=False, verbose_name='标注记录类型')
    creator = models.IntegerField(null=False, blank=False, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='标注记录创建时间')

    # name = models.CharField(max_length=128, null=False, blank=False, verbose_name='数据集名称')
    # description = models.TextField(null=True, blank=True, verbose_name='数据集描述')
    # type = models.CharField(max_length=20, null=True, blank=True, verbose_name='电话号码')
    # create_time = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='数据集创建时间')
    # update_time = models.DateTimeField(auto_now=True, null=False, blank=False, verbose_name='数据集更新时间')
    # origin_path = models.TextField(null=True, blank=True, verbose_name='原始文件名称')
    # data_set_path = models.FileField(upload_to="data_sets/", verbose_name='数据集路径', validators=[
    #     FileExtensionValidator(allowed_extensions=['xlsx', "csv", "xls"]),
    #     validate_filename,
    #     validate_no_executable_files,
    # ])
    # creator = models.IntegerField(null=False, blank=False, verbose_name='创建者')

    def __str__(self):
        return self.name
