import os
import main as m
import scipy.sparse.linalg as lin
import numpy as np
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
		return open(a,"r")
	except:
		print "doesnt exist, make sure it is sorrounded by\"\""
		return getTesting()

def character(testingdata,data,files):
	myCharIndex = {}
	originalMatrix = []
	counter = 0
	for content in data:
		if counter % 10 == 0:
			print counter/float(len(data))
		counter+=1
		originalMatrix.append([m.createCharacterMatrix(open(files+"/"+content,"r"),myCharIndex),content])
	print "finished making original Matrices"
	testingMatrix = []
	testingMatrix.append([m.createCharacterMatrix(testingdata,myCharIndex),testingdata])
	for content in data:
		if counter % 10 == 0:
			print counter/float(len(data))
		counter+=1
		originalMatrix.append([m.createCharacterMatrix(open(files+"/"+content,"r"),myCharIndex),content])
	testingMatrix = []
	testingMatrix.append([m.createCharacterMatrix(testingdata,myCharIndex),testingdata])
	testingVectors = []
	val,vec = lin.eigs(testingMatrix[0][0],k = 1)
	vec = vec.transpose()
	vec = vec[0]
	testingVectors.append([vec.real,testingMatrix[0][1]])
	originalVectors = []
	counter3 = 0
	for k in originalMatrix:
		values,vectors = lin.eigs(k[0], k = 1)
		vectors = vectors.transpose()
		vectors = vectors[0]
		originalVectors.append([vectors.real,k[1]])
		if(counter3%10 == 0):
			print counter3/float(len(originalMatrix))
		counter3+=1
	things = []
	for first in testingVectors:
		filess = os.listdir(files)
		array = []
		for second in originalVectors:
			try:
				theta = np.dot(m.unitVector(first[0]),m.unitVector(second[0]))
				if (theta < 0):
					theta *=-1
				array.append([theta,second[1]])
			except:
				pass
		array.sort()
		things.append(array[::-1])
	print "Sorted from most likely to least"
	print things


def start():
	files,data = getdata()
	testingData = getTesting()
	Which = input("Do you want to compare by Character(C), Word(W), 2character sequence(2) or 3 Character sequence(3), keep in mind that word takes the longest")
	if Which == "C":
		character(testingData,data,files)

start()
