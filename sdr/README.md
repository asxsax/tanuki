```
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
