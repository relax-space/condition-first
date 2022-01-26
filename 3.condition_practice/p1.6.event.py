'''
业务: 开3个线程按照顺序打印ABC 10次
方案: 用event,基础版本
'''
import logging
from threading import Event, Thread


def req1(e1: Event, e2: Event, count: int):
    while count > 0:
        e1.wait()
        e1.clear()
        logging.warning('A')
        e2.set()
        count -= 1


def req2(e2: Event, e3: Event, count: int):
    while count > 0:
        e2.wait()
        e2.clear()
        logging.warning('B')
        e3.set()
        count -= 1


def req3(e3: Event, e1: Event, count: int):
    while count > 0:
        e3.wait()
        e3.clear()
        logging.warning('C')
        e1.set()
        count -= 1


def main():
    count = 2
    e1, e2, e3 = Event(), Event(), Event()
    t1 = Thread(target=req1, args=(e1, e2, count))
    t2 = Thread(target=req2, args=(e2, e3, count))
    t3 = Thread(target=req3, args=(e3, e1, count))
    t1.start()
    t2.start()
    t3.start()
    e1.set()


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s')
    main()
