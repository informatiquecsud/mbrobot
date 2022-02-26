import gc
gc.collect()
# mbrobot_plus.py
# Version 1.3 (22.2.2022)
 
from microbit import i2c,pin0,pin1,pin2,sleep
import machine
import gc
import music

_v = 50
_axe = 0.082
    
def w(d1, d2, s1, s2):
    try:
        i2c.write(0x10, bytearray([0x00,d1, d2, s1, s2]))
    except:
        print("Please switch on mbRobot!")
        
def setSpeed(speed):
    global _v
    if speed < 30 and speed != 0:
        setPID(1)
        _v = speed + 30      
    elif speed >= 30 and speed < 32:
        setPID(0)
        _v = speed + 2
    else:
        setPID(0)
        _v = speed  
  
def setPID(pd):
    i2c.write(0x10, bytearray([0x0A, pd]))

def stop():
    setPID(0)
    w(0, 0, 0, 0) 
    
def resetSpeed():
    setPID(0)
    _v = 50          

def forward():
    w(1, _v, 1, _v)
    
def backward():
    w(2, _v, 2, _v)          
            
def left():
    m = 1.825 -0.0175 * _v
    w(2, int(_v * m), 1, int(_v * m))
    
def right():
    m = 1.825 -0.0175 * _v
    w(1, int(_v * m), 2, int(_v * m))
    
def rightArc(r):
    v = abs(_v)
    if r < _axe:
        v1 = 0
    else:
        f = (r - _axe) / (r + _axe) * (1 - v * v / 200000)             
        v1 = int(f * v)
    if _v > 0:
        w(1, v, 1, v1)
    else:
        w(2, v1, 2, v)

def leftArc(r):
    v = abs(_v)
    if r < _axe:
        v1 = 0
    else:
        f = (r - _axe) / (r + _axe) * (1 - v * v / 200000)        
        v1 = int(f * v)
    if _v > 0:
        w(1, v1, 1, v)
    else:
        w(2, v, 2, v1)    

def getDistance():
    pin1.write_digital(1)
    pin1.write_digital(0)
    p = machine.time_pulse_us(pin2, 1, 50000)
    cm = int(p / 58.2 - 0.5)
    return cm if cm > 0 else 255 

class Motor:
    def __init__(self, id):
        self._id = 2 * id
        
    def _w(self, d, s):
        try:
            i2c.write(0x10, bytearray([self._id, d, s]))
        except:
            print("Please switch on mbRobot!")
            while True:
                pass               

    def rotate(self, s):
        p = abs(s) 
        if s > 0:
            self._w(1, p)    
        elif s < 0:
            self._w(2, p) 
        else:   
            self._w(0, 0)
       
class LEDState:
    OFF = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    PINK = 5
    CYAN = 6
    WHITE = 7

def setLED(state, stateR=None):
    stateR = stateR or state
    i2c.write(0x10, bytearray([0x0B, state, stateR]))
        
def setLEDLeft(state):
    i2c.write(0x10, bytearray([0x0B, state])) 
    
def setLEDRight(state):
    i2c.write(0x10, bytearray([0x0C, state])) 
    
def setAlarm(on):
    if on:
        music.play(_m, wait = False, loop = True)    
    else:
        music.stop() 
        
def beep():
    music.pitch(2000, 200, wait = False)          

def ir_read_values_as_byte():
    i2c.write(0x10, bytearray([0x1D]))
    buf = i2c.read(0x10, 1)
    return ~buf[0]

class IR:
    L3 = 0
    L2 = 1
    L1 = 2
    R1 = 3
    R2 = 4
    R3 = 5  
    masks = [0x01,0x02,0x04,0x08,0x10,0x20]
   
class IRSensor:
    def __init__(self, index):
        self.index = index
        
    def read_digital(self):
        byte = ir_read_values_as_byte()
        return (byte & IR.masks[self.index]) >> self.index

irLeft = IRSensor(IR.L1)
irRight = IRSensor(IR.R1)
irL1 = IRSensor(IR.L1)
irR1 = IRSensor(IR.R1)
irL2 = IRSensor(IR.L2)
irR2 = IRSensor(IR.R2)
irL3 = IRSensor(IR.L3)
irR3 = IRSensor(IR.R3)
pin2.set_pull(pin2.NO_PULL)
motL = Motor(0)
motR = Motor(1)
delay = sleep
_m = ['c6:1', 'r', 'c6,1', 'r', 'r', 'r']

