import gc
gc.collect()
from microbit import i2c
def getValues(a=0x44):
 i2c.write(a,b'\x2c\x06')
 raw=i2c.read(a,6)
 t,h=(raw[0]<<8)+raw[1],(raw[3]<<8)+raw[4]
 return-45+(175*(t/65535)),100*(h/65535)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
