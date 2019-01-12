from random import random

LEARNING_RATE = 1/10


class Synapse:
    def __init__(self, parent_neuron):
        self.weight = (random() * (-1 if random() < 0.5 else 1))
        self.parent_neuron = parent_neuron
        self.gradient = 0

    def get_weighted_value(self):
        return self.weight * self.parent_neuron.get_activation_sigmoid()

    def applyGradient(self):
        self.weight = self.weight - (self.gradient * LEARNING_RATE)
        self.gradient = 0
