import os

from django.core.validators import FileExtensionValidator
from django.db import models

from data_manage.models import DataSet
from django_back.settings import MEDIA_ROOT
from utils.validators import validate_filename, validate_no_executable_files
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

# Create your models here.
class TimeFrequencyLabelTask(models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE, related_name="date_set")
    status = models.IntegerField(default=0)
    label_create_time = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='数据集创建时间')
    task_execute_time = models.DateTimeField(null=True, blank=True, verbose_name='数据集更新时间')
    out_put_path = models.CharField(null=True, blank=True, verbose_name='文件输出', max_length=255)
    time_out_time = models.IntegerField(default=60 * 61)

class UnsupervisedLabelTask(models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE, related_name="data_set")
    status = models.IntegerField(default=0)
    label_create_time = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='数据集创建时间')
    task_execute_time = models.DateTimeField(null=True, blank=True, verbose_name='数据集更新时间')
    out_put_path = models.CharField(null=True, blank=True, verbose_name='文件输出', max_length=255)
    time_out_time = models.IntegerField(default=60 * 61)

class CleanedData(models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE, related_name="cleaned_data_set")
    label_task_id = models.BigIntegerField(null=True, blank=True, verbose_name='标注任务ID')
    label_type = models.CharField(null=True,max_length=64, blank=True, verbose_name='标注类型')
    label_create_time = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='数据集创建时间')
    task_execute_time = models.DateTimeField(null=True, blank=True, verbose_name='数据集更新时间')
    out_put_path = models.CharField(null=True, blank=True, verbose_name='文件输出', max_length=255)
    is_executed = models.BooleanField(null=False, blank=False, default=False,verbose_name='任务是否执行')


# 创建 DataSet 时自动创建 DataLabel
@receiver(post_save, sender=DataSet)
def create_datalabel(sender, instance, created, **kwargs):
    if created:
        # 创建一个新的 DataLabel
        out_put_dir = f"{MEDIA_ROOT}marks/TimeFrequencyLabelTask/labels/{instance.id}_{instance.name}"
        os.makedirs(out_put_dir, exist_ok=True)
        TimeFrequencyLabelTask.objects.create(dataset=instance, out_put_path=out_put_dir)
        out_put_dir = f"{MEDIA_ROOT}marks/UnsupervisedLabelTask/labels/{instance.id}_{instance.name}"
        os.makedirs(out_put_dir, exist_ok=True)
        UnsupervisedLabelTask.objects.create(dataset=instance, out_put_path=out_put_dir)



# 删除 DataSet 时自动删除所有关联的 DataLabel
@receiver(pre_delete, sender=DataSet)
def delete_datalabel(sender, instance, **kwargs):
    TimeFrequencyLabelTask.objects.filter(dataset=instance).delete()
    UnsupervisedLabelTask.objects.filter(dataset=instance).delete()



@receiver(post_save, sender=TimeFrequencyLabelTask)
def create_time_clean(sender, instance, created, **kwargs):
    if created:
        CleanedData.objects.create(
            dataset=instance.dataset,
            out_put_path=instance.out_put_path,
            label_task_id=instance.id,
            label_type="TimeFrequency"
        )

@receiver(post_save, sender=UnsupervisedLabelTask)
def create_unsupervised_clean(sender, instance, created, **kwargs):
    if created:
        CleanedData.objects.create(
            dataset=instance.dataset,
            out_put_path=instance.out_put_path,
            label_task_id=instance.id,
            label_type="Unsupervised"
        )

@receiver(pre_delete, sender=TimeFrequencyLabelTask)
def delete_time_clean(sender, instance, **kwargs):
    CleanedData.objects.filter(label_task_id=instance.id).delete()

@receiver(pre_delete, sender=UnsupervisedLabelTask)
def delete_unsupervised_clean(sender, instance, **kwargs):
    CleanedData.objects.filter(label_task_id=instance.id).delete()