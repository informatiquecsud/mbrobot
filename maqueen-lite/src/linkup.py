import gc
gc.collect()
# linkup.py
# Version 1.15 - Sep 7, 2019
# I2C buffer layout: 0: nbChars M->S, 1: cmd M->S, 2: nbChars S->M, 3:cmd S->M, 4..255: data 

from microbit import i2c, sleep, display
import sys
import gc

a = 0x77

def read(reg, n):
    i2c.write(a, bytes([reg])) 
    sleep(10)
    return i2c.read(a, n)
    
def send(cmd, data, wait):
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
        print("Connection to LinkUp failed.")
        sys.exit(0)
        return
    while read(0, 1)[0] != 0: # wait ack
        sleep(10)
    if not wait:
        return ""
    s = ""
    z = 0
    while True:
        n = read(2, 1)[0]
        if n > 0:
            buf = read(4, n)
            i2c.write(a, bytearray([2, 0]))
            data = str(buf, 'utf-8')
            if buf[0] == 0: # end of data
                break
            s += data
        else:
            z += 1
            if z == 250:
                print("Connection to LinkUp failed. Reset it!")
                sys.exit(0)
                return
        sleep(100)
    sleep(100)        
    return s

def getLine():
    n = read(2, 1)[0]
    if n > 0:
        buf = read(4, n)
        i2c.write(a, bytearray([2, 0]))
        return str(buf, 'utf-8')
    return ""

# ---------- public functions -----------------    
def connectAP(ssid, password):
    return send(1, ssid + ";" + password, True)

def createAP(ssid, password):
    return send(9, ssid + ";" + password, True)
    
def httpGet(url):
    return send(2, url, True)

def httpPost(url, content):
    return send(3, url + "?" + content, True)

def httpDelete(url):
    return send(4, url, True)

def startHTTPServer(handler):
    global hdl
    print("Starting blocking HTTPServer...")
    hdl = handler
    send(5, "", False)
    while True:
        sleep(100)
        gc.collect()
        r = getLine()
        if r == "":
            continue
        a, f, p = r.split('?')
        resp = hdl(a, f, eval(p))
        send(6, '[]' if resp == None else str(resp), False)  
        
def deepsleep():
    return send(6, "", False)

def saveHTML(text):
    line = ""
    for c in text:
        line += c
        if c == '\n':
            rc = send(8, line, True)
            line = ""
    send(8, "\0", True)
     
def getVersion():
    return send(19, "", True)
    

send(20, "", False)
sleep(10000)
