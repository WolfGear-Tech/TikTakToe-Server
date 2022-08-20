from socket import socket, gethostbyname, AF_INET, SOCK_STREAM
from threading import Thread


SERVER_ADDR = (gethostbyname(socket.gethostname()), 8090)
ENCODE_FORMAT = "utf-8"
DISCONECT_MESSAGE = "!DISCONNECT"
HANDLE_CONNECTION = True
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(SERVER_ADDR)

def ClientConnectionHandlerThread(socketConnection, clientIP):
    print(f"[NEW CONNECTION] - New connection thread open for the IP: {clientIP} !!")
    while HANDLE_CONNECTION:
        recivedMessage = socketConnection.recv(2048).decode(ENCODE_FORMAT)
        if recivedMessage != DISCONECT_MESSAGE:
            print(f"[MESSAGE RECIVED] - New Message reciver from client {clientIP}  the new message is: {recivedMessage}")        
        else:
            print(f"[DISCONNECT] - Closing the connection thread for the IP: {clientIP} !!")

    socketConnection.close()
    exit()


def SocketServerHandler():
    serverSocket.listen(10)
    print(f"[LISTENING] - The server is now listening on the IP: {SERVER_ADDR[0]} and the port: {SERVER_ADDR[1]}")
    while True:
        clientSocket, clientIP = serverSocket.accept()
        Thread(target=ClientConnectionHandlerThread, args=(clientSocket, clientIP)).start()

if (__name__ == "__main__"):
    SocketServerHandler()
