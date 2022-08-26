import base64
import json
import sys
from socket import AF_INET, SOCK_STREAM, gethostbyname, gethostname, socket
from threading import Thread
import random
from OtoPy import UsefulTools

class SocketHandler:

    def __init__(self, **logSettings):
        self.oLogger = UsefulTools.OLogger(
            streamLogging=logSettings.get("logOnTerminal", False), 
            logStreamLevel=logSettings.get("logLevel", "DEBUG"),
        )
        self.SERIAL = "QLY8LNU7FqR7LhRfEJmR"
        self.__ENCODE_FORMAT = "utf-8"
        self.DISCONECT_RESPONSE = {"STATUS": 1006}
        self.ECHO_REQUEST = {"REQUEST_CODE": 100}
        self.ECHO_RESPONSE = {"STATUS": 100}


        self.SERVER_ADDR = (gethostbyname(gethostname()), 8090)
        self.SOCKET_SERVICE = True
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.connectedClients = []

    def __ReciveData(self, connectionSocket, byteSize):
        recivedDataBytes = connectionSocket.recv(byteSize)
        if not recivedDataBytes == b'':
            decodedResponseDataList = base64.b64decode(recivedDataBytes).decode(self.__ENCODE_FORMAT).replace("'",'"').replace("}{", "}&{").split("&")          
            responseDictList = []
            for response in decodedResponseDataList:
                responseDictList.append(json.loads(response))
            return responseDictList
        return [self.ECHO_RESPONSE]

    def __SendData(self, socket, **data):
        encodedMessage = base64.b64encode(bytes(str(data), "utf-8"))
        socket.send(encodedMessage)

    def __SendDataToAllConnectedClients(self, **data):
        for client in self.connectedClients:
            self.__SendData(client[0], **data)

    def __login(self, connectionSocket, numberOfTries):
        for _ in range(0, numberOfTries):
            recivedDataList = self.__ReciveData(connectionSocket, 2048)
            for recivedData in recivedDataList:
                if recivedData["REQUEST_CODE"] == 101:
                    cred = recivedData.get("CRED", False)
                    if not bool(cred): cred = {"serial": "!NO_SERIAL", "user": "!NO_USER", "password": "!NO_PASSWORD"}
                    serial = cred.get("serial", "!NO_SERIAL")
                    user = cred.get("user", "!NO_USER")
                    password = cred.get("password", "!NO_PASSWORD")
                    cred.update({"serial": serial})
                    cred.update({"user": user})
                    cred.update({"password": password})
                    clientConnectionInfo = (connectionSocket, cred)

                    if serial == self.SERIAL:
                        userNamesInUse = []
                        for client in self.connectedClients:
                            userNamesInUse.append(client[1]["user"])

                        if user != "!NO_USER":
                            if user not in userNamesInUse:
                                self.oLogger.LogWarning(f"[CONNECT CLIENT] - Name: {cred['user']}")
                                self.__SendData(connectionSocket, STATUS = 101, cred = {"user":cred["user"]})
                                self.connectedClients.append(clientConnectionInfo)
                                return True
                            else:
                                self.oLogger.LogWarning(f"[REFUSED CLIENT] - User name already in use")
                                self.__SendData(connectionSocket, STATUS = 401, REASON = "User name already in use")

                        else: 
                            cred["user"] = random.randint(1000, 2000)
                            while cred["user"] in userNamesInUse:
                                cred["user"] = random.randint(1000, 2000)
                            self.oLogger.LogWarning(f"[CONNECT CLIENT] - Random name: {cred['user']}")
                            self.connectedClients.append(clientConnectionInfo)
                            self.__SendData(connectionSocket, STATUS = 101, cred = {"user":cred["user"]})
                            return True
                    else:
                        self.oLogger.LogWarning(f"[REFUSED CLIENT] - Wrong serial number")
                        self.__SendData(connectionSocket, STATUS = 401, REASON = "Wrong serial number")
        return False
    
    def __HandleData(self, connectionSocket, data):
        REQUEST_CODE = data.get("REQUEST_CODE", 404)
        if REQUEST_CODE in range(100, 200):
            #Connection Stablisment
            if REQUEST_CODE == 100: #Echo, no need to handle
                self.__SendData(connectionSocket, STATUS=100)
            elif REQUEST_CODE == 101: pass #Login stuff, already treated in the normal process

        elif REQUEST_CODE in range(200, 300):
            # Success
            if REQUEST_CODE == 202: #Code for sending data to specific user(Requires a valid user name or returns an 414 fo no valid user found)
                self.oLogger.LogInfo(f"[REQUEST_CODE 202] - Recieved from {connectionSocket} - {data}")
                self.__SendData(connectionSocket, STATUS=202, data=data)

            elif REQUEST_CODE == 205: #Code for sending data to all connected clients with same serial repassing the data with User name of the client of origin
                self.oLogger.LogInfo(f"[REQUEST_CODE 205] - Recieved from {connectionSocket} - {data}")
                self.__SendDataToAllConnectedClients(STATUS=205, data=data)

        elif REQUEST_CODE in range(400, 500):
            # Client Error
            if REQUEST_CODE == 404: #Request code not found, function error
                self.oLogger.LogInfo(f"[REQUEST_CODE !NOT_FOUND] - Recieved from {connectionSocket} - {data}")
                self.__SendData(connectionSocket, STATUS=404, WARNING="Please specifi a REQUEST_CODE", data=data)

        elif REQUEST_CODE in range(500, 9999):
            # Server Error
            if REQUEST_CODE == 1006: #Disconnect client request
                connectedSocketsList = []
                for client in self.connectedClients:
                    connectedSocketsList.append(client[0])
                self.connectedClients.pop(connectedSocketsList.index(connectionSocket))
                connectionSocket.close()
                self.oLogger.LogInfo(f"[DISCONNECT] - {connectionSocket}")
                return False
        
        return True

    def __HandleClientConnection_thread(self, clientSocket, clientIP):
        CLIENT_THREAD_PERSIST = self.__login(clientSocket, 5)
        while self.SOCKET_SERVICE and CLIENT_THREAD_PERSIST:
            try:
                recivedDataList = self.__ReciveData(clientSocket, 2048)
                for recivedData in recivedDataList:
                    CLIENT_THREAD_PERSIST = self.__HandleData(clientSocket, recivedData)
                    if CLIENT_THREAD_PERSIST == False: break

            except ConnectionResetError:
                connectedSocketsList = []
                for client in self.connectedClients:
                    connectedSocketsList.append(client[0])
                self.connectedClients.pop(connectedSocketsList.index(clientSocket))

                clientSocket.close()
                self.oLogger.LogInfo(f"[ABRUPT DISCONNECT]-{clientIP}")
                CLIENT_THREAD_PERSIST = False
            except Exception:
                connectedSocketsList = []
                for client in self.connectedClients:
                    connectedSocketsList.append(client[0])
                self.connectedClients.pop(connectedSocketsList.index(clientSocket))

                clientSocket.close()
                self.oLogger.LogExceptError(f"[ABRUPT DISCONNECT]-{clientIP}")
                CLIENT_THREAD_PERSIST = False
        sys.exit()

    def StartSocketServer(self):
        try:
            self.serverSocket.bind(self.SERVER_ADDR)
            self.serverSocket.listen()
            self.SOCKET_SERVICE = True
            self.oLogger.LogInfo(f"[SERVER STARTED] - Listening on: {self.SERVER_ADDR}")
            while self.SOCKET_SERVICE:
                clientSocket, clientIP = self.serverSocket.accept()
                Thread(target=self.__HandleClientConnection_thread, args=(clientSocket, clientIP), daemon=True).start()
                self.oLogger.LogDebug(f"{clientSocket}")

        except Exception as e:
            self.SOCKET_SERVICE = False
            self.oLogger.LogExceptError(f"[SERVER ERROR]")

    def StopSocketServer(self):
        self.__SendDataToAllConnectedClients(self.DISCONECT_RESPONSE)
        self.SOCKET_SERVICE = False


if __name__ == "__main__":
    server = SocketHandler(logOnTerminal=True)
    sys.exit(0 if server.StartSocketServer() else "System closed with Exception")