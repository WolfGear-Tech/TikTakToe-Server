import logging
from socket import *

import mock
from faker import Faker

from tiktaktoe_server.handlers.network import SocketHandler

s = SocketHandler()
logging.getLogger("faker.factory").setLevel(logging.ERROR)

# with mock.patch('socket.socket') as mock_socket:
#     mock_socket.return_value.recv.return_value = some_data
#     t = TCPSocket()
#     t.connect('example.com', 12345)  # t.sock is a mock object, not a Socket


def test_EncodeMessage():
    # Arrange
    fake = Faker("pt_BR")
    status = 200
    text = fake.text()
    name = fake.name()
    ip = fake.ipv4()
    port = fake.port_number()
    mock_client_socket = socket(AF_INET, SOCK_STREAM)
    path = "tiktaktoe_server.handlers.network."
    with mock.patch(".s") as mock_server_socket:
        with mock.patch("SocketHandler.__ReciveData") as mockReciveData:
            mock_server_socket.accept.return_value = (mock_client_socket, ip)
            mockReciveData(mock_client_socket)

    # # Act
    # socket._SendData(client_socket, status=status, message=text, user={"name": name})

    # encode_message = socket

    # # Assert
    # assert type(encode_message) == bytes

    # # Act
    # decoded_message = socket._ReciveData(client_socket)

    # # Assert
    # assert type(decoded_message) == dict
    # assert decoded_message['status'] == 200
