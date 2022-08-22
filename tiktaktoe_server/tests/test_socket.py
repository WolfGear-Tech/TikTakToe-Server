from socket import *
from unicodedata import name

import mock


class MyClass(object):
    def __init__(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect(("172.21.0.1", 8090))


def test_class():
    socket_config = {
        "fd": 316,
        "family": AddressFamily.AF_INET,
        "type": SocketKind.SOCK_STREAM,
        "proto": 0,
        "laddr": ("172.21.0.1", 56690),
        "raddr": ("172.21.0.1", 8090),
    }
    with mock.patch("socket.socket") as mock_socket:
        mock_socket.configure_mock(**socket_config)
        # mock_socket.return_value.recv.return_value = {"status": 200}
    c = MyClass()
    c.clientSocket
    # c.clientSocket.connect.assert_called_with('0.0.0.0', '6767')
    # mock_socket.name = "newteste"
    # print(mock_socket)
    # print(c.clientSocket.type)
    print(c.clientSocket.__repr__())
    print(c.clientSocket)


test_class()
