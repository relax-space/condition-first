'''
业务: 开3个线程按照顺序打印ABC 10次
方案: 用互斥锁， 可以开100个线程看多个线程执行效果
'''
import logging
from threading import Lock, Thread, current_thread
from typing import List


def req1(lock: Lock, data_list: List):
    while len(data_list) > 0:
        # 逻辑1
        with lock:
            # 这个判断必须有, 假如线程1,在进入`逻辑1`之后,正在执行with lock的时候, 线程2将data_list的最后一条数据变为0,那么线程1执行`data_list.pop()`就会报错
            if len(data_list) == 0:
                break
            data = data_list.pop()
            for i in data:
                logging.info(f'{current_thread().name} {i}')
        # time.sleep(0.0001)


def main():
    lock = Lock()
    data_list = [['A', 'B', 'C'] for i in range(10)]
    tasks = [Thread(target=req1, args=(lock, data_list)) for i in range(3)]
    for i in tasks:
        i.start()

    for i in tasks:
        i.join()
    pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    main()
