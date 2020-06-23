import socket
import threading
import time


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (socket.gethostbyname(socket.gethostname()), 5050)
        self.server_socket.bind(self.server_address)

        # Client details
        self.clients = []

        # ACK Message details
        self.ACK_HEADER = 3
        self.ACK_FORMAT = 'utf-8'
        self.ACK_MESSAGE = 'ACK'.encode(self.ACK_FORMAT)

        # HEARTBEAT configuration
        self.DEAD_THRESH = 3

    def start(self):
        """
        Start the heartbeat server
        :return: None
        """
        print("Starting the server. Listening at {}:{}".format(*self.server_address))
        self.server_socket.listen(100)

    def monitor_client(self, client_socket, client_address):
        """
        Send heart beat every 5 second.
        If three heart beat requests are not acknowledged, the client is dead.
        :param client_socket: client socket
        :param client_address: client address
        :return: None
        """
        print("Registered a new client {}:{}".format(*client_address))
        self.clients.append(client_address)
        no_beat_count = 0
        while True:
            time.sleep(5)
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
        Return the number of healthy clients
        :return: [int] returns the number of healthy clients
        """
        return len(self.clients)

    def monitor(self):
        """
        Monitor the health of the clients.
        :return: None
        """
        print("Monitoring the clients...")
        threading.Thread(target=self.summary).start()
        while True:
            client_socket, client_address = self.server_socket.accept()
            thread = threading.Thread(target=self.monitor_client, args=(client_socket, client_address))
            thread.start()


if __name__ == '__main__':
    server = Server()
    server.start()
    server.monitor()
