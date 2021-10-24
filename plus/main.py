
from mbrobot import *
from mbtools import *
from mbservo import *

def go_to_target_to_grab(distance=6):
    while True:
        d = getDistance()
        if d <= distance:
            stop()
            break
        delay(10)

def main():
    forklift.up()
    forward()
    go_to_target_to_grab()
    forklift.down()
    forward()
    delay(1000)
    stop()
    forklift.middle()
    setSpeed(30)
    backward()
    delay(2000)
    stop()
    forklift.down()
    delay(1000)
    backward()
    delay(1000)
    stop()
    
    
main()