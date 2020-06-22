import pickle
import socket
import configure as config

config = config.config()


class dcache_client:
    def __init__(self, capacity=100):
        """
        :param capacity: capacity of the cache in MBs
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cache = {}
        self.capacity = capacity
        self.id = -1

    def connect(self):
        self.client_socket.connect(config.ADDRESS)

    def register(self):
        self.send("register")

    def query(self, key):
        self.send({"query": key})

    def _local_add(self, key, value):
        """
        Intended to be called by the client only. Not to be prompted by user.
        The server decided the key value be stored in this client.
        :param key:
        :param value:
        :return:
        """
        self.cache[key] = value

    def _local_remove(self, key):
        """
        The server wants the key deleted.
        """
        del self.cache[key]

    def add(self, key, value):
        """
        If it is new, just add to the cache
        If the key is old, update it with new value
        """
        self.send({"add": {key: value}})

    def monitor(self):
        """
        A client has a few things to listen for.
        The server may ping to monitor your health.
        The server may request for key, value pair
        The server can request you to store key, value pair
        The server can request you to delete key from cache
        :return:
        """
        pass

    def send(self, message):
        """ Central place to communicate with the server for all the needs of the client """
        print("Send message: {}".format(message))
        message = pickle.dumps(message)
        send_length = f"{len(message):<{config.HEADER_LENGTH}}"
        self.client_socket.send(bytes(send_length, config.FORMAT))
        self.client_socket.send(message)

    def parse_message(self, message):
        pass


if __name__ == '__main__':
    d1 = dcache_client(100)
    d1.connect()
    d1.register()
    d1.add(1, "apple")
    d1.add(2, "orange")
    d1.add(3, "pineapple")
