#!/usr/bin/env python3

import yaml
import subprocess
import sys
import pp

# openjtalk
X_DIC = '/var/lib/mecab/dic/open-jtalk/naist-jdic'
M_VOICE = '/usr/share/hts-voice/mei/mei_normal.htsvoice'
OW_WAVFILE = '/tmp/tmp.wav'

# aplay
CARD_NO = 1
DEVICE_NO = 0

def talk_text(t, speed, play=True, filename=OW_WAVFILE):
    open_jtalk = ['open_jtalk']
    xdic = ['-x', X_DIC]
    mvoice = ['-m', M_VOICE]
    rspeed = ['-r', speed]
    owoutwav = ['-ow',filename]
    cmd = open_jtalk + xdic + mvoice + rspeed + owoutwav
    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    c.stdin.write(t.encode('utf-8'))
    c.stdin.close()
    c.wait()
    if play:
        aplay = ['aplay', '-q', OW_WAVFILE]
        wr = subprocess.Popen(aplay)
        wr.wait()


def main():
    if len(sys.argv) == 3:
        speed = sys.argv[2]
    else:
        speed = "0.9"

    with open('/home/k-iida/dev/rc/speech/train_data/jsut-label/text_kana/basic5000.yaml', 'r') as file:
        yml = yaml.safe_load(file)

    filelist = []
    for k, n in yml.items():
        print(k, n['text_level0'])
        filename = '/home/k-iida/dev/rc/speech/scripts/jsut5000_mei/MEI_'+k+'.wav'
#        talk_text(n['text_level0'], speed, False, filename)
        _, text = pp.pp(n['text_level0'])
        filelist.append(filename+'|2|'+text+'\n')

    with open('mei_jsut5000_filelist.txt', 'w') as f:
        f.writelines(filelist)


if __name__ == '__main__':
    main()
