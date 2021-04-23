from simple_pid import PID
from gpiozero import RotaryEncoder, Button, Motor
from threading import Event
from time import sleep
from math import floor

# Skapa PID reglerare med parametrar (P, I, D, värde att uppnå)
pid = PID(0.1, 0.1, 0.01, setpoint=100)

# Skapa Rotationsenkoder med max_steps antal steg och wrap aktiverat vilket kopplar intervallen
rotor = RotaryEncoder(22, 23, wrap=True, max_steps=1000)
rotor.steps = 0

# Skapa motor
motor = Motor(17, 18)

# Avbrytknapp
btn = Button(24, pull_up=True)
done = Event()

def prnt_stp():
    stp = (rotor.steps)
    print('Step = {stp}'.format(stp=stp))
    
def set_pwr(pwr):
    # Elimination of the deadzone
    # To evaluate the minimum value, set minVal to 0
    minVal = 0.25 # The smallest value that gives non zero rotation velocity
    zero = 0.2
    val = minVal + abs(pwr)*(1-minVal) # Power sent to the motor
    if val > 1:
        val = 1
    if pwr > zero:
        motor.forward(val)
    elif pwr < zero:
        motor.backward(val)
    else:
        motor.stop()
    
def stop_script():
    print('Exiting')
    set_pwr(0)
    done.set()
    
rotor.when_rotated = prnt_stp
print('Setpoint = {pt}\nHold the button to exit'.format(pt=pid.setpoint))
btn.when_held = stop_script
#done.wait()

while True:
    pwr = pid(rotor.steps)
    print(pwr)
    set_pwr(pwr)
    sleep(0.05)