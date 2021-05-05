import sys
from scipy.io import wavfile
import numpy as np
import scipy as sp
import scipy.signal as signal
import matplotlib.pyplot as plt
import pyaudio

import single_pitch

# Record ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
form_1 = pyaudio.paFloat32 # 32-bit resolution
chans = 1 # 1 channel
samplingFreq = 44100 # 44.1kHz sampling rate
segmentLength = 4096 # 2^12 samples for buffer 4096
record_secs = 5 # seconds to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format = form_1,rate = samplingFreq,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=segmentLength)
print("recording")
#frames = np.array([])
frames = []

# loop through stream and append audio chunks to frame array
for ii in range(0,int((samplingFreq/segmentLength)*record_secs)):
    data = stream.read(segmentLength)
    #np.append(frames, data, axis=1)
    frames.append(data)
    

#speechSignal = b''.join(frames)
#speechSignal = int.from_bytes(frames, byteorder='big', signed=True)
speechSignal = np.frombuffer(b''.join(frames), dtype=np.dtype('<f4'))#i4
#print(len(data))
#print(speechSignal)
#print(speechSignal.shape)
# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

# Analyse ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#[samplingFreq, speechSignal] = wavfile.read('roy.wav')
nData = speechSignal.shape[0]

# set up
#segmentTime = 0.025 # seconds
segmentTime = segmentLength/samplingFreq
#segmentLength = round(segmentTime*samplingFreq) # samples
nSegments = int(np.floor(nData/segmentLength))
f0Bounds = np.array([5, 100])/samplingFreq
maxNoHarmonics = 15
f0Estimator = single_pitch.single_pitch(segmentLength, maxNoHarmonics, f0Bounds)

# do the analysis
idx = np.array(range(0, segmentLength))
f0Estimates = np.zeros((nSegments,)) # cycles/sample
for ii in range(nSegments):
    speechSegment = np.array(speechSignal[idx], dtype=np.float32)#64
    f0Estimates[ii] = (samplingFreq/(2*np.pi))*f0Estimator.est(speechSegment)
    idx = idx + segmentLength

timeVector = np.array(range(1, nSegments+1))*segmentTime-segmentTime/2

# compute the spectrogram of the signal
nOverlap = round(3*segmentLength/4)
[stftFreqVector, stftTimeVector, stft] = signal.spectrogram(speechSignal,
                                                            fs=samplingFreq,
                                                            nperseg=segmentLength,
                                                            noverlap=nOverlap, nfft=4096)
powerSpectrum = np.abs(stft)**2;

# plot the results
maxDynamicRange = 60 # dB
#plt.pcolormesh(stftTimeVector, stftFreqVector, 10*np.log10(powerSpectrum),shading='auto')
#plt.scatter(timeVector, f0Estimates, c='b', s=20)
plt.plot( speechSignal)#range(0, len(speechSignal)-1),
plt.title('Oppa gangnamstyle')
plt.xlabel('time [s]')
plt.ylabel('frequency [Hz]')
plt.show()
