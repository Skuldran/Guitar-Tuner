from gpiozero import Motor
from simple_pid import PID

import math

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
        if self.frq == -1:
                print('He need some milk!')
                self.power = 0;
                self.motor.stop()
                return;
        
        self.power = self.pid(self.frq)
        val = self.minval + abs(self.power)*(1-self.minval)

        if val > 1:
            val = 1

        if self.power > self.zero:
            self.motor.forward(val)
            print('Forward: ', val)
        elif self.power < -1*self.zero:
            self.motor.backward(val)
            print('Backward: ', val)
        else:
            self.motor.stop()

    def stop(self):
        self.motor.stop();
                
