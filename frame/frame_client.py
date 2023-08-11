import socket
import os,sys
from time import sleep
from struct import pack
sys.path.append(os.path.dirname(__file__))
from frame_socket_config import *

class FrameClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET)
        self.sock.connect((IPADDR, PORT))

    def __del__(self):
        print("Close socket")
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def set_positions(self, positions):        
        self.sock.send(pack('Bddd', 0x10, positions[0], positions[1], positions[2]))
