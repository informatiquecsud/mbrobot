from mbrobot import *

distances = []

def better_getDistance():
    global distances
    
    def avg(values):
        return sum(values) / len(values)
    
    d = getDistance()
    
    print("distances", distances, d)
    
    if len(distances) < 3:
        distances.append(d)
    else:
        x = avg(distances)
        
        if abs(d - x) > 2 * x:
            print("retake measure")
            d = getDistance()
        d = int(avg(distances + [d]))
        distances = distances[1:] + [d]
    return d
    

def init():
    setSpeed(60)

def forever():
    d = better_getDistance()
    print(d)

    if d < 20:
        backward()
    else:
        forward()
    delay(100)
