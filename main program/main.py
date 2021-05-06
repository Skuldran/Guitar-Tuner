import multiprocessing
import f0estimator
import motorReg
import time
import os

def listen(freq_data, vol_data):
	while True:
		estimator.listenEstimate(freq_data, vol_data)

def regulate(freq_data, vol_data):
	while True:
		frq = freq_data.get()
		vol = vol_data.get()
		regulator.frq = frq
		regulator.vol = vol
		
		os.system('clear')
		regulator.updatePower()
		print('Frequency', frq)
		print('Vol', vol)
		print('Motor power', regulator.power)
	#print(freq_data.get())

#Data queue containing estimated frequency and volume
freq_data = multiprocessing.Queue(100)
vol_data = multiprocessing.Queue(100)

estimator = f0estimator.f0Estimator() #Skapa estimator

regulator = motorReg.motorReg(minval = 0.1, kP = 0.012, kI = 0.005, kD = 0.1, endfrq = 100, zero = 0) #Skapa regulator

#print('Gogo')

#regulator.power = 1;
#regulator.updatePower(1)

#time.sleep(5)

#print('Stopstop')
#quit();

listener = multiprocessing.Process(target = listen, args=(freq_data, vol_data, ))
listener.start()

regulate(freq_data, vol_data)#@^;

#speaker = multiprocessing.Process(target = regulatre, args=(freq_data))
#speaker.start()

