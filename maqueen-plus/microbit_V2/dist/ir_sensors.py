from microbit import i2c
i2c_patrol=0x10
class IR:
 L3=0
 L2=1
 L1=2
 R1=3
 R2=4
 R3=5
 masks=[0x01,0x02,0x04,0x08,0x10,0x20]
class IRSensor:
 def __init__(self,index):
  self.index=index
 def read_digital(self):
  byte=read_ir()
  return 1-((byte&IR.masks[self.index])>>self.index)
 def read(self):
  return self.read_digital()
 def grayscale(self):
  data=read_ir_all()
  return data[self.index*2+1]<<8|data[self.index*2+2]
def read_ir():
 i2c.write(i2c_patrol,bytearray([0x1D]))
 buf=i2c.read(i2c_patrol,1)
 return buf[0]
def read_ir_all():
 i2c.write(i2c_patrol,bytearray([0x1D]))
 buf=i2c.read(i2c_patrol,13)
 return buf
irLeft=IRSensor(IR.L1)
irRight=IRSensor(IR.R1)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
