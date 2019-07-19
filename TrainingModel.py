import numpy as np
import time
from numpy import exp, array, random, dot

class EnvQLearning:
    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.actions = [0, 1, 2, 3]  #speed values
        self.states = [0, 1, 2, 3, 4, 5]  #distance from the wall, 0 = far, 5 = close
        self.stateCount = len(self.states)
        self.actionCount = len(self.actions)
        self.stop_count = 0
        
        # hyperparameters
        self.epochs = 15
        self.gamma = 0.1
        self.epsilon = 0.01
        self.decay = 0.1

        self.state = 0
        self.reward = 0

        self.qtable = np.random.rand(self.stateCount, self.actionCount).tolist()

    def _reset(self):
        time.sleep(0.5)
        print ('-----RESET-----')
        self.ctrl.robot.chassisNP.setPos(0, 0, 0)
        self.ctrl.robot.set_speed(0,0)
        self.ctrl.k+=1
        self.ctrl.robot.sim.distance = 1000
        self.ctrl.robot.count = 1   # Speed factor
        self.stop_count = 0
        self.epsilon -= self.decay*self.epsilon

        return 0, 0, False

    def step(self, action):
        done = False
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
                done = True
        elif self.dist_value == 75:
            nextState = 3
        elif self.dist_value == 90:
            nextState = 2
        elif self.dist_value == 105:
            nextState = 1
        elif self.dist_value == 45:
            nextState = 5
            done = True
        else: 
            nextState = 0

        return nextState, reward, done

    def randomAction(self):
        return np.random.choice(self.actions)

    def _update(self):
        if np.random.uniform() < self.epsilon:
            action = self.randomAction()
        else:
            action = self.qtable[self.state].index(max(self.qtable[self.state]))
           
        next_state, self.reward, self.ctrl.end_episode = self.step(action) # take action
        self.qtable[self.state][action] = self.reward + self.gamma * max(self.qtable[next_state]) # update qtable 
        self.state = next_state  # update state


####
class NeuronLayer():
    def __init__(self, number_of_neurons, number_of_inputs_per_neuron):
        self.weights = 2 * random.random((number_of_inputs_per_neuron, number_of_neurons)) - 1

class NeuralNetwork():
    def __init__(self, layer1, layer2):
        self.layer1 = layer1
        self.layer2 = layer2

    def __sigmoid(self, x): #normalize 1-0
        return 1 / (1 + exp(-x))

    def __sigmoid_derivative(self, x): #gradient
        return x * (1 - x)

    def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
        for iteration in range(number_of_training_iterations):

            output_layer_1, output_layer_2 = self.forward(training_set_inputs)

            layer2_error = training_set_outputs - output_layer_2
            layer2_delta = layer2_error * self.__sigmoid_derivative(output_layer_2)

            layer1_error = layer2_delta.dot(self.layer2.weights.T)
            layer1_delta = layer1_error * self.__sigmoid_derivative(output_layer_1)

            layer1_adjustment = training_set_inputs.T.dot(layer1_delta)
            layer2_adjustment = output_layer_1.T.dot(layer2_delta)

            self.layer1.weights += layer1_adjustment
            self.layer2.weights += layer2_adjustment

    def forward(self, inputs):
        output_layer1 = self.__sigmoid(dot(inputs, self.layer1.weights))
        output_layer2 = self.__sigmoid(dot(output_layer1, self.layer2.weights))
        return output_layer1, output_layer2

        
class EnvNN:
    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.epochs = 200
        self.ctrl.robot.sim.distance = 1000

    def train(self):
        layer1 = NeuronLayer(4, 1) # 4 neurons, 1 input
        layer2 = NeuronLayer(1, 4) # output

        self.neural_network = NeuralNetwork(layer1, layer2)
        training_set_inputs = array([[15.0],[45.0], [65.0], [75.0], [90.0], [135.0],[1000.0]])
 
        training_set_inputs = self.normalize(training_set_inputs)
        training_set_outputs = array([[ 0, 0, 0, 0.5, 0.8, 1, 1]]).T
        
        self.neural_network.train(training_set_inputs, training_set_outputs, 40000)

    def normalize(self, arr):
        _res = arr
        for i in range(len(arr)):
            _res[i][0] = (arr[i][0] - min(arr))/(max (arr) - min(arr))
        return _res

    def calculate_speed(self, dist_value):
        new_input = (dist_value - 15.0)/(1000.0 - 15.0)
        hidden_state, output = self.neural_network.forward(array([new_input]))
        print (output[0])
        if output[0]<0.1:
            self.ctrl.k+=1
        return (output[0])

    def _update(self):
        dist_value = self.ctrl.robot.get_dist()
        new_speed = self.calculate_speed(dist_value)
        self.ctrl.robot.set_speed(self.ctrl.speed*new_speed, self.ctrl.speed*new_speed)
