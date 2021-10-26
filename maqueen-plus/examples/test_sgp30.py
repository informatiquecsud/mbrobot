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

measure()