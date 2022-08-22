import socket

import mock

IP = "localhost"
PORT = 80


class classA:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.connect((IP, PORT))

    def data_collection(self):
        buf = self.s.recv.decode()
        return buf


def test_data_collection():
    with mock.patch("socket.socket") as mock_socket:
        A = classA()
        mock_socket.return_value.recv.decode.return_value = "ABC123"
        buf = A.data_collection()
        assert "ABC123" == buf
