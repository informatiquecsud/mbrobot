from mbrobot import *
from show_number import *
from microbit import *
from mucsv import *
from time import ticks_ms

class CSVRowError(Exception):
    def __init__(self, m):
        super().__init__(m)
 
    

def calibrate_urm10():
    distances = []
    tmp = 0
    for real_distance in range(5, 200, 5):
        d = 0
        while True:
            tmp = d
            d = getDistance()
            
            print("real distance", real_distance, "distance : ", d)
            sleep(100)
            
            show_number(d)
            
            if button_a.was_pressed():
                distances.append((real_distance, tmp))
                break
            
        if button_b.was_pressed():
            break
            
    with open('measurements.csv', 'w') as outfile:
        outfile.write('\n'.join(['{};{}'.format(r, d) for r, d in distances]))
        
        
def measure_power_to_distance(power, filename='power_to_distance', intervall=None):
    intervall = intervall or 100
    setSpeed(power)
    forward(power)
    t0 = ticks_ms()
    while True:    
        t, d = ticks_ms(), getDistance()
        #print(t - t0, d)
        print(d)
        delay(intervall)
        if 0 < d < 20:
            break
    stop()
    print(t, d)
    # write_data_to_csv(filename, data, headers=None, sep=None):
    
    
        
        
        
if __name__ == '__main__':
    measure_power_to_distance(30)
