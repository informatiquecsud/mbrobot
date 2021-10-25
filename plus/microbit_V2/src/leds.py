# leds.py

from microbit import i2c

i2c_leds = 0x10

class LEDState:
    
    RED = 1
    GREEN = 2
    BLUE = 4
    YELLOW = 3
    PINK = 5
    CYAN = 6
    WHITH = 7
    OFF = 8

class Leds:
    
    def __init__(self):
        self.both(LEDState.OFF)
        
    def both(self, stateL, stateR=None):
        stateR = stateR or stateL
        i2c.write(i2c_leds, bytearray([0x0B, stateL, stateR]))
        
    def left(self, state):
        i2c.write(i2c_leds, bytearray([0x0B, state]))
        
    def right(self, state):
        i2c.write(i2c_leds, bytearray([0x0C, state]))
        
    
        
leds = Leds()

def setLED(state):
    if state == 1:
        leds.both(LEDState.RED)
    else:
        leds.both(LEDState.OFF)

    
