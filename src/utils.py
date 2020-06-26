"""
Implements network utils like sending and receiving message over socket
"""
import pickle


def send_message(message, client_socket, HEADER_LENGTH, FORMAT):
    """
    sends message on the client_socket
    """
    message = pickle.dumps(message)
    send_length = f"{len(message):<{HEADER_LENGTH}}"
    client_socket.send(bytes(send_length, FORMAT))
    client_socket.send(message)


def receive_message(client_socket, HEADER_LENGTH, FORMAT):
    """
    Receives message on the client_socket
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
    Sends message on the client_socket.
    Receives message on the client_socket
    :param message: Any message/object.
    :return: response received
    """
    send_message(message, client_socket, HEADER_LENGTH, FORMAT)
    return receive_message(client_socket, HEADER_LENGTH, FORMAT)
