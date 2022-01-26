'''
业务: 开3个线程按照顺序打印ABC 10次
方案: 不用锁, 对于每个线程来说, ABC是按照顺序执行的
注:   真实的场景可能是这样的, 按顺序去做3个请求, 所以这种方案是能保证的
'''
import logging
from threading import Thread, current_thread


def req1():
    logging.info(f'{current_thread().name} A')
    logging.info(f'{current_thread().name} B')
    logging.info(f'{current_thread().name} C')


def main():
    tasks = [Thread(target=req1) for i in range(3)]
    for i in tasks:
        i.start()

    for i in tasks:
        i.join()
    pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    main()
