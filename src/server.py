from src import configure as config

import socket
import pickle

config = config.config()

"""
The server is always listening to the client. It needs to detect if the client is alive.
"""


class dcache_server:
    def __init__(self, num_virtual_replicas=10):
        # Socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind
        self.server_socket.bind(config.ADDRESS)
        self.clients = {}
        self.start()

    def start(self):
        # Listen
        print("Starting server at {}:{}".format(*config.ADDRESS))
        self.server_socket.listen(config.LISTEN_CAPACITY)

    def spawn(self):
        """
        Listens for new connections. And add it as a cache server.
        """
        while True:
            client_socket, client_address = self.server_socket.accept()

            client_id = len(self.clients)
            self.clients[client_id] = (client_socket, client_address)

            message = pickle.dumps(client_id)
            send_length = f"{len(message):<{config.HEADER_LENGTH}}"
            client_socket.send(bytes(send_length, config.FORMAT))
            client_socket.send(message)
            break

        print("Spawned a client at {}:{}".format(*client_address))

    def send(self, message, client_socket):
        print("Sending client message: {}".format(message))
        message = pickle.dumps(message)
        send_length = f"{len(message):<{config.HEADER_LENGTH}}"
        client_socket.send(bytes(send_length, config.FORMAT))
        client_socket.send(message)
        print("Sent!")

        while True:
            response = client_socket.recv(config.HEADER_LENGTH)
            if not response:
                continue
            message_length = int(response.decode(config.FORMAT))
            response = client_socket.recv(message_length)
            response = pickle.loads(response)
            break
        print("Response received: ", response)
        return response

    def set(self, key, value):
        """
        Set or update the value of key from the cache. Also updates the LRU cache for already existing key or (key, value)
        :return: bool value indicating if the operation was successful or not.
        """
        # Get the address of the server containing the key
        client_socket, client_address = self._get_server_for_key(key)
        response = self.send(("set", key, value), client_socket)
        return True if response else False

    def get(self, key):
        """
        Get the value of key from the cache
        :return: corresponding value for the key
        """
        # Get the address of the server containing the key
        client_socket, client_address = self._get_server_for_key(key)
        response = self.send(("get", key), client_socket)
        return response

    def delete(self, key):
        """
        Get the value of key from the cache
        :return: corresponding value for the key
        """
        # Get the address of the server containing the key
        client_socket, client_address = self._get_server_for_key(key)
        response = self.send(("del", key), client_socket)
        return response

    def _get_server_for_key(self, key):
        """
        Should implement a consistent hashing function.
        :return:
        """
        return self.clients[hash(key) % len(self.clients)]


if __name__ == '__main__':
    server = dcache_server(5)
    server.spawn()
    # server.spawn()
    # server.spawn()

    server.set("wasim", "akram")
    server.set("ram", "prasad")
    server.set(1, 2)
    server.set(3, 6)
    server.set("hey", "bhaga")
    print(server.get("hey"))
    print(server.get(1))
    server.set("hey", "man")
    print(server.get("hey"))
    server.delete(3)
    print(server.get(3))
    print(server.get("wasim"))
