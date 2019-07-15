import time
import math
import threading
import numpy as np
import os


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
        self.robot.count = 1
        t = threading.Timer(0.5, self.robot.get_image)
        t.start()
        t.join()

    def stop(self):
        return self.robot.condition(self)
    
    def update(self):
        print (self.robot.get_dist())
        # Calibration parameters:
        cl, cr = self.robot.odometry()

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
        t = threading.Timer(0.5, self.robot.get_image)
        t.start()
        t.join()

    def angle_reached(self):
        res = self.robot.get_offset()
        offset = max(abs(res[1]), abs(res[0]))
        turn = ((self.robot.WHEEL_CIRCUMFERENCE*offset)/(self.robot.WHEEL_BASE_CIRCUMFERENCE))/2
    
        return abs(turn)>=abs(self.angle)

    def stop(self):
        return self.angle_reached()
         
    def update(self):
        print (self.robot.get_dist())
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
        #print (self.cX, self.cY)
        if self.cX < (self.robot.CAMX/2 - 15):
            #print ('turn left')
            cl = 0.75
            cr = 1.25
        elif self.cX > (self.robot.CAMX/2 + 15):
            #print ('turn right')
            cl = 1.25
            cr = 0.75
        else:
            #print ('forward')
            cr = 1
            cl = 1
            
        if self.stop():
            self.taking_photo = False
            self.robot.shutdown() #new
            return
        self.robot.set_speed(self.speed*cl, self.speed*cr)
            
#############


class Env:
    def __init__(self, robot, speed):
        self.robot = robot
        self.speed = speed
        self.actions = [0, 1, 2, 3]  #speed values
        self.states = [1000, 150, 120, 90, 60] #distance from the wall
        self.stateCount = len(self.states)
        self.actionCount = len(self.actions)

    def reset(self):
        self.robot.set_speed(0, 0)
        self.done = False;
        return 0, 0, False;

    # take action
    def step(self, action):
        if action==0: # Full speed
            self.robot.set_speed(self.speed, self.speed)
        if action==1: # Half-speed
            self.robot.set_speed(self.speed/2, self.speed/2)
        if action==2: # Quarter-speed
            self.robot.set_speed(self.speed/4, self.speed/4)
        if action==3: # Stop
            self.robot.set_speed(0, 0)

        done = (self.robot.get_dist() == 50)
    
        nextState = self.robot.get_dist()

        if done:
            reward = 10
        elif self.robot.get_dist() == 100:
            reward = 5
        elif self.robot.get_dist() == 150:
            reward = 1
        else:
            reward = 0
        
        return nextState, reward, done

    def randomAction(self):
        return np.random.choice(self.actions);
        
class ControllerLearn:
    'Learning'
    def __init__(self, robot, speed = 300, dist = 150):
        self.speed = speed
        self.dist = dist
        self.robot = robot
        self.flag = False

    def start(self):
        env = Env(self.robot, self.speed)
        self.robot.reset()
        self.flag = False
        # QTable : contains the Q-Values for every (state,action) pair
        qtable = np.random.rand(env.stateCount, env.actionCount).tolist()

        # hyperparameters
        epochs = 20
        gamma = 0.1
        epsilon = 0.08
        decay = 0.1

        # training loop
        for i in range(epochs):
            state, reward, done = env.reset()
            steps = 0

            while not done:

                # act randomly sometimes to allow exploration
                if np.random.uniform() < epsilon:
                    action = env.randomAction()
                # if not select max action in Qtable (act greedy)
                else:
                    action = qtable[state].index(max(qtable[state]))

                # take action
                next_state, reward, done = env.step(action)

                # update qtable value with Bellman equation
                qtable[state][action] = reward + gamma * max(qtable[next_state])

                # update state
                state = next_state
            # The more we learn, the less we take random actions
            epsilon -= decay*epsilon

            #print("\nDone in", steps, "steps".format(steps))

            time.sleep(0.4)
  
