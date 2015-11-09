# This should take in all the data in each of the programs. It should count each
# of the types of words and it should determine which ones are special. Keep
# a per program average
import os.path
import re
import math
import sys

class FeatureGenerator:
    def __init__(self):
        # Training Data
        self.numberOfCategories = 7
        self.numberOfSolvers = 7
        self.trainingPath = os.path.join('..', 'Competition', 'benchmarks')
        self.trainingData = os.path.join('..', 'Competition', 'SyGuS-COMP15-results.csv')
        self.benchmarksData = self._getBenchmarks()

        # Sets up initial structure for Layer 1
        # Note that there is 1 bias per category. Hence, we have that number of biases
        self.layer1Biases = [0.0]*self.numberOfCategories
        # Note that there is one feature weight per feature per category. Hence we have
        # features*categories weights
        self.layer1Features = dict()
        # This just populates the above two listed features
        self.populateLayer1InitialValues()
        
        # Sets up initial structure for Layer 2
        self.layer2Biases = [0]*self.numberOfSolvers
        self.layer2FeatureWeights = dict()
        #self.layer2FeatureWeights = [[0]*self.numberOfSolvers]*self.numberOfCategories
        self.populateLayer2InitialValues()
        self.populateLayer2Biases()
        
    def populateLayer2InitialValues(self):
        folderIndex = 0
        benchmarksEvaluated = 0
        for folder, subs, files in os.walk(self.trainingPath):
            if folder == self.trainingPath:
                continue
            for fileName in files:
                if fileName.endswith(".sl"):
                    if(fileName not in self.benchmarksData):
                        continue;
                    benchmarkData = self.benchmarksData[fileName]
                    minTimeToCompletion = sys.maxint
                    for entry in benchmarkData:
                        if(entry.result == "correct") and entry.wallClockTime < minTimeToCompletion:
                            minTimeToCompletion = entry.wallClockTime
                    # If somebody solved it, we need to adjust our feature weights
                    if(minTimeToCompletion != sys.maxint):
                        benchmarksEvaluated += 1
                        for entry in benchmarkData:
                            featureWeights = self.layer2FeatureWeights.get(entry.solver, [0.0]*self.numberOfCategories)
                            if(entry.result == "correct"):
                                featureWeights[folderIndex] += minTimeToCompletion/entry.wallClockTime
                            self.layer2FeatureWeights[entry.solver] = featureWeights
            folderIndex += 1

    def getLayer2z(self, program):
        features = self.getLayer1Output(program)
        labels = []
        z = []
        for key in self.layer2FeatureWeights:
            labels.append(key)
            z.append(sum([f*w for f, w in zip(features, self.layer2FeatureWeights[key])]))
        # z represents the outputs of the neurons. labels represents the label of the neuron
        return zip(z, labels)
        # Each of these keys represents a single neuron
            
    def populateLayer2Biases(self):
        folderIndex = 0
        totalRuns = 0.0
        correct = 0.0
        avgCorrect = 0.0
        correctPerCategory = [0.0]*self.numberOfCategories
        totalPerCategory = [0.0]*self.numberOfCategories
        for folder, subs, files in os.walk(self.trainingPath):
            if folder == self.trainingPath:
                continue
            for fileName in files:
                if fileName.endswith(".sl"):
                    if(fileName not in self.benchmarksData):
                        continue
                    program = open(os.path.join(folder, fileName), 'rb')
                    # First, get the min solver
                    minTimeToCompletion = sys.maxint
                    minSolver = None
                    for entry in self.benchmarksData[fileName]:
                        if(entry.result == "correct") and entry.wallClockTime < minTimeToCompletion:
                            minTimeToCompletion = entry.wallClockTime
                            minSolver = entry.solver
                    if(minSolver == None):
                        continue
                    zVal, solver = sorted(self.getLayer2z(program), reverse=True)[0]
                    if solver==minSolver:
                        correct += 1
                    totalRuns += 1
                    #print(self.getLayer2z(program))
        print("hits:")
        print(correct/totalRuns)
                    
                    
    def getLayer1Output(self, program):
        z = self.layer1z(program)
        return self._sigmoid(z, self.layer1Biases)

    # wordReferences is our initial feature weight
    def layer1z(self, program):
        progDict = dict()
        wordCount = 0
        for line in program:
            if(line[0] == ';'):
                continue
            line = re.sub('[()=]', ' ', line)
            line = line.split()
            # Now that we have access to each word, we categorize it.
            for word in line:
                if(word[0]=='#'):
                    word = "#x-----"
                progDict[word] = progDict.get(word, 1.0)
                wordCount += 1
        # Now we calculate the Z values of layer 1:
        z = [0]*self.numberOfCategories
        for key in progDict:
            uses = self.layer1Features[key]
            for i in range(self.numberOfCategories):
                z[i] += uses[i]*progDict[key]/wordCount
        return z

    # This mines the data in a training path and categorizes it into features.
    # It populates the biases. There should be 1 bias per neuron.
    # It populates the weights. There sould be 1 weight per feature per neuron.
    # biases = self.layer1Biases
    # features = self.layer1Features
    def populateLayer1InitialValues(self):
        categoryIndex = 0
        for folder, subs, files in os.walk(self.trainingPath):
            if folder == self.trainingPath:
                continue
            for fileName in files:
                if fileName.endswith(".sl"):
                    program = open(os.path.join(folder, fileName), 'rb')
                    self.populateLayer1Features(program, categoryIndex)
            categoryIndex += 1
        for key in self.layer1Features:
            totalRefs = sum(self.layer1Features[key])
            self.layer1Features[key] = [WR/totalRefs for WR in self.layer1Features[key]]
        self.layer1Biases = [self.getLayer1Biases()]*self.numberOfCategories

    # This function gets the biases of the features
    def getLayer1Biases(self):
        folderIndex = 0
        totalRuns = 0.0
        correct = 0.0
        avgCorrect = 0.0
        avg = 0.0
        correctPerCategory = [0.0]*self.numberOfCategories
        totalPerCategory = [0.0]*self.numberOfCategories
        for folder, subs, files in os.walk(self.trainingPath):
            if folder == self.trainingPath:
                continue
            for fileName in files:
                if fileName.endswith(".sl"):
                    program = open(os.path.join(folder, fileName), 'rb')
                    zValues = self.layer1z(program)
                    isCorrect = (zValues.index(max(zValues)) == folderIndex)
                    correct += isCorrect
                    totalPerCategory[folderIndex] += 1
                    avg += max(zValues)
                    if isCorrect:
                        avgCorrect += max(zValues)
                        correctPerCategory[folderIndex] += 1
#                    print(zValues)
#                    print(str(max(zValues))+" "+str(zValues.index(max(zValues)) == folderIndex)

                    totalRuns += 1
            folderIndex += 1
#        print(correct/totalRuns)
#        print(avgCorrect/correct)
#        print("Correctness per category")
#        print([c/t for c, t in zip(correctPerCategory, totalPerCategory)])
        # This gives us our bias:
        return avg/totalRuns
         
    # Given a file handle, this pulls out relevant data points
    # It skips commented lines (starting with ;)
    # It removes the parentheses
    # it splits on whitespace
    # Then it goes through each word and increments the apporpriate dictionary
    # entry.
    # for space efficiency, it also categorizes memory accesses as the same word
    def populateLayer1Features(self, program, categoryIndex):
        for line in program:
            if(line[0] == ';'):
                continue
            line = re.sub('[()=]', ' ', line)
            line = line.split()
            # Now that we have access to each word, we categorize it.
            for word in line:
                if(word[0]=='#'):
                    word = "#x-----"
                self.layer1Features[word] = refArray = \
                        self.layer1Features.get(word, [0.0]*self.numberOfCategories)
                refArray[categoryIndex] += 1

    # Gets the benchmarks and stores them in a dictionary
    def _getBenchmarks(self):
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



    def _computeVariance(self, data):
        mean = sum(data)/len(data)
        for dataPoint in data:
            errorSquared = (dataPoint-mean)*(dataPoint-mean)
        return dataPoint/len(data)

    def _sigmoid(self, z, biases):
        #print("Bias"+" "+str([bias-zval for bias,zval in zip(biases, z)]))
        print(str([bias-zval<0 for bias,zval in zip(biases, z)]))
        return [1/(1+math.exp((bias - zval))*100) for bias, zval in zip(biases, z)]
    


class Entry:
    def __init__(self, line):
        self.benchmark = line[0].split('/')[-1]
        self.solver = line[1]
        self.status = line[2]
        self.cpuTime = line[3]
        self.wallClockTime = float(line[4])
        self.memoryUsage = line[5]
        self.result = line[6]
        self.exprsDetails = line[7]
        self.syntaxError = line[8]


f = FeatureGenerator()
