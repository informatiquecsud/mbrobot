# -*- pyodide:asyncify -*-
# simulated microbit module

from microbit import *
from delay import delay

_speed = 5

def m(dL, sL, dR, sR):
    i2c.write(0x10, [0x00, dL, sL, dR, sR])

def stop():
    m(0, 0, 0, 0)

def forward():
    m(1, _speed, 1, _speed)

def backward():
    i2c.write(0x10, [0x00, 2, _speed, 2, _speed])
    
def left():
    i2c.write(0x10, [0x00, 2, _speed, 1, _speed])
    
def right():
    i2c.write(0x10, [0x00, 1, _speed, 2, _speed])
    
def setSpeed(speed):
    global _speed
    _speed = speed