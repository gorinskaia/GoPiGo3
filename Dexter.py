import time
from easygopigo3 import EasyGoPiGo3
curr_time = time.time()

class Dexter:
    'Robot class'
    def __init__(self, gpg):
        self.gpg = EasyGoPiGo3()

    def set_speed(self, left_speed, right_speed):
        print('set speed')
        self.gpg.set_motor_limits(self.gpg.MOTOR_LEFT,left_speed)
        self.gpg.set_motor_limits(self.gpg.MOTOR_RIGHT,right_speed)

    def forward(self,speed):
        self.gpg.set_speed(speed)
        
    def turnRight(self,speed):
        self.gpg.set_speed(speed,0)
        
    def turnLeft(self,speed):
        self.gpg.set_speed(0,speed)
        
    def shutdown(self):
        self.forward(0)

    def reset_encoders(self):
        self.gpg.set_motor_power(self.gpg.MOTOR_LEFT + self.gpg.MOTOR_RIGHT, 0)
        left_target = self.gpg.get_motor_encoder(self.gpg.MOTOR_LEFT)
        right_target = self.gpg.get_motor_encoder(self.gpg.MOTOR_RIGHT)
        self.gpg.offset_motor_encoder(self.gpg.MOTOR_LEFT, left_target)
        self.gpg.offset_motor_encoder(self.gpg.MOTOR_RIGHT, right_target)
        
    def get_dist(self):
        dist_mm = self.gpg.init_distance_sensor()
        return dist_mm.read_mm()
        
    
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
    
    def shutdown(self):
        self.gpg.shutdown()
     
    
class ControllerForward:
    'Politics to move forward'
    def __init__(self, Dexter, speed = 300, dist = 100):
        print("init")
        self.speed = speed
        self.dist = dist
        self.gpg = Dexter
        
    def start(self):
        print("start")
        self.gpg.reset_encoders()
        self.gpg.set_speed(self.speed,self.speed)

    def stop(self):
        res = self.gpg.get_dist() <= self.dist
        if res:
            print("stop")
            return res
        else:
            return res
    
    def update(self):
        #print("update")
        if self.stop(): 
            return
        self.gpg.forward(self.speed)
    
