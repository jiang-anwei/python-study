#!/usr/bin/env python
# -*- coding: utf-8 -*-
from task import *
from celery import group, chord
import time

start = time.time()
addresult = [add_task.delay(i, i) for i in range(10)]
mult_result = [multiplication_task.delay(i, i) for i in range(20)]

for re in addresult:
    print "加法：", re.get()
for re in mult_result:
    print "乘法：", re.get()
print "cost:{}".format(str(time.time() - start))


result = add_task.apply_async((2, 2), link=[add_task.s(16), add_task.s(15)])
print result.get()
print result.children[0].get()


# chain
# 串行调用

# chain 函数接受一个任务的列表，Celery 保证一个 chain 里的子任务会依次执行，
# 在 AsynResult 上执行 get 会得到最后一个任务的返回值。和 link 功能类似，
# 每一个任务执行结果会当作参数传入下一个任务，所以如果你不需要这种特性，采用 immutable signature (si)来取消。

result = chain(add_task.s(1, 2), add_task.s(3), add_task.s(4))()
# result = chain(add_task.si(1, 2), add_task.si(3, 3), add_task.si(4, 4))()
print result.get()
print result.parent.parent.graph


# Groups
# 并行调用
#
result = group(add_task.s(1, 2), add_task.s(2, 3), add_task.s(2, 4))()
print result.get()

# Chords
# 先并行调用，再串行调用 4+8+16
# 两种写法等价
# result=chord((add_task.s(2, 2), add_task.s(4, 4), add_task.s(8, 8)), sum_all.s())()
result = chain(group(add_task.s(2, 2), add_task.s(4, 4), add_task.s(8, 8)), sum_all.s())()
print result.get()

# map
# 对并行调用的结果各自汇总
result = sum_all.map([range(10), range(100)]).delay()
print result.get()


# Starmap
# 对并行调用的结果各自汇总，汇总参数是tuple
result = add_task.starmap(zip(range(10), range(10))).delay()
print result.get()

