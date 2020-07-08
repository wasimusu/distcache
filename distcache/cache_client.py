"""
Implements distcache client. It interacts with the users.
"""

import socket

from distcache import config as conf
from distcache.consistent_hashing import ConsistentHashing
from distcache import utils


# Each client has list of all servers.
# Do servers register with the client?

class CacheClient:
    """
    Implements cache client. It responds to user requests.
    ?? monitors health of cache clients.
    """

    def __init__(self):
        """
        """
        self.config = conf.config()

        # Communication configurations
        self.FORMAT = self.config.FORMAT
        self.HEADER_LENGTH = self.config.HEADER_LENGTH

        # Start the connection with the server. socket. connect
        self.servers = self.config.get_server_pool()
        self.ring = ConsistentHashing(self.config.server_pool)

    def _get_server_for_key(self, key):
        """
        :return: client_socket for the given key
        """
        return self.ring.get_node(key)

    def execute_query(self, key, message):
        """
        The central place to execute all the client queries.
        It finds the server for the query. Creates a socket. Sends message to the server.
        And conveys the server response to the calling function.

        :param key: the user defined key which is to be manipulated.
        :param message: tuple of key plus operation and optionally values.
        :return: response of the server
        """
        # Get the address of the server containing the key
        server_address = self._get_server_for_key(key)

        # Create a socket to send the message to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(server_address)
        response = utils.send_receive_ack(message, self.client_socket, self.HEADER_LENGTH, self.FORMAT)
        self.client_socket.close()
        return response

    def set(self, key, value):
        """
        Set or update the value of key from the cache. Also updates the LRU cache for already existing key or (key, value)
        :return: bool value indicating if the operation was successful or not.
        """
        return self.execute_query(key, ("set", key, value))

    def get(self, key):
        """
        Get the value of key from the cache
        :return: corresponding value for the key
        """
        return self.execute_query(key, ("get", key))

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
        return self.execute_query(key, ("del", key))

    def increment(self, key):
        """
        Increment value corresponding to the key in a thread-safe manner.
        :return: boolean indicating if the operation was successful or not.
        """
        return self.execute_query(key, ("add", key, 1))

    def decrement(self, key):
        """
        Decrement value corresponding to the key in a thread-safe manner.
        :return: boolean indicating if the operation was successful or not.
        :rtype: bool
        """
        return self.execute_query(key, ("add", key, -1))

    def add(self, key, diff):
        """
        Add diff to the value corresponding to key in a thread safe manner.
        :param diff: the amount to be added to the value of key
        :return: boolean indicating if the operation was successful or not.
        :rtype: bool
        """
        return self.execute_query(key, ("add", key, diff))


if __name__ == '__main__':
    client = CacheClient()
