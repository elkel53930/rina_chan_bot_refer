vits_path = "~/dev/rc/speech/vits/"

import sys
sys.path.append(vits_path)

import numpy as np
import torch
import commons
import utils
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence

class VitsInf:
    def __init__(self, config, pth):
        self.hps = utils.get_hparams_from_file(config)        

        self.net_g = SynthesizerTrn(
            len(symbols),
            self.hps.data.filter_length // 2 + 1,
            self.hps.train.segment_size // self.hps.data.hop_length,
            n_speakers=self.hps.data.n_speakers,
            **self.hps.model).cuda()
        self.net_g.eval()
        
        utils.load_checkpoint(pth, self.net_g, None)

    def _get_text(self, phoneme_seq):
        text_norm = text_to_sequence(phoneme_seq, self.hps.data.text_cleaners)
        if self.hps.data.add_blank:
            text_norm = commons.intersperse(text_norm, 0)
        text_norm = torch.LongTensor(text_norm)
        return text_norm

    def infer(self, phoneme_seq, speaker_id=0):
        stn_tst = self._get_text(phoneme_seq)
        with torch.no_grad():
            x_tst = stn_tst.cuda().unsqueeze(0)
            x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
            sid = torch.LongTensor([speaker_id]).cuda()
            audio = self.net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0, 0].data.cpu().float().numpy()
        return audio, self.hps.data.sampling_rate
