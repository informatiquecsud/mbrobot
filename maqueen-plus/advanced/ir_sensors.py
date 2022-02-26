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
  byte=ir_read_values_as_byte()
  return(byte&IR.masks[self.index])>>self.index
 def read(self):
  return self.read_digital()
 def grayscale(self):
  data=ir_read_all_values_as_bytearray()
  return data[self.index*2+1]<<8|data[self.index*2+2]
def ir_all_dark(values,sensors):
 mask=0
 for s in sensors:
  mask|=s
 return~values&mask
def ir_all_light(values,sensors):
 mask=0
 for s in sensors:
  mask|=s
 return values&mask
def ir_get_values_from(values,sensors):
 result=[]
 for s in sensors:
  result.append((values&IR.masks[s])>>s)
 return result
def bits(values,length):
 result=[0]*length
 for i in range(0,6):
  result[i]=values&1
  values>>=1
 return result
def ir_read_values():
 return bits(ir_read_values_as_byte(),6)
def ir_read_values_as_byte():
 try:
  i2c.write(i2c_patrol,bytearray([0x1D]))
  buf=i2c.read(i2c_patrol,1)
  return~buf[0]
 except:
  return-1
def ir_read_all_values_as_bytearray():
 try:
  i2c.write(i2c_patrol,bytearray([0x1D]))
  buf=i2c.read(i2c_patrol,13)
  return buf
 except:
  buf=bytearray(13)
  for i in enumerate(buf):
   buf[i]=0xFF
irLeft=IRSensor(IR.L1)
irRight=IRSensor(IR.R1)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
