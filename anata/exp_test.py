import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from time import sleep

from board.board import Board, DisplayCommand
import board.exp as exp

board = Board()
sleep(2)
eyes = DisplayCommand()
mouth = DisplayCommand()
cheek = DisplayCommand()

eyes.set_from_string(exp.eyes['uruuru'])
mouth.set_from_string(exp.mouth['uruuru'])
cheek.set_from_string(exp.cheek['non'])
board.set_expression(eyes + mouth + cheek)
board.show()

sleep(3)

for e in exp.eyes:
    for m in exp.mouth:
        for c in exp.cheek:
            eyes.set_from_string(exp.eyes[e])
            mouth.set_from_string(exp.mouth[m])
            cheek.set_from_string(exp.cheek[c])
            board.set_expression(eyes + mouth + cheek)
            board.show()
            sleep(0.1)

face = DisplayCommand()
face.set_from_string(exp.face['normal'])
board.set_expression(face)
board.show()
