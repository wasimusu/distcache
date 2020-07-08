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

        # This has to be same across the distributed system
        # Has to be synced using some sync mechanisms like Anisible, Chef/Puppet
        # Each server in the server_pool has to be live/healthy
        self.server_pool = [('localhost', 2050)]

        # Snapshot setting
        self.save_every_k_seconds = 60
        self.min_changes = 1  # Snapshot only if min_changes occurred

    def get_server_pool(self):
        return self.server_pool

    def add_server(self, server):
        self.server_pool.append(server)

    def remove_server(self, server):
        self.server_pool.remove(server)
