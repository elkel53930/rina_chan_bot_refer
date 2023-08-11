import socket
import os,sys
from time import sleep
from struct import pack
sys.path.append(os.path.dirname(__file__))
from board_socket_config import *
from board.board import BOARD_WIDTH, BOARD_HEIGHT

class BoardClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET)
        self.sock.connect((IPADDR, PORT))

    def __del__(self):
        print("Close socket")
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def set_expression(self, exp):
        self.sock.send(pack('B' + str(BOARD_WIDTH * BOARD_HEIGHT) + 's', 0x10, exp.get_expression().encode()))
