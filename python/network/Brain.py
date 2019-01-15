from typing import Dict, List
from network import Neuron
from math import pow
from functools import reduce


class Brain:
    def __init__(self, number_of_layers: int, neurons_per_layer: int, number_of_inputs: int):
        self.current_batch: int = 0
        self.layers: List[List[Neuron]] = []
        input_neurons: List[Neuron] = []
        for i in range(number_of_inputs):
            input_neurons.append(Neuron([]))

        self.layers.append(input_neurons)

        for i in range(number_of_layers):
            layer_neurons = []
            for j in range(neurons_per_layer):
                layer_neurons.append(Neuron(self.layers[i]))
            self.layers.append(layer_neurons)

        output_neurons = []
        for i in range(10):
            output_neurons.append(Neuron(self.layers[-1]))
        self.layers.append(output_neurons)

    def set_input_activations(self, inputs):
        for i in range(len(self.layers[0])):
            self.layers[0][i].activation = inputs[i]

    def calculate_output(self):
        for layer in self.layers:
            for neuron in layer:
                neuron.calculate_activation()

        for neuron in self.layers[-1]:
            neuron.calculate_activation_without_bias()

        max_activation = 0
        max_index = 0
        for i in range(10):
            if self.layers[-1][i].get_activation_sigmoid() > max_activation:
                max_activation = self.layers[-1][i].get_activation_sigmoid()
                max_index = i

        return max_index

    def calculate_cost(self, expected_output):
        last_layer = self.layers[-1]
        cost = 0

        for i in range(len(expected_output)):
            cost = cost + pow(
                expected_output[i] - last_layer[i].get_activation_sigmoid(),
                2
            )

        return cost

    def train(self, expected_output, batch_size):
        self.apply_backwards_propagation(expected_output)
        if self.current_batch == batch_size:
            self.apply_gradients(batch_size)
            self.current_batch = 0
        else:
            self.current_batch += 1

    def calculate_gradient_neuron(self, neuron, current_layer, expected_output):
        neuron_obj = self.layers[current_layer][neuron]

        if current_layer == len(self.layers) - 1:
            neuron_obj.relation_to_cost = 2 * \
                (neuron_obj.get_activation_sigmoid() - expected_output)
        else:
            neuron_obj.relation_to_cost = reduce(lambda a, b: a + b, map(lambda it: it.relationToCost *
                                                                         it.synapses[neuron].weight * it.get_activation_sigmoid() * (1 - it.get_activation_sigmoid()), self.layers[current_layer + 1]))

        neuron_obj.bias_gradient = neuron_obj.bias_gradient + neuron_obj.get_activation_sigmoid() * \
            (1 - neuron_obj.get_activation_sigmoid()
             ) * neuron_obj.relation_to_cost

        for synapse in neuron_obj.synapses:
            gradient = synapse.parent_neuron.get_activation_sigmoid() * neuron_obj.get_activation_sigmoid() * \
                (1 - neuron_obj.get_activation_sigmoid()
                 ) * neuron_obj.relation_to_cost

            synapse.gradient += gradient

        return neuron_obj

    def apply_backwards_propagation(self, expected_output, layer=None):
        if layer is None:
            layer = len(self.layers) - 1
        if layer == 0:
            return
        for i in range(len(self.layers[layer])):
            if layer == len(self.layers) - 1:
                self.layers[layer][i] = self.calculate_gradient_neuron(
                    i,
                    layer,
                    expected_output[i]
                )
            else:
                self.layers[layer][i] = self.calculate_gradient_neuron(
                    i,
                    layer,
                    None
                )
        self.apply_backwards_propagation(expected_output, layer - 1)

    def apply_gradients(self, batch_size):
        for layer in self.layers:
            for neuron in layer:
                neuron.bias_gradient = neuron.bias_gradient / batch_size
                neuron.apply_gradient()
                for synapse in neuron.synapses:
                    synapse.gradient = synapse.gradient / batch_size
                    synapse.applyGradient()
