import socket
import threading
import time

from distcache import config
from distcache import utils

config = config.config()


class HealthServer:
    """
    Implements a health server to monitor health of all clients and report it to the cache server.
    """

    def __init__(self):
        """
        Initializes a HealthServer object.
        """
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
        self.server_address = (config.IP, config.HEALTH_PROBE_PORT)
        self.server_socket.bind(self.server_address)
        print("Starting the server. Listening at {}:{}".format(*self.server_address))
        self.server_socket.listen()

        # Configure and start the health reporting client
        self.reporting_address = (config.IP, config.HEALTH_REPORT_PORT)
        self.reporting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Trying to connect to {}:{}".format(*self.reporting_address))
        self.reporting_socket.connect(self.reporting_address)

    def probe_health(self, client_socket, client_address):
        """
        Sends heart beat every k second. If three heart beat requests are not acknowledged for n times, the client is dead.

        :param client_socket: client socket on which health probes are to be sent and response received.
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

    def monitor(self):
        """
        Listens for new HealthClient connections. Monitors the health of the clients.

        :return: None
        """
        print("Monitoring the clients...")
        threading.Thread(target=self.summary).start()
        threading.Thread(target=self.report_health, args=([], self.reporting_socket)).start()
        while True:
            client_socket, client_address = self.server_socket.accept()
            thread = threading.Thread(target=self.probe_health, args=(client_socket, client_address))
            thread.start()

    def report_health(self, message, client_socket):
        """
        Report the cache clients health to the server

        :param message: any message. In this case list of unavailable servers
        :param client_socket: socket object connected to the cache server
        :return: None
        """
        while True:
            time.sleep(5)  # Report health regularly.

            # The response is false if the server does is unable to send any ACK
            response = utils.send_receive_ack(message, client_socket, config.HEADER_LENGTH, config.FORMAT)

            print("Report received by server: {}\n".format(response))
            if response:
                self.unhealthy_clients = []

    def summary(self):
        """
        Keep logging the number of healthy clients in a fixed time interval

        :return: None
        """
        while True:
            time.sleep(5)
            print("Active healthy clients: {}".format(len(self.clients)))


if __name__ == '__main__':
    server = HealthServer()
    server.monitor()
