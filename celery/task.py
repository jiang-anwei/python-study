#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery import Celery, platforms, Task
import time

platforms.C_FORCE_ROOT = True

app = Celery()
app.config_from_object("celeryconfig")


class CalculationTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        print 'task done: {0}'.format(retval)
        return super(CalculationTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print 'task fail, reason: {0}'.format(exc)
        return super(CalculationTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    # 不关心结果
    # @app.task(ignore_result=True)


@app.task(base=CalculationTask)
def multiplication_task(x, y):
    time.sleep(1)
    raise Exception("test")
    return x * y


@app.task(base=CalculationTask)
def add_task(x, y):
    time.sleep(1)
    return x + y
