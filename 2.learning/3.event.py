
'''
说明: 用于线程通讯, 一个线程完成之后,通知其他的线程
'''
from threading import Event, Thread


def work(event: Event):
    print('员工:工作完成')
    event.set()


def boss(event: Event):
    print('老板:分配工作')
    w = Thread(target=work, args=(event,))
    w.start()
    event.wait()
    print('老板:good job')


def main():
    event = Event()
    b = Thread(target=boss, args=(event,))
    b.start()


if __name__ == '__main__':
    main()
