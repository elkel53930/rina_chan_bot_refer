import os
import sys
import subprocess
import mei_speech

# 引数はtranscriptへのパス

transcript = {}


def load_transcript(filename):
    with open(filename) as f:
        l_strip = [s.strip() for s in f.readlines()]
        corpus = []
        for row in l_strip:
            corpus.append(tuple(row.split(',')))
        return corpus


def play(filename):
    aplay = ['aplay', '-q', filename]
    wr = subprocess.Popen(aplay)
    wr.wait()


def main():
    transcript = sys.argv[1]
    base_dir = os.path.dirname(transcript)
    while True:
        corpus = load_transcript(transcript)
        i = 0
        for c in corpus:
            wav, script = c
            print(str(i)+' '*(3-len(str(i)))+wav, script)
            i = i + 1
        n = input()
        if n == "":
            pass
        elif n == "a":
            for c in corpus:
                wav, _ = c
                play(os.path.join(base_dir, wav))
        else:
            try:
                wav, _ = corpus[int(n)]
            except:
                print("input again")
                continue
            play(os.path.join(base_dir, wav))
#          mei_speech.speech(dialogue)


if __name__ == "__main__":
    main()
