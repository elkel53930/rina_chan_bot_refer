import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from frame.frame import Frame, Await
from board.board import Board, DisplayCommand
import board.exp as exp

from time import sleep
import math

board = Board()
wait = Await()

exps = []
for c in "aot":
    e = DisplayCommand()
    e.load(("../board/exp/"+c+".csv"))
    exps.append(e)

speed = 0.05
amp = 0.35
theta = 0

frame = Frame()

sleep(3)

i = 0
while True:
    wait.wait(0.01)
    frame.set_positions([math.sin(theta)*amp]*3)
    theta = theta + speed
    if theta > 2 * math.pi:
        theta = theta - 2 * math.pi
        i += 1
        if i >= len(exps):
            i = 0
        board.set_expression(exps[i])

