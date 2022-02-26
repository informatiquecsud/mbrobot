from program import *
from microbit import display
from mbrobot_plus import *

try:
    init()
    while True:        
        forever()
        
except Exception as e:
    print("Runetime error happened", str(e))
    display.scroll(str(e))
except:
    print("Interrupted")
finally:
    stop()
    setPID(0)
