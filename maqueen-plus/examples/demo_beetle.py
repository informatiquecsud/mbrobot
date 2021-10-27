from mbrobot import *
from mbtools import *

stop()

def demo_beetle():
    '''

    The closing angle is not the same on all robots. It is around 90°.
    To further close the beetle, increase the closing_angle.
    Open angle is fixed at 30°.
    
    '''
    closing_angle = 100
    beetle.set_close_angle(closing_angle)
    beetle.open()
    delay(2000)
    beetle.close()
    delay(1000)
    beetle.set_angle(50)
    delay(1000)
    beetle.close()
    
demo_beetle()