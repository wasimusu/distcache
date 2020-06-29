"""
Implements network utils like sending and receiving message over socket
"""
import pickle


def send_message(message, client_socket, HEADER_LENGTH, FORMAT):
    """
    Sends message on the client_socket.

    Message sending occurs in two stages:
        First, the message is serialized using serializer and the length of message is sent encoded in FORMAT.
        Then, message is sent.

    :param message: the message to be sent. It can be any combination of different data types.
    :param client_socket: the socket on which message is sent
    :param FORMAT: the format in which length of message is to be encoded. (UTF-8 is default FORMAT)
    :returns: None
    """
    message = pickle.dumps(message)
    send_length = "{:<{}}".format(len(message), HEADER_LENGTH)
    client_socket.send(bytes(send_length, FORMAT))
    client_socket.send(message)


def receive_message(client_socket, HEADER_LENGTH, FORMAT):
    """
    Receives message on the client_socket

    :param client_socket: the socket on which message is received
    :param FORMAT: the format in which message length is to be encoded. (UTF-8 is default FORMAT)
    :returns: False if receiving message was not successful. Else, returns whatever message was received after
    deserializing it.
    """
    client_socket.settimeout(5)
    response = False  # In case of no response from cache servers, the response will be False (failed)
    while True:
        try:
            response = client_socket.recv(HEADER_LENGTH)
            if not response:
                continue
            message_length = int(response.decode(FORMAT))
            response = client_socket.recv(message_length)
            response = pickle.loads(response)
        finally:
            break
    return response


def send_receive_ack(message, client_socket, HEADER_LENGTH, FORMAT):
    """
    Sends message from the client_socket.
    Receives message on the client_socket

    :param message: Any message/object that is to be sent.
    :param client_socket: the socket on which to send and receive message.
    :param HEADER_LENGTH: the header length of the message.
    :param FORMAT: the format in which message length is to be encoded. (UTF-8 is default FORMAT)
    :return: response received. False if no response was received
    """
    send_message(message, client_socket, HEADER_LENGTH, FORMAT)
    return receive_message(client_socket, HEADER_LENGTH, FORMAT)
