from random import random
from network import Synapse
from math import exp

LEARNING_RATE = 1/1


class Neuron:
    def __init__(self, connected_neurons):
        self.activation = 0
        self.synapses = []
        self.relationToCost = 0
        self.bias = random() * 10 * (-1 if random() < 0.5 else 1)
        self.bias_gradient = 0

        for neuron in connected_neurons:
            self.synapses.append(Synapse(neuron))

    def calculate_activation(self):
        self.activation = self.bias
        for synapse in self.synapses:
            self.activation += synapse.get_weighted_value()

    def calculate_activation_without_bias(self):
        self.activation = 0
        for synapse in self.synapses:
            self.activation = self.activation + \
                synapse.get_weighted_value()

    def get_activation_rectified(self):
        return max(self.activation, 0)

    def get_activation_sigmoid(self):
        return 1 / (1 + exp(-self.activation))

    def apply_gradient(self):
        self.bias = self.bias - self.bias_gradient * LEARNING_RATE
        self.bias_gradient = 0
