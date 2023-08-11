import os
import socket
from board import Board, DisplayCommand, BOARD_WIDTH, BOARD_HEIGHT
from struct import unpack
from board_socket_config import *


def show_exp(exp_str): # 文字列は20x15 = 300文字
    tenji="⠀⠁⠂⠃⠄⠅⠆⠇⡀⡁⡂⡃⡄⡅⡆⡇⠈⠉⠊⠋⠌⠍⠎⠏⡈⡉⡊⡋⡌⡍⡎⡏⠐⠑⠒⠓⠔⠕⠖⠗⡐⡑⡒⡓⡔⡕⡖⡗⠘⠙⠚⠛⠜⠝⠞⠟⡘⡙⡚⡛⡜⡝⡞⡟⠠⠡⠢⠣⠤⠥⠦⠧⡠⡡⡢⡣⡤⡥⡦⡧⠨⠩⠪⠫⠬⠭⠮⠯⡨⡩⡪⡫⡬⡭⡮⡯⠰⠱⠲⠳⠴⠵⠶⠷⡰⡱⡲⡳⡴⡵⡶⡷⠸⠹⠺⠻⠼⠽⠾⠿⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⣀⣁⣂⣃⣄⣅⣆⣇⢈⢉⢊⢋⢌⢍⢎⢏⣈⣉⣊⣋⣌⣍⣎⣏⢐⢑⢒⢓⢔⢕⢖⢗⣐⣑⣒⣓⣔⣕⣖⣗⢘⢙⢚⢛⢜⢝⢞⢟⣘⣙⣚⣛⣜⣝⣞⣟⢠⢡⢢⢣⢤⢥⢦⢧⣠⣡⣢⣣⣤⣥⣦⣧⢨⢩⢪⢫⢬⢭⢮⢯⣨⣩⣪⣫⣬⣭⣮⣯⢰⢱⢲⢳⢴⢵⢶⢷⣰⣱⣲⣳⣴⣵⣶⣷⢸⢹⢺⢻⢼⢽⢾⢿⣸⣹⣺⣻⣼⣽⣾⣿"
    s = []
    for i in range(0, 300, 20):
        s.append(exp_str[i:i+20])
    s.append("0"*20)

    print("------------")
    for j in range(4):
        print('|',end='')
        for i in range(10):
            index  = int(s[j*4  ][i*2]) * 1
            index += int(s[j*4+1][i*2]) * 2
            index += int(s[j*4+2][i*2]) * 4
            index += int(s[j*4+3][i*2]) * 8
            index += int(s[j*4  ][i*2+1]) * 16
            index += int(s[j*4+1][i*2+1]) * 32
            index += int(s[j*4+2][i*2+1]) * 64
            index += int(s[j*4+3][i*2+1]) * 128
            print(tenji[index], end='')
        print('|')
    print("------------")


sock_sv = socket.socket(socket.AF_INET)
sock_sv.bind((IPADDR, PORT))
sock_sv.listen()

b = Board()
exp = DisplayCommand()

while True:
    sock_cl, addr = sock_sv.accept()
    print("Connected")
    while True:
        try:
            data = sock_cl.recv(1024)
            if len(data) == 0:
                break
            if data[0] == 0x10:
                args = unpack('B' + str(BOARD_WIDTH * BOARD_HEIGHT) + 's', data)
                exp_str = args[1].strip(b'\x00').decode()
                n = 20
                show_exp(exp_str)
                exp.set_from_string(exp_str)
                b.set_expression(exp)
        except ConnectionResetError:
            break
        except:
            pass
    print("Disconnected")
    sock_cl.shutdown(socket.SHUT_RDWR)
    sock_cl.close()