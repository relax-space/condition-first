'''
说明: 解释 使用Condition限制并发数 和 不限制并发数的情况
详细说明: 服务器每秒只能接收2个并发请求, 如果开3个线程就会报错, 加Semaphore之后, 成功限制了请求数量
启动说明: 先启动webapi.py, 然后新打开一个终端, 运行sem.py的代码
'''

import _thread
from collections import deque as _deque
from itertools import islice as _islice
from threading import Lock, RLock, Thread
from typing import List

import requests

_allocate_lock = _thread.allocate_lock


class Condition:

    def __init__(self, lock=None):
        if not lock:
            lock = RLock()
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


def req1(second: int, param: int):
    resp = requests.get(f'http://127.0.0.1:5000/delay/{second}/{param}')
    return resp.text


def trunk(param: int, res_value: List, cond: Condition, limit_list: List):
    with cond:
        while limit_list[0] == 0:
            cond.wait()
        else:
            limit_list[0] -= 1
    res_value.append(req1(1, param))
    with cond:
        limit_list[0] += 1
        for i in range(1):
            cond.notify()


def main():
    res_value: List[str] = []
    limit_list = [2]
    # 下面的condition里传rlock和lock都一样,因为都会在wait的到时候,被这句话释放`saved_state = self._release_save()`,这种都可以的情况,据说lock效率会更高
    cond = Condition(Lock())
    tasks = [Thread(target=trunk, args=(i, res_value, cond, limit_list), name=f'thread-{i+1}')
             for i in range(3)]
    for i in tasks:
        i.start()
    for i in tasks:
        i.join()
    # 因为req1方法至少需要1秒钟, 前面2个请求是并发,所以不能确定顺序, 但是第三个可以,因为第三个请求至少1秒钟之后执行
    assert res_value[2] == '2', '并发限制失败'
    print(res_value)


if __name__ == '__main__':
    main()
