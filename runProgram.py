import os
import main as m
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
	testingVectors = []
	val,vec = lin.eigs(testingMatrix[0][0],k = 1)
	vec = vec.transpose()
	vec = vec[0]
	testingVectors.append([vec.real,k[testingMatrix[0][1]]])
	originalVectors = []

	for k in originalMatrix:
		try:
			values,vectors = lin.eigs(k[0], k = 1)
			vectors = vectors.transpose()
			vectors = vectors[0]
			originalVectors.append([vectors.real,k[1]])
			print counter3
			counter3+=1
		except:
			print "error, non convergence"


def start():
	files,data = getdata()
	testingData = getTesting()
	Which = input("Do you want to compare by Character(C), Word(W), 2character sequence(2) or 3 Character sequence(3), keep in mind that word takes the longest")
	if Which == "C":
		character(testingData,data,files)

start()
