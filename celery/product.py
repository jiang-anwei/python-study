from task import *
import time

start = time.time()
for i in range(10):
    result = task.delay(i, i)
    print result.get()
print "cost:{}".format(str(time.time() - start))
