import time
import math
import threading
import numpy as np
import os


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
        #print (self.robot.get_dist())
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
    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.actions = [0, 1, 2, 3]  #speed values
        self.states = [0, 1, 2, 3, 4, 5]  #distance from the wall, 0 = far, 4 = close
        self.stateCount = len(self.states)
        self.actionCount = len(self.actions)
        self.done = False
        self.stop_count = 0

    def reset(self):
        time.sleep(0.5)
        self.ctrl.robot.chassisNP.setPos(0, 0, 0.1)
        self.done = False
        self.ctrl.robot.condition(self.ctrl) #to force distance reset?..
        self.ctrl.k+=1
        
        self.ctrl.robot.sim.distance = 1000
        self.dist_value = 1000
        self.stop_count = 0

        print ('-----RESET-----')
        
        return 0, 0, False

    def step(self, action):

        self.dist_value = self.ctrl.robot.get_dist()
        print ('For the love of god '+str(self.ctrl.robot.sim.distance))
        print ('Distance is '+str(self.dist_value))
        
        if action==0: # Full speed
            #print ('Full speed')
            self.ctrl.robot.set_speed(self.ctrl.speed, self.ctrl.speed)
        if action==1: # Half-speed
            #print ('speed 0.8')
            self.ctrl.robot.set_speed(self.ctrl.speed*0.8, self.ctrl.speed*0.8)
        if action==2: # Quarter-speed
            #print ('speed 0.6')
            self.ctrl.robot.set_speed(self.ctrl.speed*0.6, self.ctrl.speed*0.6)
        if action==3: # Stop
            #print ('speed 0')
            self.ctrl.robot.set_speed(0, 0)

        # Reward table
        if self.dist_value == 60:
            reward = 100
        elif self.dist_value == 75:
            reward = 0
        elif self.dist_value == 90:
            reward = 0
        elif self.dist_value == 105:
            reward = 0
        elif self.dist_value == 45:
            reward = -1000
        else:
            reward = -1
  
        # Choosing next state?..
        if self.dist_value == 60:
            nextState = 4
            self.stop_count +=1
            if self.stop_count>50:
                self.done = True
        elif self.dist_value == 75:
            nextState = 3
        elif self.dist_value == 90:
            nextState = 2
        elif self.dist_value == 105:
            nextState = 1
        elif self.dist_value == 45:
            nextState = 5
            self.done = True
        else: 
            nextState = 0

        return nextState, reward, self.done

    def randomAction(self):
        return np.random.choice(self.actions);


        
class ControllerLearn:
    'Training'
    def __init__(self, robot, speed = 300):
        self.speed = speed
        self.robot = robot
        self.flag = False

    def start(self):
        self.env = Env(self)
        self.robot.reset()
        self.k = 0
        self.flag = False
        self.done = False
        self.state = 0
        self.reward = 0

        # QTable : contains the Q-Values for every (state,action) pair
        self.qtable = np.random.rand(self.env.stateCount, self.env.actionCount).tolist()

        # hyperparameters
        self.epochs = 5
        self.gamma = 0.1
        self.epsilon = 0.08
        self.decay = 0.1

    def next_episode(self): # End of one episode
        return self.done
    
    def stop(self): # End of learning
        return self.k > self.epochs
    
    def update(self):
        if self.stop():
            print ('GAME OVER')
            return
          
        if self.next_episode():
            print ('EPISODE OVER')
            self.state, self.reward, self.done = self.env.reset()
            self.env.dist_value = 1000
            print ('AAA '+ str(self.env.dist_value))
            print ('BBB '+ str(self.robot.get_dist()))
        
        if np.random.uniform() < self.epsilon:
            action = self.env.randomAction()
        else:
            action = self.qtable[self.state].index(max(self.qtable[self.state]))
           
        next_state, self.reward, self.done = self.env.step(action) # take action
        self.qtable[self.state][action] = self.reward + self.gamma * max(self.qtable[next_state]) # update qtable 
        self.state = next_state  # update state

        # The more we learn, the less we take random actions
        self.epsilon -= self.decay*self.epsilon

