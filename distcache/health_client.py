import socket
from distcache import config

config = config.config()


class HealthClient:
    """
    Implements a health client to respond to health probes from health server
    """

    def __init__(self):
        """
        Implements a health client to send report of CacheClient
        """

        # ACK Message details
        self.ACK_HEADER = 3
        self.ACK_FORMAT = 'utf-8'
        self.ACK_MESSAGE = 'ACK'.encode(self.ACK_FORMAT)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (config.IP, config.HEALTH_PROBE_PORT)
        self.client_socket.connect(self.server_address)

    def relay_health(self):
        """
        If it receives any health probe from the server it replies with an ACK_MESSAGE to acknowledge that it is alive
        and well.

        :return: None
        """
        print("Responding to health query from the server...")
        while True:
            response = self.client_socket.recv(3)
            if not response: continue
            if response == self.ACK_MESSAGE:
                self.client_socket.send(self.ACK_MESSAGE)


if __name__ == '__main__':
    client = HealthClient()
    client.relay_health()
