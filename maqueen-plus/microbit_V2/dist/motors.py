from microbit import i2c
from delay import delay
i2c_motors=0x10
def cm2deg(cm):
 return cm/13.5*360
def deg2cm(deg):
 return deg*13.5/360
class Motor:
 powers=[0,0]
 dirs=[1,1]
 def __init__(self,motor_id):
  self.id=motor_id
 def rotate(self,p):
  if p<0:
   Motor.powers[self.id]=-p
   Motor.dirs[self.id]=2
  else:
   Motor.powers[self.id]=p
   Motor.dirs[self.id]=1
  pL,pR=Motor.powers
  dL,dR=Motor.dirs
  motor(dL,pL,dR,pR)
 def resetDeg(self):
  buf=bytearray([0x04+self.id*2,0])
  i2c.write(i2c_motors,buf)
 def readDirection(self):
  i2c.write(i2c_motors,bytearray([0]))
  buf=i2c.read(i2c_motors,4)
  return buf[self.id*2]
 def readDeg(self):
  i2c.write(i2c_motors,bytearray([4]))
  buf=i2c.read(i2c_motors,4)
  value=(buf[self.id*2]<<8|buf[self.id*2+1])
  return value*360/79
debug=True
def rotateTo(tL,tR):
 dirL,dirR=[1 if x>0 else 2 for x in[tL,tR]]
 sgnL,sgnR=[1 if x>0 else-1 for x in[tL,tR]]
 stop()
 delay(100)
 motL.resetDeg()
 motR.resetDeg()
 delay(50)
 reduction=(tL-sgnL*int(0.05*_p))/tL
 tL*=reduction
 tR*=reduction
 if abs(tL)<abs(tR):
  pL,pR=_p*(1-abs(tR-tL)/tR),_p
 elif abs(tL)>abs(tR):
  pL,pR=_p,_p*(1-abs(tR-tL)/tL)
 else:
  pL=pR=_p
 while True:
  degL,degR=motL.readDeg(),motR.readDeg()
  if degL>tL and degR>tR:
   break
  if debug:
   print(dirL,int(pL),dirR,int(pR))
  motor(dirL,int(pL),dirR,int(pR))
  delay(10)
 inverse_dirL,inverse_dirR=[3-d for d in[dirL,dirR]]
 motor(inverse_dirL,255,inverse_dirR,255)
 delay(20)
 motor(0,0,0,0)
 degL=sgnL*motL.readDeg()
 degR=sgnR*motR.readDeg()
 if debug:print("motor degrees; ",degL,degR)
 return degL,degR
def motor(dirL,pL,dirR,pR):
 try:
  buf=bytearray([0x00,dirL,pL,dirR,pR])
  i2c.write(i2c_motors,buf)
 except:
  print("Please switch on mbRobot!")
def forward(cm=None):
 if cm:
  deg=cm2deg(cm)
  rotateTo(deg,deg)
 else:
  motor(1,_p,1,_p)
def backward(cm=None):
 if cm:
  forward(-cm)
 else:
  motor(2,_p,2,_p)
def left(deg=None):
 if deg:
  rotateTo(-2*deg,2*deg)
 else:
  motor(2,_p,1,_p)
def right(deg=None):
 if deg:
  tL,tR=2*deg,-2*deg
  degL,degR=rotateTo(tL,tR)
 else:
  motor(1,_p,2,_p)
def stop():
 motor(0,0,0,0)
def setPID(switch):
 buf=bytearray(2)
 buf[0]=0x0A
 buf[1]=switch
 i2c.write(i2c_motors,buf)
PID=setPid
def setSpeed(power):
 global _p
 _p=power
def w(dL,dR,pL,pR):
 motor(dL,pL,dR,pR)
def v1_helper(r,v):
 if r<_axle_track:
  v1=0
 else: 
  f=(r-_axle_track)/(r+_axle_track)*(1-v*v/200000) 
  v1=int(f*v)
 return v1
def rightArc(r):
 v=abs(_p)
 v1=v1_helper(r,v)
 if _p>0:
  w(1,1,v,v1)
 else:
  w(2,2,v1,v)
def leftArc(r):
 v=abs(_p)
 v1=v1_helper(r,v)
 if _p>0:
  w(1,1,v1,v)
 else:
  w(2,2,v,v1)
motL=Motor(0)
motR=Motor(1)
_p=50
_axle_track=0.095
# Created by pyminifier (https://github.com/liftoff/pyminifier)
