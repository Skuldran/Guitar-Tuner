from gpiozero import Motor

import math
import numpy as np

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
P  = '\033[35m' # purple

class stepMotorReg:
    def __init__(self, pinA = 17, pinB = 27, step = 0.0, \
                 endfrq = 100, zero=0.0):
        # Motor values aka dunder functions
        self.power = 0.0
        self.pinA = pinA
        self.pinB = pinB
        
        self.oldpower = 0.0

        self.endfrq = endfrq
        self.frq = endfrq

        self.motor = Motor(pinA, pinB)
        
        self.vol = 0
        
        self.step = step
        self.zero = 0;
        
        self.freqArray = np.zeros(5)

    def updatePower(self):
        if self.frq <= 0:
                print(P+'Percent error: NaN'+W)
                print(P+'He need some milk!'+W)
                #self.power = 0;
                self.motor.stop()
                return;

        self.freqArray = self.shift(self.freqArray, -1, self.frq)
        
        x = np.array([-2,-1,0,1,2])
        n = 5
  
        x_mean = np.mean(x)
        y_mean = np.mean(self.freqArray)
  
        Sxy = np.sum(x*self.freqArray)-5*x_mean*y_mean
        Sxx = np.sum(x*x)-n*x_mean*x_mean
  
        b1 = Sxy/Sxx
        b0 = y_mean-b1*x_mean
        
        self.frq = self.frq+4*b1;
        if self.frq <= 0:
          self.frq = 1;
        #print(b1)
        
        percentError = 1200*math.log2(self.frq/self.endfrq);
        print('Percent error: ', percentError, W)
        
        if abs(percentError) < 15:
                print(R+'The milk is delivered: ', self.frq, W)
                self.motor.stop();
                self.power = 0;
                return 1;

        if self.endfrq > self.frq:
            self.power = max(self.power/3, min(self.power+self.step, 1))
        else:
            self.power = min(self.power/3, max(self.power-self.step, -1))

        if self.power > 0:
            self.motor.backward(self.power)
            print(R+'Forward: ', self.power, W)
            
        elif self.power < 0:
            self.motor.forward(-self.power)
            print(R+'Backward: ', self.power, W)
            
        else:
            self.motor.stop()

    def stop(self):
        self.motor.stop();
        
    def override(self, power):
        if power > 0:
                self.motor.forward(power)
        else:
                self.motor.backward(power)
                
    def shift(self, arr, num, fill_value=np.nan):
      arr = np.roll(arr,num)
      if num < 0:
        arr[num:] = fill_value
      elif num > 0:
        arr[:num] = fill_value
      return arr
                

                
