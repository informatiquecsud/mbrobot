import gc
gc.collect()
# mbglow.py
# V1.5, June 30, 2018
# Module for a crash course in Python
# An implementation of a glowbug, firefly (Leuchtkaefer)

from microbit import *

_x = 0
_y = 0
_dir = 0
_speed = 50
_trace = True
_visible = False

def makeGlow():
   global _visible
   display.set_pixel(2, 2, 9)
   _visible = True

def clear():
    display.clear()
    
def forward():    
    _forward(1)

def back():    
    _forward(-1)
    
def right(angle):
    global _dir
    _dir = (_dir + angle) % 360

def left(angle):
    right(-angle)

def setPos(x, y):
    global _x, _y
    _x = x
    _y = y
    _render()

def getPos():
    return _x, _y

def setSpeed(speed):
    global _speed
    _speed = speed
    
def showTrace(enable):
    global _trace
    _trace = enable    

def isLit():
    return (display.get_pixel(_x + 2, 4 - (_y + 2)) == 9)
   
def _forward(s):
    global _x, _y
    sleep(2000 - _speed * 20)
    d = _dir // 45
    if d in [1, 2, 3]:    
        _x += s
    if d in [5, 6, 7]:    
        _x -= s
    if d in [0, 1, 7]:    
        _y += s
    if d in [3, 4, 5]:    
        _y -= s
    _render()

def _render():
    if not _visible:
       print("Use \"makeGlow()\" to create a Glow.")
       raise Exception("Glow not initialized.")
    if not _trace:
        display.clear()
    if -2 <= _x <= 2 and -2 <= _y <= 2:    
        display.set_pixel(_x + 2, 4 - (_y + 2), 9)

