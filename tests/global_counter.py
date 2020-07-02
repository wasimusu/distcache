import sys, os
import threading

sys.path.insert(0, os.path.abspath('..'))  # root of the project
from distcache.lru_cache import LRUCache

lru_cache = LRUCache(100000)
lru_cache.set("counter", 0)


def function1(N=1000):
    for i in range(N):
        lru_cache.add("counter", 1)


def test_counter(k=5, N=1000):
    threads = []
    for _ in range(k):
        threads.append(threading.Thread(target=function1, args=[N]))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    k = 134
    N = 5487
    test_counter(k, N)
    assert lru_cache.get("counter") == k * N
