from frame import Frame, Await
from time import sleep
import math

frame = Frame()

wait = Await()

speed = 0.05
amp = 0.35
theta = 0

sleep(2)

while True:
    wait.wait(0.01)
    frame.set_positions([math.sin(theta)*amp]*3)
    theta = theta + speed
    if theta > 2 * math.pi:
        theta = theta - 2 * math.pi