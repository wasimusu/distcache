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
    query, key
    store key, value
    remove key
    
    The server is always listening to the client. 
    It needs to detect if the client is:
    - It is alive.
    - It is not overwhelmed.
    
    Whose job is it to determine that a client is not overwhelmed?    
    How does a client reserve memory in python? Store until it reaches certain threshold.      
"""


# The server has a few things to do with the client


class dcache_server:
    def __init__(self):
        # Socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind
        self.server_socket.bind(config.ADDRESS)
        self.clients = []

    def start(self):
        # Listen
        print("Starting server at {}:{}".format(*config.ADDRESS))
        self.server_socket.listen(config.LISTEN_CAPACITY)

    def handle_connection(self, client_socket, addr):
        while True:
            message = client_socket.recv(config.HEADER_LENGTH)
            if not message:
                continue
            message_length = int(message.decode(config.FORMAT))

            message = client_socket.recv(message_length)
            response = self.parse_message(message, addr)
            self.send(response, addr)

    def register_client(self, addr):
        client_id = len(self.clients) + 1
        print("Adding a new client ", client_id, addr)
        self.clients.append(client_id)
        return client_id

    def parse_message(self, message, addr):
        message = pickle.loads(message)

        if isinstance(message, str):
            return self.register_client(addr)

        elif message.get("add", config.RANDOM_STRING) != config.RANDOM_STRING:
            print("add ", message["add"])

        elif message.get("remove", config.RANDOM_STRING) != config.RANDOM_STRING:
            print("remove ", message["remove"])

        elif message.get("query", config.RANDOM_STRING) != config.RANDOM_STRING:
            print("query ", message["query"])

        elif message.get("update", config.RANDOM_STRING) != config.RANDOM_STRING:
            print("update ", message["update"])

        else:
            print("Only these keywords are supported: register, add, remove, query, update")

        return None

    def monitor(self):
        print("Listening to clients now...")
        while True:
            addr, conn = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_connection, args=(addr, conn))
            thread.start()

    def send(self, message, addr):
        print("Client Send message: {}".format(message))
        message = pickle.dumps(message)
        send_length = f"{len(message):<{config.HEADER_LENGTH}}"
        # self.server_socket.connect(addr)
        self.server_socket.sendto(bytes(send_length, config.FORMAT), addr)
        self.server_socket.send(message)


if __name__ == '__main__':
    server = dcache_server()
    server.start()
    server.monitor()
