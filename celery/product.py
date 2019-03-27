from task import *
import time

start = time.time()
addresult = [add_task.delay(i, i) for i in range(10)]
mult_result = [multiplication_task.delay(i, i) for i in range(20)]

for re in addresult:
    print "加法：", re.get()
for re in mult_result:
    print "乘法：", re.get()
print "cost:{}".format(str(time.time() - start))
