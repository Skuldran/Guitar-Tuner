from threading import Event
#from colorzero import Color
from gpiozero import RotaryEncoder, Button #,RGBLED

rotor = RotaryEncoder(22, 23, wrap=True, max_steps=180)
rotor.steps = 0
#led = RGBLED(22, 23, 24, active_high=False)
btn = Button(24, pull_up=True)
#led.color = Color('#f00')
done = Event()

def prnt_stp():
    stp = (rotor.steps)
    print('Step = {stp}'.format(stp=stp))
    
#def change_hue():
    # Scale the rotor steps (-180..180) to 0..1
    #hue = (rotor.steps + 180) / 360
    #led.color = Color(h=hue, s=1, v=1)

#def show_color():
    #print('Hue {led.color.hue.deg:.1f}° = {led.color.html}'.format(led=led))

def stop_script():
    print('Exiting')
    done.set()

#print('Select a color by turning the knob')
rotor.when_rotated = prnt_stp
#rotor.when_rotated = change_hue
#print('Push the button to see the HTML code for the color')
#btn.when_released = show_color
print('Hold the button to exit')
btn.when_held = stop_script
done.wait()