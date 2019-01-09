const Neuron = require("./Neuron");

class Brain {
  constructor(numberOfLayers, neuronsPerLayer, numberOfInputs) {
    this.currentBatch = 0;
    this.layers = [];

    const inputNeurons = [];
    for (let i = 0; i < numberOfInputs; i++) {
      inputNeurons.push(new Neuron([]));
    }

    this.layers.push(inputNeurons);
    for (let i = 0; i < numberOfLayers; i++) {
      const layerNeurons = [];
      for (let j = 0; j < neuronsPerLayer; j++) {
        layerNeurons.push(new Neuron(this.layers[i]));
      }
      this.layers.push(layerNeurons);
    }

    const outputNeurons = [];
    for (let i = 0; i < 10; i++) {
      outputNeurons.push(new Neuron(this.layers[this.layers.length - 1]));
    }
    this.layers.push(outputNeurons);
  }

  setInputActivations(inputs) {
    this.layers[0].forEach((e, i) => {
      e.activation = inputs[i];
    });
  }

  calculateOutput() {
    for (let i = 1; i < this.layers.length - 1; i++) {
      for (let neuron in this.layers[i]) {
        this.layers[i][neuron].calculateActivation();
      }
    }

    for (let neuron in this.layers[this.layers.length - 1]) {
      this.layers[this.layers.length - 1][
        neuron
      ].calculateActivationWithoutBias();
      console.log(
        neuron,
        "digit",
        this.layers[this.layers.length - 1][neuron].getActivationSigmoid()
      );
    }
  }

  calculateCost(expectedOutput) {
    const lastLayer = this.layers[this.layers.length - 1];
    let cost = 0;

    for (let i = 0; i < expectedOutput.length; i++) {
      cost += Math.pow(
        expectedOutput[i] - lastLayer[i].getActivationSigmoid(),
        2
      );
    }

    return cost;
  }

  train(expectedOutput, batchSize) {
    this.applyBackwardsPropagation(expectedOutput);
    if (this.currentBatch === batchSize) {
      this.applyGradients(batchSize);
      this.currentBatch = 0;
    } else {
      this.currentBatch++;
    }
  }

  calculateGradientNeuron(neuron, currentLayer, expectedOutput) {
    const neuronObj = this.layers[currentLayer][neuron];
    // calculate neuron relation to cost
    if (currentLayer === this.layers.length - 1) {
      // last layer
      neuronObj.relationToCost =
        2 * (neuronObj.getActivationSigmoid() - expectedOutput); // derivative of cost function
    } else {
      //neuronObj.relationToCost = this.layers[currentLayer + 1]
      //  .map(it => it.synapses[neuron].gradient)
      //  .reduce((a, b) => a + b);
      neuronObj.relationToCost = this.layers[currentLayer + 1]
        .map(
          it =>
            it.relationToCost *
            it.synapses[neuron].weight *
            it.getActivationSigmoid() *
            (1 - it.getActivationSigmoid())
        )
        .reduce((a, b) => a + b);
    }

    neuronObj.biasGradient +=
      neuronObj.getActivationSigmoid() *
      (1 - neuronObj.getActivationSigmoid()) *
      neuronObj.relationToCost;

    for (let synapse in neuronObj.synapses) {
      const gradient =
        neuronObj.synapses[synapse].parentNeuron.getActivationSigmoid() *
        neuronObj.getActivationSigmoid() *
        (1 - neuronObj.getActivationSigmoid()) *
        neuronObj.relationToCost;

      neuronObj.synapses[synapse].gradient += gradient;
    }

    return neuronObj;
  }

  applyBackwardsPropagation(expectedOutput, layer = this.layers.length - 1) {
    if (layer === 0) {
      return;
    }
    for (let i = 0; i < this.layers[layer].length; i++) {
      this.layers[layer][i] = this.calculateGradientNeuron(
        i,
        layer,
        expectedOutput[i]
      );
    }
    this.applyBackwardsPropagation(expectedOutput, layer - 1);
  }

  applyGradients(batchSize) {
    for (let layer in this.layers) {
      for (let neuron in this.layers[layer]) {
        this.layers[layer][neuron].biasGradient =
          this.layers[layer][neuron].biasGradient / batchSize;
        this.layers[layer][neuron].applyGradient();
        for (let synapse in this.layers[layer][neuron].synapses) {
          this.layers[layer][neuron].synapses[synapse].gradient =
            this.layers[layer][neuron].synapses[synapse].gradient / batchSize;
          this.layers[layer][neuron].synapses[synapse].applyGradient();
        }
      }
    }
  }
}

module.exports = Brain;
