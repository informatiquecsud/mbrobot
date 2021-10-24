# PID motor control
# @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com) 

from microbit import *
import struct
I2caddr = 0x10

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

# PID parameters opeen:0 close:1
def PID(switch):
    buf = bytearray(2)
    buf[0] = 0x0A
    buf[1] = switch
    i2c.write(I2caddr, buf)

while True:
   PID