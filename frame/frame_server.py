import os
import socket
from frame import Frame
from struct import unpack
from frame_socket_config import *
import time

sock_sv = socket.socket(socket.AF_INET)
sock_sv.bind((IPADDR, PORT))
sock_sv.listen()

f = Frame()

while True:
    sock_cl, addr = sock_sv.accept()
    print("Connected")
    prev = None
    while True:
        try:
            data = sock_cl.recv(1024)
            if len(data) == 0:
                break
            if data[0] == 0x10:
                args = unpack('Bddd', data)
                if prev != args:
                    print(time.time(),args[1],args[2],args[3],sep=',')
                f.set_positions(args[1:])
                prev = args
        except ConnectionResetError:
            break
        except:
            pass
    print("Disconnected")
    sock_cl.shutdown(socket.SHUT_RDWR)
    sock_cl.close()