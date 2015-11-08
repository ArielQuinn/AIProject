# This should take in all the data in each of the programs. It should count each
# of the types of words and it should determine which ones are special. Keep
# a per program average
import os.path
import re
import math

class FeatureGenerator:
    def __init__(self):
        self.trainingPath = os.path.join('..', 'Competition', 'benchmarks')
        self.wordReferences = dict()
        self.numberOfCategores = 7 # just a guess
        self.trainingData = os.path.join('..', 'Competition', 'SyGuS-COMP15-results.csv')
        self.benchmarksData = self.getBenchmarks()
        self.totalNumberOfWords = [0.0]*self.numberOfCategores
        self.features = self.mineData()

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

    def testLayer1InitialValues(self):
        folderIndex = 0
        totalRuns = 0.0
        correct = 0.0
        avgCorrect = 0.0
        for folder, subs, files in os.walk(self.trainingPath):
            if folder == self.trainingPath:
                continue
            for fileName in files:
                if fileName.endswith(".sl"):
                    program = open(os.path.join(folder, fileName), 'rb')
                    zValues = self.classify(program)
                    isCorrect = (zValues.index(max(zValues)) == folderIndex)
                    correct += isCorrect
                    if isCorrect:
                        avgCorrect += max(zValues)
                    print(str(max(zValues))+" "+str(zValues.index(max(zValues)) == folderIndex)
)
                    totalRuns += 1
            folderIndex += 1
        print(correct/totalRuns)
        print(avgCorrect/correct)
         
    def classifyLayer2(self, z):
        

    # wordReferences is our initial feature weight
    def classify(self, program):
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
        z = [0]*self.numberOfCategores
        for key in progDict:
            uses = self.wordReferences[key]
            for i in range(self.numberOfCategores):
                z[i] += uses[i]*progDict[key]/wordCount
        return sigmoid(z)

    def sigmoid(self, z, bias):
        return [1/(1+math.exp(bias - zval)) for zval in z]
    
    # This mines the data in a training path and categorizes it into features.
    def mineData(self):
        categoryIndex = 0
        for folder, subs, files in os.walk(self.trainingPath):
            if folder == self.trainingPath:
                continue
            for fileName in files:
                if fileName.endswith(".sl"):
                    program = open(os.path.join(folder, fileName), 'rb')
                    self.mineProgram(program, categoryIndex)
            categoryIndex += 1
        features = []
        for key in self.wordReferences:
            totalRefs = sum(self.wordReferences[key])
            self.wordReferences[key] = [WR/totalRefs for WR in self.wordReferences[key]]
            features.append((totalRefs, self.wordReferences[key]))
        return features

    # Given a file handle, this pulls out relevant data points
    # It skips commented lines (starting with ;)
    # It removes the parentheses
    # it splits on whitespace
    # Then it goes through each word and increments the apporpriate dictionary
    # entry.
    # for space efficiency, it also categorizes memory accesses as the same word
    def mineProgram(self, program, categoryIndex):
        for line in program:
            if(line[0] == ';'):
                continue
            line = re.sub('[()=]', ' ', line)
            line = line.split()
            # Now that we have access to each word, we categorize it.
            for word in line:
                if(word[0]=='#'):
                    word = "#x-----"
                self.wordReferences[word] = refArray = \
                        self.wordReferences.get(word, [0.0]*self.numberOfCategores)
                refArray[categoryIndex] += 1
                self.totalNumberOfWords[categoryIndex] += 1

    def _computeVariance(self, data):
        mean = sum(data)/len(data)
        for dataPoint in data:
            errorSquared = (dataPoint-mean)*(dataPoint-mean)
        return dataPoint/len(data)

class Entry:
    def __init__(self, line):
        self.benchmark = line[0].split('/')[-1]
        self.solver = line[1]
        self.status = line[2]
        self.cpuTime = line[3]
        self.wallClockTime = line[4]
        self.memoryUsage = line[5]
        self.result = line[6]
        self.exprsDetails = line[7]
        self.syntaxError = line[8]


f = FeatureGenerator()
f.testLayer1InitialValues() 
