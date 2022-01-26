'''
业务: 开3个线程按照顺序打印ABC 10次
方案: 用semaphore
'''

import logging
import time
from threading import Semaphore, Thread, current_thread
from typing import List

import requests

session = requests.Session()


def req1(list: List, sem: Semaphore):
    while len(list) > 0:
        with sem:
            if len(list) <= 0:
                break
            session.get(f'https://deelay.me/100/http://httpbin.org/get?a=1')
            logging.info(f'{current_thread().name}-{list.pop(0)}')
        time.sleep(0.000000000000000001)


def main():
    sem = Semaphore(1)
    list = ['A', 'B', 'C'] * 10
    tasks = [Thread(target=req1, args=(list, sem)) for i in range(3)]
    for i in tasks:
        i.start()
    for i in tasks:
        i.join()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
