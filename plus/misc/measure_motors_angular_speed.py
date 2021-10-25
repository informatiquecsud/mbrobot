from mbrobot import *
from utime import ticks_ms, sleep_ms

def angular_speed(power):
    
    motL.resetDeg()
    delay(50)
    t0 = ticks_ms()
    motor(1, power, 1, power)
    sleep_ms(2000)
    motL.rotate(0)
    t1 = ticks_ms()
    deg = motL.readDeg()
    
    return int(deg / (t1 - t0) * 1000)

for power in range(10, 50, 5):
    print('{};{}'.format(power, angular_speed(power)))