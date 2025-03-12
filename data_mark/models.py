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
    update_time = models.DateTimeField(auto_now=True, null=False, blank=False, verbose_name='数据集更新时间')
    output_dir_path = models.TextField(null=False, blank=False, verbose_name='输出目录路径')



    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        # 生成 output_dir_path，根据 data_set_id 或其他字段拼接路径
        if not self.output_dir_path:
            self.output_dir_path = f"data_marks/{self.data_set_id}_output"

        super().save(*args, **kwargs)