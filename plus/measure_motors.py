from mbrobot import *
from mucsv import *
from microbit import display

from time import ticks_ms


data = []

def get_distances(duration=5000, intervall=100, stop_distance=20):
    data = []
    nb = int(duration // intervall)
    
    t0 = ticks_ms()
    for _ in range(nb):
        while True:
            d = getDistance()
            t = ticks_ms()
            if  0 < d < stop_distance:
                break
            if len(data) == 0 or stop_distance < d <= data[-1][1] + 1:
                break
            delay(2)
        print(d)
        data.append((t-t0, d))
        delay(intervall)
        if d < stop_distance:
            break
        
    return data

def measure_v(power, duration, intervall, ignore=0):
    setSpeed(power)
    forward()
    data = get_distances(duration)
    stop()
    
    t2, d2 = data[-ignore]
    t1, d1 = len(data) > ignore and data[ignore]
    total_time = abs(t2 - t1)
    total_distance =  abs(d2 - d1)
    avg_v = total_distance / total_time * 1000
    
    t0 = data[0][0]
    return total_time, total_distance, t2 - t0
        

def experiment(power, duration, intervall):
    filename = '{power}-measures.csv'.format(power=power)
    headers = ('temps', 'distance')
    setSpeed(power)
    forward()
    data = get_distances(duration, intervall)
    stop()
    write_data_to_csv(filename, data, headers)
    

if __name__ == '__main__':
    all_v = []
    power = 100
    nb_runs = 5
    for _ in range(nb_runs):
        t, d, exp_time = measure_v(power, 3000, 100, 4)
        stop()
        delay(500)
        backward()
        v = d / t
        print("v = ", v)
        all_v.append(v)
        delay(int(exp_time * 1.08))
        stop()
        delay(1000)
        
    avg = sum(all_v) / len(all_v)
    print("all v", all_v)
    all_v = [v for v in all_v if abs(v - avg) < 0.005]
    print("avg velocity for power={power} and {n} runs".format(power=power, n=nb_runs),
          sum(all_v) / len(all_v) * 1000)
