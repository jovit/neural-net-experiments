from network import Neuron
from math import pow


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
        for j in range(neuronsPerLayer):
            layer_neurons.append(Neuron(self.layers[i]))
        self.layers.append(layer_neurons)

    output_neurons = []
    for i in range(10):
        output_neurons.append(Neuron(self.layers[self.layers.length - 1]))
    self.layers.append(output_neurons)

  def set_input_activations(self, inputs):
      for (neuron, input) in zip(self.layers[0], inputs):
          neuron.activation = input

  def calculate_output(self):
    for layer in self.layers:
      for neuron in layer:
        neuron.calculate_activation()

    for neuron in self.layers[self.layers.length - 1]:
      neuron.calculate_activation_withoutBias();
      print(
        neuron,
        "digit",
        neuron.get_activation_sigmoid()
      )

  def calculate_cost(self, expected_output):
    last_layer = self.layers[self.layers.length - 1]
    cost = 0

    for i in range(expectedOutput.length):
      cost = cost + pow(
        expectedOutput[i] - lastLayer[i].get_activation_sigmoid(),
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

  def calculate_gradient_neuron(neuron, current_layer, expected_output) {
    neuron_obj = self.layers[currentLayer][neuron]

    if current_layer ==  self.layers.length - 1:
      // last layer
      neuron_obj.relation_to_cost =
        2 * (neuron_obj.get_activation_sigmoid() - expected_output)
    else:
      neuron_obj.relation_to_cost = self.layers[currentLayer + 1]
        .map(
          it=>
            it.relationToCost *
            it.synapses[neuron].weight *
            it.getActivationSigmoid() *
            (1 - it.getActivationSigmoid())
        )
        .reduce((a, b) = > a + b);}

    neuron_obj.biasGradient +=
      neuron_obj.getActivationSigmoid() *
      (1 - neuron_obj.getActivationSigmoid()) *
      neuron_obj.relationToCost;

    for (let synapse in neuron_obj.synapses) {
      const gradient =
        neuron_obj.synapses[synapse].parentNeuron.getActivationSigmoid() *
        neuron_obj.getActivationSigmoid() *
        (1 - neuron_obj.getActivationSigmoid()) *
        neuron_obj.relationToCost;

      neuron_obj.synapses[synapse].gradient += gradient; }

    return neuron_obj

  applyBackwardsPropagation(expectedOutput, layer=self.layers.length - 1) {
    if (layer == = 0) {
      return; }
    for (let i=0; i < self.layers[layer].length; i++) {
      self.layers[layer][i] = self.calculateGradientNeuron(
        i,
        layer,
        expectedOutput[i]
      ); }
    self.applyBackwardsPropagation(expectedOutput, layer - 1);}

  applyGradients(batchSize) {
    for (let layer in self.layers) {
      for (let neuron in self.layers[layer]) {
        self.layers[layer][neuron].biasGradient =
          self.layers[layer][neuron].biasGradient / batchSize;
        self.layers[layer][neuron].applyGradient();
        for (let synapse in self.layers[layer][neuron].synapses) {
          self.layers[layer][neuron].synapses[synapse].gradient =
            self.layers[layer][neuron].synapses[synapse].gradient / batchSize;
          self.layers[layer][neuron].synapses[synapse].applyGradient(); }
      }
    }
  }


}

module.exports = Brain;
