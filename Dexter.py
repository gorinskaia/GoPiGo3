import time
from easygopigo3 import EasyGoPiGo3
import math

class Dexter:
    'Robot class'
    def __init__(self, gpg):
        self.gpg = EasyGoPiGo3()
        self.dist_mm = gpg.init_distance_sensor()

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

    def get_offset(self):
        left_pos = self.gpg.get_motor_encoder(self.gpg.MOTOR_LEFT)
        right_pos = self.gpg.get_motor_encoder(self.gpg.MOTOR_RIGHT)
        return (left_pos, right_pos)
        
    def get_dist(self):
        return self.dist_mm.read_mm()

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
        print("start forward")
        self.gpg.reset_encoders()

    def stop(self):
        return self.gpg.get_dist() <= self.dist
    
    def update(self):
        if self.stop(): 
            return
        self.gpg.forward(self.speed)


class ControllerTurn:
    'Politics to turn'
    def __init__(self, Dexter, speed = 300, angle = 90):
        self.speed = speed
        self.angle = angle
        self.gpg = Dexter
        
    def start(self):
        print("start turn")
        self.gpg.reset_encoders()

    def stop(self):
        res = self.gpg.get_offset()
        offset = max(abs(res[1]), abs(res[0]))
        turn = ((self.gpg.gpg.WHEEL_CIRCUMFERENCE*offset)/(self.gpg.gpg.WHEEL_BASE_CIRCUMFERENCE))/2
        return abs(turn)>=abs(self.angle)   
    
    def update(self):
        if self.stop(): 
            return
        if self.angle>=0:
            self.gpg.turnRight(self.speed)
        else:
            self.gpg.turnLeft(self.speed)

class ControllerSequence:
    'Sequence of commands'
    def __init__(self, Dexter,commands = []):
        self.gpg = Dexter
        
        self.commands = []
        self.commands = [x for x in commands]
        self.count = 0 # Number of a command counter
        
    def start(self):
        self.count = -1
    
    def stop(self):
        return self.count >= len(self.commands)

    def update(self):
        if self.stop():
            return
        if self.count < 0 or self.commands[self.count].stop():
            self.count+=1
            if self.stop():
                return
            self.commands[self.count].start()
        self.commands[self.count].update()
