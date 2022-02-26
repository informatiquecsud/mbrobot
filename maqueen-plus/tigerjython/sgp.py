import gc
gc.collect()
#sgp.py for SDP30 Air Quality Sensor
#Version 15.9.2021, Author: Patrik Arnold
from microbit import i2c, sleep

raw = [0, 0]
buf = [0,0,0,0,0,0]

# Initialize the IAQ algorithm
i2c.write(0x58, bytearray([0x20,0x03]))
sleep(1500) # wait for initialize

def getValue(a=0x58):
    # IAQ measure, cmmand must be split! (wait for write)
    i2c.write(0x58, bytearray([0x20,0x08]))
    sleep(600)

    # IAQ Read (see NOTE)
    block = i2c.read(0x58, 6)