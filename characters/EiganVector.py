import createMatrix as mm
import numpy as np
from scipy.sparse import csr_matrix
from scipy import sparse
import os
import EiganWorker as ew
import scipy.sparse.linalg as lin



def getmyCharsIndex():
    target = open("myCharIndex",'r')
    mycharIndex = {}
    for k in target:
        new = k.split(" - ")
        thing =(new[1].replace("\n",""))
        try:
            mycharIndex[new[0]] = int(thing)
        except:
            print thing
    return mycharIndex

myCharIndex  = getmyCharsIndex()
maxV = mm.getMaximum(myCharIndex)
maxV +=1

def findmax(first):
    maxS = 0
    for i in first:
        if maxS < i:
            maxS = i
    return maxS

def createDictionary(folder):
    dic = []
    files = os.listdir(folder+"createdMatrix")
    for fileName in files:
        CurrentDic = []
        target = open(folder+"createdMatrix/" + fileName,'r')
        for line in target:
            newline = line.replace("\n","").split(" - ")
            currentline = []
            for char in newline:
                try:
                    currentline.append(char)
                except:
                    print "invalid literal"
            CurrentDic.append(currentline)
        dic.append(CurrentDic)
    return dic

def turnIntoEigan(dictionary):
    eigenVectorArray = []
    for current in dictionary:
        first  = []
        second = []
        value = []
        for i in range(len(current)):
            first.append(int(current[i][0]))
            second.append(int(current[i][1]))
            value.append(int(current[i][2]))
        csrMatrix = csr_matrix((value,(first,second)),shape=(maxV,maxV),dtype='d')
      #  print csrMatrix
        vals,vecs = lin.eigs(csrMatrix)
        vecs = vecs.transpose()
        eigenVectorArray.append(vecs[0])
    return eigenVectorArray


if __name__ == "__main__":
    dic = createDictionary()

    print turnIntoEigan(dic,myCharIndex)