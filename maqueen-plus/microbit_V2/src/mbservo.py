from microbit import i2c, sleep

i2c_address = 0x10

class ServoPort:
    
    S1 = 0x14
    S2 = 0x15
    S3 = 0x16

    @staticmethod
    def list():
        return [ServoPort.S1, ServoPort.S2, ServoPort.S3]


class Servo:

    def __init__(self, id):
        if id not in ServoPort.list():
            raise ValueError("Servo connector " + str(id) + "is invalid")
        else:
            self.id = id

    def rotateTo(self, angle: int) -> None:
        try:
            i2c.write(i2c_address, bytearray([self.id, angle]))
        except Exception as e:
            print("Error: " + str(e))
        
            
    def read_angle(self):
        i2c.write(i2c_address, bytearray([self.id]))
        buf = i2c.read(i2c_address, 1)
        return buf[0]


servo_1 = Servo(ServoPort.S1)
servo_2 = Servo(ServoPort.S2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
servo_3 = Servo(ServoPort.S3)

if __name__ == '__main__':
    servo_1.rotateTo(90)
                                                         
