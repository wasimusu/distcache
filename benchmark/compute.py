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
import time

from benchmark.utils import timeit
from distcache.cache_server import CacheServer
import random


class ProductDBBench:
    def __init__(self):
        self.server = CacheServer()
        self.server.spawn()  # Spawn one localhost

    def expensive_compute_func(self, key):
        time.sleep(random.randint(1, 5) / 10.0)  # Sleep between 1 to 5ms
        return key * key * key

    @timeit
    def queries_with_cache(self):
        # Populate the cache
        for i in range(10, 20):
            self.server.set(i, self.expensive_compute_func(i))

        # Make queries
        for i in range(100):
            self.server.get(random.randint(10, 20))

    @timeit
    def queries_without_cache(self):
        # Make queries
        for i in range(100):
            print(i)
            self.expensive_compute_func(random.randint(10, 20))


if __name__ == '__main__':
    product_bench = ProductDBBench()
    product_bench.queries_with_cache()
    product_bench.queries_without_cache()
