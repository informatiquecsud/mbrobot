from microbit import pin0, pin1, pin2, sleep

class PIR:
    
    def __init__(s, out):
        if out not in [pin0, pin1, pin2]:
            raise ValueError("PIR Sensor: yellow cable must be connected to pin 0-2")
        s._out = out
        
    def is_motion(s):
        return s._out.read_analog() > 0
    
pir0 = PIR(pin0)
pir1 = PIR(pin1)
pir2 = PIR(pin2)
        
