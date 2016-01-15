import os
import sys
from scipy.sparse import csr_matrix
import scipy.sparse.linalg as lin
import numpy as np
import shutil

def unitVector(vector):
    return np.divide(vector,np.linalg.norm(vector))

def addSpaces(text):
	text = text.strip()
	toAdd = [[","," , "],["."," . "],[":", " : "],[";"," ; "],["("," ( "],["["," [ "]]
	for current in toAdd:
		text = text.replace(current[0],current[1])
	return text

def createWordsMatrix(toRead,myCharIndex):
    dictionaryOfValues = {}
    text = addSpaces(toRead.read())
    splitText = text.split()
    maxV = 0   
    for i in range(0,len(splitText)-1):
        curWord = myCharIndex.setdefault(splitText[i],len(myCharIndex))
        nxtWord = myCharIndex.setdefault(splitText[i+1],len(myCharIndex))
        tup = (curWord,nxtWord)
        dictionaryOfValues.setdefault(tup,0);
        dictionaryOfValues[tup]+=1
    maxV = len(myCharIndex) + 1
    arrayOfCoordinates = []
    for key, val in dictionaryOfValues.iteritems():
        arrayOfCoordinates.append([key[0],key[1],val])
    first  = []
    second = []
    value = []
    for i in range(len(arrayOfCoordinates)):
        first.append(int(arrayOfCoordinates[i][0]))
        second.append(int(arrayOfCoordinates[i][1]))
        value.append(int(arrayOfCoordinates[i][2]))
    csrMatrix = csr_matrix((value,(first,second)),shape=(maxV,maxV),dtype='d')
    return csrMatrix

def createCharacterMatrix(toRead,myCharIndex):
    dictinaryOfValues = {}
    maxV = 0
    for sentence in toRead:
        sentence = sentence.strip()
        for i in range(0, len(sentence)-1,1):
            curLetter = myCharIndex.setdefault(sentence[i],len(myCharIndex))
            nxtLetter = myCharIndex.setdefault(sentence[i+1],len(myCharIndex))
            tup = (curLetter,nxtLetter)
            dictinaryOfValues.setdefault(tup,0);
            dictinaryOfValues[tup]+=1
    maxV = len(myCharIndex) + 1
    arrayOfCoordinates = []
    for key, val in dictinaryOfValues.iteritems():
        arrayOfCoordinates.append([key[0],key[1],val])
    first  = []
    second = []
    value = []
    for i in range(len(arrayOfCoordinates)):
        first.append(int(arrayOfCoordinates[i][0]))
        second.append(int(arrayOfCoordinates[i][1]))
        value.append(int(arrayOfCoordinates[i][2]))
    csrMatrix = csr_matrix((value,(first,second)),shape=(maxV,maxV),dtype='d')
    return csrMatrix
    
#def createTwoSeqMatrix(toRead):
	#return 1

#def createThreeSeqMatrix(toRead):
	#return 1

def doDot(eigan1, eigan2):
    #creates a 2D array of the relationship
    averageDot = []
    averageArray = []
    for first in eigan1:
        arrayOfTheta = []
        cAverage = 0
        unitfirstToCompare =unitVector(first)
        for second in eigan2:
                unitsecondToCompare =unitVector(second[1])
                theta = (np.dot(unitfirstToCompare, unitsecondToCompare))
                if(theta < 0):
                    theta *=-1
                cAverage+=theta
                arrayOfTheta.append(theta)
        cAverage = cAverage/len(eigan2)
        averageDot.append(cAverage)
        averageArray.append(arrayOfTheta)
    return averageDot,averageArray

def checkPositive(data):
    counter = 0
    for k in data:
        counter+=k
    if counter < 0:
        return np.multiply(data,-1)
    else:
        return data

def makeEigan(data,testingData,myCharIndex):
    for files in testingData:
        toRead = open("testing/" + files,"r")
        csrMatrix = createCharacterMatrix(toRead,myCharIndex)
    original = []
    for files in data:
        toRead = open("Enron_collection/" + files,"r")
        # if(sys.argv[3] == "W"):
        #     csrMatrix = createWordsMatrix(toRead,myCharIndex)
        # else:
        csrMatrix = createCharacterMatrix(toRead,myCharIndex)
        
        
        vals,vecs = lin.eigs(csrMatrix)
        
        vecs = vecs.transpose()
        vecs = vecs[0]
        original.append(checkPositive(vecs.real))
        print checkPositive(vecs.real)
        break
        # toRead.close()

    testA = []
    for files in testingData:
        target = open("testing" + "/" + files,"r")
        # if(sys.argv[3] == "W"):
        #     csrMatrix = createWordsMatrix(toRead,myCharIndex)
        # else:
        csrMatrix = createCharacterMatrix(target,myCharIndex)
        
        values,vectors = lin.eigs(csrMatrix)
        vectors = vectors.transpose()
        vectors = vectors[0]
        testA.append(checkPositive(vectors.real))
        target.close()
        print checkPositive(vectors.real)
        break
    #return original,testA

def dotter(testA,original,myCharIndex,data,testingData):
    newArray = []
    for vectors in testA:
        answer = []
        try:
            averageM,averages = doDot([vectors[1]],original)
        except:
            original,testA = makeEigan(data,testingData,myCharIndex)
            newArray = dotter(testA,original,myCharIndex,data,testingData)
            break
        for k in range(len(averages[0])):
            answer.append([testingData[k],float(averages[0][k].real)])
        answer =sorted(answer, key=lambda row: row[1])
        newArray.append(answer)
    return newArray

def checkCorrolation(dotted,filename,positionFromFront):
    files = os.listdir("testing")
    files.sort()
    counter = 0
    for i in dotted:
        if(str(i[0]) == str(filename)):
            positionFromFront.append([i[1],i[0]])
            break
        counter+=1

def split(foldername, newfolder, percentage):
    files = os.listdir(foldername)
    for f in files:
        target = open(foldername + '/' + f,"r")
        contents = target.read()
        length = int(len(contents)*(percentage/100))
        towrite = contents[0:length:]
        target = open(foldername+"/" + f,"w")
        target.write(towrite)

        towrite = contents[length::]
        target = open(newfolder+"/" + f,"w")
        target.write(towrite)

def amountOfsuccess(positionFromFront,number):
    files = os.listdir("Enron_collection")
    counter = 0
    for i in positionFromFront:
        if(i < number):
            counter+=1
        else:
            print i
    return counter

def copyFolder(original,toCopy):
    files = os.listdir(original)
    for f in files:
        shutil.copyfile(original+"/" + f,toCopy+"/"+f)
def checkData(filezizes):
    for k in filezizes:
        if k[0] < 204800:
            try:
                os.remove("Enron_collection/"+k[1])
            except:
                pass
            try:
                os.remove("testing/"+k[1])
            except:
                pass
            filezizes.remove(k)
    return filezizes

if (__name__ == "__main__"):
    strings = ""
    copyFolder("realunchanged","Enron_collection")
    files = os.listdir("Enron_collection")
    filesSizes = []
    success = []
    for f in files:
        filesSizes.append([int(os.stat("Enron_collection/"+f).st_size),f])
    filesSizes.sort()
    #filesSizes = checkData(filesSizes)
    myCharIndex = {}
    #split("Enron_collection","testing",50.0)
    data = os.listdir("Enron_collection")
    testingData = os.listdir("testing")
    testingData.sort()
    data.sort()
        #data would be a large folder of text files, with a lot of text in each file, testingData is what you would compare to the large folder of data.
         #holds which letter/word/sequence coorosponds to which number
    original,testA = makeEigan(data,testingData,myCharIndex)

    if(a[0]==b[0]):
        print "aasda"
    # dotted =  dotter(testA,original,myCharIndex,data,testingData)
    # positionFromFront = []
    # counter = 0
    # print dotted
    # for k in data:
    #     checkCorrolation(dotted[counter],k,positionFromFront)
    #     counter+=1
    # print positionFromFront
    # positionFromFront =sorted(positionFromFront, key=lambda row: row[0])
    # print positionFromFront