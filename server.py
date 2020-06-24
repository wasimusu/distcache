import configure as config
import socket
import threading
import pickle

config = config.config()

"""
    When there is a new key, value. The client sends that key value to the server.
    The server finds a client to store that key value. And sends the (key, value) pair to that server

    Starting a new client.
    Each client is assigned a unique ID upon start and is registered with the server.
        
    What are the functions of the client.
    Every PC has a client running with a local cache.
    Whenever there is a query, first the local cache is consulted then if the key is not found, the server is queried.
    The server then determines the location of the cache and queries that location for the value of the key
    
    So there are three kinds of message, the client sends to the server. 
    The message always is a dictionary, apart from the first message being the length of the message.
    
    register
    get, key
    set key, value
    delete key
    
    The server is always listening to the client. 
    It needs to detect if the client is:
    - It is alive.
    - It is not overwhelmed. It should not be overwhelmed. It should just clear some of the cache.
    And get back to work.
    
    Whose job is it to determine that a client is not overwhelmed?    
    How does a client reserve memory in python? Store until it reaches certain threshold.      
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

    def handle_connection(self, client_socket, client_address):
        while True:
            message = client_socket.recv(config.HEADER_LENGTH)
            if not message:
                continue
            message_length = int(message.decode(config.FORMAT))

            message = client_socket.recv(message_length)
            response = self.parse_message(message, client_address)
            self.send(response, client_socket, client_address)

    def send(self, message, client_socket):
        print("Client Send message: {}".format(message))
        message = pickle.dumps(message)
        send_length = f"{len(message):<{config.HEADER_LENGTH}}"
        client_socket.send(bytes(send_length, config.FORMAT))
        client_socket.send(message)

        while True:
            response = client_socket.recv(config.HEADER_LENGTH)
            if not response:
                continue
            message_length = response.decode(config.FORMAT)
            response = client_socket.recv(message_length)
            response = response.decode(config.FORMAT)
            break
        return response

    def set(self, key, value):
        """
        Set or update the value of key from the cache. Also updates the LRU cache for already existing key or (key, value)
        :return: bool value indicating if the operation was successful or not.
        """
        # Get the address of the server containing the key
        client_socket, client_address = self._get_server_for_key(key)
        response = self.send(("set", (key, value)), client_socket, client_address)
        return True if response else False

    def get(self, key):
        """
        Get the value of key from the cache
        :return: corresponding value for the key
        """
        # Get the address of the server containing the key
        client_socket, client_address = self._get_server_for_key(key)
        response = self.send(("get", key), client_socket, client_address)
        return response

    def delete(self, key):
        """
        Get the value of key from the cache
        :return: corresponding value for the key
        """
        # Get the address of the server containing the key
        client_socket, client_address = self._get_server_for_key(key)
        response = self.send(("del", key), client_socket, client_address)
        return response

    def _get_server_for_key(self, key):
        """
        Should implement a consistent hashing function.
        :return:
        """
        return hash(key) % len(self.clients)


if __name__ == '__main__':
    server = dcache_server(5)
    server.spawn()
    server.spawn()
