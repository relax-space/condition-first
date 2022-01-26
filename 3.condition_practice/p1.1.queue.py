'''
业务: 开3个线程按照顺序打印ABC 10次
方案: 用queue
'''

import logging
from queue import Queue
from threading import Thread, current_thread

import requests

session = requests.Session()


def req1(q: Queue):
    while q.qsize() > 0:
        session.get(f'https://deelay.me/100/http://httpbin.org/get?a=1')
        v = q.get()
        if v:
            logging.info(f'{current_thread().name} - {v}')
    else:
        # 队列里最后一条数据, 如果3个线程同时进入while循环,那么`v=q.get()`只能读取一条数据,其他两个线程将被锁,为了释放锁加入下面的代码
        q.put(None)


def main():
    list = ['A', 'B', 'C'] * 10
    q = Queue()
    for i in list:
        q.put(i)

    tasks = [Thread(target=req1, args=(
        q,), name=f'thread-{i+1}') for i in range(3)]
    for i in tasks:
        i.start()

    for i in tasks:
        i.join()
    print('done')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    main()
