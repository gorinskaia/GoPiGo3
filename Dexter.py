import time
from easygopigo3 import EasyGoPiGo3
curr_time = time.time()

class Dexter:
    'Robot class'
    def __init__(self, gpg):
        self.gpg = EasyGoPiGo3()

    def set_speed(self,left_speed, right_speed):
        self.gpg.set_motor_dps(self.gpg.MOTOR_LEFT,lspeed)
        self.gpg.set_motor_dps(self.gpg.MOTOR_RIGHT,rspeed)

    def forward(self,speed):
        self.gpg.set_speed(speed,speed)
        
    def turnRight(self,speed):
        self.gpg.set_speed(speed,0)
        
    def turnLeft(self,speed):
        self.gpg.set_speed(0,speed)
        
    def shutdown(self):
        self.forward(0)
        self.set_off()

    def reset_encoders(self):
        self.set_motor_power(self.MOTOR_LEFT + self.MOTOR_RIGHT, 0)
        left_target = self.get_motor_encoder(self.MOTOR_LEFT)
        right_target = self.get_motor_encoder(self.MOTOR_RIGHT)
        self.offset_motor_encoder(self.MOTOR_LEFT, left_target)
        self.offset_motor_encoder(self.MOTOR_RIGHT, right_target)

    
class ControllerForward:
    'Politics to move forward'
    def __init__(self, Dexter, speed = 300, dist = 100):
        self.speed = speed
        self.dist = dist
        self.Dexter = Dexter
        
    def start(self):
        self.Dexter.reset_encoders()
        self.gpg.set_speed(speed,speed)

    def stop(self):
        my_dist = self.gpg.init_distance_sensor()
        return my_dist.read_mm() >= self.dist
    
    def update(self):
        if self.stop(): 
            return
        self.Dexter.forward(self.speed)
    
