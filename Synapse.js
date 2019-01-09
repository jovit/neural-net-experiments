const LEARNING_RATE = 1/1;

class Synapse {
  constructor(parentNeuron) {
    this.weight = (Math.random()) * (Math.random() < 0.5 ? -1 : 1);
    this.parentNeuron = parentNeuron;
    this.gradient = 0;
  }

  getWeightedValue() {
    if (this.parentNeuron.synapses.length > 0)
      return this.weight * this.parentNeuron.getActivationSigmoid();
    else {
      return this.weight * this.parentNeuron.activation;
    }
  }

  applyGradient() {
    this.weight -= this.gradient * LEARNING_RATE;
    this.gradient = 0;
  }
}

module.exports = Synapse;
