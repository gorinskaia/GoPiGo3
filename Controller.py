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
