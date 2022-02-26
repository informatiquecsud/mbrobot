
from microbit import display
from utime import ticks_ms
from mbrobot_plus import *

try:
    t0 = ticks_ms()
    from program import *
    t1 = ticks_ms()
    
    print("loading time", t1 - t0)
    
    # if program loading time is less than 50ms, nothing has been done in the module
    # try to call init() and forever() like the setup() and loop() functions in Arduino
    if t1 - t0 < 50:
        init()
        while True:        
            forever()
    else:
        stop()
        setPID(0)
        
except Exception as e:
    print("Runetime error happened", str(e))
    display.scroll(str(e))
except:
    print("Interrupted")
finally:
    stop()
    setPID(0)
