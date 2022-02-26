import gc
gc.collect()
# mbrobot.py
# Version 2.4, May, 2021

import gc
from microbit import i2c, pin1, pin2, pin8, pin12, pin13, pin14, sleep
import machine

_axe = 0.097
def w(d1, d2, s1, s2):
    try:
        i2c.write(0x10, bytearray([0, d1, s1]))
        i2c.write(0x10, bytearray([2, d2, s2]))
    except:
        print("Please switch on mbRobot!")
        while True:
            pass
    
def setSpeed(speed):
    global _v
    if speed < 20:
        _v = speed + 5
    else:
        _v = speed    

def forward():
    w(0, 0, _v, _v)

def backward():
    w(1, 1, _v, _v)
    
def stop():
    w(0, 0, 0, 0)
        
def right():
    w(0 if _v > 0 else 1, 1 if _v > 0 else 0, int(_v * 0.9), int(_v * 0.9))  

def left():
    w(1 if _v > 0 else 0, 0 if _v > 0 else 1, int(_v * 0.9) , int(_v * 0.9))

def rightArc(r):
    v = abs(_v)
    if r < _axe:
        v1 = 0
    else:            
        f = (r - _axe) / (r + _axe) * (1 - v * v / 200000)             
        v1 = int(f * v)
    if _v > 0:
        w(0, 0, v, v1)
    else:
        w(1, 1, v1, v)

def leftArc(r):
    v = abs(_v)
    if r < _axe:
        v1 = 0
    else:
        f = (r - _axe) / (r + _axe) * (1 - v * v / 200000)                
        v1 = int(f * v)
    if _v > 0:
        w(0, 0, v1, v)
    else:
        w(1, 1, v, v1)

exit = stop
delay = sleep

def getDistance():
    pin1.write_digital(1)
    pin1.write_digital(0)
    p = machine.time_pulse_us(pin2, 1, 50000)
    cm = int(p / 58.2 + 0.5)
    return cm if cm > 0 else 255

def setLED(on):
    pin8.write_digital(on)
    pin12.write_digital(on)

pin2.set_pull(pin2.NO_PULL)
_v = 50 # entspricht default 50
irLeft = pin13
irRight = pin14
ledLeft = pin8
ledRight = pin12


