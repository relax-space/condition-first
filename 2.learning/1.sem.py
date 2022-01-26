'''
说明: 做了两个例子, 解释 使用Semaphore限制并发数 和 不限制并发数的情况
详细说明: 服务器每秒只能接收2个并发请求, 如果开3个线程就会报错, 加Semaphore之后, 成功限制了请求数量
启动说明: 先启动webapi.py, 然后新打开一个终端, 运行sem.py的代码
'''

import _thread
from collections import deque as _deque
from itertools import islice as _islice
from threading import Lock, Thread
from typing import Dict, List

import requests

_allocate_lock = _thread.allocate_lock


class Condition:

    def __init__(self, lock=None):
        self._lock = lock
        self.acquire = lock.acquire
        self.release = lock.release
        self._waiters = _deque()

    def __enter__(self):
        res = self._lock.__enter__()
        return res

    def __exit__(self, *args):
        return self._lock.__exit__(*args)

    def __repr__(self):
        return "<Condition(%s, %d)>" % (self._lock, len(self._waiters))

    def _release_save(self):
        self._lock.release()

    def _acquire_restore(self, x):
        self._lock.acquire()

    def wait(self, timeout=None):
        waiter = _allocate_lock()
        waiter.acquire()
        self._waiters.append(waiter)
        saved_state = self._release_save()
        gotit = False
        try:
            if timeout is None:
                waiter.acquire()
                gotit = True
            return gotit
        finally:
            self._acquire_restore(saved_state)
            if not gotit:
                try:
                    self._waiters.remove(waiter)
                except ValueError:
                    pass

    def notify(self, n=1):
        all_waiters = self._waiters
        waiters_to_notify = _deque(_islice(all_waiters, n))
        if not waiters_to_notify:
            return
        for waiter in waiters_to_notify:
            waiter.release()
            try:
                all_waiters.remove(waiter)
            except ValueError:
                pass


class Semaphore:

    def __init__(self, value=1):
        self._cond = Condition(Lock())
        self._value = value

    def acquire(self, blocking=True, timeout=None):
        rc = False
        with self._cond:
            while self._value == 0:
                self._cond.wait(timeout)
            else:
                self._value -= 1
                rc = True
        return rc
    __enter__ = acquire

    def release(self, n=1):
        with self._cond:
            self._value += n
            for i in range(n):
                self._cond.notify()

    def __exit__(self, t, v, tb):
        self.release()


session = requests.Session()


def req1(param: int, res_value: List, sem=None):
    resp = session.get(f'http://127.0.0.1:5000/{param}')
    res_value.append(resp.text)


def req2(param: int, res_value: List, sem: Semaphore):
    with sem:
        return req1(param, res_value)


def main(req, sem=None):
    res_value: List[str] = []
    thread_number = 3
    tasks = [Thread(target=req, args=(i, res_value, sem), name=f'thread-{i+1}')
             for i in range(thread_number)]
    for i in tasks:
        i.start()
    for i in tasks:
        i.join()
    assert thread_number == len(res_value), '线程返回结果有误'
    print(res_value)


if __name__ == '__main__':
    main(req1)
    sem = Semaphore(2)
    main(req2, sem)

'''
输出:
    INFO:root:['<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>429 Too Many Requests</title>\n<h1>Too Many Requests</h1>\n<p>2 per 1 second</p>\n', '1', '0']
    INFO:root:['1', '0', '2']
    
webapi.py输出: 可以看到不加semaphore时, GET /2的请求失败: http状态码: 429 Too Many Requests
    127.0.0.1 - - [21/Jan/2022 02:56:06] "GET /2 HTTP/1.1" 429 -
    127.0.0.1 - - [21/Jan/2022 02:56:07] "GET /0 HTTP/1.1" 200 -
    127.0.0.1 - - [21/Jan/2022 02:56:07] "GET /1 HTTP/1.1" 200 -
    127.0.0.1 - - [21/Jan/2022 02:56:08] "GET /0 HTTP/1.1" 200 -
    127.0.0.1 - - [21/Jan/2022 02:56:08] "GET /1 HTTP/1.1" 200 -
    127.0.0.1 - - [21/Jan/2022 02:56:09] "GET /2 HTTP/1.1" 200 -
'''
