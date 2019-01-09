const Synapse = require("./Synapse");

const LEARNING_RATE = 1/1 ;

class Neuron {
  constructor(connectedNeurons) {
    this.activation = 0;
    this.synapses = [];
    this.relationToCost = 0;
    this.bias = Math.random() * 10 * (Math.random() < 0.5 ? -1 : 1);
    this.biasGradient = 0;

    for (let i = 0; i < connectedNeurons.length; i++) {
      this.synapses.push(new Synapse(connectedNeurons[i]));
    }
  }

  calculateActivation() {
    this.activation = this.bias;
    for (let synapse in this.synapses) {
      this.activation += this.synapses[synapse].getWeightedValue();
    }
  }

  calculateActivationWithoutBias() {
    this.activation = 0;
    for (let synapse in this.synapses) {
      this.activation += this.synapses[synapse].getWeightedValue();
    }
  }


  getActivationRectified() {
    return Math.max(this.activation, 0);
  }

  getActivationSigmoid() {
    return 1 / (1 + Math.exp(-this.activation));
  }

  applyGradient() {
    this.bias -= this.biasGradient * LEARNING_RATE;
    this.biasGradient = 0;
  }
}

module.exports = Neuron;
