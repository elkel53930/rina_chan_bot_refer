#!/usr/bin/env python3

from anata import *
from active_wait import Await

from time import sleep
import random


set_exp(eyes['normal']+mouth['normal'])
sleep(0.1)

def choice(arr):
    total_prob = sum([tup[0] for tup in arr])
    prob_list = [tup[0] / total_prob for tup in arr]
    r = random.random()
    for i, prob in enumerate(prob_list):
        if r < prob:
            return arr[i][1]
        r -= prob
    return None


def probability(p):
    return random.random() < p

def blink():
    print('blink')
    sleep(0.5)
    set_exp(eyes['non']+mouth['normal'])
    sleep(0.1)
    set_exp(eyes['normal']+mouth['normal'])
    sleep(0.1)
    set_exp(eyes['non']+mouth['normal'])
    sleep(0.1)
    set_exp(eyes['normal']+mouth['normal'])
    sleep(0.1)

def distract():
    angle_pitch = random.uniform(0, 0.15)
    if probability(0.5):
        going_face = 'right'
        returning_face = 'left'
        angle_yaw = -1 * random.uniform(0.1,0.4)
    else:
        returning_face = 'right'
        going_face = 'left'
        angle_yaw = random.uniform(0.1,0.4)
    print('distract', going_face, 'yaw',angle_yaw, 'pitch', angle_pitch)
    set_exp(eyes[going_face]+mouth['normal'])
    move(2, [angle_yaw,0,angle_pitch])
    sleep(random.randint(4,8))
    set_exp(eyes[returning_face]+mouth['normal'])
    move(2, [0,0,0])
    sleep(1.5)
    set_exp(eyes['normal']+mouth['normal'])
    sleep(2.5)

def wink():
    print('wink')
    move(0.4, [0,0.2,-0.1])
    set_exp(eyes['wink']+mouth['normal'])
    sleep(1)
    move(0.7, [0,0,0])
    set_exp(eyes['normal']+mouth['normal'])
    sleep(2)

def glance():
    if probability(0.5):
        dir = 'right'
        angle = -0.02
    else:
        dir = 'left'
        angle = 0.02
    print("glance", dir)
    move(0.5, [angle,0,0])
    set_exp(eyes['non']+mouth['normal'])
    sleep(0.1)
    set_exp(eyes[dir]+mouth['normal'])
    sleep(random.randint(1,6))
    set_exp(eyes['non']+mouth['normal'])
    sleep(0.1)
    move(1, [0,0,0])
    set_exp(eyes['normal']+mouth['normal'])
    sleep(1)


def tilt_head():
    if probability(0.5):
        angle = 0.1
    else:
        angle = -0.1
    print("tilt_head")
    move(2, [0,angle,0])
    sleep(3)
    move(2, [0,0,0])


def mun():
    print('mun')
    move(0.4, [0,0,-0.1])
    sleep(0.4)
    set_exp(eyes['mun']+mouth['normal']+cheek['normal'])
    sleep(random.randint(3,5))
    move(1, [0,0,0])
    set_exp(eyes['normal']+mouth['normal'])
    sleep(2)


def nikkorin():

    if probability(0.5):
        dir = 1
    else:
        dir = -1

    print("nikkorin", dir)

    set_exp(face['nikkori'])
    for i in range(4):
        move_add(0.2, [0.02,dir*i*0.04,0.02])
        move_add(0.2, [0.02,dir*i*0.04,-0.02])
        move_add(0.2, [-0.02,dir*i*0.04,0.02])
        move_add(0.2, [-0.02,dir*i*0.04,-0.02])
    
    move_add(1, [0,0,0])
    sleep(4)
    set_exp(eyes['normal']+mouth['normal'])
    sleep(2)

def sleepy():
    print("sleepy")
    sleep(1)
    move(3, [0,0.15,0])
    move_add(3, [0,0.2,-0.05])
    move_add(5, [0,0.2,-0.3])
    set_exp(eyes['toji'])
    sleep(3)
    set_exp(face['non'])
    sleep(random.randint(0,10))
    set_exp(eyes['bikkuri']+mouth['waan2'])
    move(0.4, [0,0,0])
    sleep(1)
    set_exp(eyes['non']+mouth['waan2'])
    sleep(0.1)
    set_exp(eyes['bikkuri']+mouth['waan2'])
    sleep(0.1)
    set_exp(eyes['non']+mouth['waan2'])
    sleep(0.1)
    set_exp(eyes['bikkuri']+mouth['waan2'])
    sleep(1)
    if probability(0.7):
        set_exp(eyes['right']+mouth['normal']+cheek['normal'])
        sleep(1)
        set_exp(eyes['left']+mouth['normal']+cheek['normal'])
        sleep(1)
    set_exp(eyes['normal']+mouth['normal'])
    sleep(1)


def nop():
    pass


def test(f):
    while True:
        f()
        sleep(1)



def standby_loop():
    sleep(1)
    set_exp(eyes['normal']+mouth['normal'])

    action_list = [
        (0.2, blink),
        (0.15, glance),
        (0.1, distract),
        (0.1, tilt_head),
        (0.03, mun),
        (0.03, nikkorin),
        (0.03, sleepy),
        (0.01, wink),
        (3, nop),
    ]

    try:
        while True:
            sleep(1)
            choice(action_list)()
    except:
        pass

if __name__ == "__main__":
    try:
        standby_loop()
        s(4)
    except:
        pass
    end_script()
