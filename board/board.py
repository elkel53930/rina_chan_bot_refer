import serial
import csv
from time import sleep
import os, sys
sys.path.append(os.path.dirname(__file__))
from exp import _face, _eyes, _cheek, _mouth

BOARD_WIDTH = 20
BOARD_HEIGHT = 15

class DisplayCommand:
    def __init__(self, exp=None):
        self.clear()
        if exp is not None:
            self.set_from_string(exp)

    def clear(self):
        self.graphic = [[False] * BOARD_WIDTH for i in range(BOARD_HEIGHT)]

    def load(self, filename):
        self.clear()
        with open(filename, 'r') as f:
            r = csv.reader(f)
            l = [row for row in r]

        for x in range(BOARD_HEIGHT):
            for y in range(BOARD_WIDTH):
                if l[x][y] is '1':
                    self.graphic[x][y] = True

    def set_from_string(self, str):
        self.clear()
        i = 0
        exp_data = list(str.replace('\n', '').replace(',', ''))
        for x in range(BOARD_HEIGHT):
            for y in range(BOARD_WIDTH):
                if exp_data[i] is '1':
                    self.graphic[x][y] = True
                i += 1

    def get_graphic(self):
        return self.graphic
    
    def __add__(self, other):
        e = DisplayCommand()
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                e.graphic[i][j] = self.graphic[i][j] or other.graphic[i][j]
        return e

    def get_expression(self):
        flatten = [item for sublist in self.graphic for item in sublist]
        result = ''.join(['1' if b else '0' for b in flatten])
        return result

class Board:
    NUM_OF_LED = 200

    WIDTH = BOARD_WIDTH
    HEIGHT = BOARD_HEIGHT

    _LED_ALLOCATION = [
         [  0,  1,  2,  3,  4,  5,  0,  0,  0,  0,  0,  0,  0,  0,200,199,198,197,196,  0],
         [  0,  6,  7,  8,  9, 10,  0,  0,  0,  0,  0,  0,  0,  0,195,194,193,192,191,  0],
         [  0, 11, 12, 13, 14, 15,  0,  0,  0,  0,  0,  0,  0,  0,190,189,188,187,186,  0],
         [  0, 16, 17, 18, 19, 20,  0,  0,  0,  0,  0,  0,  0,  0,185,184,183,182,181,  0],
         [  0, 21, 22, 23, 24, 25,  0,  0,  0,  0,  0,  0,  0,  0,180,179,178,177,176,  0],
         [ 26, 27, 28, 29, 30, 71, 66, 61, 56, 51,146,141,136,131,126,175,174,173,172,171],
         [ 31, 32, 33, 34, 35, 72, 67, 62, 57, 52,147,142,137,132,127,170,169,168,167,166],
         [ 36, 37, 38, 39, 40, 73, 68, 63, 58, 53,148,143,138,133,128,165,164,163,162,161],
         [ 41, 42, 43, 44, 45, 74, 69, 64, 59, 54,149,144,139,134,129,160,159,158,157,156],
         [ 46, 47, 48, 49, 50, 75, 70, 65, 60, 55,150,145,140,135,130,155,154,153,152,151],
         [  0,  0,  0,  0,  0, 76, 77, 78, 79, 80,125,124,123,122,121,  0,  0,  0,  0,  0],
         [  0,  0,  0,  0,  0, 81, 82, 83, 84, 85,120,119,118,117,116,  0,  0,  0,  0,  0],
         [  0,  0,  0,  0,  0, 86, 87, 88, 89, 90,115,114,113,112,111,  0,  0,  0,  0,  0],
         [  0,  0,  0,  0,  0, 91, 92, 93, 94, 95,110,109,108,107,106,  0,  0,  0,  0,  0],
         [  0,  0,  0,  0,  0, 96, 97, 98, 99,100,105,104,103,102,101,  0,  0,  0,  0,  0]]


    def __init__(self, port='/dev/ttyUSB0'):
        self.ser = serial.Serial(port, 38400, timeout=None)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.graphic = None
        sleep(2)

    def __del__(self):
        self.ser.close()

    def set_test_pattern(self, step):
        cycle = self.NUM_OF_LED + 30
        step = step % cycle
        test_code = [0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        
        if step <= self.NUM_OF_LED:
            test_code[step // 7 + 1] = 1 << (step % 7)
        else:
            for i in range(29):
                test_code[i+1] = 0x7F
        self.graphic = bytes(test_code)


    def set_expression(self, expression):
        code = [0x80, 
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        e = expression.get_graphic()
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                if e[y][x]:
                    led_index = self._LED_ALLOCATION[y][x]
                    if led_index == 0:
                        print("LEDs are not located at [%d, %d]" % (x, y))
                    else:
                        led_index -= 1
                        code[led_index // 7 + 1] |= 1 << (led_index % 7)
        self.graphic = bytes(code)
        self.ser.write(self.graphic)
    


eyes = {}
for key in _eyes:
    e = DisplayCommand()
    e.set_from_string(_eyes[key])
    eyes[key] = e

mouth = {}
for key in _mouth:
    e = DisplayCommand()
    e.set_from_string(_mouth[key])
    mouth[key] = e

cheek = {}
for key in _cheek:
    e = DisplayCommand()
    e.set_from_string(_cheek[key])
    cheek[key] = e

face = {}
for key in _face:
    e = DisplayCommand()
    e.set_from_string(_face[key])
    face[key] = e


if __name__ == '__main__':
    i = 0
    board = Board('/dev/ttyUSB0')
    sleep(2)

    while True:
        board.set_test_pattern(i)
        i += 1
        sleep(0.02)