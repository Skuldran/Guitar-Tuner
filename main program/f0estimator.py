import sys
from math import ceil, log2
import time
import numpy as np
import scipy as sp
import scipy.signal as signal
import pyaudio

import single_pitch

def shift(arr, num, fill_value=np.nan):
	arr = np.roll(arr,num)
	if num < 0:
		arr[num:] = fill_value
	elif num > 0:
		arr[:num] = fill_value
	return arr

def moving_average(x, w):
	y = np.convolve(x, np.ones(w)/w, 'valid')
	y = np.append(y, x[-w:-1])
	return y
	
def getmicindex(audio):
	for i in range(audio.get_device_count()):
		if 'i2s' in audio.get_device_info_by_index(i).get('name'):
			return i

class f0Estimator:	
	def __init__(self):
		#stream, chunklength, shitLen, samplingFreq, 

		audio = pyaudio.PyAudio() # create pyaudio instantiation
		
		#print('INIT: Estimator')
			# Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		fmin = 60
		dev_index = getmicindex(audio)
		maxNoHarmonics = 10
		self.shitLen = 100

		smooth = 5
		self.smoothVarArray = np.zeros(smooth)
		self.smoothPitchArray = np.zeros(smooth)

		# Record ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		form_1 = pyaudio.paFloat32 # 32-bit resolution
		chans = 1 # 1 channel
		self.samplingFreq = 44100 # 44.1kHz sampling rate
		self.chunkLength = 2**ceil(log2(4*self.samplingFreq/fmin)) # 2^12 samples for buffer 4096
		
		# create pyaudio stream
		self.stream = audio.open(format = form_1,rate = self.samplingFreq,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=(self.chunkLength+self.shitLen))

		# f0 setup
		f0Bounds = np.array([fmin, 300])/self.samplingFreq
		self.f0EstimatorAlg = single_pitch.single_pitch(self.chunkLength, maxNoHarmonics, f0Bounds)
		vol = 0

		# Smoothing setup

	
	def listenEstimate(self, f0queue, f0TrueQueue, volqueue):
		chunk = np.frombuffer(self.stream.read(self.chunkLength+self.shitLen, exception_on_overflow=False),   \
                         dtype=np.dtype('f4'), offset=4*self.shitLen)
    
		chunk = chunk-moving_average(chunk, 50)
		vol = np.var(chunk)
		
		#Estimate f0
		f0Estimate = (self.samplingFreq/(2*np.pi))*self.f0EstimatorAlg.est(np.array(chunk, dtype=np.float64))
    
		# Adjust smoothing
		self.smoothVarArray = shift(self.smoothVarArray, 1, fill_value=vol)
		vol = np.median(self.smoothVarArray)
		
		f0auld = self.smoothPitchArray[0]
		
		div = f0Estimate/f0auld
		
		#print(f0Estimate)
		#print('div: ', div)
		
		margin = 10
		
		truef0 = f0Estimate
		
		if vol > 7e-6 and ((div > 1/margin and div < margin) or f0auld==0):
			self.smoothPitchArray = shift(self.smoothPitchArray, 1, fill_value=f0Estimate)
			f0Estimate = np.median(self.smoothPitchArray)
			#print(self.smoothPitchArray)
		else:
			f0Estimate = -1
		
		f0queue.put(f0Estimate)
		f0TrueQueue.put(truef0)
		volqueue.put(vol)
