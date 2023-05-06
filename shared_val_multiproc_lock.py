"""replicate the shared_val_multiproc.py example, but using the lock"""
import time
from multiprocessing import Process, Value, Lock

val = Value('i', 0)
lock = Lock()


class ProcessA(Process):

    def __init__(self, name):
        Process.__init__(self)
        global lock
        self.name = name
        self.lock = lock

    def run(self):
        global val
        count = 0
        while True:
            if count >= 1000:
                break
            self.lock.acquire()
            count += 1
            print("A: val=" + str(val.value))
            val.value += 10
            self.lock.release()
            time.sleep(0)


class ProcessB(Process):

    def __init__(self, name):
        Process.__init__(self)
        global lock
        self.name = name
        self.lock = lock

    def run(self):
        global val
        count = 0
        while True:
            if count >= 1000:
                break
            self.lock.acquire()
            count += 1
            print("B: val=" + str(val.value))
            val.value += 10
            self.lock.release()
            time.sleep(0)


a = ProcessA("myProcess_name_A")
b = ProcessB("myProcess_name_B")

start_time = time.time()
b.start()
a.start()

a.join()
b.join()
print(time.time() - start_time)
print(val.value)
