import gc
gc.collect()

from microbit import pin0, pin1, pin2, pin8, pin12, pin13, pin14, pin15
from microbit import sleep, button_a, button_b, display
import machine

_trig_pin = pin1
_echo_pin = pin2

def getDistance(trig=None, echo=None):
    trig = trig or _trig_pin
    echo = echo or _echo_pin
    cm = read_us_value(trig, echo)
    return cm
    
def read_us_value(trig, echo):
    # urm10 sensor can detect distances up to 500cm
    max_distance = 500
    
    trig.write_digital(0)
    if echo.read_digital() == 0:
        trig.write_digital(0)
        trig.write_digital(1)
        p = machine.time_pulse_us(echo, 1, max_distance * 58)
    else:
        trig.write_digital(1)
        trig.write_digital(0)
        p = machine.time_pulse_us(echo, 0, max_distance * 58)
        
    cm = int(p / 58.4 - 2.5)
    return cm
    

if __name__ == '__main__':
    from show_number import show_number
    while True:
        d = getDistance()
        show_number(d)
        delay(100)
        
