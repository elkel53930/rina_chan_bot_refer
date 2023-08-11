import socket
import os,sys
sys.path.append(os.path.dirname(__file__))
from chat_socket_config import *

class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET)
        self.sock.connect((IPADDR, PORT))

    def __del__(self):
        print("Close socket")
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def make_response(self, prompt):        
        self.sock.send(prompt.encode())
        data = self.sock.recv(1024)
        return data.decode()


def main():
    client = ChatClient()
    while True:
        print("🗣️ : ", end='')
        print("💻 :", client.make_response(input()))

if __name__ == "__main__":
    main()
