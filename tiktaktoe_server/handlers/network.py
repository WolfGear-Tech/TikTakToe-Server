from logging import exception
import sys
import json
import base64
from socket import socket, gethostbyname, gethostname, AF_INET, SOCK_STREAM
from threading import Thread
from OtoPy import UsefulTools

class SocketHandler():
    oLogger = UsefulTools.OLogger(logStreamLevel="DEBUG")
    
    def __init__(self):
        self.SERVER_ADDR = (gethostbyname(gethostname()), 8090)
        self.DISCONECT_MESSAGE = "!DISCONNECT"
        self.SOCKET_SERVICE = True
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.connectedClients = []

    def __ReciveData(self, socket):
        data = socket.recv(2048)
        decodedData = json.loads(base64.b64decode(data).decode('utf-8').replace("'",'"'))
        self.oLogger.LogDebug(sys.getsizeof(data))
        return decodedData

    def __SendData(self, socket,  **data):
        encodedMessage = base64.b64encode(bytes(str(data),'utf-8'))
        socket.send(encodedMessage)

    def __SendDataToAllConnectedClients(self, **data):
        for client in self.connectedClients:
            self.__SendData(client, **data)

    def __HandleClientConnection(self, clientSocket, clientIP):
        while self.SOCKET_SERVICE:
            try:
                recivedData = self.__ReciveData(clientSocket)

                if recivedData["message"] != self.DISCONECT_MESSAGE:
                    self.__SendData(clientSocket, status=202, message="Message Recived")
                    self.oLogger.LogInfo(f"[DATA RECIVED]-{clientIP}: {recivedData}")
                    self.__SendDataToAllConnectedClients(status=210, message=recivedData["message"], user=recivedData["user"]["name"])
                        
                else:
                    self.connectedClients.remove(clientSocket)
                    self.__SendData(clientSocket, status=1006, message=self.DISCONECT_MESSAGE, user="Server")
                    clientSocket.close()
                    self.oLogger.LogInfo(f"[DISCONNECT]-{clientIP}")
                    break
            except ConnectionResetError:
                clientSocket.close()
                self.connectedClients.remove(clientSocket)
                self.oLogger.LogInfo(f"[ABRUPT DISCONNECT]-{clientIP}")
                break
            except Exception as e:
                clientSocket.close()
                self.connectedClients.remove(clientSocket)
                self.oLogger.LogExceptError(f"[ABRUPT DISCONNECT]-{clientIP}")
                break
        sys.exit()

    def StartSocketServer(self):
        try:
            self.SOCKET_SERVICE = True
            self.serverSocket.bind(self.SERVER_ADDR)
            self.serverSocket.listen()
            self.oLogger.LogInfo(f"[SERVER STARTED] - Listening on: {self.SERVER_ADDR}")
            while self.SOCKET_SERVICE:
                clientSocket, clientIP = self.serverSocket.accept()
                self.connectedClients.append(clientSocket)
                Thread(target=self.__HandleClientConnection, args=(clientSocket, clientIP), daemon=True).start()
                self.oLogger.LogDebug(f"{clientSocket} : {self.connectedClients}")
            return True
        except Exception as e:
            self.oLogger.LogExceptError(f"[SERVER ERROR]")
            return False

    def StopSocketServer(self):
        self.__SendDataToAllConnectedClients(status=1006, message=self.DISCONECT_MESSAGE, user="Server")
        self.SOCKET_SERVICE = False


if (__name__ == "__main__"):
    server = SocketHandler()
    sys.exit(0 if server.StartSocketServer() else "System closed with Exception")
