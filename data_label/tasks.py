import os
import shutil
import subprocess
import tarfile
import py7zr
import zipfile

from celery import shared_task
from django.db import transaction
from django.utils import timezone
import logging

from utils import tools
from data_label.models import TimeFrequencyLabelTask, UnsupervisedLabelTask, CleanedData
from django_back import settings

logger = logging.getLogger(__name__)


class BaseLabelTaskService:
    """基础标注任务服务类，包含公共流程"""

    @classmethod
    def execute_task(cls, task_id, task_model, update_cleaned_data=False,  task_label="1,2,3,4,5,6,7"):
        """
        执行标注任务的公共流程

        :param task_id: 任务ID
        :param task_model: 任务模型类
        :param update_cleaned_data: 是否更新CleanedData记录
        :return: 执行结果
        """
        logger.info(f"开始执行任务 {task_id}")

        try:
            with transaction.atomic():  # 开启事务
                # 获取任务对象并锁定行，防止并发修改
                task = task_model.objects.select_for_update().filter(id=task_id).first()
                if task is None:
                    logger.warning(f"任务 {task_id} 不存在")
                    return False

                try:
                    # 执行具体任务逻辑(由子类实现)
                    cls._do_task(task, task_label)

                    # 任务成功 - 更新任务状态为3(成功)
                    task.status = 3
                    task.task_execute_time = timezone.now()
                    task.save()

                    # 如果需要更新CleanedData记录
                    if update_cleaned_data:
                        cls._update_cleaned_data(task)

                    logger.info(f"任务 {task_id} 执行成功")
                    return True

                except Exception as e:
                    # 任务失败 - 更新任务状态为2(失败)
                    logger.info(f"任务 {task_id} 执行失败: {str(e)}", exc_info=True)
                    task.status = 2
                    task.task_execute_time = timezone.now()
                    task.save()
                    raise  # 重新抛出异常

        except Exception as e:
            logger.error(f"处理任务 {task_id} 时发生错误: {str(e)}", exc_info=True)
            raise

    @classmethod
    def _do_task(cls, task, task_label):
        """执行具体任务逻辑，由子类实现"""
        raise NotImplementedError("子类必须实现此方法")

    @classmethod
    def _update_cleaned_data(cls, task):
        """更新CleanedData记录"""
        cleaned_data = CleanedData.objects.filter(label_task_id=task.id).first()
        cleaned_data.task_execute_time = timezone.now()
        cleaned_data.is_executed = True
        cleaned_data.save()

    @classmethod
    def _get_label_type(cls):
        """获取标注类型，由子类实现"""
        raise NotImplementedError("子类必须实现此方法")

    @classmethod
    def prepare_the_environment(cls, task):
        target_dir = os.path.normpath(task.out_put_path)  # 目标目录
        origin_dataset_path = os.path.normpath(task.dataset.data_set_path.path)

        # 2.生成input_dir
        input_dir = os.path.join(target_dir, "data_set")
        print(f"重新生成输入文件夹：{input_dir}")
        # 3. 清空目标目录（如果存在）
        cls.clear_and_recreate_dir(target_dir)
        print(f"重新生成输出文件夹：{target_dir}")
        # 3. 清空目标目录（如果存在）
        cls.clear_and_recreate_dir(input_dir)
        print(f"同步输入数据集：{origin_dataset_path}")
        # 3.将data_path拷贝到data_set目录中
        shutil.copy2(origin_dataset_path, input_dir)
        # 4.尝试解压压缩文件（如果有的话）
        print(f"尝试进行解压缩")
        tools.try_unzip_files(input_dir)
        return input_dir, target_dir

    @classmethod
    def do_start_matlab_model(cls, input_dir, target_dir, call_modes=None, task_label="1,2,3,4,5,6,7"):
        work_dir = os.path.join(settings.BASE_DIR, "data_label", "model_code", call_modes)

        command = f"cd {work_dir} && matlab -nosplash -batch \"try, run('{input_dir}', '{target_dir}', '{task_label}') ; catch, disp(lasterr), end; exit;\""
        print(f"执行命令：{command}")
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("return code:", result.returncode)
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)
        if result.returncode == 0:
            pass
        else:
            raise RuntimeError(f"模型调用失败: {str(result.stderr)}")

    @classmethod
    def clear_and_recreate_dir(cls, input_dir):
        try:
            if os.path.exists(input_dir):
                print(f"正在清空目标目录: {input_dir}")
                shutil.rmtree(input_dir)  # 递归删除目录
            os.makedirs(input_dir, exist_ok=True)  # 重新创建空目录
        except Exception as e:
            raise RuntimeError(f"清空目标目录失败: {str(e)}")


class TimeFrequencyLabelTaskService(BaseLabelTaskService):
    """时间频率标注任务服务"""

    @classmethod
    def _do_task(cls, task, task_label):
        """执行时频注任务（先清空目标目录，再递归复制所有内容）"""
        print("正在执行时频标注任务")
        # 1. 定义路径（统一使用 os.path 处理路径）
        input_dir, target_dir = cls.prepare_the_environment(task)
        print("调用时频模型")
        cls.do_start_matlab_model(input_dir, target_dir, call_modes=cls._get_label_type(), task_label=task_label)
        print("正在执行时频标注任务")

    @classmethod
    def _get_label_type(cls):
        return "TimeFrequency"


class UnsupervisedLabelTaskService(BaseLabelTaskService):
    """无监督标注任务服务"""

    @classmethod
    def _do_task(cls, task, task_label):
        """执行无监督标注任务（先清空目标目录，再递归复制所有内容）"""
        print("正在执行无监督标注任务")
        # 1. 定义路径（统一使用 os.path 处理路径）
        input_dir, target_dir = cls.prepare_the_environment(task)
        print("调用无监督模型")
        cls.do_start_matlab_model(input_dir, target_dir, call_modes=cls._get_label_type(), task_label=task_label)
        print("无监督标注任务执行完毕")

    @classmethod
    def _get_label_type(cls):
        return "Unsupervised"


@shared_task
def time_data_label_execute(task_id, task_label):
    """执行时间频率标注任务"""
    TimeFrequencyLabelTaskService.execute_task(
        task_id=task_id,
        task_model=TimeFrequencyLabelTask,
        update_cleaned_data=True,  # 需要更新CleanedData
        task_label = task_label
    )


@shared_task
def unsupervised_data_label_execute(task_id, task_label):
    """执行无监督标注任务"""
    UnsupervisedLabelTaskService.execute_task(
        task_id=task_id,
        task_model=UnsupervisedLabelTask,
        update_cleaned_data=True,  # 不需要更新CleanedData
        task_label=task_label
    )
