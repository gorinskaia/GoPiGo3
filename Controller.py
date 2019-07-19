import time
import math
import threading
import numpy as np
from numpy import random
import os
import matplotlib.pyplot as plt
from TrainingModel import EnvQLearning
from TrainingModel import EnvNN
from TrainingModel import NeuralNetwork
from TrainingModel import NeuronLayer


class ControllerInit:
    'Initial state'
    def __init__(self,robot):
        self.robot = robot
        
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
        self.robot.count = 1
        t = threading.Timer(0.5, self.robot.get_image)
        t.start()
        t.join()

    def stop(self):
        return self.robot.condition(self)
    
    def update(self):
        #print (self.robot.get_dist())
        cl, cr = self.robot.odometry()

        if self.stop():
            self.robot.shutdown()
            return
        self.robot.set_speed(self.speed*cl, self.speed*cr)

class ControllerTurn:
    'Politics to turn'
    def __init__(self, robot, speed = 300, angle = 90):
        self.speed = speed
        self.angle = angle
        self.robot = robot

    def start(self):
        self.robot.reset()
        #t = threading.Timer(0.5, self.robot.get_image)
        #t.start()
        #t.join()

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

class ControllerFollow:
    'Politics to follow an object'
    def __init__(self, robot, speed = 300, dist = 150):
        self.speed = speed
        self.dist = dist
        self.robot = robot
        self.cX = self.robot.CAMX/2
        self.cY = self.robot.CAMY/2
        self.flag = False
        self.taking_photo = True
        
        t = threading.Thread(target=self.image, daemon = True) #or put it outside of controllers
        t.start()

    def start(self):
        self.robot.reset()
        self.flag = False
        self.robot.count = 1

    def image(self):
        while self.taking_photo:
            self.cX, self.cY = self.robot.get_image()

    def stop(self):
        return self.robot.condition(self)
    
    def update(self):
        cl = 1
        cr = 1
        diff = int(self.robot.CAMX/10)
        if self.cX < (self.robot.CAMX/2 - diff):
            cl = 0.75
            cr = 1.25
        elif self.cX > (self.robot.CAMX/2 + diff):
            cl = 1.25
            cr = 0.75
        else:
            cr = 1
            cl = 1
            
        if self.stop():
            self.taking_photo = False
            self.robot.shutdown()
            return
        self.robot.set_speed(self.speed*cl, self.speed*cr)

class ControllerLearn:
    'Training'
    def __init__(self, robot, option, speed = 300):
        self.speed = speed
        self.robot = robot
        self.option = option

    def start(self):
        if self.option =="Q":
            self.env = EnvQLearning(self)
        if self.option =="NN":
            self.env = EnvNN(self)
            self.env.train()

        self.robot.reset()
        self.k = 0
        self.end_episode = False
        self.stop_simulation = False

    def stop(self):
        return self.stop_simulation
    
    def update(self):
        if self.end_episode:
            print ('EPISODE OVER')
            self.env._reset()
            
        if self.k >= self.env.epochs:
            print ('GAME OVER')
            self.stop_simulation = True

            f = open("weights.txt","w+")
            f.write(str(self.env.neural_network.layer1.weights))
            f.write(str(self.env.neural_network.layer2.weights))
            f.close()
            
            return
        self.env._update()

class ControllerForwardSmart:
    'Testing the ANN'
    def __init__(self, robot, ctrl, speed = 300):
        self.robot = robot
        self.speed = speed
        self.ctrl = ctrl
        self.k = 0

    def start(self):
        self.env = EnvNN(self)
        layer1 = NeuronLayer(4, 1) # 4 neurons, 1 input
        layer2 = NeuronLayer(1, 4) # output
        layer1.weights = [[9.33508627 , -0.14762897, -13.5186365,  0.97483954]]
        layer2.weights = [[  8.49960835], [ -1.6299063 ], [-17.82664448], [ -0.43608188]]
        self.env.neural_network = NeuralNetwork(layer1, layer2)

    def stop(self):
        return self.k >= self.env.epochs
    
    def update(self):
        self.env._update()
