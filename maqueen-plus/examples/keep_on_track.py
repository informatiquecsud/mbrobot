# more accurate line following strategy using all 6 IR sensors

from mbrobot import *
from mbtools import *

def keep_on_track(values):
    l3, l2, l1, r1, r2, r3 = values
    if l1 == 1 and r1 == 0:
        rightArc(0.2)
    elif l1 == 0 and r1 == 1:
        leftArc(0.2)
    elif l1 == 0 and r1 == 0:
        # sensors L1 and R1 are dark
        forward()
    elif l1 == 1 and r1 == 1:
        setSpeed(80)
        if l3 == 0 or l2 == 0:
            left()
        elif r3 == 0 or r2 == 0:
            right()
        else:
            backward()
            delay(30)
            rightArc(0.2)
            delay(100)


INIT = 0
GO_GRAB_OBJECT = 1
GO_DEPOSIT_OBJECT = 2
GO_TO_GARAGE = 3
NO_MORE_OBJECTS = 4
FINISHED = 5

state = INIT

while True:
    values = ir_read_values()
    l3, l2, l1, r1, r2, r3 = values
    d = getDistance()
    
    print(values)
    
    setSpeed(80)
    
    keep_on_track(values)
    
    if state == GO_GRAB_OBJECT:
        beetle.open()
        if d < 7:
            beetle.close()
            stop()
            backward(cm=5)
            right(180)
            state = GO_DEPOSIT_OBJECT
            
        if l1 == 1 and l2 == 1 and l3 == 0 and r3 == 0:
            state = FINISHED
    
    elif state == GO_DEPOSIT_OBJECT:
        
        if d < 7:
            beetle.open()
            backward(5)
            right(180)
        elif d < 15:
            setSpeed(45)
            
    elif state == 
        
        
        
    delay(15)



