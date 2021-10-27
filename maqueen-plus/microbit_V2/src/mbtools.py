from mbservo import *


class Forklift:

    def __init__(self, servo=None, up_angle=0, down_angle=110):
        self.servo = servo or servo_1
        self.up_angle = up_angle
        self.down_angle = down_angle

    def up(self):
           print('moving to', self.servo.rotateTo(self.up_angle))

    def down(self):
        self.servo.rotateTo(self.down_angle)
        
    def middle(self):
        self.servo.rotateTo(abs(self.down_angle + self.up_angle) // 2)


class Beetle:

    def __init__(self, servo, close_angle=86, open_angle=30):
        self.servo = servo
        self.close_angle = close_angle
        self.open_angle = open_angle

    def open(self):
        self.servo.rotateTo(self.open_angle)

    def close(self):
        self.servo.rotateTo(self.close_angle)
        
    def set_angle(self, angle):
        if 30 <= angle <= 110:
            self.servo.rotateTo(angle)
        else:
            raise ValueError("angle should be between 30° and 110°")
        
    def set_close_angle(self, angle):
        self.close_angle = angle


forklift = Forklift(servo_1)
beetle = Beetle(servo_1)


if __name__ == '__main__':
    f = Forklift(up_angle=0, down_angle=90)
    f.middle()
