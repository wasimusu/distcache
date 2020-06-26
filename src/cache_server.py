import socket
import threading
import json
import os

from src import configure as config
from src.consistenthashing import ConsistentHashing
from src import utils
from src import logger

config = config.config()

"""
The server is always listening to the client. It needs to detect if the client is alive.
"""


class CacheServer:
    def __init__(self, num_virtual_replicas=5, expire=0, reconstruct=False):
        """
        :param[int] num_virtual_replicas: number of virtual replicas of each cache server
        :param[int] expire: expiration time for keys in seconds.
        """
        self.num_virtual_replicas = num_virtual_replicas
        self.expire = expire
        self.ring = ConsistentHashing()
        self.cache_server_count = 0

        # Cache server configuration
        self.ADDRESS = config.ADDRESS
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.ADDRESS)
        self.clients = {}  # (ip, (id, socket, ip:port)
        print("Starting server at {}:{}".format(*self.ADDRESS))
        self.server_socket.listen(config.LISTEN_CAPACITY)

        # Health monitor server configuration
        self.health_server_address = (config.IP, config.HEALTH_REPORT_PORT)
        self.health_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.health_server_socket.bind(self.health_server_address)
        self.health_server_socket.listen()  # Only one health server is reporting health status
        threading.Thread(target=self.monitor_health).start()

        # Cache stats
        self.cache_hits = 0
        self.query_count = 0

        # Communication configuration
        self.HEADER_LENGTH = config.HEADER_LENGTH
        self.FORMAT = config.FORMAT
        self.LISTEN_CAPACITY = config.LISTEN_CAPACITY

        # Logging
        # TODO: If there is already a cache.json file, run reconstruction
        self.filename = 'cache.json'
        self.logger = logger.Logger(filename=self.filename, mode='a', batch_size=1)

    def spawn(self):
        """
        Listens for new connections. And add it as a cache server.
        """
        while True:
            client_socket, client_address = self.server_socket.accept()
            utils.send_message(self.cache_server_count, client_socket, self.HEADER_LENGTH, self.FORMAT)

            self.clients[client_address[0]] = (self.cache_server_count, client_socket, client_address)
            self.ring.add_node(client_address[0], self.num_virtual_replicas)  # Consistent hashing on IP Address alone
            break

        self.cache_server_count += 1
        print("Spawned a client at {}:{}".format(*client_address))

    def monitor_health(self):
        """
        Continuously listens to health monitoring server.
        Health monitoring server sends list of unavailable servers if any.
        :return: None
        """
        client_socket, health_client_address = self.health_server_socket.accept()
        print("Connected to health monitoring server at {}:{}".format(*health_client_address))
        while True:
            try:
                unavailable_servers = utils.receive_message(client_socket, self.HEADER_LENGTH, self.FORMAT)
                response = True if unavailable_servers else False
                if response:
                    for server in unavailable_servers:
                        self._delist_unavailable_server(server)
                utils.send_message(response, client_socket, self.HEADER_LENGTH, self.FORMAT)
            except:
                pass  # We will continue to monitor the health of servers until we die

    def send_receive(self, message, client_socket):
        print("Sending client message: {}".format(message))
        response = utils.send_receive_ack(message, client_socket, self.HEADER_LENGTH, self.FORMAT)
        print("Response received: {}\n".format(response))
        return response

    def set(self, key, value):
        """
        Set or update the value of key from the cache. Also updates the LRU cache for already existing key or (key, value)
        :return: bool value indicating if the operation was successful or not.
        """
        # Get the address of the server containing the key
        client_socket, client_address = self._get_server_for_key(key)
        response = self.send_receive(("set", key, value), client_socket)
        self.logger.log(("set", key, value))
        return True if response else False

    def get(self, key):
        """
        Get the value of key from the cache
        :return: corresponding value for the key
        """
        # Get the address of the server containing the key
        client_socket, client_address = self._get_server_for_key(key)
        response = self.send_receive(("get", key), client_socket)
        self.logger.log(("get", key))

        self.query_count += 1
        self.cache_hits += (response != False)

        return response

    def gets(self, keys):
        """
        Gets the values of keys from the cache. Same as get but avoids expensive network calls.
        If you want two keys which are on different server, gets is same as get or a bit slower.
        :return [list of values]: corresponding values for the keys
        """
        pass

    def delete(self, key):
        """
        Get the value of key from the cache
        :return: corresponding value for the key
        """
        # Get the address of the server containing the key
        client_socket, client_address = self._get_server_for_key(key)
        response = self.send_receive(("del", key), client_socket)
        self.logger.log(("del", key))
        return response

    def increment(self, key):
        """
        Increment value corresponding to the key in a thread-safe manner.
        :return: boolean indicating if the operation was successful or not.
        """
        return self.add(key, 1)

    def decrement(self, key):
        """
        Decrement value corresponding to the key in a thread-safe manner.
        :return: boolean indicating if the operation was successful or not.
        :rtype: bool
        """
        return self.add(key, -1)

    def add(self, key, diff):
        """
        Add diff to the value corresponding to key in a thread safe manner.
        :param diff: the amount to be added to the value of key
        :return: boolean indicating if the operation was successful or not.
        :rtype: bool
        """
        client_socket, client_address = self._get_server_for_key(key)
        response = self.send_receive(("add", key, diff), client_socket)
        self.logger.log(("add", key, diff))
        return response

    def _get_server_for_key(self, key):
        """
        :return: client_socket for the given key
        """
        return self.clients[self.ring.get_node(key)][1], None

    def _delist_unavailable_server(self, client_address):
        """
        The health check metrics found an unavailable server. It should be removed from the server space.
        :return: None
        """
        self.ring.remove_node(client_address[0])

    def stats(self):
        """
        Prints some of the important stats like hits, misses and total query counts
        :return: None
        """
        print("Total queries: ".format(self.query_count))
        print("Cache hits   : {}\t{.2f}".format(self.cache_hits, self.cache_hits / self.query_count))
        print("Cache miss   : {}\t{.2f}".format(self.cache_hits, self.cache_hits / self.query_count))

    def reconstruct_from_log(self):
        """
        Usage:
            Start the server.
            Spawn the clients.
            Then ask the server to reconstruct from log file
        """
        # Can't reconstruct if there is no file
        if not os.path.exists(self.filename):
            return

        with open(self.filename, mode='r') as file:
            for line in file.readlines():
                object = json.loads(line)
                print("Object : ", object)

                # Now you need to parse
                if object[0] == "set":
                    self.set(object[1], object[2])

                elif object[0] == "get":
                    self.get(object[1])

                elif object[0] == "del":
                    self.delete(object[1])

                elif object[0] == "gets":
                    self.gets(object[1:])

                else:
                    pass

    def close(self):
        """
        Close the cache server. Close all of its clients.
        :return:
        """
        # Send (close) to every cache client.
        # Ask the health server to shutdown.

        self.logger.close()  # Flushes the objects in logging queues as well

        # Just an interesting thought. If the server shuts down, eventually everyone shuts down.
        self.health_server_socket.close()
        self.server_socket.close()


if __name__ == '__main__':
    pass
