'''
业务: 开3个线程按照顺序打印ABC 10次
方案: 用condition
'''
from threading import Condition, Thread
from typing import List


def req1(cond1: Condition, cond2: Condition, data: List, count: int):
    while count > 0:
        with cond1:
            cond1.wait()
            v = data.pop(0)
            print(v)
            data.append(v)
        with cond2:
            cond2.notify()
        count -= 1


def main():
    data = ['A', 'B', 'C']
    n = len(data)
    conds = [Condition() for i in range(n)]
    tasks = []
    count = 1
    for i in range(n):
        tasks.append(Thread(target=req1, args=(
            conds[i], conds[0 if i == n-1 else i+1], data, count)))
    for i in tasks:
        i.start()

    with conds[0]:
        conds[0].notify()


if __name__ == '__main__':
    main()
