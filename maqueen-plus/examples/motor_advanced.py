from mbrobot import *


def square(size_cm):
    for _ in range(4):
        forward(size_cm)
        right(90)
        
square(20)