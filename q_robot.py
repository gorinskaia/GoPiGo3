import numpy as np
import time
import os


class Env():
    def __init__(self):
        self.actions = [0, 1, 2, 3]  #speed values
        self.states = [0, 1, 2, 3, 4] #distance from the wall
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
    
        nextState = ???

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


# create environment
env = Env()

# QTable : contains the Q-Values for every (state,action) pair
qtable = np.random.rand(env.stateCount, env.actionCount).tolist()

# hyperparameters
epochs = 60
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

