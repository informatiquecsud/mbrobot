from microbit import i2c
from utime import sleep_ms

class SonicUnit:
    
    def __init__(s, addr):
        s._addr = addr
    
    def read_value(s):
        # reference: https://github.com/m5stack/UNIT_SONIC/blob/master/src/SONIC_I2C.cpp
        i2c.write(s._addr, bytearray([0x01]))
        sleep_ms(10)
        b1, b2, b3 = i2c.read(s._addr, 3)
        d = (b1 << 16 | b2 << 8 | b3) / 1000
        return d if d <= 4500 else 4500
        
    
sonic = SonicUnit(0x57)
getDistance2 = sonic.read_value


