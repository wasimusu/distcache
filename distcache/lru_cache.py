"""
Implementation of LRU Cache.
Implementing Cache in a separate class/file allows for robust testing and is a practice of loose-coupling.
It allows, in future, to implement other types of cache (eviction policy) and just interchange different types of cache.
Also, it allows clean code, in other places using cache.
Allows for easier reasoning of code.

# Tested against leetcode's test cases: https://leetcode.com/submissions/detail/359080389/
In project, test cases would be way better though.
"""


class LRUCache:
    def __init__(self, capacity=100):
        """
        :param capacity: number of items to be stored in the cache. That's our cache capacity for now.
        For now
        """
        # TODO: Add time expiration.
        # TODO: Instead of item counts, use memory usage as cache capacity
        # cache configuration
        self.cache = {}  # (key, (value, time))
        self.time_key = {}  # (time, key)
        self.capacity = capacity
        self.time = 0
        self.least_recent_time = 0
        self.key_not_found = "!@#@!#$!#@$!@"

    def get(self, key):
        """
        Get the value corresponding to the key.
        For now, the value of keys can not be boolean
        :return: value of the key if it exists, otherwise False.
        """
        value, _ = self.cache.get(key, (self.key_not_found, -1))

        if value == self.key_not_found:
            return False

        self.set(key, value)  # TODO: Asynchronously update the timestamp also
        return value

    def add(self, key, diff):
        """
        Add diff to the value corresponding to key in a thread safe manner.
        :param diff: the amount to be added to the value of key
        :return: boolean indicating if the operation was successful or not.
        """
        value, _ = self.cache.get(key, (self.key_not_found, -1))

        # TODO: Add diff to value in a thread-safe manner
        value += diff

        self.set(key, value)  # TODO: Asynchronously update the timestamp also
        return value

    def set(self, key, value):
        """
        The server decided the key value be stored in this client.
        If it is new, just add to the cache
        If the key is old, update it with new value and also the LRU
        :return: boolean indicating success of the operation
        """
        if key in self.cache:
            # TODO: I am moving whole objects instead of just changing timestamp. Not good!
            # This code is faster than changing just time and not deleting the object than deleting
            # the object and adding another
            _, time = self.cache[key]
            del self.cache[key]
            del self.time_key[time]

        self.cache[key] = (value, self.time)
        self.time_key[self.time] = key
        self.time += 1

        self.lru_eviction()
        return True

    def delete(self, key):
        """
        The server wants the key deleted.
        """
        if key in self.cache:
            _, time = self.cache[key]
            del self.cache[key]
            del self.time_key[time]
        return True

    def lru_eviction(self):
        """
        Implements LRU cache eviction on the cache
        :return: None
        """
        while self.cache.__len__() > self.capacity:
            while self.least_recent_time not in self.time_key:
                self.least_recent_time += 1
            del self.cache[self.time_key[self.least_recent_time]]
            del self.time_key[self.least_recent_time]
