from mbrobot_plus import *
from m5stack_unit_pir import *

def init():
    pass

def handle_motion_detected():
    right()
    delay(500)
    stop()

def forever():
    if state['pir'] == False and pir0.is_motion():
        state['pir'] = True
        handle_motion_detected()
    elif state['pir'] == True and not pir0.is_motion():
        state['pir'] = False
    
state = {'pir': False}

while True:
    forever()
