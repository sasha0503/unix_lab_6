import threading
import time

c = threading.Condition()
flag = 0
val = 0


class ThreadA(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global flag
        global val
        count = 0
        while True:
            if count >= 1000:
                break
            c.acquire()
            if flag == 0:
                count += 1
                print("A: val=" + str(val))
                flag = 1
                val += 10
                c.notify_all()
            else:
                c.wait()
            c.release()


class ThreadB(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global flag
        global val
        count = 0
        while True:
            if count >= 1000:
                break
            c.acquire()
            if flag == 1:
                count += 1
                print("B: val=" + str(val))
                flag = 0
                val += 10
                c.notify_all()
            else:
                c.wait()
            c.release()


a = ThreadA("myThread_name_A")
b = ThreadB("myThread_name_B")

start_time = time.time()
b.start()
a.start()

a.join()
b.join()
print(time.time() - start_time)
print(val)
