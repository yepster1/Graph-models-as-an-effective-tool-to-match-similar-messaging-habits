import os
import shutil
import EiganWorker as ew
import comparer as co
import shutil
Values = []
names = ["50-50","75-25","95-5","99-1"]
percentages = [50.0,75.0,95.0,99.0]
numbers = [10,5,4,3,2,1]

def checkCorrolation(filename,positionFromFront):
    files = os.listdir("Values")
    target = open("Values/" + filename,"r")
    line = -1
    counter = 0
    while (line != ""):
        line = target.readline()
        split = line.split(" - ")
        if(split[0] == filename):
            Values.append(float(split[1].replace("\n","")))
            positionFromFront.append(counter)
            break
        counter+=1

def RemoveCorrolation(foldername,percentage):
    files = os.listdir(foldername)
    for f in files:
        target = open(foldername + '/' + f,"r")
        contents = target.read()
        length = int(len(contents)*(percentage/100))
        towrite = contents[0:length:]
        target = open(foldername+"/" + f,"w")
        target.write(towrite)

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

def getAverage(array):
    avg = 0
    for i in array:
        avg = avg + i
    return avg/len(array)

def copyFolder(original,toCopy):
    files = os.listdir(original)
    for f in files:
        shutil.copyfile(original+"/" + f,toCopy+"/"+f)

def amountOfsuccess(positionFromFront,number):
    files = os.listdir("Enron_collection")
    counter = 0
    for i in positionFromFront:
        if(i >= len(files)-len(files)/10):
            counter+=1
    return counter

def ChangeFileSize(foldername,filename, size):
    target = open(foldername + "/" + filename,"r")
    String = target.read()
    target = open(foldername + "/" + filename,"w")
    target.write(String[:size:])

def recreatefiles():
    shutil.rmtree("Enron_collection") 
    os.mkdir("Enron_collection")
    shutil.rmtree("testing") 
    os.mkdir("testing")
    shutil.rmtree("Enron_collectioncreatedMatrix") 
    os.mkdir("Enron_collectioncreatedMatrix")
    shutil.rmtree("testingcreatedMatrix") 
    os.mkdir("testingcreatedMatrix")

def runSizeTest(foldername):
        strings = ""
        copyFolder("realunchanged","unchangedFiles")
        copyFolder("unchangedFiles","Enron_collection")
        files = os.listdir(foldername)
        filesSizes = []
        success = []
        for f in files:
            filesSizes.append([int(os.stat(foldername+"/"+f).st_size),f])
        filesSizes.sort()
        for f in filesSizes:
            print f
            copyFolder("unchangedFiles","Enron_collection")
            positionFromFront = []
            files = os.listdir(foldername)
            #for r in files:
            #   ChangeFileSize(foldername,r,f[0])
            split("Enron_collection","testing",percentages[1])
            ew.original()
            ew.tester()
            co.doIT()
            for k in files:
                checkCorrolation(k,positionFromFront)
            #for k in numbers:
            target = open("data/"+str("relative coorolation")+".txt","a")
            a =  amountOfsuccess(positionFromFront,k)
            target.write(str(f[0]) + " - " + str(a/float(len(files))) + "\n")  
            success.append(a)
            os.remove("unchangedFiles/"+f[1])
            #os.remove("testing/" + f[1])
            #os.remove("Enron_collection/" + f[1])
            #os.remove("Enron_collectioncreatedMatrix/" + f[1])
            #os.remove("testingcreatedMatrix/" + f[1])
            shutil.rmtree("Values")
            os.mkdir("Values")
            recreatefiles()
            
if __name__ == "__main__":
        runSizeTest("Enron_collection")

    # ChangeFileSize("Enron_collection")
        #copyFolder("unchangedFiles","Enron_collection")
        #split("Enron_collection","testing",50.0)
        # positionFromFront = []
        # files = os.listdir("Values")
        # for k in files:
        #     checkCorrolation(k,positionFromFront)
        # print len(files) - getAverage(positionFromFront)
        # print getAverage(Values)
        # print positionFromFront
        # positionFromFront.sort()
        # print len(files) - positionFromFront[int(len(positionFromFront)/2)]
        # print Values
        # print amountOfsuccess(positionFromFront)