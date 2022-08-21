from socket import socket, gethostbyname, gethostname, AF_INET, SOCK_STREAM
from threading import Thread


SERVER_ADDR = (gethostbyname(gethostname()), 8090)
ENCODE_FORMAT = "utf-8"
DISCONECT_MESSAGE = "!DISCONNECT"
HANDLE_CONNECTION = True
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(SERVER_ADDR)

connectedClients = []

def ClientConnectionHandlerThread(socketConnection, clientIP):
    print(f"[NEW CONNECTION] - New connection thread open for the IP: {clientIP} !!")
    while HANDLE_CONNECTION:
        recivedMessage = socketConnection.recv(2048).decode(ENCODE_FORMAT)
        if recivedMessage != DISCONECT_MESSAGE:
            socketConnection.send("200".encode(ENCODE_FORMAT))
            print(f"[MESSAGE RECIVED] - New Message reciver from client {clientIP}  the new message is: {recivedMessage}")
            for client in connectedClients:
                client.send(recivedMessage.encode(ENCODE_FORMAT))
        else:
            connectedClients.remove(socketConnection)
            print(f"[DISCONNECT] - Closing the connection thread for the IP: {clientIP} !!")
            break

    socketConnection.close()
    exit()


def SocketServerHandler():
    serverSocket.listen(10)
    print(f"[LISTENING] - The server is now listening on the IP: {SERVER_ADDR[0]} and the port: {SERVER_ADDR[1]}")
    while True:
        clientSocket, clientIP = serverSocket.accept()
        connectedClients.append(clientSocket)
        Thread(target=ClientConnectionHandlerThread, args=(clientSocket, clientIP), daemon=True).start()

if (__name__ == "__main__"):
    try:
        SocketServerHandler()
    except :
        print("[FORCED DISCONNECT] - One of the clients has disconnected !!")