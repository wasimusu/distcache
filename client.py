"""
Still a cache server. This does not interact with the client.
"""

import pickle
import socket
import configure as config
import sys
import threading

config = config.config()


class dcache_client:
    def __init__(self, server_ip, server_port, client_id, capacity=100):
        """
        :param capacity: capacity of the cache in MBs
        """
        self.cache = {}
        self.capacity = capacity
        self.id = client_id  # Congrats! You're already registered with the server
        self.server_address = (server_ip, int(server_port))
        self.garbage_cache_response = "@!#$!@#"

        # Start the connection with the server. socket. connect
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)
        print("Client connected at address {}:{}".format(*self.server_address))
        # TODO: Need to register the client so that server knows port also

    def get(self, key):
        """
        Get the value corresponding to the key.
        For now, the value of keys can not be boolean
        :return: value of the key if it exists, otherwise False.
        """
        response = self.cache.get(key, self.garbage_cache_response)
        return response if response != self.garbage_cache_response else False

    def set(self, key, value):
        """
        The server decided the key value be stored in this client.
        If it is new, just add to the cache
        If the key is old, update it with new value and also the LRU
        :return: boolean indicating success of the operation
        """
        self.cache[key] = value
        return True

    def delete(self, key):
        """
        The server wants the key deleted.
        """
        del self.cache[key]
        return True

    def execute_query(self, message):
        response = self.parse_message(message)
        return self.send(response)

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
            response = self.client_socket.recv(config.HEADER_LENGTH)
            if not response:
                continue
            message_length = int(response.decode(config.FORMAT))
            message = self.client_socket.recv(message_length)
            thread = threading.Thread(target=self.execute_query, args=(message))

    def parse_message(self, message):
        """
        Parse and execute the command
        :param message: the message sent by the dcache_server
        :return: depends on the operation that was carried out after parsing message
        """
        # This should run in a separate thread
        message = pickle.loads(message)

        if message.get("set", config.RANDOM_STRING) != config.RANDOM_STRING:
            print("set ", message[0:])
            return self.set(message[1], message[2])

        elif message.get("delete", config.RANDOM_STRING) != config.RANDOM_STRING:
            print("delete ", message[0:])
            return self.delete(message[1])

        elif message.get("get", config.RANDOM_STRING) != config.RANDOM_STRING:
            print("get ", message[0:])
            return self.get(message[1])

        else:
            print("Only these keywords are supported: get, set, delete")

        return None

    def send(self, message):
        """ Central place to communicate with the server for all the needs of the client """
        print("Client Send message: {}".format(message))
        message = pickle.dumps(message)
        send_length = f"{len(message):<{config.HEADER_LENGTH}}"
        self.client_socket.send(bytes(send_length, config.FORMAT))
        self.client_socket.send(message)

        # Receive and decode response
        while True:
            message = self.client_socket.recv(config.HEADER_LENGTH)
            if not message:
                continue
            message_length = int(message.decode(config.FORMAT))

            message = self.client_socket.recv(message_length)

            response = pickle.loads(message)
            print("Server's response: ", response)
            break

        return response


if __name__ == '__main__':
    print(sys.argv)
    server_ip, server_port, client_id = sys.argv[1:]
    client = dcache_client(server_ip, server_port, client_id)
    pass
