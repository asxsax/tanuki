#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr

#%% Capture

# fm radio center_freq found using sdr++
# samp_rate is generally used as 2.4e6~
freq = 95.7e6        # 95.7 MHz
samp_rate = 2.048e6  # 2.048 MSPS

def capture_fm(frequency, sample_rate, gain, duration, output_file):
    sdr = RtlSdr()

    try:
        sdr.sample_rate = sample_rate  # Hz
        sdr.center_freq = frequency    # Hz
        sdr.gain = gain                # dB

        samples = sdr.read_samples(duration * sample_rate)
        np.save(output_file, samples)

    finally:
        sdr.close()

# capture fm
capture_fm(frequency=freq, sample_rate=samp_rate, gain=10,
           duration=2, output_file='fm_radio_samples.npy')

#%% Visualization

samples = np.load('fm_radio_samples.npy')

plt.plot(samples.real, label='Real Part')
plt.plot(samples.imag, label='Imaginary Part')

plt.legend()

plt.title('Captured Signal')
plt.xlabel('Sample Number')
plt.ylabel('Amplitude')

plt.show()

# FFT and freuqency axis set to center_freq
fft_result = np.fft.fftshift(np.fft.fft(samples))
freqs = np.fft.fftshift(np.fft.fftfreq(len(samples), 1/samp_rate)) + freq

plt.figure()
plt.plot(freqs/1e6, 20*np.log10(np.abs(fft_result)))  # Convert frequency to MHz for plotting

plt.title("Frequency Spectrum")
plt.xlabel("Frequency (MHz)")
plt.ylabel("Power (dB)")

fm_bandwidth = 1e6  # Adjust as needed
center_freq = freq  # Tuned frequency
plt.xlim((center_freq - fm_bandwidth)/1e6, (center_freq + fm_bandwidth)/1e6)

plt.show()
