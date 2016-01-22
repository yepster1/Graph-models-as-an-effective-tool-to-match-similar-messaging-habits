import os
from scipy.sparse import csr_matrix
import scipy.sparse.linalg as lin
import numpy as np
from scipy import sparse
import copy
import shutil
import time

def unitVector(vector):
    return np.divide(vector,np.linalg.norm(vector))

def writeChar(myCharsIndex,types):
    target = open(types+"myCharIndex","w")
    for key,val in myCharsIndex.iteritems():
        target.write(str(key) + " - " + str(val) + "\n")

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

def create2sequenceMatrix(toRead,myCharIndex):
    dictinaryOfValues = {}
    maxV = 0
    for sentence in toRead:
        sentence = sentence.strip()
        for i in range(0, len(sentence)-4,2):
            curLetter = myCharIndex.setdefault(sentence[i:i+2],len(myCharIndex))
            nxtLetter = myCharIndex.setdefault(sentence[i+2:i+4],len(myCharIndex))
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

def create3sequenceMatrix(toRead,myCharIndex):
    dictinaryOfValues = {}
    maxV = 0
    sentence=toRead.read()
    sentence = sentence.strip()
    for i in range(0, len(sentence)-6,3):
        curLetter = myCharIndex.setdefault(sentence[i:i+3],len(myCharIndex))
        nxtLetter = myCharIndex.setdefault(sentence[i+3:i+6],len(myCharIndex))
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

def addSpaces(files):
    spaces = [[","," , "],["."," . "],["["," [ "],["]"," ] "],["!"," ! "],["?"," ? "],["("," ( "],[")"," ) "],["\""," \" "],["-"," - "],["\'"," \' "]]
    for s in spaces:
        files.replace(s[0],s[1])
    return files

def deleteFillers(text):
    target = open("fillerwords.txt",'r')
    for k in target:
        text = text.replace(k,"")
    return text

def createWordsMatrix(toRead,myCharIndex):
    dictionaryOfValues = {}
    text = addSpaces(toRead.read())
    text = deleteFillers(text)
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

def checkCorrolation(dotted,filename,positionFromFront):
    files = os.listdir("testing")
    files.sort()
    counter = 0
    for i in dotted:
        if(str(i[1]) == str(filename)):
            positionFromFront.append(i[0])
            break
        counter+=1

def ceckdistancefromfront(dotted,filename):
    files = os.listdir("testing")
    files.sort()
    counter = 0
    for i in dotted:
        if(str(i[1]) == str(filename)):
            return counter
        counter+=1
    return counter

def checkdistancefromfront(dotted,filename,array):
    files = os.listdir("testing")
    files.sort()
    counter = 0
    for i in dotted:
        if(str(i[1]) == str(filename)):
            array.append(counter)
            break
        counter+=1

def copyFolder(original,toCopy):
    files = os.listdir(original)
    for f in files:
        shutil.copyfile(original+"/" + f,toCopy+"/"+f)

def amountOfsuccess(positionFromFront,folder):
    files = os.listdir(folder)
    counter = 0
    for i in positionFromFront:
        counter+=i
    return counter/float(len(positionFromFront))

def amountOfsuccessFromFront(positionFromFront,number,folder):
    files = os.listdir(folder)
    counter = 0
    for i in positionFromFront:
        if(i <= number):
            counter+=1
    return counter/float(len(positionFromFront))

def percentsuccessFromFront(positionFromFront,folder):
    files = os.listdir(folder)
    counter = 0
    for i in positionFromFront:
        if(i <= len(positionFromFront)/10.0):
            counter+=1
    return counter/float(len(positionFromFront))

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

def main(files,tester,percentage):
    start_time = time.time()
    copyFolder("realunchanged",files)
    split(files,tester,percentage)
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
    testingsizes.sort()
    testingData.sort()
    data.sort()
    try:
        myCharIndex = getmyCharsIndex("100seq")
    except:
        print "first run detected, creating character matrix"
        originalMatrix = []
        testingMatrix = []
        myCharIndex = {}
        counter = 0
        for content in testingsizes:
            if counter % 100 == 0:
                print counter
            counter+=1
            testingMatrix.append([createWordsMatrix(open(tester+"/"+content[1],"r"),myCharIndex),content[1]])
        for content in filesSizes:
            if counter % 100 == 0:
                print counter
            counter+=1
            originalMatrix.append([createWordsMatrix(open(files+"/"+content[1],"r"),myCharIndex),content[1]])
    writeChar(myCharIndex,"10seq")
    originalMatrix = []
    testingMatrix = []
    print "continuing"
    counter =0

    for content in testingsizes[::-2]:
        if counter % 10 == 0:
            print counter
        counter +=1
        testingMatrix.append([createWordsMatrix(open(tester+"/"+content[1],"r"),myCharIndex),content[1]])
    for content in filesSizes:
        if counter % 10 == 0:
            print counter
        counter+=1
        originalMatrix.append([createWordsMatrix(open(files+"/"+content[1],"r"),myCharIndex),content[1]])
    counter2 = 0
    originalVectors = []
    testingVectors = []
    counter3 = 0
    data = []
    for p in range(len(filesSizes)):
        data.append(filesSizes[p][1])
    testingData = []
    for p in range(len(testingsizes)):
        testingData.append(filesSizes[p][1])
    
    for k in testingMatrix:
        try:
            val,vec = lin.eigs(k[0],k = 1)
            vec = vec.transpose()
            vec = vec[0]
            testingVectors.append([vec.real,k[1]])
            print counter3
            counter3+=1
        except:
            print k[1]
            print "error, non convergence"
            del data[counter3]
    counter3 = 0
    for k in originalMatrix:
        try:
            values,vectors = lin.eigs(k[0], k = 1)
            vectors = vectors.transpose()
            vectors = vectors[0]
            originalVectors.append([vectors.real,k[1]])
            print counter3
            counter3+=1
        except:
            print k[1]
            del testingData[counter3]
            print "error, non convergence"
    for j in filesSizes[:-2]:
        print j
        things = []
        for first in testingVectors:
            filess = os.listdir(files)
            array = []
            for second in originalVectors:
                theta = np.dot(unitVector(first[0]),unitVector(second[0]))
                if (theta < 0):
                    theta *=-1
                array.append([theta,second[1]])
            array.sort()
            things.append(array[::-1])
        values = []
        counter = 0
        for k in data:
            checkCorrolation(things[counter],k,values)
            counter+=1
        positionFromFront = []
        counter = 0
        for r in data:
            checkdistancefromfront(things[counter],r,positionFromFront)
            counter+=1
        target = open("answers/thetaValues" + str(percentage) + ".txt","a")
        target.write(str(amountOfsuccess(values,files))+" - "+ str(j)+"\n")
        counter = 0
        amount = 0
        for r in data:
            amount += ceckdistancefromfront(things[counter],r)
            counter+=1
        try:
            target = open("answers/averagedistancefromfront" + str(percentage) + ".txt","a")
            target.write(str(amount/float(len(data))) + " - " + str(j) + "\n")
            target = open("answers/Amountofsucess10-" + str(percentage) + ".txt","a")
            target.write(str(amountOfsuccessFromFront(positionFromFront,10,files))+" - " + str(j)  +"\n")
            target = open("answers/Amountofsucess5-" + str(percentage) + ".txt","a")
            target.write(str(amountOfsuccessFromFront(positionFromFront,5,files))+" - " + str(j) + "\n")
            target = open("answers/Amountofsucess4-" + str(percentage) + ".txt","a")
            target.write(str(amountOfsuccessFromFront(positionFromFront,4,files))+" - " + str(j) + "\n")
            target = open("answers/Amountofsucess3-" + str(percentage) + ".txt","a")
            target.write(str(amountOfsuccessFromFront(positionFromFront,3,files))+" - " + str(j) + "\n")
            target = open("answers/Amountofsucess2-" + str(percentage) + ".txt","a")
            target.write(str(amountOfsuccessFromFront(positionFromFront,2,files))+" - " + str(j) + "\n")
            target = open("answers/Amountofsucess1-" + str(percentage) + ".txt","a")
            target.write(str(amountOfsuccessFromFront(positionFromFront,1,files))+" - " + str(j) + "\n")
            target = open("answers/PercentAmountofsucess-" + str(percentage) + ".txt","a")
            target.write(str(percentsuccessFromFront(positionFromFront,files))+" - " + str(j) + "\n")
        except:
            print "done"
        os.remove(files + "/" + j[1])
        os.remove(tester + "/" + j[1])
        del originalMatrix[0]
        del testingMatrix[0]
        del originalVectors[0]
        del testingVectors[0]
        for k in originalVectors:
            np.delete(k,[0],None)
        for l in testingVectors:
            np.delete(l,[0],None)
        del data[0]
        del testingData[0]
    end_time = time.time()

if __name__ == "__main__":
    percentages = [75.0,90.0,95.0]
    for r in percentages:
        print r
        main("People","testing",r)