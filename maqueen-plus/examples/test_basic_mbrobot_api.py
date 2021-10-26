# This scripts runs compatibility tests with the basic APLU mbrobot API

from mbrobot import *

def test_blink_leds(nb_blinks=2, duration=1000):
    for _ in range(int(nb_blinks)):
        setLED(1)
        delay(duration // nb_blinks // 2)
        setLED(0)
        delay(duration // nb_blinks // 2)

    
def test_leds():
    print("testing leds ...")
    print("blink 2 times during 1 second")
    test_blink_leds()
    print("blink 4 times during 2 seconds")
    test_blink_leds(4, 2000)
    
    
def run_square(side_time, rotation_time, speed=50):
    setSpeed(speed)
    for _ in range(4):
        forward()
        delay(side_time)
        right()
        delay(rotation_time)
    stop()
    
def run_square_reverse(side_time, rotation_time, speed=50):
    setSpeed(speed)
    for _ in range(4):
        backward()
        delay(side_time)
        left()
        delay(rotation_time)
    stop()
    
def test_change_speed():
    for power in range(50, 150, 20):
        setSpeed(power)
        forward()
        delay(1000)
        
    stop()
    
def test_arcs(radius, power, duration):
    print("testing leftArc")
    setSpeed(power)
    leftArc(radius)
    delay(duration)
    rightArc(radius)
    delay(duration)
    stop()
    
    
def test_spiral(power=255, init_radius=0.1, max_radius=0.6, incr=0.02, duration_per_value=1000):
    # With PID, the wheels really turn at the prescribed velocity
    setPID(1)
    setSpeed(power)
    
    radius = init_radius
    while radius < max_radius:
        print("Radius", radius)
        leftArc(radius)
        delay(duration_per_value)
        radius += incr
        
    stop()
    setPID(0)
    
    
def test_individual_motors():
    # forward left motor
    motL.rotate(100)
    delay(2000)
    motL.rotate(-100)
    delay(2000)
    motR.rotate(100)
    delay(2000)
    motR.rotate(100)
    
    setPID(1)
    motL.rotate(30)
    motR.rotate(60)
    delay(4000)
    stop()
    setPID(0)
    
def test_movements():
    print("testing forward and right")
    run_square(1000, 600, 50)
    print("testing backward and left")
    run_square_reverse(1000, 600, 50)
    print("testing setSpeed ... robot should accelerate each 1 second")
    test_change_speed()
    print("testing leftArc and rightArc. Robot should be turing along a spiral")
    test_spiral()
    print("testing individual motors control à la APLU mborobt")
    test_individual_motors()
    
def test_urm10_ultrasonic_sensor():
    for _ in range(100):
        d = getDistance()
        print("Distance :", d)
        delay(100)
        
def test_ir_L1_R1():
    for _ in range(100):
        vL = irLeft.read_digital()
        vR = irRight.read_digital()
        
        print("values: ", vL, vR)
        delay(100)
    
if __name__ == '__main__':
    test_leds()
    test_movements()
    test_urm10_ultrasonic_sensor()
    test_ir_L1_R1()
    
    
    
    
    
    
    