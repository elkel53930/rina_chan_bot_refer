from board import Board, DisplayCommand
from time import sleep
from random import random, randint
from playsound import playsound
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../frame'))
from frame import Joint
 
board = Board('/dev/ttyUSB0')
joint3 = Joint('/dev/ttyACM0')

sleep(3)

joint3.init_actuator()
joint3.set_velocity_limit(5)
joint3.set_position(0.1)

anim = {}
for c in "aiueot":
    anim[c] = DisplayCommand()
    anim[c].load("exp/" + c + ".csv")
anim["/"] = DisplayCommand()
anim["/"].load("anim3.csv")
anim["E"] = DisplayCommand()
anim["E"].load("exp/e2.csv")


board.set_expression(anim["/"].get_graphic())
board.show()

for i in range(10):
    print(10-i)
    sleep(1)

joint3.set_velocity_limit(1)
joint3.set_position(0.3)

playsound("hanaseru.wav", block=False)
sleep(0.5)
for c in "uoiaeaaEuooiatao":
    board.set_expression(anim[c].get_graphic())
    board.show()
    sleep(0.135)
sleep(0.1)
board.set_expression(anim["/"].get_graphic())
board.show()

sleep(1)

joint3.set_velocity_limit(2)
joint3.set_position(-0.25)

playsound("hayaku.wav", block=False)
sleep(0.1)
for c in "aaioaaui/aoaiaai":
    board.set_expression(anim[c].get_graphic())
    board.show()
    sleep(0.141)
sleep(0.1)
board.set_expression(anim["/"].get_graphic())
board.show()
