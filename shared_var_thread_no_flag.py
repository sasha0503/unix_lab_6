import threading
import time

val = 0


class ThreadA(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global val
        count = 0
        while True:
            if count >= 1000:
                break
            count += 1
            print("A: val=" + str(val))
            val += 10


class ThreadB(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global val
        count = 0
        while True:
            if count >= 1000:
                break
            count += 1
            print("B: val=" + str(val))
            val += 10


a = ThreadA("myThread_name_A")
b = ThreadB("myThread_name_B")

start_time = time.time()
b.start()
a.start()

a.join()
b.join()
print(time.time() - start_time)
print(val)
