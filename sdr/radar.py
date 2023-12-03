import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve, correlate
from numpy.fft import fftshift, fft
from scipy.signal import butter, lfilter, fftconvolve, periodogram


def cross_ambiguity(xr, xe, max_lag, Fs, lambda_, idx, caf_figure_no):
    c = 3e8
    T = len(xr) / Fs
    corr = correlate(xe, xr, mode='full', method='auto')
    lags = np.arange(-max_lag, max_lag + 1)
    corr = np.abs(corr) / np.max(np.abs(corr))
    D = -c * lags / Fs

    plt.figure(5)
    plt.plot(D / 1000, 20 * np.log10(corr))
    plt.title('Crosscorrelation Signal')
    plt.xlabel('Bistatic Range (km)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True)
    plt.xlim([-100, 100])
    plt.show()

    decimation = 1000
    f_dec = np.linspace(-Fs / 2 / decimation, (Fs / 2 - 1 / T) / decimation, int(T * Fs / decimation))
    D = c * lags / Fs
    V = -lambda_ * f_dec

    psi = np.zeros((2 * max_lag + 1, len(f_dec)))
    for lag in range(-max_lag, max_lag + 1):
        m = lag + max_lag
        y = decimate(np.conj(xr) * np.roll(xe, lag), decimation, Fs)
        psi[m, :] = fftshift(fft(y))

    psi = np.abs(psi)

    plt.figure(6)
    plt.plot(V, 20 * np.log10(psi[max_lag, :]))
    plt.title('0-Range Cut of Ambiguity Function')
    plt.xlabel('Bistatic Velocity (m/s)')
    plt.ylabel('|χ(0,V)| (dB)')
    plt.show()

    plt.figure(caf_figure_no)
    plt.imshow(20 * np.log10(psi), extent=(V[0], V[-1], D[0] / 1000, D[-1] / 1000), aspect='auto')
    plt.xlabel('Bistatic Velocity (m/s)')
    plt.xlim([-450, 450])
    plt.ylabel('Bistatic Range (km)')
    plt.ylim([10, 100])
    plt.title('Cross-Ambiguity Function')
    plt.colorbar()
    plt.show()

    return psi

def low_pass(signal, order, normalized_cutoff_freq):
    N = order - 1
    n = np.arange(0, N + 1)
    fc = normalized_cutoff_freq
    sinc_func = np.sinc(2 * fc * (n - N / 2))
    hamming_window = 0.54 - 0.46 * np.cos(2 * np.pi * n / N)

    filter_coeffs = sinc_func * hamming_window
    filter_coeffs /= np.sum(filter_coeffs)
    filtered_signal = convolve(signal, filter_coeffs, mode='same')

    return filtered_signal

def decimate(signal, decimation, fs):
    f_cutoff_normalized = 0.8 / decimation
    filtered_signal = low_pass(signal, order=501, normalized_cutoff_freq=f_cutoff_normalized)
    decimated_signal = filtered_signal[::decimation]
    return decimated_signal

def plot_fft_station(complex_signal, f, radio_station):
    complex_signal_fft = np.fft.fftshift(np.fft.fft(complex_signal))
    complex_signal_fft_normalized = np.abs(complex_signal_fft) / np.max(np.abs(complex_signal_fft))
    
    plt.figure()
    plt.plot(f/1e3, 20*np.log10(complex_signal_fft_normalized))
    plt.xlabel('Frequency (kHz)')
    plt.ylabel('Magnitude (dBFS)')
    plt.title(f'Frequency Domain Signal for Station {radio_station}')
    plt.show()

    return complex_signal_fft_normalized

def plot_xcorr(complex_signal, Fs, radio_station):
    lags = np.arange(-len(complex_signal) + 1, len(complex_signal))
    R = fftconvolve(complex_signal, complex_signal.conj()[::-1], mode='full')
    R_normalized = np.abs(R) / np.max(np.abs(R))
    plt.figure()
    plt.plot(lags / Fs * 1e6, 20 * np.log10(R_normalized))
    plt.xlabel('Lag (μs)')
    plt.ylabel('|R(τ)| (dB)')
    plt.title(f'Autocorrelation of the Complex Signal for Station {radio_station}')
    plt.show()

def calc_3db_bw(f, complex_signal_fft_normalized):
    power_signal_fft = complex_signal_fft_normalized**2
    peak_power = np.max(power_signal_fft)
    peak_power_db = 20 * np.log10(power_signal_fft)
    f_lower = f[np.where(peak_power_db >= -3)[0][0]]
    f_upper = f[np.where(peak_power_db >= -3)[0][-1]]
    BW_3db = f_upper - f_lower
    return BW_3db

def process_passive_radar(filename, Fs, fc):
    data = np.fromfile(filename, dtype=np.uint8)
    c = 3e8
    lambda_ = c / fc
    T = 1.0
    cpi = int(T * Fs * 2)
    num_steps = 30

    BWs_list = []

    for inc in range(100):
        data_segment = data[1 + (inc - 1) * cpi : cpi + (inc - 1) * cpi]
        real_data = data_segment[0::2]
        complex_data = data_segment[1::2]
        complex_signal = real_data + 1j * complex_data
        complex_signal -= np.mean(complex_signal)

        complex_signal = low_pass(complex_signal, 50, 0.4)

        N = len(complex_signal)
        f = np.linspace(-Fs / 2, Fs / 2 - Fs / N, N)

        complex_signal_fft_normalized = plot_fft_station(complex_signal, f, "93.3 MHz")
        plot_xcorr(complex_signal, Fs, "93.3 MHz")
        BW_3db = calc_3db_bw(f, complex_signal_fft_normalized)
        BWs_list.append(BW_3db)

    plt.figure()
    plt.plot(np.arange(1, num_steps + 1), BWs_list)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Bandwidth (kHz)')
    plt.title(f'Bandwidth Over Time for Channel 93.3 MHz')
    plt.show()

process_passive_radar('104_3', 2.4e6, 104.3e6)
