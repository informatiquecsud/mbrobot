from microbit import i2c
from utime import ticks_ms, sleep_ms

i2c_addr = 0x10

def motor(dirL, pL, dirR, pR):
    i2c.write(i2c_addr, bytearray([0x00,dirL, pL, dirR, pR]))

def reset_degrees():
    # réinitialise le compteur interne de rotation à 0° pour les deux moteurs
    i2c.write(i2c_addr, bytearray([0x04, 0, 0, 0]))
    
def read_degrees(motor_id):
    ''' motor_id: 0=LEFT, 1=RIGHT '''
    i2c.write(i2c_addr, bytearray([4]))
    buf = i2c.read(i2c_addr, 4)
        
    # retourne la position du moteur en degrés
    value = (buf[motor_id * 2] << 8 | buf[motor_id * 2 + 1])
    return value * 360 / 80
    

def angular_speed(power, duration=1000):
    reset_degrees()
    sleep_ms(50)
    t0 = ticks_ms()
    motor(1, power, 1, power)
    sleep_ms(duration)
    t1 = ticks_ms()
    deg = read_degrees(0)
    
    # retourne la vitesse angulaire en °/seconde
    return int(deg / (t1 - t0) * 1000)

with open('angular_speed.csv', 'w') as csvfile:
    power_values = range(20, 256, 10)
    for power in power_values:
        value =  angular_speed(power)
        print('{}\t{}'.format(power, value))
        csvfile.write('{};{}\n'.format(power, value))