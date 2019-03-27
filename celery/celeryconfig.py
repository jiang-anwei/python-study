#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kombu import Exchange, Queue

BROKER_URL = "redis://172.16.101.24:6379/1"
CELERY_RESULT_BACKEND = "redis://172.16.101.24:6379/2"

BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 43200}

# 内存泄漏
# 长时间运行Celery有可能发生内存泄露，可以像下面这样设置

CELERYD_CONCURRENCY = 20  # 并发worker数

CELERYD_MAX_TASKS_PER_CHILD = 40  # 每个worker执行了多少任务就会死掉
CELERY_QUEUES = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("for_task", Exchange("for_task"), routing_key="for_task")
)

CELERY_ROUTES = {
    'task.task': {"queue": "for_task", "routing_key": "for_task"}}
# celery -A proj worker --loglevel=INFO --concurrency=10 -n worker1.%h -Q for_task
