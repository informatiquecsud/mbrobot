# basic line following strategy using only the L1 and LR IR sensors

from mbrobot import *

while True:
    vL = irLeft.read_digital()
    vR = irRight.read_digital()
    
    print(vL, vR)
    
    setSpeed(80)
        
    if vL == 1 and vR == 0:
        rightArc(0.2)
    elif vL == 0 and vR == 1:
        leftArc(0.2)
    elif vL == 0 and vR == 0:
        forward()
    elif vL == 1 and vR == 1:
        
        setSpeed(80)
        right()
        
    delay(5)


