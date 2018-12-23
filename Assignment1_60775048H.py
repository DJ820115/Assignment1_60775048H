import numpy as np
import pandas as pd
import operator

def loadDataSet():

    dataSet = pd.read_csv('C:/Users/daniel/Downloads/simple test data 2.csv', delimiter=',')
    labelSet = list(dataSet.columns.values)
    dataSet = dataSet.values
    return dataSet, labelSet

def calcShannonEnt(dataSet):

    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
    
        currentLabel = featVec[-1]
        
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob*np.log2(prob)
    return shannonEnt

def splitDataSet(dataSet, axis, value):

    retDataSet = []
    for featVec in dataSet:
    
        if featVec[axis] == value:
            reducedFeatVec = list(featVec[:axis])
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeature(dataSet):

   
    numFeature = len(dataSet[0])-1
    baseEntroy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeature):
       
        featureList = [example[i] for example in dataSet]
      
        uniqueVals = set(featureList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
           
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * np.log2(prob)
        inforGain = baseEntroy - newEntropy

        if inforGain > bestInfoGain:
            bestInfoGain = inforGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):

    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount += 1
  
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
  
    return sortedClassCount[0][0]

def createTree(dataSet, labels):

    classList = [example[-1] for example in dataSet]
   
    if classList.count(classList[0]) == len(classList):
        return classList[0]
   
    if (len(dataSet[0]) == 1):
        return majorityCnt(classList)


    bestFeat = chooseBestFeature(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
 
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
      
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree


if __name__ == '__main__':
    dataSet, labelSet = loadDataSet()
    shannonEnt = calcShannonEnt(dataSet)
    tree= createTree(dataSet, labelSet)
    print (tree)


