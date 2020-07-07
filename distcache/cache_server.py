import socket
import threading
import pickle

from distcache import configure as conf
from distcache.lru_cache import LRUCache
from distcache import utils
from distcache import logger

"""
The server is always listening to the client. It needs to detect if the client is alive.
"""


class CacheServer:
    """
    Implements cache client. It has different types of cache eviction policies at disposal.
    It responds to queries of cache server.
    """

    def __init__(self, address=None, num_virtual_replicas=5, capacity=100, expire=0, filename=None, reconstruct=False):
        """
        :param num_virtual_replicas: number of virtual replicas of each cache server
        :param expire: expiration time for keys in seconds.
        """
        config = conf.config()

        self.cache = LRUCache(capacity)
        self.num_virtual_replicas = num_virtual_replicas

        # Cache server configuration
        self.ADDRESS = address if address else config.ADDRESS
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.ADDRESS)
        self.clients = {}  # (ip, (id, socket, ip:port)
        print("Starting server at {}:{}".format(*self.ADDRESS))
        self.server_socket.listen(config.LISTEN_CAPACITY)

        # Communication configuration
        self.HEADER_LENGTH = config.HEADER_LENGTH
        self.FORMAT = config.FORMAT
        self.LISTEN_CAPACITY = config.LISTEN_CAPACITY

        # Logging
        # TODO: If there is already a cache.json file, run reconstruction
        self.filename = 'cache.json' if filename is None else filename
        self.logger = logger.Logger(filename=self.filename, mode='a', batch_size=1)

        self.monitor()  # start the server

    def parse_message(self, message):
        """
        Parse and execute the command
        :param message: the message sent by the cache_server
        :return: depends on the operation that was carried out after parsing message
        """
        # This should run in a separate thread
        message = pickle.loads(message)
        self.logger.log(message)

        if message[0] == "set":
            return self.cache.set(message[1], message[2])

        elif message[0] == "del":
            return self.cache.delete(message[1])

        elif message[0] == "get":
            return self.cache.get(message[1])

        elif message[0] == "add":
            return self.cache.add(message[1], message[2])

        else:
            print("Only these keywords are supported: get, set, delete")

        return message

    def handle_client(self, client_socket):
        """
        Listen to queries from specific client.
        :param client_socket:
        :param client_address:
        :return:
        """
        while True:
            response = client_socket.recv(self.HEADER_LENGTH)
            if not response:
                continue
            message_length = int(response.decode(self.FORMAT))
            message = client_socket.recv(message_length)
            response = self.parse_message(message)
            utils.send_message(response, client_socket, self.HEADER_LENGTH, self.FORMAT)

    def monitor(self):
        """
        Listens for new connections and queries from the clients. And add it as a cache server.
        """
        while True:
            client_socket, client_address = self.server_socket.accept()
            print("New client connection accepted: {}:{}".format(*client_address))
            threading.Thread(target=self.handle_client, args=[client_socket]).start()


if __name__ == '__main__':
    server = CacheServer(address=('localhost', 2050))
