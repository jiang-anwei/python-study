#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery import Celery, platforms
import time

platforms.C_FORCE_ROOT = True

app = Celery()
app.config_from_object("celeryconfig")


# 不关心结果
# @app.task(ignore_result=True)
@app.task
def task(x, y):
    time.sleep(1)
    return x * y
