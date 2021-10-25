from mbservo import*
class Forklift:
 def __init__(self,servo=None,up_angle=0,down_angle=110):
  self.servo=servo or servo_1
  self.up_angle=up_angle
  self.down_angle=down_angle
 def up(self):
  print('moving to',self.servo.rotateTo(self.up_angle))
 def down(self):
  self.servo.rotateTo(self.down_angle)
 def middle(self):
  self.servo.rotateTo(abs(self.down_angle+self.up_angle)//2)
class Beetle:
 def __init__(self,servo):
  self.servo=servo
 def open(self):
  self.servo.rotateTo(0)
 def close(self):
  self.servo.rotateTo(96)
forklift=Forklift(servo_1)
beetle=Beetle(servo_1)
if __name__=='__main__':
 f=Forklift(up_angle=0,down_angle=90)
 f.middle()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
