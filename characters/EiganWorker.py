import EiganVector as ev
import createMatrix as mm
import numpy as np
import os
import gc
def unitVector(vector):
    return np.divide(vector,np.linalg.norm(vector))

def doDot(eigan1, eigan2):
    #creates a 2D array of the relationship
    averageDot = []
    averageArray = []
    for first in eigan1:
        arrayOfTheta = []
        cAverage = 0
        unitfirstToCompare =unitVector(first)
        for second in eigan2:
                unitsecondToCompare =unitVector(second)
                try:
                    theta = (np.dot(unitfirstToCompare, unitsecondToCompare))
                except:
                    print "interesting"
                if(theta < 0):
                    theta *=-1
                cAverage+=theta
                arrayOfTheta.append(theta)
        cAverage = cAverage/len(eigan2)
        averageDot.append(cAverage)
        averageArray.append(arrayOfTheta)
    return averageDot,averageArray

def writeToFile(filename, array):
    target = open("Values/" + filename, "w")
    string = ""
    for k in range(len(array)):
        for r in array[k]:
            for b in r:
                string = string + str(b) + " - "
            string = string[:len(string)-3:] + "\n"
    target.write(string)

def getToCheck(filename):
    target = open(filename,'r')
    myCharIndex = ev.getmyCharsIndex()
    arrayOfCoordinates = mm.createDictionaryOfValues(target, myCharIndex)
    dic = []
    for key,val in arrayOfCoordinates.iteritems():
        dic.append([key[0],key[1],val])
    newar = [dic]#needs to be an aray to pass into turnIntoEigan
    ieganVec = ev.turnIntoEigan(newar,myCharIndex)
    return ieganVec

def original():
    files = os.listdir("Enron_collection")
    #dic = ev.createDictionary("Enron_collection")
    myCharIndex  = ev.getmyCharsIndex()
    files, array, myChar = mm.infoIntoDic("Enron_collection",myCharIndex)
    dic2 = ev.createDictionary("Enron_collection")
    eiganVectors = ev.turnIntoEigan(dic2)
    target = open("Original.txt","w")
    for l in eiganVectors:
        strs = ""
        for k in l:
            strs += str(k.real) + " - "
        strs[:len(strs)-3:]
        target.write(strs + "\n")
        strs = ""

def tester():
    files = os.listdir("Enron_collection")
    #dic = ev.createDictionary("Enron_collection")
    myCharIndex  = ev.getmyCharsIndex()
    files, array, myChar = mm.infoIntoDic("testing",myCharIndex)
    dic2 = ev.createDictionary("testing")
    eiganVectors = ev.turnIntoEigan(dic2)
    target = open("testing.txt","w")
    for l in eiganVectors:
        strs = ""
        for k in l:
            strs += str(k.real) + " - "
        strs[:len(strs)-3:]
        target.write(strs + "\n")
        strs = ""

if __name__ == "__main__":
    tester()
    """
        this might seem a little weird, as I change this code whenever I run it to test it,
        this way I save time as I dont need to recreate the enron matrixes and eigan vectors many times
        I was also getting an error where if I pass something into the lin.eigs function I would get two different answers, that are quite different
        This has been fixed by my rerunning the program twice, which also happens to save time with multiple tests which is good.
    """

