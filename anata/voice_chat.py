#!/usr/bin/env python3

import os, sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from time import sleep
import random
from anata import *

# rina lib
from recog.recog import Recognition
from chat.chat_client import ChatClient


def choice(arr):
    total_prob = sum([tup[0] for tup in arr])
    prob_list = [tup[0] / total_prob for tup in arr]
    r = random.random()
    for i, prob in enumerate(prob_list):
        if r < prob:
            return arr[i][1]
        r -= prob
    return None

chat = ChatClient()
recog = Recognition()

set_exp(face["normal"])

exp_list = [
    (0.5, eyes["normal"]),
    (0.3, eyes["kirakira"]),
    (0.1, eyes["niko"]),
    (0.1, eyes["batsu"]),
]

#try:
continue_flag = True
while continue_flag:
    sleep(0.1)
    set_exp(face["normal"])
    prompt = recog.recognition()
    if prompt == "終了":
        continue_flag = False
    if prompt == None:
        continue
    response = chat.make_response(prompt)
    talk(response, choice(exp_list))
#except:
#    pass
end_script()
