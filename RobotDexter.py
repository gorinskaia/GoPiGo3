import time
import math

class Dexter:
    'Robot class'
    def __init__(self, gpg):
        self.gpg = gpg
        self.dist_mm = gpg.init_distance_sensor()

    def set_speed(self, left_speed, right_speed):
        self.gpg.set_motor_dps(self.gpg.MOTOR_LEFT,left_speed)
        self.gpg.set_motor_dps(self.gpg.MOTOR_RIGHT,right_speed)

    def reset(self):
        left_target = self.gpg.get_motor_encoder(self.gpg.MOTOR_LEFT)
        right_target = self.gpg.get_motor_encoder(self.gpg.MOTOR_RIGHT)
        self.gpg.offset_motor_encoder(self.gpg.MOTOR_LEFT, left_target)
        self.gpg.offset_motor_encoder(self.gpg.MOTOR_RIGHT, right_target)

    def get_offset(self):
        left_pos = self.gpg.get_motor_encoder(self.gpg.MOTOR_LEFT)
        right_pos = self.gpg.get_motor_encoder(self.gpg.MOTOR_RIGHT)
        return (left_pos, right_pos)
        
    def get_dist(self):
        return self.dist_mm.read_mm()

    def condition(self, ctrl):
        return self.gpg.get_dist() <= self.dist

    def angle_reached(self, ctrl):
        res = self.gpg.get_offset()
        offset = max(abs(res[1]), abs(res[0]))
        turn = ((self.gpg.gpg.WHEEL_CIRCUMFERENCE*offset)/(self.gpg.gpg.WHEEL_BASE_CIRCUMFERENCE))/2
        return abs(turn)>=abs(self.angle)
    
    def shutdown(self):
        self.forward(0)
