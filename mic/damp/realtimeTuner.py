import sys
from math import ceil, log2
import time
from scipy.io import wavfile
import numpy as np
import scipy as sp
import scipy.signal as signal
import matplotlib.pyplot as plt
import pyaudio

import single_pitch

# Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fmin = 10
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
maxNoHarmonics = 8
shitLen = 400

# Record ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
form_1 = pyaudio.paFloat32 # 32-bit resolution
chans = 1 # 1 channel
samplingFreq = 44100 # 44.1kHz sampling rate
chunkLength = 2**ceil(log2(2*samplingFreq/fmin)) # 2^12 samples for buffer 4096
print(chunkLength)
audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format = form_1,rate = samplingFreq,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=(chunkLength+shitLen))

# f0 setup
f0Bounds = np.array([fmin, 2000])/samplingFreq
f0Estimator = single_pitch.single_pitch(chunkLength, maxNoHarmonics, f0Bounds)
vol = 0

tic = time.perf_counter()

# The thing:
#while True:
forMax = 50
for ii in range(0,forMax):
#    print(stream.get_read_available())
    chunk = np.frombuffer(stream.read(chunkLength+shitLen, exception_on_overflow=False),   \
                         dtype=np.dtype('f4'), offset=4*shitLen)
    chunk = chunk - np.mean(chunk)
#    print(stream.get_read_available())
#    vol = 0.7*vol + np.var(chunk)/5
    vol = np.var(chunk)
    f0Estimate = (samplingFreq/(2*np.pi))*f0Estimator.est(np.array(chunk, dtype=np.float64))#chunk
    print(vol)
    print(len(chunk))
    print(f0Estimate)
    plt.plot(chunk)
    plt.title(f'Oppa gangnamstyle{ii}')
    plt.xlabel('sample')
    plt.ylabel('amplitude')
    plt.show()

    #print(f0Estimate)

toc = time.perf_counter()
print(f"{(toc-tic)/forMax:0.4f}")

# Close stream
stream.stop_stream()
stream.close()
audio.terminate()
