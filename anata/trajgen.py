from math import fabs, sin, pi
from random import random

def uniform_motion(start, end, time, dt=0.05):
    if time == 0:
        return [end]
    if start == end:
        return [start] * (int(time / dt) + 1)

    step = int(time/dt)
    delta = (end - start) / step
    return [start + x * delta for x in range(step)] + [end]


def fluctuation(x):
    if x < 0.05 or x > 0.95:
        r = random()
    elif x < 0.5:
        r = x + 2 * x * x
    else:
        r = x - 2 * (1 - x) * (1 - x)
    return r


def t_sin(start, end, time, dt=0.05):
    if time == 0:
        return [end]
    if start == end:
        return [start] * (int(time / dt) + 1)

    result = []
    S = end - start
    step = int(time/dt)
    dt = dt * 2 * pi / time
    S = S / 2 / pi
    for i in range(step):
        t = i * dt
        result.append((t - sin(t)) * S + start)
    result.append(end)
    return result


def t_linear(start, end, time, dt=0.05):
    if time == 0:
        return [end]
    if start == end:
        return [start] * (int(time / dt) + 1)
    t_step = int(time/dt)
    x_step = (end-start)/t_step
    result = [start + x_step * i for i in range(t_step)]
    result.append(end)
    return result
