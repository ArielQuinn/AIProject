# This should take in all the data in each of the programs. It should count each
# of the types of words and it should determine which ones are special. Keep
# a per program average
import os.path
import re
import numpy

class FeatureGenerator:
    def __init__(self):
        self.trainingPath = os.path.join('..', 'Competition', 'benchmarks')
        self.wordReferences = dict()
        self.numberOfCategores = 7 # just a guess
        self.totalNumberOfWords = [0.0]*self.numberOfCategores
        self.features = []
    
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
        for key in self.wordReferences:
            self.wordReferences[key] = [WR/nWR for WR, nWR in zip(self.wordReferences[key], self.totalNumberOfWords)]
            self.features.append((self._computeVariance(self.wordReferences[key]), key))
            print(self.features)

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

    def _computeVariance(self, data)
        mean = sum(data)/len(data)
        for dataPoint in data:
            errorSquared = (dataPoint-mean)*(dataPoint-mean)
        return datapoint/len(data)

f = FeatureGenerator()
f.mineData()
 
