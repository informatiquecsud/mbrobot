import gc
gc.collect()
# mbrobotmot.py
# Version 1.2, Aug 9, 2019

import gc
from microbit import *
import machine

class Motor:
    def __init__(self, id):
        self._id = 2 * id

    def rotate(self, s):
        v = abs(s)
        if s > 0:
            self._w(0, v)    
        elif s < 0:
            self._w(1, v) 
        else:   
            self._w(0, 0)    
        

    def _w(self, d, s):
        try:
            i2c.write(0x10, bytearray([self._id, d, s]))
        except:
            print("Please switch on mbRobot!")
            while True:
                pass

delay = sleep

def getDistance():
    return sim.robots[0].getDistance()

def setLED(on):
    pin8.write_digital(on)
    pin12.write_digital(on)

pin2.set_pull(pin2.NO_PULL)
irLeft = pin13
irRight = pin14
ledLeft = pin8
ledRight = pin12
motL = Motor(0)
motR = Motor(1)


