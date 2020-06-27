"""
Still a cache server. This does not interact with the client.
"""

import pickle
import socket

from distcache import configure as config
from distcache import utils
from distcache.lru_cache import LRUCache

config = config.config()


class CacheClient:
    def __init__(self, capacity=100):
        """
        :param capacity: capacity of the cache in MBs
        """
        self.cache = LRUCache(capacity)

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
        self.client_socket.settimeout(30)  # TODO: Increasing timeout is not the solution.
        while True:
            response = self.client_socket.recv(config.HEADER_LENGTH)
            if not response:
                continue
            message_length = int(response.decode(config.FORMAT))
            message = self.client_socket.recv(message_length)
            self.execute_query(message)  # TODO: Should ultimately be an async operation

    def parse_message(self, message):
        """
        Parse and execute the command
        :param message: the message sent by the cache_server
        :return: depends on the operation that was carried out after parsing message
        """
        # This should run in a separate thread
        message = pickle.loads(message)

        if message[0] == "set":
            print("set ", message[1:])
            return self.cache.set(message[1], message[2])

        elif message[0] == "del":
            print("delete ", message[1:])
            return self.cache.delete(message[1])

        elif message[0] == "get":
            print("get ", message[1:])
            return self.cache.get(message[1])

        elif message[0] == "add":
            print("get ", message[1:])
            return self.cache.add(message[1], message[2])

        else:
            print("Only these keywords are supported: get, set, delete")

        return message


if __name__ == '__main__':
    client = CacheClient()
    client.monitor()