#!/usr/bin/env python3

vits_path = "/home/k-iida/dev/rc/speech/vits/"

import os
import sys
sys.path.append(vits_path)
import re
import glob
import argparse
import subprocess

import numpy as np
import torch
import commons
import utils
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
from scipy.io.wavfile import write

sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))
import pp

import time
t = time.time()


# log_dir = os.path.join(vits_path, "logs/logs/rina_jsut_mei")
# config_file = os.path.join(vits_path, "configs/rina_jsut_mei.json")
log_dir = os.path.join(vits_path, "logs/rina")
config_file = os.path.join(vits_path, "configs/rina.json")

thres = 0.05 # silence threshold


def get_text(text, hps, is_pp=True):
    if not is_pp:
        _, text = pp.pp(text)
    print("[%2.2fsec]:" % (time.time()-t), text)
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm


parser = argparse.ArgumentParser(description='TTS with vits')
parser.add_argument('text', help='Text to be spoken.')
parser.add_argument('--step', type=int, default=-1)
parser.add_argument('--out', type=str, default="inf.wav")
parser.add_argument('--play', action='store_true', help='Play wave file after infer.')
parser.add_argument('--pp', action='store_true', help='Input text is phoneme sequence.')

args = parser.parse_args()


# find latest pth file
if args.step == -1:
    pths = glob.glob(os.path.join(log_dir, "G*pth"))
    latest_itr = 0
    for pth in pths:
        m = re.match(r'G_([0-9]*)\.pth', os.path.basename(pth))
        latest_itr = max(latest_itr, int(m.group(1)))
    pth_filename = os.path.join(log_dir, "G_%d.pth" % latest_itr)
else:
    pth_filename = os.path.join(log_dir, "G_%d.pth" % args.step)

print("[%2.2fsec]:Infer by" % (time.time()-t), pth_filename)

hps = utils.get_hparams_from_file(config_file)

net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    n_speakers=hps.data.n_speakers,
    **hps.model).cuda()
_ = net_g.eval()

_ = utils.load_checkpoint(pth_filename, net_g, None)

text = args.text
print("[%2.2fsec]:" % (time.time()-t), text)
stn_tst = get_text(text, hps, args.pp)

with torch.no_grad():
    x_tst = stn_tst.cuda().unsqueeze(0)
    x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
    sid = torch.LongTensor([1]).cuda()
    audio = net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0, 0].data.cpu().float().numpy()

wave_max = np.max(audio)
#audio = audio / wave_max * 32000
#audio = audio.astype(np.int16)

# ipd.display(ipd.Audio(audio, rate=hps.data.sampling_rate, normalize=False))
write(args.out, rate=hps.data.sampling_rate, data=audio)

if args.play:
        command_output = ["aplay", args.out]
        print("[%2.2fsec]:" % (time.time()-t), command_output)
        subprocess.run(command_output)
