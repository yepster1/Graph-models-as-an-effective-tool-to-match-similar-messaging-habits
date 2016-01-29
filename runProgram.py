import os
import main as m
import scipy.sparse.linalg as lin
import numpy as np
from scipy.sparse import csr_matrix

def getdata():
	try:
		f = input("Please enter the directory name of the data sorrounded by \"\" ")
		return f,os.listdir(f)
	except:
		print "does not exist, please make sure that the data is either in your current working directory or enter the full location"
		return getdata()

def getTesting():
	try:
		a = str(input("please enter the file name (and extension) that you want to compare to the data"))
		return a
	except:
		print "doesnt exist, make sure it is sorrounded by\"\""
		return getTesting()
def createMatrix(toRead,myCharIndex):
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
    return myCharIndex

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

def character(testingdata,data,files):
	myCharIndex = {}
	counter = 0	
	originalMatrix = []
	myCharIndex = createMatrix(testingdata,myCharIndex)
	for content in data:
		myCharIndex = createMatrix(open(files+"/"+content,"r"),myCharIndex)
	print "creating character index"
	originalMatrix = []
	for content in data:
		if counter % 10 == 0:
			print counter/float(len(data))
		counter+=1
		originalMatrix.append([createCharacterMatrix(open(files+"/"+content,"r"),myCharIndex),content])
	testingMatrix = []
	testingMatrix.append([createCharacterMatrix(open(testingdata,"r"),myCharIndex),testingdata])
	testingVectors = []
	# counter = 0	
	# originalMatrix = []
	# print "creating matrix's"
	# for content in data:
	# 	if counter % 10 == 0:
	# 		print counter/float(len(data))
	# 	counter+=1
	# 	originalMatrix.append([m.createCharacterMatrix(open(files+"/"+content,"r"),myCharIndex),content])
	# testingMatrix = []
	# testingMatrix.append([m.createCharacterMatrix(testingdata,myCharIndex),testingdata])
	
	originalVectors = []
	counter3 = 0
	print "creating vectors"
	for k in originalMatrix:
		values,vectors = lin.eigs(k[0], k = 1)
		vectors = vectors.transpose()
		
		originalVectors.append([vectors[0].real,k[1]])
		if(counter3%10 == 0):
			print counter3/float(len(originalMatrix))
		counter3+=1
	print len((originalVectors[0][0]))
	testingVectors = []
	val,vec = lin.eigs(testingMatrix[0][0],k = 1)
	vec = vec.transpose()

	testingVectors.append([vec[0].real,testingMatrix[0][1]])
	print len(testingVectors[0][0])
	print "dotting"
	things = []
	for first in testingVectors:
		filess = os.listdir(files)
		array = []
		for second in originalVectors:
			theta = np.dot(m.unitVector(first[0]),m.unitVector(second[0]))
			if (theta < 0):
				theta *=-1
			array.append([theta,second[1]])
		array.sort()
		things.append(array[::-1])
	print "Sorted from most likely to least"
	for k in things[0]:
		print k


def start():
	files,data = getdata()
	testingData = getTesting()
	character(testingData,data,files)

start()
