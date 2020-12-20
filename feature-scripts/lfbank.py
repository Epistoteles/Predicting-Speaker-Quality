#!/usr/bin/env python3.7

from python_speech_features import logfbank
import scipy.io.wavfile as wav
import sys

(rate, sig) = wav.read(sys.argv[1])
lfbank_feat = logfbank(sig, rate)

for frame in lfbank_feat:
	print(" ".join(map(str, frame)))
