# more accurate line following strategy using all 6 IR sensors

from mbrobot import *

while True:
    values = ir_read_values()
    l3, l2, l1, r1, r2, r3 = values
    print(values)
    
    setSpeed(80)
        
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
                
    delay(15)


