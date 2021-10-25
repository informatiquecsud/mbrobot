from microbit import pin0, pin1, pin2, pin8, pin12, pin13, pin14, pin15, sleep

try:
    from microbit import i2c
except:
    from i2c_adapter import i2c

import machine
import struct
from urm10 import getDistance


i2c_motors = 0x10
i2c_patrol = 0x10
i2c_leds = 0x10

def cm2deg(cm):
    return cm / 14 * 360

def deg2cm(deg):
    return deg * 14 / 360

def rotateSync(targetL, degR):
    # dirL = 
    [m.resetDeg() for m in motors]
    while (motL.readDeg(), motR.readDeg()) < (degL, degR):
        motL.rotate(dirL * _p)
        motR.rotate(dirR * _p)
        delay(5)

class Motor:
    
    powers = [0, 0]
    directions = [1, 1]
    
    def __init__(self, motor_id):
        self.id = motor_id
    
    def rotate(self, power, cm=None):
        if power < 0:
            Motor.powers[self.id] = -power
            Motor.directions[self.id] = 2
        else:
            Motor.powers[self.id] = power
            Motor.directions[self.id] = 1
            
        left_power, right_power = Motor.powers
        left_dir, right_dir = Motor.directions
        motor(left_dir, left_power, right_dir, right_power)
        
    def resetDeg(self):
        buf = bytearray([0x04 + self.id * 2, 0])
        i2c.write(i2c_motors, buf)
    
    def readDirection(self):
        i2c.write(i2c_motors, bytearray([0]))
        buf = i2c.read(i2c_motors, 4)
        return buf[self.id * 2]
        
    def readDeg(self):
        i2c.write(i2c_motors, bytearray([4]))
        buf = i2c.read(i2c_motors, 4)
        
        value =  (buf[self.id * 2] << 8 | buf[self.id * 2 + 1])
        return value * 360 / 80

       
# Maqueen Plus motor control 
# direction:1 forward  2 back
# speed：0~255

def rotateTo(tL, tR, unit=None, rec_count=0):
    unit = unit or "deg"

    dirL, dirR = [1 if x > 0 else 2 for x in [tL, tR]]
    sgnL, sgnR = [1 if x > 0 else -1 for x in [tL, tR]]
    
    motL.resetDeg()
    motR.resetDeg()
    
    if abs(tL) < abs(tR):
        pL, pR = _p * (1 - abs(tR - tL) / tR), _p
    elif abs(tL) > abs(tR):
        pL, pR = _p, _p * (1 - abs(tR - tL) / tL)
    else:
        pL = pR = _p
    
    while (motL.readDeg(), motR.readDeg()) < (abs(tL), abs(tR)):
        motor(dirL, int(pL), dirR, int(pR))
        print("deg", sgnL * motL.readDeg(), sgnR * motR.readDeg())
        delay(20)
    print("deg", sgnL * motL.readDeg(), sgnR * motR.readDeg())
        
    # correction
    delta_L = tL - sgnL * motL.readDeg()
    delta_R = tR - sgnR * motR.readDeg()
    
    print("delta", delta_L, delta_R)

    if abs(delta_L) + abs(delta_R) > 2 and rec_count < 4:
        stop()
        rotateTo(delta_L, delta_R, unit, rec_count + 1)
    
    stop()
    

def motor(directionL, speedL, directionR, speedR):
    try:
        buf = bytearray(5)
        buf[0] = 0x00
        buf[1] = directionL
        buf[2] = speedL
        buf[3] = directionR
        buf[4] = speedR
        i2c.write(i2c_motors, buf)
    except:
        print("Please switch on mbRobot!")
        
def forward(time=None):
    motor(1, _p, 1, _p)
    
def backward(time=None):
    motor(2, _p, 2, _p)
    
def left(time=None):
    motor(2, _p, 1, _p)
    
def right(time=None):
    motor(1, _p, 2, _p)
    
def stop():
    motor(1, 0, 1, 0)

# PID parameters opeen:0 close:1
def PID(switch):
    buf = bytearray(2)
    buf[0] = 0x0A
    buf[1] = switch
    i2c.write(i2c_motors, buf)
    
def setSpeed(power):
    global _p
    _p = power
    
    
def w(dL, dR, pL, pR):
    motor(dL, pL, dR, pR)
    
def rightArc(r):
    v = abs(_p)
    if r < _axle_track:
        v1 = 0
    else:            
        f = (r - _axle_track) / (r + _axle_track) * (1 - v * v / 200000)             
        v1 = int(f * v)
    if 0 < v1 < 18:
        v1 = int(20 + 18 / 5)
    if _p > 0:
        w(1, 1, v, v1)
    else:
        w(2, 2, v1, v)

def leftArc(r):
    v = abs(_p)
    if r < _axle_track:
        v1 = 0
    else:
        f = (r - _axle_track) / (r + _axle_track) * (1 - v * v / 200000)                
        v1 = int(f * v)
    if 0 < v1 < 18:
        v1 = int(20 + 18 / 5)
    if _p > 0:
        w(1, 1, v1, v)
    else:
        w(2, 2, v, v1)
        
    

    
class IR:

    L3 = 0
    L2 = 1
    L1 = 2
    R1 = 3
    R2 = 4
    R3 = 5
    
    masks = [
        0x01,
        0x02,
        0x04,
        0x08,
        0x10,
        0x20
    ]
    
class IRSensor:
    
    def __init__(self, index):
        self.index = index
        
    def read_digital(self):
        byte = read_ir()
        return 1 - ((byte & IR.masks[self.index]) >> self.index)
    
    def read(self):
        return self.read_digital()
    
    def grayscale(self):
        data = read_ir_all()
        return data[self.index * 2 + 1] << 8 | data[self.index * 2 + 2]

def read_ir():
    i2c.write(i2c_patrol, bytearray([0x1D]))
    buf = i2c.read(i2c_patrol, 1)
    return buf[0]

def read_ir_all():
    # use address 0x1E to ask only for grayscale values
    i2c.write(i2c_patrol, bytearray([0x1D]))
    buf = i2c.read(i2c_patrol, 13)
    return buf

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

    

delay = sleep
    
    
#############################################
## Global variables
#############################################
    
motL = Motor(0)
motR = Motor(1)
# default power
_p = 50
# axle track
_axle_track = 0.095

# ir sensors
irLeft = IRSensor(IR.L1)
irRight = IRSensor(IR.R1)


if __name__ == '__main__':    
    right()
    delay(1000)
    stop()

