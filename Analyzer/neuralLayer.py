# This class represents the fully function neural network.

from neuron import *

class NeuralLayer:
    def __init__(self, neuronCount):
        # This will be a matrix of methods.
        # The row will signify for which node the method is intended as input
        # The number of rows will signify the number of nodes in the first layer.
        self.neurons = [Neuron([.5], .5) for i in range(neuronCount)]

    # This takes the inputs and allocates them to the appropriate outputs.
    def generateOutputs(self, inputs):
        outputs = [None]*len(inputs)
        for i in xrange(len(inputs)):
            inputVector = inputs[i]
            outputs[i] = self.neurons[i].produceOutput(inputVector)
        return outputs

