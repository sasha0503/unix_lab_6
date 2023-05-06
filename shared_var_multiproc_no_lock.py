import time
from multiprocessing import Process, Value

val = Value('i', 0)


class ProcessA(Process):
    def __init__(self, name):
        Process.__init__(self)
        self.name = name

    def run(self):
        global val
        count = 0
        while True:
            if count >= 1000:
                break
            count += 1
            print("A: val=" + str(val.value))
            val.value += 10


class ProcessB(Process):
    def __init__(self, name):
        Process.__init__(self)
        self.name = name

    def run(self):
        global val
        count = 0
        while True:
            if count >= 1000:
                break
            count += 1
            print("B: val=" + str(val.value))
            val.value += 10


a = ProcessA("myProcess_name_A")
b = ProcessB("myProcess_name_B")

start_time = time.time()
b.start()
a.start()

a.join()
b.join()
print(time.time() - start_time)
print(val.value)
