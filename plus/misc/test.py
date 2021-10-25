from microbit import i2c
from utime import sleep_ms

delay = sleep_ms

i2c_addr = 0x10

ALL_MOTORS = 0x00
MOTOR_LEFT = 0x00
MOTOR_RIGHT = 0x02
DIR_STOP = 0
DIR_FORWARD = 1
DIR_BACKWARD = 2

def forward(power):
    i2c.write(i2c_addr, bytearray([ALL_MOTORS, DIR_FORWARD, power, DIR_FORWARD, power]))
    

def stop():
    i2c.write(i2c_addr, bytearray([ALL_MOTORS, DIR_STOP, 0, DIR_STOP, 0]))
              
    
def reset_motor_pos():
    i2c.write(i2c_addr, bytearray([0x04, 0, 0, 0]))
    

def read_motor_pos():
    i2c.write(i2c_addr, bytearray([4]))
    buf = i2c.read(i2c_addr, 4)
        
    degL = (buf[MOTOR_LEFT] << 8 | buf[MOTOR_LEFT + 1])
    degR = (buf[MOTOR_RIGHT] << 8 | buf[MOTOR_RIGHT + 1])
    return degL, degR

def read_encoder_values():
    # écrire l'octet 0x00=lire toutes les valeurs des deux moteurs
    i2c.write(i2c_addr, bytearray([ALL_MOTORS]))
    # lire 4 octets
    buffer = i2c.read(i2c_addr, 4)
    dirL, speedL, dirR, speedR = buffer
    return dirL, speedL, dirR, speedR


def cm2pos(cm):
    # le compteur de rotation augmente de 578 tous les 100 cm
    return cm * 5.78

def pos2cm(pos):
    return pos / 5.78

    
def forward_to(power, target_cm):
    reset_motor_pos()
    delay(100)
    
    # compenser le dépassement dû à l'inertie
    target_cm -= power / 4
    
    while True:
        degL, degR = read_motor_pos()
        if (degL + degR) / 2 > target_cm:
            break
        
        forward(power)
        delay(5)
        
    stop()
    # attendre tant que le robot n'est pas arrêté pour retourner la position des moteurs
    while True:
        dirL, speedL, dirR, speedR = read_encoder_values()
        if speedL + speedR == 0:
            break
        delay(10)
    
    return read_motor_pos()
        
    
def measure():
    reset_motor_pos()
    while True:
        print(read_motor_pos())
        delay(100)
    
degL, degR = forward_to(100, cm2pos(20))
print(pos2cm(degL), pos2cm(degR))