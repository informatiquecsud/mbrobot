from microbit import __i2c


class MicrobitI2CAdapter:
    
    def __init__(self, freq=100000, scl=19, sda=20):
        pass
     
    '''
    def init(self, freq=100000, scl=19, sda=20):
        self.__I2C.init(scl, sda, freq)
        
    def scan(self):
        return self.__I2C.scan()
    '''
    
    def read(self, addr, n):
        return __i2c.readfrom(addr, n)        
        
    def write(self, address, buf):
        return __i2c.writeto(addr, buf)
        

i2c = MicrobitI2CAdapter()

