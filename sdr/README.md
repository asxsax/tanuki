```
data collection:
> gnu radio wbfm capture; 3 stations or so
> save capture to file

filter:
> low pass, hamming window
> plot frequency response and autocorrelation response

analysis:
> compare autocorrelation and bandwidth
> measure performance via bandwidth calculation every .1~ seconds
> best signal quality is one with highest average bandwidth

target detection:
> cross-ambiguity function calculation, create range-velocity map
> compare time-day of arrival between illuminator and transmitter

echo signal simulation:
> simulated echo signal to calculate doppler-shift
> can do some attenuation
> calculate cross-ambiguity function of the two signals
> clutter removal to get rid of positive-delay reflections in ref. signals

signal capture:
> filter:
  > low pass to remove filter
  > bandpass to center around center_freq [+100KHz each side (200KHz)]
> demodulator: [haha... demod manually in python...]
  > look soapysdr or gr-osmosdr

> machine learning:
  > pytorch/tensorflow. whichever easier.
  > look for something to classify
    > type of signal,
    > type of filter,
    > signal quality,
```
