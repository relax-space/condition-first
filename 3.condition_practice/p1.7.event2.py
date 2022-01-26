'''
业务: 开3个线程按照顺序打印ABC 10次
方案: 用event, 优化后的版本
'''
from threading import Event, Thread


def req1(e1: Event, e2: Event, count: int, char: str):
    while count > 0:
        e1.wait()
        e1.clear()
        print(char)
        e2.set()
        count -= 1


def main():
    count = 10
    e1, e2, e3 = Event(), Event(), Event()
    t1 = Thread(target=req1, args=(e1, e2, count, 'A'))
    t2 = Thread(target=req1, args=(e2, e3, count, 'B'))
    t3 = Thread(target=req1, args=(e3, e1, count, 'C'))
    t1.start()
    t2.start()
    t3.start()
    e1.set()


if __name__ == '__main__':
    main()
