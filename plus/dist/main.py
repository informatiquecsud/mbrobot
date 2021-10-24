from mbrobot import *
from show_number import *

def reverse_dir(d):
    return 3 - d

speed = 50
dirL = 1

try:
    setSpeed(255)
    for _ in range(4):
        forward(5)
        right(180)
    

except Exception as e:
    print(str(e))
    stop()
    

