#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kombu import Exchange, Queue

BROKER_URL = "redis://172.16.101.24:6379/1"
CELERY_RESULT_BACKEND = "redis://172.16.101.24:6379/2"

CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 24 * 60 * 60

# 如果任务没有在 可见性超时 内确认接收，任务会被重新委派给另一个职程并执行。
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 43200}

# 内存泄漏
# 长时间运行Celery有可能发生内存泄露，可以像下面这样设置

CELERYD_CONCURRENCY = 20  # 并发worker数

CELERYD_MAX_TASKS_PER_CHILD = 40  # 每个worker执行了多少任务就会死掉
CELERY_QUEUES = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("multiplication_task_queue", Exchange("multiplication_task"), routing_key="multiplication_task"),
    Queue("sum_all", Exchange("sum_all"), routing_key="sum_all"),
    Queue("add_task_queue", Exchange("add_task"), routing_key="add_task")
)

CELERY_ROUTES = {
    'task.multiplication_task': {"queue": "multiplication_task_queue", "routing_key": "multiplication_task"},
    'task.sum_all': {"queue": "sum_all", "routing_key": "sum_all"},
    'task.add_task': {"queue": "add_task_queue", "routing_key": "add_task"}}
# celery -A proj worker --loglevel=INFO --concurrency=10 -n worker1.%h -Q for_task
