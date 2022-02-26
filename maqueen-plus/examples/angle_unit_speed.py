from mbrobot_plus import *
from m5stack_angle_unit import *

# range: min speed=20, max speed=100
angle_0.set_range(20, 100)

# calibrate the angle sensor
angle_0.calibrate()

while True:
    a = angle_0.read_value()
    print("speed", a)
    setSpeed(a)
    forward()
    delay(50)
