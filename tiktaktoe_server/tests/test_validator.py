# import logging
# import mock
# from faker import Faker
# from ..handlers.network import SocketHandler

# logging.getLogger('faker.factory').setLevel(logging.ERROR)

# # with mock.patch('socket.socket') as mock_socket:
# #     mock_socket.return_value.recv.return_value = some_data
# #     t = TCPSocket()
# #     t.connect('example.com', 12345)  # t.sock is a mock object, not a Socket

# def test_EncodeMessage(client_socket):
#     # Arrange
#     fake = Faker("pt_BR")
#     status = 200
#     text = fake.text()
#     name = fake.name()
#     ip = fake.ipv4()
#     port = fake.port_number()
#     with mock.patch('socket.socket') as mock_socket:
#         clientSocket = socket(AF_INET, SOCK_STREAM)
#         mock_socket.return_value.recv.return_value = (ip,port)
#         socket = SocketHandler()
#         mock_socket.connect(ip, port)

#     # Act
#     socket._SendData(client_socket, status=status, message=text, user={"name": name})
    
#     encode_message = socket
    
#     # Assert
#     assert type(encode_message) == bytes

#     # Act
#     decoded_message = socket._ReciveData(client_socket)
     
#     # Assert
#     assert type(decoded_message) == dict
#     assert decoded_message['status'] == 200

