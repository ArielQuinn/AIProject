# This is the first implementation of the SuperSynthesizer.
# For the first attempt, all the nodes will have a clear meaning.
# The first layer nodes will be defined as the category.
# The second layer nodes will be defined as the synthesizer of choice

from neuralLayer import *
import os.path

class MultilayerPerceptron:
    # len(networkDimensions) = number of layers
    # networkDimensions[i] = number of nodes at layer i
    def __init__(self, inputMethods, networkDimensions):
        self.inputMethods = inputMethods
        self.layers = [NeuralLayer(dim) for dim in networkDimensions]
        self.trainingData = os.path.join('..', 'Competition', 'SyGuS-COMP15-results.csv')
        self.benchmarks = self.getBenchmarks()

    # This uses backward propagation to train the neural network
    # Suppose our cost function is 1/2*sum(err)^2
    # where err = desired output - real output
    def train(self, examplesPath):
        # Open all the files in the path of interest
        
        for example in examples:
            layer0Outputs = self.layers[0].generateOutputs(layer0Outputs)
            layer1Outputs = self.layers[1].generateOutputs([layer0Outputs]*3)
            trueOutputs = self.getTrueOutputs(example)

    def getTrueOutputs(self, example)
        

    def getBenchmarks(self):
        trueOutputs = open(self.trainingData, 'rb')
        trueOutputs.readline()

        benchmarkIndex = 0
        # Now we want to make a dictionary that stores entries associated with the
        # benchmark as the key
        benchmarks = dict()
        for entry in trueOutputs:
            entry = entry.split(',')
            entry = Entry(entry)
            benchmarks[entry.benchmark] = benchmarkArray = benchmarks.get(entry.benchmark,[])
            benchmarkArray.append(entry)
        return benchmarks

    # The following method creates the layer 1 inputs using the method matrix:
    def getLayer0Inputs(self, rawInput):
        layerInputs = [None]*len(self.inputMethods)
        for j in xrange(len(self.inputMethods)):
            nodeInputMethods = self.inputMethods[j]
            nodeInputs = [None]*len(nodeInputMethods)
            for i in range(len(nodeInputMethods)):
                inputMethod = nodeInputMethods[i]
                nodeInputs[i] = inputMethod(rawInput)
            layerInputs[j] = nodeInputs
        return layerInputs

    # This function gets the input from the previous layers and passes it on
    # to the next layers.
    def getPredictions(self, rawInput):
        layer0Inputs = self.getLayer0Inputs(rawInput)
        layer0Outputs = self.layers[0].generateOutputs(layer0Inputs)
        print([layer0Outputs]*3)
        return self.layers[1].generateOutputs([layer0Outputs]*3)

class Entry:
    def __init__(self, line):
        self.benchmark = line[0]
        self.solver = line[1]
        self.status = line[2]
        self.cpuTime = line[3]
        self.wallClockTime = line[4]
        self.memoryUsage = line[5]
        self.result = line[6]
        self.exprsDetails = line[7]
        self.syntaxError = line[8]

def method1(rawInput):
    return float(.8)

def method2(rawInput):
    return float(.2)

methodArray=[method1]
methodArray2 = [method2]
dMethodArray = [methodArray, methodArray2]
p = MultilayerPerceptron(dMethodArray, [2, 4])
print(p.getPredictions(5))
