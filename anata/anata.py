import os, sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

# rina lib
from frame.frame_client import FrameClient
from board.board import face, mouth, eyes, cheek
from board.board_client import BoardClient
from speech.scripts.speech import Speech
from active_wait import Await

# multi thread
import threading
import queue
# trajectory
from trajgen import uniform_motion, fluctuation, t_sin, t_linear

from time import sleep
import random


board = BoardClient()
wait = Await()
speech = Speech()


def s(t):
    wait.wait(t)

def wait_init():
    wait.init()


TRAJ_SIN = 0
TRAJ_LINEAR = 1
traj_generator = t_sin

def change_traj_generator(gen_id):
    if gen_id == TRAJ_SIN:
        traj_generator = t_sin
    elif gen_id == TRAJ_LINEAR:
        traj_generator = t_linear
    else:
        traj_generator = t_sin

def countdown():
    board.set_expression(face["3"])
    s(1)
    board.set_expression(face["2"])
    s(1)
    board.set_expression(face["1"])
    s(1)
    board.set_expression(face["non"])
    s(1)


FRESH = 0
ADD = 1


def frame_traj_thread(cmdq):
    DT = 0.02
    print("start frame_traj_thread")
    frame = FrameClient()
    current_j = [0,0,0]
    traj = []
    traj.append([0])
    traj.append([0])
    traj.append([0])
#    flu = [0,0,0]
    index = 0
    w = Await()
    while True:
        if not cmdq.empty():
            cmd = cmdq.get()
            if cmd is None:
                break
            if cmd['type'] is FRESH:
                # generate trajectory
                traj[0] = traj_generator(current_j[0], cmd['target'][0], cmd['time'], DT)
                traj[1] = traj_generator(current_j[1], cmd['target'][1], cmd['time'], DT)
                traj[2] = traj_generator(current_j[2], cmd['target'][2], cmd['time'], DT)
                index = 0
            elif cmd['type'] is ADD:
                traj[0] += traj_generator(traj[0][-1], cmd['target'][0], cmd['time'], DT)
                traj[1] += traj_generator(traj[1][-1], cmd['target'][1], cmd['time'], DT)
                traj[2] += traj_generator(traj[2][-1], cmd['target'][2], cmd['time'], DT)


        if index != len(traj[0])-1:
            index += 1
        current_j = [traj[0][index], traj[1][index], traj[2][index]]

#        flu[0] = fluctuation(flu[0])
#        flu[1] = fluctuation(flu[1])
#        flu[2] = fluctuation(flu[2])

        w.wait(DT)
#        frame.set_positions([current_j[0]+flu[0]/100,
#                             current_j[1]+flu[1]/100,
#                             current_j[2]+flu[2]/100])
        frame.set_positions([current_j[0],
                             current_j[1],
                             current_j[2]])


rc_frame_queue = queue.Queue()
t1 = threading.Thread(target=frame_traj_thread, args=(rc_frame_queue,))
t1.start()


def move(time, target, sp_max=1, acc=1, dec=1):
    cmd = {}
    cmd['type'] = FRESH
    cmd['time'] = time
    cmd['target'] = target
    cmd['sp_max'] = sp_max
    cmd['acc'] = acc
    cmd['dec'] = dec
    rc_frame_queue.put(cmd)


def move_add(time, target, sp_max=1, acc=1, dec=1):
    cmd = {}
    cmd['type'] = ADD
    cmd['time'] = time
    cmd['target'] = target
    cmd['sp_max'] = sp_max
    cmd['acc'] = acc
    cmd['dec'] = dec
    rc_frame_queue.put(cmd)


def end_script():
    set_exp(eyes['non'])
    s(1)
    set_exp(eyes['normal'] + mouth['normal'])
    move(1, [0,0,0])
    s(1.2)
    rc_frame_queue.put(None)


def exp_gen(pp):
    index = 0
    result = ''

    while index != len(pp):
        if pp[index] in 'aiueo':
            result += pp[index]
            index += 1
        elif pp[index] in '_':
            result += 'tt'
            index += 1
        elif pp[index] in 'N':
            result += 't'
            index += 1
        elif pp[index] is 'c':
            if pp[index+1] is 'l':
                result += 't'
                index += 2
            else:
                index += 1
        else:
            index += 1
    return result


def motion_for_talk(duration):
    angle1 = random.uniform(-0.1,0.1)
    angle2 = random.uniform(-0.1,0.1)
    angle3 = random.uniform(0,-0.1)
    move(duration/2, [angle1, angle2, angle3])
    move_add(duration/2, [0, 0, 0])


def talk(text, base_exp):
    file, pseq, duration = speech.get_wav_file(text)
    mouth_anim = exp_gen(pseq)
    print(mouth_anim)
    print(file, pseq, duration)
    speech.play(file)
    interval = (duration) / len(mouth_anim)
    sleep(0.1)
    motion_for_talk(duration)
    prev = ''
    for v in mouth_anim:
        if v == prev:
            board.set_expression(base_exp)
            sleep(interval/2)
            board.set_expression(base_exp + mouth[v])
            sleep(interval/2)
        else:
            board.set_expression(base_exp + mouth[v])
            sleep(interval)
        prev = v
    board.set_expression(base_exp + mouth['t'])
    sleep(interval/2)


def set_exp(exp):
    board.set_expression(exp)
