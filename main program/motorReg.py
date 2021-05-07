from gpiozero import Motor
from simple_pid import PID

import math

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
P  = '\033[35m' # purple

class motorReg:
    def __init__(self, pinA = 17, pinB = 27, minval = 0.0, zero = 0.2, \
                 kP = 0.1, kI = 0.1, kD = 0.01, endfrq = 100):
        # Motor values aka dunder functions
        self.power = 0.0
        self.minval = minval
        self.zero = zero
        self.pinA = pinA
        self.pinB = pinB

        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.endfrq = endfrq
        self.frq = endfrq

        self.motor = Motor(pinA, pinB)
        self.pid = PID(kP, kI, kD, endfrq)
        
        self.vol = 0

    def updatePower(self):
        if self.frq == -1 or self.frq == 0:
                print(P+'Percent error: NaN'+W)
                print(P+'He need some milk!'+W)
                self.power = 0;
                self.motor.stop()
                return;
        
        self.power = self.pid(self.frq)
        #val = self.minval + abs(self.power)*(1-self.minval)

        #if val > 1:
        #    val = 1
        
        percentError = 1200*math.log2(self.frq/self.endfrq);
        print('Percent error: ', percentError, W)
        
        if abs(percentError) < 20:
                print(R+'The milk is delivered: ', self.frq, W);
                self.motor.stop();
                return;

        if self.power > self.zero:
            forwardMin = forward_min_val(self.frq);
            val = forwardMin + abs(self.power)*(1-forwardMin)
            
            
            if val>1:
                val = 1
            
            self.motor.forward(val)
            print(R+'Forward: ', val, W)
        elif self.power < -1*self.zero:
            val = self.minval + abs(self.power)*(1-self.minval)
            
            if val>1:
                val = 1
            
            self.motor.backward(val)
            print(R+'Backward: ', val, W)
        else:
            self.motor.stop()

    def stop(self):
        self.motor.stop();
        
    def override(self, power):
        if power > 0:
                self.motor.forward(power)
        else:
                self.motor.backward(power)
                

def forward_min_val(frq):
        return 0.0105*frq-0.303333;
                
