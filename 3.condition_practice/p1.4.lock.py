
'''
业务: 开3个线程按照顺序打印ABC 10次
方案: 用lock
'''

from threading import Lock, Thread
from typing import List


def req1(data: List, lock: Lock, count: int):
    while count > 0:
        with lock:
            v = data.pop(0)
            data.append(v)
            print(v)
            count -= 1


def main():
    data = ['A', 'B', 'C']
    count = 2
    lock = Lock()
    tasks = [Thread(target=req1, args=(data, lock, count)) for i in range(3)]
    for i in tasks:
        i.start()

    for i in tasks:
        i.join()


if __name__ == '__main__':
    main()
