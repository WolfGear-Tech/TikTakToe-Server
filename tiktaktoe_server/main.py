import sys
from handlers.network import SocketHandler

if (__name__ == "__main__"):
    server = SocketHandler()
    sys.exit(0 if server.StartSocketServer() else "System closed with Exception")
