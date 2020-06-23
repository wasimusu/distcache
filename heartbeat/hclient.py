import socket

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (socket.gethostbyname(socket.gethostname()), 5050)

        # ACK Message details
        self.ACK_HEADER = 3
        self.ACK_FORMAT = 'utf-8'
        self.ACK_MESSAGE = 'ACK'.encode(self.ACK_FORMAT)

    def start(self):
        self.client_socket.connect(self.server_address)

    def relay_health(self):
        print("Responding to health query from the server...")
        while True:
            response = self.client_socket.recv(3)
            if not response: continue
            if response == self.ACK_MESSAGE:
                self.client_socket.send(self.ACK_MESSAGE)


if __name__ == '__main__':
    client = Client()
    client.start()
    client.relay_health()
