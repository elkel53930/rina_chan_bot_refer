import serial
from math import pi
from time import sleep

class Joint:
    def __init__(self, port='/dev/ttyACM0'):
        self.ser = serial.Serial(port, 38400, timeout=10)
        
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def __del__(self):
        self.ser.close()

    def _send(self, data):
        self.ser.write(bytes(data))

    def init_actuator(self):
        self._send([0x80])
        self.ser.readline()
    
    def end_actuator(self):
        self._send([0x81])
        self.ser.readline()

    def set_velocity_limit(self, vel):
        self._send([0x90, int(vel)])

    def set_current_limit(self, current):
        self._send([0x92, int(current * 10)])

    def set_position(self, rad):
        angle = int(rad*16384/pi/2+8192)
        upper = angle >> 7
        lower = angle & 0x7F
        self._send([0x91, upper, lower])

    def set_zero(self, rad):
        angle = int(rad*16384/pi/2+8192)
        upper = angle >> 7
        lower = angle & 0x7F
        self._send([0x93, upper, lower])

    def get_position(self):
        self._send([0x94])        
        return str(self.ser.readline())


class Frame:
    def __init__(self, ports=['/dev/ttyACM0','/dev/ttyACM1','/dev/ttyACM2'], zeros=[0.55,0.03,-0.5]):
        self.joints = []
        for i in range(3):
            print("Open", ports[i])
            self.joints.append(Joint(ports[i]))

        sleep(2)

        for i in range(3):
            print("Initialize J"+str(i)+"...")
            self.joints[i].init_actuator()
            self.joints[i].set_velocity_limit(3)
            self.joints[i].set_zero(zeros[i])
            self.joints[i].set_position(0)
        print("done")

        sleep(1)
        self.set_velocity_limits([255,255,255])


    def set_positions(self, positions):
        for i in range(3):
            self.joints[i].set_position(positions[i])

    def set_velocity_limits(self, vels):
        for i in range(3):
            self.joints[i].set_velocity_limit(vels[i])