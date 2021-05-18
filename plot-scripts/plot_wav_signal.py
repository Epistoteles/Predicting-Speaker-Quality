import wave
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

signal_wave = wave.open('../wavs/split-10/ulrichbessler/dievorstadtkrokodile/8.wav', 'rb')
sample_rate = signal_wave.getframerate()
sig = np.frombuffer(signal_wave.readframes(signal_wave.getnframes()), dtype=np.int16)

sig = sig[:]

plt.figure(figsize=(12, 7))
sns.set_style('darkgrid')
plt.subplots_adjust(hspace=0.3)
plt.suptitle('Waveform and spectrogram of audio sample', y=0.95)

plot_a = plt.subplot(211)
plot_a.plot(sig)
plot_a.set_xlabel('sample steps')
plot_a.set_ylabel('energy')
plt.xlim(0, 160000)

plot_b = plt.subplot(212)
plot_b.specgram(sig, NFFT=1024, Fs=sample_rate, noverlap=900, cmap='viridis')
plot_b.set_xlabel('seconds')
plot_b.set_ylabel('frequency')
plt.xlim(0, 10)

plt.savefig(f'../plots/waveform-spectrogram.png', dpi=300)
plt.close()
