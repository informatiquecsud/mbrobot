from microbit import i2c,sleep
i2c_adress=0x10
class ServoPort:
 S1=0x14
 S2=0x15
 S3=0x16
 @staticmethod
 def list():
  return[ServoPort.S1,ServoPort.S2,ServoPort.S3]
class Servo:
 def __init__(self,id):
  if id not in ServoPort.list():
   raise ValueError("Servo connector "+str(id)+"is invalid")
  else:
   self.id=id
 def rotateTo(self,angle:int)->None:
  try:
   buf=bytearray(2)
   buf[0]=self.id
   buf[1]=angle
   i2c.write(i2c_adress,buf)
  except Exception as e:
   print("Error: "+str(e))
servo_1=Servo(ServoPort.S1)
servo_2=Servo(ServoPort.S2) 
servo_3=Servo(ServoPort.S3)
if __name__=='__main__':
 servo_1.rotateTo(90)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
