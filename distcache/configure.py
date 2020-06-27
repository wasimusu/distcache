import socket


class config:
    def __init__(self):
        self.FORMAT = 'utf-8'
        self.HEADER_LENGTH = 64
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 5050
        self.ADDRESS = (self.IP, self.PORT)
        self.LISTEN_CAPACITY = 100
        self.RANDOM_STRING = "!@#@#$!@#!@"

        # Health probe configuration
        self.HEALTH_PROBE_PORT = 5190
        self.HEALTH_REPORT_PORT = self.HEALTH_PROBE_PORT + 100
        self.PROBE_EVERY_K_SECOND = 5
        self.HEARTBEAT_THRESH = 5  # k consecutive missing heartbeat means the server is dead
