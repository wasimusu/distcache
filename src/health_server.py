import socket
import threading
import time
import pickle

from src import configure as config

config = config.config()


class Server:
    def __init__(self):
        # Client details
        self.clients = []
        self.unhealthy_clients = []  # list of client_socket

        # ACK Message details
        self.ACK_HEADER = 3
        self.ACK_FORMAT = config.FORMAT
        self.ACK_MESSAGE = 'ACK'.encode(self.ACK_FORMAT)

        # HEARTBEAT configuration
        self.DEAD_THRESH = config.HEARTBEAT_THRESH
        self.probe_every_k_second = config.PROBE_EVERY_K_SECOND

        # Configure and start the health monitoring server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (config.IP, config.HEALTH_PORT)
        self.server_socket.bind(self.server_address)
        print("Starting the server. Listening at {}:{}".format(*self.server_address))
        self.server_socket.listen()

        # Configure and start the health reporting client
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_address = (config.IP, config.PORT)
        # self.client_socket.connect(self.client_address)

    def monitor_client(self, client_socket, client_address):
        """
        Send heart beat every k second.
        If three heart beat requests are not acknowledged, the client is dead.
        :param client_socket: client socket
        :param client_address: client address
        :return: None
        """
        print("Registered a new client {}:{}".format(*client_address))
        self.clients.append(client_address)
        no_beat_count = 0
        while True:
            time.sleep(self.probe_every_k_second)
            try:
                bytes_sent = client_socket.send(self.ACK_MESSAGE)
                if bytes_sent != self.ACK_HEADER:
                    break

                client_socket.settimeout(5)
                response = client_socket.recv(self.ACK_HEADER)
                if response:
                    if response == self.ACK_MESSAGE:
                        no_beat_count = 0
                        continue
                    else:
                        no_beat_count += 1
            except:
                no_beat_count += 1

            if no_beat_count == self.DEAD_THRESH:
                break

        print("The client {}:{} is dead. No beat detected in the last {} attempts.".format(*client_address,
                                                                                           self.DEAD_THRESH))
        self.clients.remove(client_address)
        self.unhealthy_clients.append(client_address)

    def summary(self):
        """
        Keep logging the number of healthy clients in a fixed time interval
        :return: None
        """
        while True:
            time.sleep(5)
            print("Active healthy clients: {}".format(len(self.clients)))

    def get_healthy_clients(self):
        """
        Return the list of healthy clients
        :return: [int] returns the number of healthy clients
        """
        return self.unhealthy_clients

    def send(self, message, client_socket):
        print("Sending health report: {}".format(message))
        message = pickle.dumps(message)
        send_length = f"{len(message):<{config.HEADER_LENGTH}}"
        client_socket.send(bytes(send_length, config.FORMAT))
        client_socket.send(message)

        client_socket.settimeout(5)
        response = False  # In case of no response from cache servers, the response will be False (failed)
        while True:
            try:
                response = client_socket.recv(config.HEADER_LENGTH)
                if not response:
                    continue
                message_length = int(response.decode(config.FORMAT))
                response = client_socket.recv(message_length)
                response = pickle.loads(response)
            finally:
                break

        print("Response received: {}\n".format(response))
        if response:
            self.unhealthy_clients = []
        return response

    def monitor(self):
        """
        Monitor the health of the clients.
        :return: None
        """
        print("Monitoring the clients...")
        threading.Thread(target=self.summary).start()
        # threading.Thread(target=self.send, args=([], self.client_socket, self.client_address)).start()
        while True:
            client_socket, client_address = self.server_socket.accept()
            thread = threading.Thread(target=self.monitor_client, args=(client_socket, client_address))
            thread.start()


if __name__ == '__main__':
    server = Server()
    server.monitor()
