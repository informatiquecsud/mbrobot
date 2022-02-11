import gc
gc.collect()
# mytt.py
# Version 1.08 - Aug 31, 2019

import sys
import gc
from microbit import *

a = 0x77

def _read(reg, n):
    i2c.write(a, bytes([reg])) 
    sleep(10)
    return i2c.read(a, n)
    
def _send(cmd, data, wait):
    gc.collect()
    ary = bytearray([0, len(data), cmd, 0, 0])
    for c in data:
        ary.append(ord(c))
    for n in range(5):    
        try:    
            i2c.write(a, ary)
            break
        except:
            display.set_pixel(n, 0, 9)
            sleep(2500)
    if n == 4:
        print("Error: Connection to LinkUp failed.")
        sys.exit(0)
        return ""       
    sleep(100)
    if not wait:
        return ""
    s = ""
    z = 0
    while True:
        n = _read(2, 1)[0]
        if n > 0:
            buf = _read(4, n)
            i2c.write(a, bytearray([2, 0]))
            data = str(buf, 'utf-8')
            if buf[0] == 0: # end of data
                break
            s += data
        else:
            z += 1
            if z == 250:
                print("Error: Timeout while waiting for LinkUp to reply")
                return ""
        sleep(100)
    sleep(100)        
    return s

# ---------- public functions -----------------    
def connectAP(ssid, password):
    return _send(1, ssid + ";" + password, True)
 
def broker(host, port = 1883, user = "", password = "", keepalive = 0):
    _send(10, "%s\1%s\1%s\1%s\1%s" %(host, port, user, password, keepalive), True)

def connect(cleanSession = True):
    return eval(_send(17, "True" if cleanSession else "False", True))

def disconnect():
    _send(11, "", False)

def publish(topic, payload, retain = False, qos = 0):
    if _send(12, "%s\1%s\1%s\1%s" %(topic, payload, "True" if retain else "False", qos), True) == "True":
       return True
    return False

def ping():
    if _send(15, "", True) == "True":
        return True
    return False

def subscribe(topic, qos = 0):
    if _send(13, "%s\1%s" %(topic, qos), True) == "True":
        sleep(2000) # until slave ready
        return True
    return False
    
def receive():
    data = _send(14, "", True)
    if data == "":
        return None
    try:
        topic, payload = data.split('\1')
    except:
        return (None, None)
    if topic == "":
        return (None, None)
    return (topic, payload)

    
