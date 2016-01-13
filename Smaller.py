import ast
import os
names = {}
files = os.listdir("files")
for k in files:
	target = open("files/"+k,'r')

	counter = 0
	for line in target:
		CurrentLine = line.replace("null","None")
		CurrentLine = CurrentLine.replace("true","True")
		CurrentLine = CurrentLine.replace("false","False")
		dictionary = ast.literal_eval(CurrentLine)
		toWrite =  open("People/"+dictionary["author"],"a")
		toWrite.write(dictionary["body"])
		toWrite.close()
		counter +=1
		if(counter % 100000 == 0):
			print counter