from socket import socket, gethostbyname, gethostname, AF_INET, SOCK_STREAM
from threading import Thread
from OtoPy import UsefulTools

oLogger = UsefulTools.OLogger(logStreamLevel="INFO")


SERVER_ADDR = (gethostbyname(gethostname()), 8090)
ENCODE_FORMAT = "utf-8"
DISCONECT_MESSAGE = "!DISCONNECT"
HANDLE_CONNECTION = True
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(SERVER_ADDR)

connectedClients = []

def ClientConnectionHandlerThread(socketConnection, clientIP):
    global HANDLE_CONNECTION
    oLogger.LogInfo(f"[NEW CONNECTION] - New connection thread open for the IP: <{clientIP}> !!")
    while HANDLE_CONNECTION:
        try:
            recivedMessage = socketConnection.recv(2048).decode(ENCODE_FORMAT)
            if recivedMessage != DISCONECT_MESSAGE:
                socketConnection.send("202#Message Recived and progagated".encode(ENCODE_FORMAT))
                oLogger.LogInfo(f"[MESSAGE RECIVED] - New Message recived from client {clientIP}  the new message is: <{recivedMessage}>")

                for client in connectedClients:
                    client.send(f"210#{recivedMessage}".encode(ENCODE_FORMAT)) # Send the message to all clients with code 210
            else:
                connectedClients.remove(socketConnection)
                socketConnection.send(f"1006#{DISCONECT_MESSAGE}".encode(ENCODE_FORMAT))
                socketConnection.close()
                oLogger.LogInfo(f"[DISCONNECT] - Client {clientIP} has disconnected from the server")
                break
        except:
            HANDLE_CONNECTION = False
            socketConnection.close()
            connectedClients.remove(socketConnection)
            oLogger.LogExceptError(f"[CLIENT DISCONNECTED] - The client with the IP: <{clientIP}> has disconnected")
    exit()


def SocketServerHandler():
    serverSocket.listen(10)
    oLogger.LogInfo(f"[SERVER STARTED] - Server is now listening on {SERVER_ADDR}")
    while True:
        clientSocket, clientIP = serverSocket.accept()
        connectedClients.append(clientSocket)
        Thread(target=ClientConnectionHandlerThread, args=(clientSocket, clientIP), daemon=True).start()
    

if (__name__ == "__main__"):
        SocketServerHandler()