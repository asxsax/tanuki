import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve, correlate, fftconvolve
from numpy.fft import fftshift, fft

def cross_ambiguity(receiver_signal, emitter_signal, max_lag, sampling_frequency, wavelength, index, figure_number):
    speed_of_light = 3e8
    signal_duration = len(receiver_signal) / sampling_frequency
    correlation = correlate(emitter_signal, receiver_signal, mode='full', method='auto')
    lags = np.arange(-max_lag, max_lag + 1)
    correlation = np.abs(correlation) / np.max(np.abs(correlation))
    bistatic_range = -speed_of_light * lags / sampling_frequency

    plt.figure(5)
    plt.plot(bistatic_range / 1000, 20 * np.log10(correlation))
    plt.title('Crosscorrelation')
    plt.xlabel('Bistatic Range (KM)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True)
    plt.xlim([-100, 100])
    plt.show()

    decimation_factor = 1000
    frequency_decimated = np.linspace(-sampling_frequency / 2 / decimation_factor, 
                                      (sampling_frequency / 2 - 1 / signal_duration) / decimation_factor,
                                      int(signal_duration * sampling_frequency / decimation_factor))
    bistatic_velocity = -wavelength * frequency_decimated

    ambiguity_function = np.zeros((2 * max_lag + 1, len(frequency_decimated)))
    for lag in range(-max_lag, max_lag + 1):
        m = lag + max_lag
        decimated_correlation = decimate(np.conj(receiver_signal) * np.roll(emitter_signal, lag), 
                                         decimation_factor, sampling_frequency)
        ambiguity_function[m, :] = fftshift(fft(decimated_correlation))

    ambiguity_function = np.abs(ambiguity_function)

    plt.figure(6)
    plt.plot(bistatic_velocity, 20 * np.log10(ambiguity_function[max_lag, :]))
    plt.title('0 Time Delay of Ambiguity Function')
    plt.xlabel('Bistatic Velocity (m/s)')
    plt.ylabel('|χ(0,V)| (dB)')
    plt.show()

    plt.figure(figure_number)
    plt.imshow(20 * np.log10(ambiguity_function), extent=(bistatic_velocity[0], bistatic_velocity[-1], 
                                                         bistatic_range[0] / 1000, bistatic_range[-1] / 1000), 
               aspect='auto')
    plt.xlabel('Bistatic Velocity (m/s)')
    plt.xlim([-450, 450])
    plt.ylabel('Bistatic Range (KM)')
    plt.ylim([10, 100])
    plt.title('Cross-Ambiguity Function')
    plt.colorbar()
    plt.show()

    return ambiguity_function

def low_pass_filter(signal, filter_order, normalized_cutoff_frequency):
    num_taps = filter_order - 1
    n = np.arange(0, num_taps + 1)
    cutoff_frequency = normalized_cutoff_frequency
    sinc_function = np.sinc(2 * cutoff_frequency * (n - num_taps / 2))
    hamming_window = 0.54 - 0.46 * np.cos(2 * np.pi * n / num_taps)

    filter_coefficients = sinc_function * hamming_window
    filter_coefficients /= np.sum(filter_coefficients)
    filtered_signal = convolve(signal, filter_coefficients, mode='same')

    return filtered_signal

def decimate_signal(signal, decimation_factor, sampling_frequency):
    cutoff_frequency_normalized = 0.8 / decimation_factor
    filtered_signal = low_pass_filter(signal, order=501, normalized_cutoff_frequency=cutoff_frequency_normalized)
    decimated_signal = filtered_signal[::decimation_factor]
    return decimated_signal

def plot_fft_station_spectrum(complex_signal, frequency, station_name):
    complex_signal_fft = np.fft.fftshift(np.fft.fft(complex_signal))
    complex_signal_fft_normalized = np.abs(complex_signal_fft) / np.max(np.abs(complex_signal_fft))
    
    plt.figure()
    plt.plot(frequency/1e3, 20*np.log10(complex_signal_fft_normalized))
    plt.xlabel('Frequency (kHz)')
    plt.ylabel('Magnitude (dB)')
    plt.title(f'Raw {station_name}')
    plt.show()

    return complex_signal_fft_normalized

def plot_autocorrelation(complex_signal, sampling_frequency, station_name):
    lags = np.arange(-len(complex_signal) + 1, len(complex_signal))
    autocorrelation = fftconvolve(complex_signal, complex_signal.conj()[::-1], mode='full')
    autocorrelation_normalized = np.abs(autocorrelation) / np.max(np.abs(autocorrelation))
    plt.figure()
    plt.plot(lags / sampling_frequency * 1e6, 20 * np.log10(autocorrelation_normalized))
    plt.xlabel('Lag (μs)')
    plt.ylabel('|R(τ)| (dB)')
    plt.title(f'Autocorrelation {station_name}')
    plt.show()

def calculate_3db_bandwidth(frequency, complex_signal_fft_normalized):
    power_signal_fft = complex_signal_fft_normalized**2
    peak_power = np.max(power_signal_fft)
    peak_power_dB = 20 * np.log10(power_signal_fft)
    lower_frequency = frequency[np.where(peak_power_dB >= -3)[0][0]]
    upper_frequency = frequency[np.where(peak_power_dB >= -3)[0][-1]]
    bandwidth_3db = upper_frequency - lower_frequency
    return bandwidth_3db

def process_passive_radar_data(filename, sampling_frequency, center_frequency):
    data = np.fromfile(filename, dtype=np.uint8)
    speed_of_light = 3e8
    wavelength = speed_of_light / center_frequency
    signal_duration = 1.0
    cpi = int(signal_duration * sampling_frequency * 2)
    num_steps = 30

    bandwidths_list = []

    for inc in range(100):
        data_segment = data[1 + (inc - 1) * cpi : cpi + (inc - 1) * cpi]
        real_data = data_segment[0::2]
        complex_data = data_segment[1::2]
        complex_signal = real_data + 1j * complex_data
        complex_signal -= np.mean(complex_signal)

        complex_signal = low_pass_filter(complex_signal, 50, 0.4)

        N = len(complex_signal)
        frequency = np.linspace(-sampling_frequency / 2, sampling_frequency / 2 - sampling_frequency / N, N)

        complex_signal_fft_normalized = plot_fft_station_spectrum(complex_signal, frequency, "104.3 MHz")
        plot_autocorrelation(complex_signal, sampling_frequency, "104.3 MHz")
        bandwidth_3db = calculate_3db_bandwidth(frequency, complex_signal_fft_normalized)
        bandwidths_list.append(bandwidth_3db)

    plt.figure()
    plt.plot(np.arange(1, num_steps + 1), bandwidths_list)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Bandwidth (kHz)')
    plt.title(f'Bandwidth [] MHz')
    plt.show()

process_passive_radar_data('104_3', 2.4e6, 104.3e6)