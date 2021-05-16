from gpiozero import Motor

import math

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
P  = '\033[35m' # purple

class stepMotorReg:
    def __init__(self, pinA = 17, pinB = 27, step = 0.0, \
                 endfrq = 100):
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

    def updatePower(self):
        if self.frq <= 0:
                print(P+'Percent error: NaN'+W)
                print(P+'He need some milk!'+W)
                self.power = 0;
                self.motor.stop()
                return;
        
        #If need more kräm

        
        percentError = 1200*math.log2(self.frq/self.endfrq);
        print('Percent error: ', percentError, W)
        
        if abs(percentError) < 20:
                print(R+'The milk is delivered: ', self.frq, W);
                self.motor.stop();
                self.power = 0;
                return 1;

        if self.endfrq > self.frq:
            self.power = math.min(self.power+self.step, 1)
        else:
            self.power = math.max(self.power-self.step, -1)

        if self.power > 0:
            self.motor.forward(self.power)
            print(R+'Forward: ', self.power, W)
            
        elif self.power < 0:
            self.motor.backward(self.power)
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
                
