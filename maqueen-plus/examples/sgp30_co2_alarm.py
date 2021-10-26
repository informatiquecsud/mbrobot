from mbrobot import *
from mbalarm import *

from microbit import i2c
from utime import sleep_ms as delay

def sgp30_init(addr=0x58):
    i2c.write(addr, bytearray([0x20, 0x03]))
    delay(1500)

def sgp30_get_values(addr=0x58):
    # écrire la commande sgp30_measure_iaq
    i2c.write(addr, bytearray([0x20, 0x08]))
    delay(600)

    # lire 6 octets
    co2_1, co2_2, _, tvoc_1, tvoc_2, _ = i2c.read(addr, 6)

    # interpréter les valeurs
    co2_value = co2_1 << 8 | co2_2
    tvoc_value = tvoc_1 << 8 | tvoc_2

    return co2_value, tvoc_value

def measure():
    sgp30_init()
    while True:
        co2, tvoc = sgp30_get_values()
        print("Concentration de CO2 mesurée", co2)
        delay(500)
        
        
def blink_once(color=LEDState.RED, duration=1000):
    leds.both(color)
    delay(duration // 2)
    leds.both(LEDState.OFF)
    delay(duration // 2)
    

def co2_alert(warning_value=800, bad_value=1200, critical_value=2000):
    sgp30_init()
    delay(1500)
    
    while True:
        co2, _ = sgp30_get_values()
        print("CO2 value: ", co2)
        
        if co2 < critical_value:
            setAlarm(0)
            
        if co2 < warning_value:
            leds.both(LEDState.GREEN)
        elif co2 < bad_value:
            leds.both(LEDState.YELLOW)
        elif co2 < critical_value:
            leds.both(LEDState.RED)
        else:
            setAlarm(1)
            blink_once(color=LEDState.RED, duration=500)
            
        delay(300)
    
    
co2_alert()
    

