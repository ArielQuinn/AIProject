import math

# This class will be used as the base building block of the Neural Network.
class Neuron:
    # This initializes the neuron
    #   Feature vector: a vector of inputs. Each entry should be between 0 and 1. 
    #   Feature Weights: these are simply the weights that the neural netowrk
    #       will be tuning.
    def __init__(self, featureWeights, bias):
        self.featureWeights = featureWeights
        self.bias = bias
        self.learningRate = 0.7
    
    # This basically determines how strongly the sigmoid neuron will output
    # its beliefs
    def produceOutput(self, featureVector):
        inputValue = sum([feature*weight for feature, weight in zip(featureVector, self.featureWeights)])
        v = 1/(1+math.exp(-inputValue - self.bias))
        return v
