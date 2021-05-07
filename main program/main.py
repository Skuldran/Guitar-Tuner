import multiprocessing
import f0estimator
import motorReg
import time
import os
import matplotlib.pyplot as plt
import atexit
import math


def exit_handler():
	regulator.stop()
	
	plt.figure()
	plt.scatter(timeList, pitchList);
	plt.title('Pitch over time');
	#plt.show()
	plt.figure();
	plt.semilogy(timeList, volList);
	plt.title('Volume over time');
	plt.show();

def listen(freq_data, vol_data):
	while True:
		estimator.listenEstimate(freq_data, vol_data)

def regulate(freq_data, vol_data):
	while True:
		frq = freq_data.get()
		vol = vol_data.get()
		regulator.frq = frq
		regulator.vol = vol
		
		
		pitchList.append(frq);
		volList.append(vol);
		timeList.append(time.time());

			
		
		os.system('clear')
		regulator.updatePower()
		print('Target frequency', regulator.endfrq)
		print('Frequency', frq)
		print('Vol', vol)
		print('Motor power', regulator.power)
	#print(freq_data.get())
		ui_input(regulator)
	
def ui_input(regulator):
	#while True:
		#dt = (starttime-time.time());
		regulator.endfrq = 20*math.sin(time.perf_counter())+100;
		
#Data queue containing estimated frequency and volume
freq_data = multiprocessing.Queue(100)
vol_data = multiprocessing.Queue(100)

estimator = f0estimator.f0Estimator() #Skapa estimator

regulator = motorReg.motorReg(minval = 0.0, kP = 0.08, kI = 0.0007, kD = 0.04, endfrq = 120, zero = 0) #Skapa regulator

atexit.register(exit_handler)

# for i in range(50):
	
	# print(i/50)
	# regulator.override(i/50);
	# time.sleep(1)

# quit();



pitchList = [];
volList = [];
timeList = [];

listener = multiprocessing.Process(target = listen, args=(freq_data, vol_data, ))
listener.start()

starttime = time.time()

#oscilator = multiprocessing.Process(target = ui_input, args=(regulator, ))
#oscilator.start()

regulate(freq_data, vol_data)#@^;

#speaker = multiprocessing.Process(target = regulatre, args=(freq_data))
#speaker.start()

