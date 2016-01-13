import os
import EiganVector as ev
def createDictionaryOfValues(toRead,myCharsIndex):
    dictinaryOfValues = {}
    for sentence in toRead:
        sentence = sentence.strip()
        for i in range(0, len(sentence)-1,1):
            curLetter = myCharsIndex.setdefault(sentence[i],len(myCharsIndex))
            nxtLetter = myCharsIndex.setdefault(sentence[i+1],len(myCharsIndex))
            tup = (curLetter,nxtLetter)
            dictinaryOfValues.setdefault(tup,0);
            dictinaryOfValues[tup]+=1
    return dictinaryOfValues

def writeChar(myCharsIndex):
    target = open("myCharIndex","w")
    for key,val in myCharsIndex.iteritems():
        target.write(str(key) + " - " + str(val) + "\n")

def toMatrix(folder,myCharsIndex,fileName,arrayOfCoordinates):
    if(folder == ""):
        toRead = open(fileName,"r")
    else:
        toRead = open(folder+"/" + fileName,"r")
    dictinaryOfValues = createDictionaryOfValues(toRead, myCharsIndex)
    target = open(folder + "createdMatrix/" + fileName, 'w')
    writeToFile = ""
    for key, val in dictinaryOfValues.iteritems():
        writeToFile += str(key[0]) + " - " + str(key[1]) + " - " + str(val) + "\n"
    target.write(writeToFile)

def infoIntoDic(foldername,myCharsIndex):
    files = os.listdir(foldername)
    files.sort()
    arrayOfCoordinates = []
    for fileName in files:
        toMatrix(foldername,myCharsIndex,fileName,arrayOfCoordinates)
    return files, arrayOfCoordinates,myCharsIndex

def getMaximum(myCharsIndex):
    max = 0
    for key,val in myCharsIndex.iteritems():
        if (max < val):
            max = val
    max+=1
    return max

if __name__ == "__main__":
    myChar = ev.getmyCharsIndex()
    files, array, myChar = infoIntoDic("Enron_collection",myChar)
    getMaximum(myChar)
    writeChar(myChar)
#fileNames, dictinaryOfContents =
