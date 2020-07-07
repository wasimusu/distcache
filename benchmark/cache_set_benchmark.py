"""
Mimic a computationally intensive function.

Takes a number. And does lots of computation on it.
Add random delay between (min_delay, max_delay) to add a little bit of randomness to each computation.

Benchmark single cache client on it.

Running this benchmark:
Run this server.
Also run the client file which contains code to start up a client. That's all.
You can also run the cache client implementation in this package.

Summary: cache is useful when the compute time is more than fetching it from some remote computer.
"""

from benchmark.utils import timeit
from distcache.cache_client import CacheClient
from distcache.lru_cache import LRUCache


class ProductDBBench:
    def __init__(self):
        self.client = CacheClient()
        # self.client = LRUCache(10000000)

    @timeit
    def set_values(self):
        """
        The current benchmark is to 8000ms for 100 values.
        However, the LRU Cache can set 10M keys in 9s.
        """
        # Cache operations
        for i in range(10000):
            self.client.set(i * 10, i)


if __name__ == '__main__':
    product_bench = ProductDBBench()
    product_bench.set_values()
