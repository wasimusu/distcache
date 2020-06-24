import socket


class config:
    def __init__(self):
        self.FORMAT = 'utf-8'
        self.HEADER_LENGTH = 64
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 5040
        self.ADDRESS = (self.IP, self.PORT)
        self.LISTEN_CAPACITY = 100
        self.RANDOM_STRING = "!@#@#$!@#!@"
