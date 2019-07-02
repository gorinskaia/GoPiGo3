import time
import math
from picamera import PiCamera
from io import BytesIO
from PIL import Image

class Dexter:
    'Robot class'

    WHEEL_BASE_WIDTH         = 117  # distance (mm) de la roue gauche a la roue droite.
    WHEEL_DIAMETER           = 66.5 #  diametre de la roue (mm)
    WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi # perimetre du cercle de rotation (mm)
    WHEEL_CIRCUMFERENCE      = WHEEL_DIAMETER   * math.pi # perimetre de la roue (mm)
    
    def __init__(self, gpg):
        self.gpg = gpg
        self.dist_mm = gpg.init_distance_sensor()
        self.camera = PiCamera()
        self.camera.resolution = (320, 240)
        self.camera.framerate = 30

    def set_speed(self, left_speed, right_speed):
        self.gpg.set_motor_dps(self.gpg.MOTOR_LEFT,left_speed)
        self.gpg.set_motor_dps(self.gpg.MOTOR_RIGHT,right_speed)

    def setAngle(self, angle, speed = 300):
        if angle>0:                         # Turn right
            self.set_speed(speed,0)
        else:                               # Turn left
            self.set_speed(0,speed)    
        
    def shutdown(self):
        self.set_speed(0,0)

    def reset(self):
        left_target, right_target = self.get_offset()
        self.gpg.offset_motor_encoder(self.gpg.MOTOR_LEFT, left_target)
        self.gpg.offset_motor_encoder(self.gpg.MOTOR_RIGHT, right_target)
        self.N = 0

    def get_offset(self):
        left_pos = self.gpg.get_motor_encoder(self.gpg.MOTOR_LEFT)
        right_pos = self.gpg.get_motor_encoder(self.gpg.MOTOR_RIGHT)
        return (left_pos, right_pos)
        
    def get_dist(self):
        return self.dist_mm.read_mm()
    
    def get_speed(self):
        return self.gpg.get_speed()

    def condition(self, ctrl):
        return self.get_dist() <= ctrl.dist

    def get_image(self):
        print ('Cheese!')
        stream = BytesIO()
        self.camera.capture(stream,format="jpeg")
        self.camera.capture('result.jpeg')
        stream.seek(0)
        img = Image.open(stream).copy()
        stream.close()
        return img
