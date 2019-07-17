import numpy as np
import time

class EnvQLearning:
    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.actions = [0, 1, 2, 3]  #speed values
        self.states = [0, 1, 2, 3, 4, 5]  #distance from the wall, 0 = far, 5 = close
        self.stateCount = len(self.states)
        self.actionCount = len(self.actions)
        self.done = False
        self.stop_count = 0
        
        # hyperparameters
        self.epochs = 15
        self.gamma = 0.1
        self.epsilon = 0.1
        self.decay = 0.05

        self.qtable = np.random.rand(self.stateCount, self.actionCount).tolist()

    def reset(self):
        time.sleep(0.5)
        print ('-----RESET-----')
        self.ctrl.robot.chassisNP.setPos(0, 0, 0)
        self.ctrl.robot.set_speed(0,0)
        self.done = False
        self.ctrl.k+=1
        self.ctrl.robot.sim.distance = 1000
        self.ctrl.robot.count = 1   # Speed factor
        self.stop_count = 0

        return 0, 0, False

    def step(self, action):
        
        self.dist_value = self.ctrl.robot.get_dist()
        print ('Distance is '+str(self.dist_value))
        if action==0: # Full speed
            print ('Full speed')
            self.ctrl.robot.set_speed(self.ctrl.speed, self.ctrl.speed)
        if action==1: # Half-speed
            print ('speed 0.8')
            self.ctrl.robot.set_speed(self.ctrl.speed*0.8, self.ctrl.speed*0.8)
        if action==2: # Quarter-speed
            print ('speed 0.5')
            self.ctrl.robot.set_speed(self.ctrl.speed*0.5, self.ctrl.speed*0.5)
        if action==3: # Stop
            print ('Full stop')
            self.ctrl.robot.set_speed(0, 0)

        # Reward table
        if self.dist_value == 60:
            reward = 5
        elif self.dist_value == 75:
            reward = 1
        elif self.dist_value == 90:
            reward = 0
        elif  120 >= self.dist_value >= 105:
            reward = 0
        elif self.dist_value == 45:
            reward = -100
        else:
            reward = -1
  
        # Choosing next state?..
        if self.dist_value == 60:
            nextState = 4
            self.stop_count +=1
            if self.stop_count>100:
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
        return np.random.choice(self.actions)

    def _update(self):
        if np.random.uniform() < self.epsilon:
            action = self.randomAction()
        else:
            action = self.qtable[self.ctrl.state].index(max(self.qtable[self.ctrl.state]))
           
        next_state, self.ctrl.reward, self.ctrl.done = self.step(action) # take action
        self.qtable[self.ctrl.state][action] = self.ctrl.reward + self.gamma * max(self.qtable[next_state]) # update qtable 
        self.ctrl.state = next_state  # update state

        self.epsilon -= self.decay*self.epsilon
        
