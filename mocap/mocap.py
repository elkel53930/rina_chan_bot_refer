from re import A
import serial
import time
import struct

class Mocap:
    def __init__(self, port='/dev/ttyACM0'):
        self.ser = serial.Serial(port, 115200, timeout=10)
        time.sleep(2)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        self.offset_x = 0
        self.offset_y = 0
        self.offset_z = 0
        self.x_prev = 0
    
    def __del__(self):
        self.ser.close()

    def get_raw(self):
        prev = [0]
        while True:
            bin = self.ser.read(1)
            if prev[0] == 0xff and bin[0] == 0xff:
                break
            prev = bin

        bin = self.ser.read(8)

        return struct.unpack('Hhhh', bin)

    def get_euler(self):
        LIMIT = 45
        (c, x,y,z) = self.get_raw()

        if abs(x - self.x_prev) > 60:
            self.offset_x += x - self.x_prev
        self.x_prev = x

        x = int(x - self.offset_x)
#        y -= self.offset_y
#        z -= self.offset_z


        while x > 180:
            x -= 360
        while x < -180:
            x += 360

        # Ignore values greater than plus or minus LIMIT (40 for X) degrees
        if z > LIMIT:
            z = LIMIT
        if z < -LIMIT:
            z = -LIMIT
        if y > LIMIT:
            y = LIMIT
        if y < -LIMIT:
            y = -LIMIT
#        if x > 40:
#            x = 40
#        if x < -40:
#            x = -40

        # Go to center slowly
        if x != 0:
            self.offset_x += 0.05 * (abs(x) / x)

        return (c, x, y, z)


class FIR:
    def __init__(self, parameters):
        self.depth = len(parameters)
        self.parameters = parameters
        self.reset()

    def reset(self):
        self.history = [0] * self.depth
        self.index = 0        

    def apply(self, x):
        self.history[self.index] = x

        result = 0
        for i in range(self.depth):
            result += self.history[self.index - self.depth + i] * self.parameters[i]
        
        self.index = (self.index + 1) % self.depth

        return result


class IIRChild:
    K = 0
    B1 = 1
    B2 = 2
    A0 = 3
    A1 = 4
    A2 = 5

    def __init__(self, param):
        self.reset(param)

    def reset(self, param=None):
        if param != None:
            self.param = param
        self.z = 0.0
        self.zz = 0.0

    def apply(self, x):
        temp = x * self.param[IIRChild.K] - (self.param[IIRChild.B1] * self.z + self.param[IIRChild.B2] * self.zz)
        result = self.param[IIRChild.A0] * temp + self.param[IIRChild.A1] * self.z + self.param[IIRChild.A2] * self.zz
        self.zz = self.z
        self.z = temp
        return result


class IIRWrongParameterError(Exception):
    pass


class IIR:
    def __init__(self, param):
        self.reset(param)

    def reset(self, param=None):
        if param != None:
            if not param: # empty list
                raise IIRWrongParameterError('The parameter is empty.')
            if len(param) % 6 != 0:
                raise IIRWrongParameterError('The length of parameter is not multiple of 6.')
            num_of_section = len(param) // 6
            self.childs = []
            for i in range(num_of_section):
                self.childs.append(IIRChild(param[6*i:6*(i+1)]))
        else:
            for child in self.childs:
                child.reset()

    def apply(self, x):
        for child in self.childs:
            x = child.apply(x)
        return x


if __name__ == "__main__":
    m = Mocap()
    print("Start...")
    time.sleep(2)


    while True:
        (c,x,y,z) = m.get_euler()
        print(hex(c),x,y,z)


