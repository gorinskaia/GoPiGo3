import time
from easygopigo3 import EasyGoPiGo3

class Dexter:
    'Robot class'
    def __init__(self, gpg):
        self.gpg = EasyGoPiGo3()

    def set_speed(self, left_speed, right_speed):
        self.gpg.set_motor_dps(self.gpg.MOTOR_LEFT,left_speed)
        self.gpg.set_motor_dps(self.gpg.MOTOR_RIGHT,right_speed)

    def forward(self,speed):
        self.set_speed(speed, speed)
        
    def turnRight(self,speed):
        self.set_speed(speed,0)
        
    def turnLeft(self,speed):
        self.set_speed(0,speed)
        
    def shutdown(self):
        self.forward(0)

    def reset_encoders(self):
        left_target = self.gpg.get_motor_encoder(self.gpg.MOTOR_LEFT)
        right_target = self.gpg.get_motor_encoder(self.gpg.MOTOR_RIGHT)
        self.gpg.offset_motor_encoder(self.gpg.MOTOR_LEFT, left_target)
        self.gpg.offset_motor_encoder(self.gpg.MOTOR_RIGHT, right_target)
        
    def get_dist(self):
        dist_mm = self.gpg.init_distance_sensor()
        return dist_mm.read_mm()

    def shutdown(self):
        self.set_speed(0,0)
        
    
class ControllerInit:
    'Initial state'
    def __init__(self,gpg):
        self.gpg = gpg
        
    def start(self):
        pass
    
    def stop(self):
        pass
    
    def update(self):
        pass
    
    
class ControllerForward:
    'Politics to move forward'
    def __init__(self, Dexter, speed = 300, dist = 150):
        self.speed = speed
        self.dist = dist
        self.gpg = Dexter
        
    def start(self):
        print("start")
        self.gpg.reset_encoders()

    def stop(self):
        return self.gpg.get_dist() <= self.dist
    
    def update(self):
        if self.stop(): 
            return
        self.gpg.forward(self.speed)

'''class ControllerTurn:
    'Politics to turn'
    def __init__(self, Dexter, speed = 300, angle = 90):
        print("init")
        self.speed = speed
        self.angle = angle
        self.gpg = Dexter
        
    def start(self):
        print("start")
        self.gpg.reset_encoders()

    def stop(self):
        res = self.gpg.get_dist() <= self.dist
        if res:
            print("stop")
            return res
        else:
            return res
    
    def update(self):
        print("update")
        if self.stop(): 
            return
        self.gpg.forward(self.speed)'''
    
