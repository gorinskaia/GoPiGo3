from numpy import exp, array, random, dot
import numpy


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

    def print_weights(self):
        print ("    Layer 1: ")
        print (self.layer1.weights)
        print ("    Layer 2: ")
        print (self.layer2.weights)


def normalize(arr):
    _res = arr
    for i in range(len(arr)):
        _res[i][0] = (arr[i][0] - min(arr))/(max (arr) - min(arr))
    return _res

if __name__ == "__main__":

    random.seed(1)
    
    # Create layer 1 (4 neurons, each with 1 inputs)
    layer1 = NeuronLayer(4, 1)

    # Create layer 2 (a single neuron with 4 inputs)
    layer2 = NeuronLayer(1, 4)

    neural_network = NeuralNetwork(layer1, layer2)

    training_set_inputs = array([[15.0],[45.0], [60.0], [90.0],[1000.0]])
    new_input = (80 - min(training_set_inputs))/(max (training_set_inputs) - min(training_set_inputs))
    
    training_set_inputs = normalize(training_set_inputs)

    training_set_outputs = array([[ 0, 0, 0, 0.8, 1]]).T

    neural_network.train(training_set_inputs, training_set_outputs, 10)

    print ("New weights after training: ")
    neural_network.print_weights()

    # Test the neural network with a new situation.
    print ("Considering a new situation: ")
    hidden_state, output = neural_network.forward(array([new_input]))
    
    print (output)
    _output = output*(max(training_set_outputs) - min(training_set_outputs)) + min(training_set_outputs)
    print (_output)


