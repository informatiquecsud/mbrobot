import gc
gc.collect()

from microbit import pin0, pin1, pin2

from machine import Pin, time_pulse_us

_trig_pin = pin1
_echo_pin = pin2

_trig = Pin(1, Pin.OUT)
_echo = Pin(2, Pin.OUT)

def getDistance(trig=None, echo=None):
    trig = trig or _trig_pin
    echo = echo or _echo_pin
    cm = read_us_value(_trig, _echo)
    return cm
    
def read_us_value(trig, echo):
    # urm10 sensor can detect distances up to 500cm
    max_distance = 500
    
    trig.write_digital(0)
    if echo.read_digital() == 0:
        _trig.off()
        _trig.on()
        p = time_pulse_us(_echo, 1, max_distance * 58)
    else:
        _trig.on()
        _trig.off()
        p = time_pulse_us(_echo, 0, max_distance * 58)
        
    cm = int(p / 58.4 - 2.5)
    return cm
    

if __name__ == '__main__':
    from show_number import show_number
    while True:
        d = getDistance()
        show_number(d)
        delay(100)
        
