import os

from celery import Celery

from pathlib import Path

proj_name = Path(os.path.realpath(__file__)).parent.stem
print(proj_name)
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{proj_name}.settings')

app = Celery(proj_name)


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# 最小资源配置
app.conf.update(
    worker_max_tasks_per_child=50,  # 处理50个任务后重启worker
    worker_prefetch_multiplier=1,   # 每次只预取1个任务
    task_acks_late=True,            # 任务完成后才确认
    broker_pool_limit=None,         # 禁用broker连接池
    worker_concurrency=1,           # 只使用1个worker进程
    task_serializer='json',         # 使用轻量级的JSON序列化
    event_queue_expires=60,         # 事件队列60秒过期
    worker_send_task_events=False,  # 不发送任务事件
)
# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')