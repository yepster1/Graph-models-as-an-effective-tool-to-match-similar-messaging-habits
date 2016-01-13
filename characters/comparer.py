import EiganWorker as ew
import os
def doIT():
	original = open("Original.txt","r")
	test = open("testing.txt","r")

	originalA = []
	for l in original:
		splited = l.split(" - ")
		line = []
		for k in splited:
			try:
				line.append(float(k))
			except:
				pass
		originalA.append(line)

	testA = []
	for l in test:
		split = l.split(" - ")
		line = []
		for k in split:
			try:
				line.append(float(k))
			except:
				pass
		testA.append(line)
	files = os.listdir("testing")
	newArray = []
	inputs = 0
	for vectors in testA:
		answer = []
		averageM,averages = ew.doDot([vectors],originalA)
		for k in range(len(averages[0])):
	   		answer.append([files[k],averages[0][k]])
	   	answer =sorted(answer, key=lambda row: row[1])
		newArray.append(answer)
		ew.writeToFile(files[inputs],[answer])
		inputs+=1
if __name__ == "__main__":
	doIT()