import soundfile as sf
import os
import glob
import shutil
import numpy as np
import sys
import subprocess
from read import Read


OUTPUT_DIR = "output/"
TEMP_DIR = "temp/"


def exec(command):
    return subprocess.run(command.split(" "))


src_file = sys.argv[1]
prefix, _ = os.path.splitext(os.path.basename(src_file))
prefix += "_"
extracted_wav_file = OUTPUT_DIR + prefix + "%04d.wav"
png_file = TEMP_DIR+prefix+"output%04d.png"
audio_file = TEMP_DIR+prefix+"audio.wav"

exec("mkdir -p " + TEMP_DIR)
exec("mkdir -p " + OUTPUT_DIR)

# extract audio track as 16KHz mono
exec("ffmpeg -n -i " + src_file + " -ac 1 -ar 22050 -b:a 128K " + audio_file)

# extract images with 1 fps
command_output = ["ffmpeg", "-n", "-i", src_file, "-r",
                  "1",  png_file]
subprocess.run(command_output)

# Read audio file
data, samplerate = sf.read(audio_file)

min_silence_duration = 1.4
thres = 0.05

# get silence duration
amp = np.abs(data)
b = amp > thres

silence_blocks = []
prev = 0
entered = 0
for i, v in enumerate(b):
    if prev == True and v == False:  # enter silence
        entered = i
    elif prev == False and v == True:  # exit silence
        duration = (i - entered) / samplerate
        if duration > min_silence_duration:
            silence_blocks.append({"from": entered, "to": i, "suffix": "cut"})
            entered = 0
    prev = v
if entered > 0 and entered < len(b):
    silence_blocks.append({"from": entered, "to": len(b), "suffix": "cut"})

keep_blocks = []
for i, block in enumerate(silence_blocks):
    if i == 0 and block["from"] > 0:
        keep_blocks.append({"from": 0, "to": block["from"], "suffix": "keep"})
    if i > 0:
        prev = silence_blocks[i - 1]
        keep_blocks.append(
            {"from": prev["to"], "to": block["from"], "suffix": "keep"})
    if i == len(silence_blocks) - 1 and block["to"] < len(data):
        keep_blocks.append(
            {"from": block["to"], "to": len(data), "suffix": "keep"})

reader = Read()
padding_time = 0.3
i = 1
transcript = ""
for _, block in enumerate(keep_blocks):
    fr = max(block["from"] / samplerate - padding_time, 0)
    to = min(block["to"] / samplerate + padding_time, len(data) / samplerate)
    duration = to - fr

    (dialogue, name, img) = reader.read(png_file % int(to+2))
    if "璃" in name or "奈" in name:
        # it's renaree
        command_output = ["ffmpeg", "-n", "-i", audio_file, "-ss",
                          str(fr), "-t", str(duration), extracted_wav_file % i]
        subprocess.run(command_output)
        transcript = transcript + os.path.basename(extracted_wav_file % i) + "," + dialogue + "\n"
        i = i + 1


with open(OUTPUT_DIR + prefix + "transcript.txt", mode='w') as f:
    f.write(transcript)

print(transcript)
