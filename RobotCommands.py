
class ControlRobot:
    'Common functions'
    def __init__(self, robot):
        self.robot = robot
        
    def forward(self,speed):
        self.robot.set_speed(speed, speed)

    def shutdown(self):
        self.forward(0)
