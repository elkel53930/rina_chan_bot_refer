import os, sys
sys.path.append(os.path.dirname(__file__))
from vits_inf import VitsInf
from scipy.io.wavfile import write
import pp
import glob
from binascii import crc32
from playsound import playsound
from pydub import AudioSegment

class Speech:
    audio_dir = '~/dev/rc/speech/wav_files/'
    def __init__(self):
        vits_path = "/home/k-iida/dev/rc/speech/vits/"
        config_file = os.path.join(vits_path, "configs/rina.json")
        log_dir = os.path.join(vits_path, "logs/rina")
        pth_file = os.path.join(log_dir, 'G_95000.pth')
        self.vits = VitsInf(config_file, pth_file)

    def get_wav_file_pp(self, pseq, force_reproduce=False):
        speaker_id = 1
        wav_file_name = hex(crc32(pseq.encode(), 0))+'.wav'
        wav_file_path = os.path.join(self.audio_dir, wav_file_name)
        if not glob.glob(wav_file_path) or force_reproduce:
            # WAVEファイルが存在しない
            audio, sampling_rate = self.vits.infer(pseq, speaker_id)
            write(wav_file_path, rate=sampling_rate, data=audio)
        sound = AudioSegment.from_file(wav_file_path)
        seconds = sound.duration_seconds
        return wav_file_path, pseq, seconds

    def get_wav_file(self, text, force_reproduce=False):
        _, pseq = pp.pp(text)
        return self.get_wav_file_pp('_'+pseq, force_reproduce)

    def play(self, wav_file_path, block=False):
        playsound(wav_file_path, block)

