import os
from scipy.sparse import csr_matrix
import scipy.sparse.linalg as lin
import numpy as np
from scipy import sparse
import copy

def unitVector(vector):
    return np.divide(vector,np.linalg.norm(vector))

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

def checkCorrolation(dotted,filename,positionFromFront):
    files = os.listdir("testing")
    files.sort()
    counter = 0
    for i in dotted:
        if(str(i[1]) == str(filename)):
            positionFromFront.append(counter)
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

def getmyCharsIndex(types):
    target = open(types+"myCharIndex",'r')
    mycharIndex = {}
    for k in target:
        new = k.split(" - ")
        thing =(new[1].replace("\n",""))
        try:
            mycharIndex[new[0]] = int(thing)
        except:
            print thing
    return mycharIndex

def writeChar(myCharsIndex,types):
    target = open(types+"myCharIndex","w")
    for key,val in myCharsIndex.iteritems():
        target.write(str(key) + " - " + str(val) + "\n")

def amountOfsuccess(positionFromFront,number,folder):
    files = os.listdir(folder)
    counter = 0
    for i in positionFromFront:
        if(i <= number):
            counter+=1
    return counter/float(len(positionFromFront))

def PercentamountOfsuccess(positionFromFront,folder):
    files = os.listdir(folder)
    counter = 0
    for i in positionFromFront:
        if(i <= len(files)/10):
            counter+=1
    return counter/float(len(positionFromFront))

def main(files,tester):
    split(files,tester,75.0)
    filess = os.listdir(files)
    filesSizes = []
    success = []
    print "Total Files = " + str(len(filess))
    for f in filess:
        filesSizes.append([int(os.stat(files+"/"+f).st_size),f])
    filesSizes.sort()
    data = os.listdir(files)
    testingData = os.listdir(tester)
    testingsizes = []
    for f in testingData:
        testingsizes.append([int(os.stat(tester+"/"+f).st_size),f])

    testingData.sort()
    data.sort()
    try:
        myCharIndex = getmyCharsIndex("char")
    except:
	print "first run detected, creating character matrix"
        originalMatrix = []
        testingMatrix = []
        myCharIndex = {}
	counter = 0
        for content in testingsizes:
	    if counter % 10 == 0:
		print counter
	    counter+=1
            testingMatrix.append([createCharacterMatrix(open(tester+"/"+content[1],"r"),myCharIndex),content[1]])
        for content in filesSizes:
	    if counter % 10 == 0:
		print counter
	    counter+=1
            originalMatrix.append([createCharacterMatrix(open(files+"/"+content[1],"r"),myCharIndex),content[1]])
    writeChar(myCharIndex,"char")
    originalMatrix = []
    testingMatrix = []
    print "continuing"
    counter =0
    for content in testingsizes:
        if counter % 10 == 0:
 	    print counter
        counter +=1
        testingMatrix.append([createCharacterMatrix(open(tester+"/"+content[1],"r"),myCharIndex),content[1]])
    for content in filesSizes:
	if counter % 10 == 0:
	    print counter
	counter+=1
        originalMatrix.append([createCharacterMatrix(open(files+"/"+content[1],"r"),myCharIndex),content[1]])
    counter = 0
    for j in filesSizes:
        print counter
        counter+=1
        filess = os.listdir(files)
        data = os.listdir(files)
        testingData = os.listdir(tester)      
        originalVectors = []
        testingVectors = []
        for k in testingMatrix:
            try:
                val,vec = lin.eigs(k[0])
                vec = vec.transpose()
                vec = vec[0]
                testingVectors.append([vec.real,k[1]])
            except:
                print j
                print "error, non convergence"
        for k in originalMatrix:
            try:
                values,vectors = lin.eigs(k[0])
                vectors = vectors.transpose()
                vectors = vectors[0]
                originalVectors.append([vectors.real,k[1]])
            except:
                print j
                print "error, non convergence"
        #print testingVectors[0]
        #print originalVectors[0]
        print j
        things = []
        for first in testingVectors:
            array = []
            for second in originalVectors:
                theta = np.dot(unitVector(first[0]),unitVector(second[0]))
                if (theta < 0):
                    theta *=-1
                array.append([theta,second[1]])
            array.sort()
            things.append(array[::-1])
        positionFromFront = []
        counter = 0
        for k in data:
            checkCorrolation(things[counter],k,positionFromFront)
            counter+=1
        positionFromFront2 = copy.deepcopy(positionFromFront)
        target = open("toptensucess.txt","a")
        target.write(str(amountOfsuccess(positionFromFront,10,files))+"\n")
        target = open("tenpercent.txt","a")
        target.write(str(PercentamountOfsuccess(positionFromFront,files))+"\n")
        os.remove(files + "/" + j[1])
        os.remove(tester + "/" + j[1])
        del originalMatrix[0]
        del testingMatrix[0]

if __name__ == "__main__":
    main("People","testing")
