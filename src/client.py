"""
Still a cache server. This does not interact with the client.
"""

import pickle
import socket
import sys

from src import configure as config
from src import utils

config = config.config()


class CacheClient:
    def __init__(self, capacity=100):
        """
        :param capacity: capacity of the cache in MBs
        """
        # cache configuration
        self.cache = {}  # (key, (value, time))
        self.time_key = {}  # (time, key)
        self.capacity = capacity * 1024
        self.garbage_cache_response = "@!#$!@#"
        self.time = 0
        self.least_recent_time = 0

        # Communication configurations
        self.FORMAT = config.FORMAT
        self.HEADER_LENGTH = config.HEADER_LENGTH

        # Start the connection with the server. socket. connect
        self.server_address = (config.IP, config.PORT)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = self.register()  # Congrats! You're registered with the server. Server now knows you IP, PORT
        print("About: ", self.client_socket.getsockname(), self.id)

    def register(self):
        """
        Just try connecting to the server. And it will register you.
        :return:
        """
        self.client_socket.connect(self.server_address)
        print("Client connected at address {}:{}".format(*self.server_address))

        # TODO: Make sure a proper client_id is always received.
        return utils.receive_message(self.client_socket, self.HEADER_LENGTH, self.FORMAT)

    def get(self, key):
        """
        Get the value corresponding to the key.
        For now, the value of keys can not be boolean
        :return: value of the key if it exists, otherwise False.
        """
        value, _ = self.cache.get(key, (self.garbage_cache_response, -1))
        print("{} fetched from server {}".format(key, self.id))

        if value == self.garbage_cache_response:
            return False

        self.set(key, value)  # TODO: Asynchronously update the timestamp also
        return value

    def add(self, key, diff):
        """
        Add diff to the value corresponding to key in a thread safe manner.
        :param diff: the amount to be added to the value of key
        :return: boolean indicating if the operation was successful or not.
        """
        value, _ = self.cache.get(key, (self.garbage_cache_response, -1))

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
            _, time = self.cache[key]
            del self.cache[key]
            del self.time_key[time]

        self.cache[key] = (value, self.time)
        self.time_key[self.time] = key
        self.time += 1

        print("{} stored in server {}".format(key, self.id))
        self.lru_eviction()  # TODO: Asynchronously update the timer also
        return True

    def delete(self, key):
        """
        The server wants the key deleted.
        """
        if key in self.cache:
            _, time = self.cache[key]
            del self.cache[key]
            del self.time_key[time]
        print("{} deleted from server {}".format(key, self.id))
        return True

    def execute_query(self, message):
        response = self.parse_message(message)
        utils.send_message(response, self.client_socket, self.HEADER_LENGTH, self.FORMAT)
        return

    def monitor(self):
        """
        A client has a few things to listen for.
        The server may ping to monitor your health.
        The server may request for key, value pair
        The server can request you to store key, value pair
        The server can request you to delete key from cache
        :return:
        """
        print("Monitoring queries from server and responding...")
        while True:
            try:
                response = self.client_socket.recv(config.HEADER_LENGTH)
                if not response:
                    continue
                message_length = int(response.decode(config.FORMAT))
                message = self.client_socket.recv(message_length)
                self.execute_query(message)
            except ConnectionResetError as err:
                print(err)

    def parse_message(self, message):
        """
        Parse and execute the command
        :param message: the message sent by the dcache_server
        :return: depends on the operation that was carried out after parsing message
        """
        # This should run in a separate thread
        message = pickle.loads(message)

        if message[0] == "set":
            print("set ", message[1:])
            return self.set(message[1], message[2])

        elif message[0] == "del":
            print("delete ", message[1:])
            return self.delete(message[1])

        elif message[0] == "get":
            print("get ", message[1:])
            return self.get(message[1])

        elif message[0] == "add":
            print("get ", message[1:])
            return self.add(message[1], message[2])

        else:
            print("Only these keywords are supported: get, set, delete")

        return message

    def lru_eviction(self):
        """
        Implements LRU cache eviction on the cache
        :return: None
        """
        if sys.getsizeof(self.cache) > self.capacity:
            print("We need to evict some items from cache")

        while sys.getsizeof(self.cache) > self.capacity:
            while self.least_recent_time not in self.time_key:
                self.least_recent_time += 1
            del self.cache[self.time_key[self.least_recent_time]]
            del self.time_key[self.least_recent_time]


if __name__ == '__main__':
    client = CacheClient()
    client.monitor()
