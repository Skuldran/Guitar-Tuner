# Pins motordrivare
# 1. +5V
# 2. EnA - active high
# 3. In1 - MT1
# 4. In2 - MT1
# 5. EnB - active high
# 6. In3 - MT2
# 7. In4 - MT2
# 8. GND

# Kabel med text - + - +12V

from gpiozero import Motor

motor = Motor(17, 27)

pwr = 1 # Motor power -1 to 1
# Elimination of the deadzone
# To evaluate the minimum value, set minVal to 0

minVal = 0.0 # The smallest value that gives non zero rotation velocity
zero = 0.0
val = minVal + abs(pwr)*(1-minVal) # Power sent to the motor

if val > 1:
    val = 1
    
if pwr > zero:
    motor.forward(val)
elif pwr < -1*zero:
    motor.backward(val)
else:
    motor.stop()
