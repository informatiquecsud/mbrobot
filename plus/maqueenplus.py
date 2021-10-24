# PID motor control
# @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com) 

from microbit import *
from time import sleep
import struct
I2caddr = 0x10


class Motor:
    
    powers = [0, 0]
    directions = [1, 1]
    
    def __init__(self, motor_id):
        self.id = motor_id
    
    def rotate(self, power):
        if power < 0:
            Motor.powers[self.id] = -power
            Motor.directions[self.id] = 2
        else:
            Motor.powers[self.id] = power
            Motor.directions[self.id] = 1
            
        left_power, right_power = Motor.powers
        left_dir, right_dir = Motor.directions
        motor(left_dir, left_power, right_dir, right_power)
       
# Maqueen Plus motor control 
# direction:1 forward  2 back
# speed：0~255
def motor(directionL, speedL, directionR, speedR):
    buf = bytearray(5)
    buf[0] = 0x00
    buf[1] = directionL
    buf[2] = speedL
    buf[3] = directionR
    buf[4] = speedR
    i2c.write(I2caddr, buf)
    
def forward(time=None):
    motor(1, _v, 1, _v)
    
def backward(time=None):
    motor(2, _v, 2, _v)
    
def stop():
    motor(1, 0, 1, 0)

# PID parameters opeen:0 close:1
def PID(switch):
    buf = bytearray(2)
    buf[0] = 0x0A
    buf[1] = switch
    i2c.write(I2caddr, buf)
    
def delay(ms):
    sleep(ms / 1000)
    
def setSpeed(power):
    global _v
    _v = power
    
#############################################
## Global variables
#############################################
    
motL = Motor(0)
motR = Motor(1)

# default power
_p = 50


if __name__ == '__main__':
    motL.rotate(255)
    motR.rotate(-255)
    delay(1000)
    stop()