import sys, os
import subprocess
from scipy.io.wavfile import write

import vits_inf

log_dir = os.path.join(vits_inf.vits_path, "logs/jsut")
config_file = os.path.join(vits_inf.vits_path, "configs/jsut.json")
tmp_wav = "/var/tmp/ram/vits_inf.wav"

# 引数はtranscriptへのパス
transcript = {}


def load_transcript(filename):
    with open(filename) as f:
        l_strip = [s.strip() for s in f.readlines()]
        corpus = []
        for row in l_strip:
            c = row.split(',')
            if len(c) == 2:
                c.append("")
            corpus.append(c)
        return corpus


def vits_speech(vits, phonome_seq):
    audio, sr = vits.infer(phonome_seq)
    write(tmp_wav, rate=sr, data=audio)
    command_output = ["aplay", tmp_wav]
    subprocess.run(command_output)

def main():
    transcript = sys.argv[1]
    base_dir = os.path.dirname(transcript)
    vits = vits_inf.VitsInf(config_file, "~/dev/rc/speech/vits/logs/jsut/G_380000.pth")
    while True:
        corpus = load_transcript(transcript)
        i = 0
        for c in corpus:
            [wav, script, phonome_seq] = c
            print(str(i)+' '*(3-len(str(i)))+wav, script)
            i = i + 1
        n = input()
        print("detect", n)
        corpus = load_transcript(transcript)

        if n == "":
            pass
        elif n == "a":
            for c in corpus:
                [wav, dialogue, phonome_seq] = c
                vits_speech(vits, phonome_seq)
        elif n == "exit":
            break
        else:
            print("else")
            try:
                [wav, dialogue, phonome_seq] = corpus[int(n)]
                print(wav, dialogue, phonome_seq)
            except:
                print("input again")
                continue
            if len(phonome_seq):
                print('vits_speec')
                vits_speech(vits, phonome_seq)



if __name__ == "__main__":
    main()
