from gpiozero import Motor
from simple_pid import PID

class motorReg:
    def __init__(self, pinA = 17, pinB = 27, minval = 0.0, zero = 0.2, /
                 kP = 0.1, kI = 0.1, KD = 0.01, endfrq = 50):
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
        self.pid = PID(P, I, D, setpoint)

    def updatePower(motor, self.power):
        self.power = self.pid(frq)
        val = self.minval + abs(self.power)*(1-self.minval)

        if val > 1:
            val = 1

        if self.power > self.zero:
            self.motor.forward(val)
        elif self.power < -1*self.zero:
            self.motor.backward(val)
        else:
            self.motor.stop()
