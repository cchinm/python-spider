import threading
import time

lA = threading.Lock()
lB = lA

def A():
    lA.acquire()
    time.sleep(1)
    print('Lock a')
    lB.acquire()
    time.sleep(1)
    print('Lock B')
    lB.release()
    lA.release()

def B():
    lB.acquire()
    time.sleep(1)
    print('Lock b')
    lA.acquire()
    time.sleep(1)
    print('Lock a')
    lA.release()
    lB.release()

a = threading.Thread(target=A)
b = threading.Thread(target=B)
a.start()
b.start()