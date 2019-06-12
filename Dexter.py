import time
from easygopigo3 import EasyGoPiGo3
curr_time = time.time()

class Dexter:

    'Robot class'
    def __init__(self, speed = 300):
        self.speed = speed # Initial speed
        self.dist = dist
        self.gpg = EasyGoPiGo3()

    def get_speed(self):
        return int(self.speed)

    def set_speed(self,left_speed, right_speed):
        self.gpg.set_motor_dps(self.gpg.MOTOR_LEFT,lspeed)
        self.gpg.set_motor_dps(self.gpg.MOTOR_RIGHT,rspeed)

    def stop(self):
        my_dist = self.gpg.init_distance_sensor()
        return my_dist.read_mm() >= self.dist
        #self.gpg.set_motor_dps(self.gpg.MOTOR_LEFT + self.gpg.MOTOR_RIGHT, 0)

    def forward(self,speed):
        self.gpg.set_speed(speed,speed)
        
    def turnRight(self,speed):
        self.gpg.set_speed(speed,0)
        
    def turnLeft(self,speed):
        self.gpg.set_speed(0,speed)

    def update(self):
        for i in range(4):
          set_speed(self,self.speed, self.speed):
          time.sleep(2)
          turnRight(self,self.speed)
          time.sleep(0.6)
    
