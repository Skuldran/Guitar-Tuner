# Pins motordrivare
# 1. +5V
# 2. EnA - active high
# 3. In1 - MT1
# 4. In2 - MT1
# 5. EnB - active high
# 6. In3 - MT2
# 7. In4 - MT2
# 8. GND

from gpiozero import Motor
from time import sleep

motor = Motor(17, 18)

pwr = 0.5 # Motor power -1 to 1
# Elimination of the deadzone
# To evaluate the minimum value, set minVal to 0
minVal = 0.2 # The smallest value that gives non zero rotation velocity
val = minVal + abs(pwr)*(minVal) # Power sent to the motor

if pwr > 0:
    motor.forward(val)
    sleep(2)
elif pwr < 0:
    motor.backward(val)
    sleep(2)
else:
    motor.stop()
