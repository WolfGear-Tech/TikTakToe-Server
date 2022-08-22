import mock
import socket

class MyClass(object):

    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.connect('0.0.0.0', '6767')

def test_class():
    with mock.patch('socket.socket'):
        c = MyClass()
        c.tcp_socket.connect.assert_called_with('0.0.0.0', '6767')
        