import time
import math
import threading

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
        # Calibration parameters:
        cl = 1
        cr = 1
        '''left_steps, right_steps = self.robot.get_offset()
        if left_steps>0 and right_steps>0:
            cl = self.robot.WHEEL_CIRCUMFERENCE / left_steps
            cr = self.robot.WHEEL_CIRCUMFERENCE / right_steps
            if cl > 1 or cr > 1:
                cl = 1
                cr = 1
            print('left: ',cl,' right', cr)'''

        left_steps, right_steps = self.robot.get_offset()
        print (left_steps, right_steps)
        
        if self.stop():
            self.robot.shutdown() #new
            return
        self.robot.set_speed(self.speed*cl, self.speed*cr)

class ControllerTurn:
    'Politics to turn'
    def __init__(self, robot, speed = 300, angle = 90):
        self.speed = speed
        self.angle = angle
        self.robot = robot
        self.start_time = 0

    def start(self):
        self.robot.reset()

    def angle_reached(self):
        res = self.robot.get_offset()
        offset = max(abs(res[1]), abs(res[0]))
        turn = ((self.robot.WHEEL_CIRCUMFERENCE*offset)/(self.robot.WHEEL_BASE_CIRCUMFERENCE))/2
    
        return abs(turn)>=abs(self.angle)

    def stop(self):
        return self.angle_reached()
         
    def update(self):
        if self.stop(): 
            return
        self.robot.get_offset()
        
        if self.angle>0:                         # Turn right
            self.robot.set_speed(0, self.speed)
        else:                                    # Turn left
            self.robot.set_speed(self.speed, 0)

class ControllerSequence:
    'Sequence of commands'
    def __init__(self, commands = []):
        self.commands = []
        self.commands = [x for x in commands]
        self.count = 0
        
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
        
