import time

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
    def __init__(self, robot, speed = 300, dist = 150):
        self.speed = speed
        self.dist = dist
        self.robot = robot
        self.flag = False
        
    def start(self):
        self.robot.reset()
        self.flag = False

    def stop(self):
        return self.robot.condition(self)
    
    def update(self):
        if self.stop():
            return
        self.robot.forward(self.speed)


class ControllerTurn:
    'Politics to turn'
    def __init__(self, robot, speed = 300, angle = 90):
        self.speed = speed
        self.angle = angle
        self.robot = robot
        self.start_time = 0
        self.t_rotation = abs(angle/32.7)
        
    def start(self):
        self.robot.reset()
        self.start_time = time.time()

    def stop(self):
        return self.robot.angle_reached(self)
         
    def update(self):
        if self.stop(): 
            return
        self.robot.setAngle(self.angle, self.speed)
        
