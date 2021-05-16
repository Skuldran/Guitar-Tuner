import multiprocessing
import f0estimator
import motorReg
import stepMotorReg
import time
import os
import matplotlib.pyplot as plt
import atexit
import math
import numpy as np
import pandas as pd

def shift(arr, num, fill_value=np.nan):
	arr = np.roll(arr,num)
	if num < 0:
		arr[num:] = fill_value
	elif num > 0:
		arr[:num] = fill_value
	return arr

def exit_handler():
	regulator.stop()
	
	
def plot_shit(timeList, pitchList, truePitchList, volList, powerList):
	data =  {'time':timeList, 'pitch':pitchList, 'truePitch':truePitchList, 'volume':volList, 'motorPower':powerList};
	df = pd.DataFrame(data);
	df.to_csv("data.csv", index=False, header=True)
	
	plt.figure()
	plt.scatter(timeList, pitchList);
	plt.scatter(timeList, truePitchList)
	plt.title('Pitch over time');
	#plt.show()
	
	#plt.figure();
	#plt.semilogy(timeList, volList);
	#plt.title('Volume over time');
	#plt.show();
	
	#plt.figure();
	#plt.scatter(timeList, powerList);
	#plt.title('Power over time');
	plt.show();

def listen(freq_data, true_freq_data, vol_data):
	while True:
		estimator.listenEstimate(freq_data, true_freq_data, vol_data)

def regulate(freq_data, true_freq_data, vol_dat):
	greatlistener = 0
	pitchList = [];
	truePitchList =  [];
	volList = [];
	timeList = [];
	powerList = [];
	
	volMem = np.zeros(10)
	while True:
		frq = freq_data.get()
		true_frq = true_freq_data.get()
		vol = vol_data.get()
		regulator.frq = frq
		regulator.vol = vol
		
		volMem = shift(volMem, 1, vol);
		

		
		os.system('clear')
		
		regulatorval = regulator.updatePower()
		
		pitchList.append(frq);
		truePitchList.append(true_frq)
		volList.append(vol);
		timeList.append(time.time());
		powerList.append(regulator.power);
		
		if regulatorval == 1:
			greatlistener += 1
			if greatlistener > 25:
				plot_shit(timeList, pitchList, truePitchList, volList, powerList);
				
				pitchList = [];
				truePitchList = [];
				volList = [];
				timeList = [];
				powerList = [];
				break
		
		print('Target frequency', regulator.endfrq)
		print('Frequency', frq)
		print('True frequency', true_frq)
		print('Vol', vol)
		print('Max vol: ', np.max(volMem))
		print('Motor power', regulator.power)
	#print(freq_data.get())
		#ui_input(regulator)
	
#def ui_input(regulator):
#	while True:
#		dt = (starttime-time.time());
#		regulator.endfrq = 20*math.sin(time.perf_counter())+100;
		
#Data queue containing estimated frequency and volume
freq_data = multiprocessing.Queue(20)
true_freq_data = multiprocessing.Queue(20)
vol_data = multiprocessing.Queue(20)

estimator = f0estimator.f0Estimator() #Skapa estimator

regulator = motorReg.motorReg(minval = 0., kP = 0.3, kI = 0.00, kD = 0.1, endfrq = 120, zero = 0) #Skapa regulator
#regulator = stepMotorReg.stepMotorReg(step=0.1, endfrq = 120) #Skapa regulator

atexit.register(exit_handler)

#for i in range(50):
#	
#	print(-i/50)
#	regulator.override(-i/50)
#	time.sleep(1)



listener = multiprocessing.Process(target = listen, args=(freq_data, true_freq_data, vol_data, ))
listener.start()

starttime = time.time()


#oscilator = multiprocessing.Process(target = ui_input, args=(regulator, ))
#oscilator.start()


while True:
	time.sleep(2)
	os.system('clear')
	while True:
		try:
			regulator.endfrq = float(input('Enter your desired frequency: '))
			regulator.pid.reset();
			regulator.frq = regulator.endfrq;
			break;
		except:
			print("Write a real number");
	regulate(freq_data, true_freq_data, vol_data)#@^;


#speaker = multiprocessing.Process(target = regulatre, args=(freq_data))
#speaker.start()

