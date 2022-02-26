
from microbit import sleep

class AngleUnit:
    
    def __init__(s, out_pin, r_min=0, r_max=1023, V_max=390):
        s.r_min = r_min
        s.r_max = r_max
        s.V_max = V_max
        try:
            out_pin.read_analog()
            s._out_pin = out_pin
        except:
            raise ValueError("Angle Unit: Out pin (yellow) should be connected to an analog pin (Pin 0-4 or 10)")
        
    def calibrate(s, nb_try=5):
        print("Put potentiometer on max ...")
        for _ in range(nb_try):
            s.V_max = int(s._out_pin.read_analog() * 0.98)
            print("reading value...", s.V_max)
            sleep(1000)
        
    def read_value(s):
        value = s._out_pin.read_analog()
        return min(int(s.r_min + value / s.V_max * (s.r_max - s.r_min)), s.r_max)
