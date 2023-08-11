#!/usr/bin/env python3

from anata import *
from recog.recog import Recognition
from chat.chat_client import ChatClient

from standby import standby_loop
import pygame.mixer
import time

from time import sleep

bpm = 145
intv = 60 / bpm


chat = ChatClient()
recog = Recognition()

def lip_sync(base_exp, vow, interval):
    prev = ''
    for v in vow:
        if v == prev:
            set_exp(base_exp)
            s(interval / 4)
            set_exp(base_exp + mouth[v])
            s(interval / 4 * 3)
        else:
            set_exp(base_exp + mouth[v])
            s(interval)
        prev = v


set_exp(eyes['non'])
sleep(2)

set_exp(eyes['toji'])

pygame.mixer.init(frequency = 44100)
time.sleep(0.5)
pygame.mixer.music.load("bgm/tele.wav")
time.sleep(0.5)
pygame.mixer.music.play(1)

time.sleep(0.6)
wait_init()

s(0.5)
print("move")
move(intv, [0,0,-0.02])
for _ in range(5):
    move_add(intv/2, [0.02,0,0.02])
    move_add(intv/2, [0.02,0,-0.02])
    move_add(intv/2, [-0.02,0,0.02])
    move_add(intv/2, [-0.02,0,-0.02])

s(2.9)

set_exp(eyes['normal']+mouth['normal'])
sleep(0.5)
set_exp(eyes['non']+mouth['normal'])
sleep(0.1)
set_exp(eyes['normal']+mouth['normal'])
sleep(0.1)
set_exp(eyes['non']+mouth['normal'])
sleep(0.1)
set_exp(eyes['normal']+mouth['normal'])

s(2.2)

set_exp(eyes['kirakira']+mouth['normal'])
move_add(intv/2, [0.02,0,0.02])
move_add(0.2, [0.1,0.2,-0.1]) # 顔を下げて
s(0.4)
set_exp(eyes['batsu']+mouth['a'])
move_add(1, [-0.1,-0.2,0.1]) # 音楽に合わせて上を向く
move_add(2, [0.1,0.2,0.1])
move_add(0.5, [0,0,-0.02])
s(3)
set_exp(eyes['normal']+mouth['normal'])
for i in range(4):
    move_add(intv/2, [0.02,-i*0.04,0.02])
    move_add(intv/2, [0.02,-i*0.04,-0.02])
    move_add(intv/2, [-0.02,-i*0.04,0.02])
    move_add(intv/2, [-0.02,-i*0.04,-0.02])

s(2)
set_exp(eyes['normal']+mouth['normal'])
sleep(0.5)
set_exp(eyes['non']+mouth['normal'])
sleep(0.1)
set_exp(eyes['normal']+mouth['normal'])
sleep(0.1)
set_exp(eyes['non']+mouth['normal'])
sleep(0.1)
set_exp(eyes['normal']+mouth['normal'])
s(1.8)

move(1.6,[0.4,0.2,0])
move_add(2,[-0.4,-0.2,0])
move_add(2,[0.4,0.2,0])
move_add(0.9,[0,0,0])
print("思いよ届け")
lip_sync(eyes['normal'],'ooioooe',intv/2) # 思いよ届け
print("笑顔を繋いで")
lip_sync(eyes['right']+cheek['normal'],'eaoouaiet',intv/2) # 笑顔を繋いで
print("何度も何度も")
lip_sync(eyes['toji'],'atooatoo',intv/2) # 何度も何度も
print("送るよメッセージ")
lip_sync(eyes['normal'],'ouuoeteeit',intv/2) # 送るよメッセージ
move_add(0.4,[0.1,0.1,0.2])
move_add(0.65,[0,0,0])
move_add(0.65,[0,-0.3,0])
move_add(0.65,[0,0,0.1])
print("みんなの")
lip_sync(eyes['batsu'], 'itaot',intv/2*1.25) # みんなの
print("ひかりが")
lip_sync(eyes['toji'], 'iaiat',intv/2*1.25) # ひかりが
print("導いてるんだ")
lip_sync(eyes['kirakira'], 'iiii',intv/2*1.25)
lip_sync(eyes['normal'], 'etat',intv/2*1.25)
set_exp(eyes['toji']+cheek['normal']+mouth['normal'])
move(1.4,[0,0,-0.1])
s(1.25)
set_exp(eyes['normal']+mouth['normal'])
sleep(0.5)
set_exp(eyes['non']+mouth['normal'])
sleep(0.1)
set_exp(eyes['normal']+mouth['normal'])
sleep(0.1)
set_exp(eyes['non']+mouth['normal'])
sleep(0.1)
set_exp(eyes['normal']+mouth['normal'])
s(1.2)
move(1,[0,0,0])
s(1)
print("届けよう")
lip_sync(eyes['kirakira'], 'oo',intv/2*1.45)
move(1.5,[0,0,0.3])
lip_sync(eyes['kirakira'], 'eo',intv/2*1.45)
s(1.35)
move(0.5, [-0.2,0.2,-0.2])
print("Yeah")
lip_sync(eyes['wink'], 'iiit', 0.2)

s(4)

# End of live performance

# Go to original position
set_exp(face['normal'])
move(1, [0,0,0])

s(2)

move(0.5, [0,0,0])
move_add(1, [-0.3,0,0])
move_add(1, [0.3,0,0])
move_add(1, [0,0,0])
talk("みんな、今日は来てくれてありがとう！",  eyes["kirakira"])

s(1)

move(2, [0,0,0])
move_add(0.8, [0,0.2,0])
move_add(0.5, [0,0.2,0])
move_add(0.8, [0,0,0])
talk("私、みんなに会えて、とっても嬉しい",  eyes["batsu"])

s(6)
set_exp(face['normal'])
s(1)


print("Waiting for Enter...")
input()

set_exp(face["normal"])

try:
    while True:
        sleep(0.1)
        set_exp(face["normal"])
        prompt = recog.recognition()
        if prompt == "以上です":
            break
        if prompt == None:
            continue
        response = chat.make_response(prompt)
        talk(response, eyes["normal"])
except:
    pass

print("standby...")

standby_loop()