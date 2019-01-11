from network import Neuron
from math import pow
from functools import reduce


class Brain:
    def __init__(self, number_of_layers, neurons_per_layer, number_of_inputs):
        self.current_batch = 0
        self.layers = []
        input_neurons = []
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
        for (neuron, input) in zip(self.layers[0], inputs):
            neuron.activation = input

    def calculate_output(self):
        for layer in self.layers:
            for neuron in layer:
                neuron.calculate_activation()

        for neuron in self.layers[-1]:
            neuron.calculate_activation_withoutBias()
            print(
                neuron,
                "digit",
                neuron.get_activation_sigmoid()
            )

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
                                                                         it.synapses[neuron].weight * it.get_activation_sigmoid() * (1 - it.get_activation_sigmoid()), self.layers[currentLayer + 1]))

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
        for i in range(self.layers[layer].length):
            self.layers[layer][i] = self.calculate_gradient_neuron(
                i,
                layer,
                expected_output[i]
            )
        self.apply_backwards_propagation(expected_output, layer - 1)

    def apply_gradients(self, batchSize):
        for layer in self.layers:
            for neuron in layer:
                neuron.biasGradient = neuron.biasGradient / batchSize
                neuron.applyGradient()
                for synapse in neuron.synapses:
                    synapse.gradient = synapse.gradient / batchSize
                    synapse.applyGradient()
