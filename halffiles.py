import os
files = os.listdir("files")

for k in files:
	 r = open("files/"+k,"r")
	 p = r.read()
	 c = open("files/"+k+"_01","w")
	 d = open("files/"+k+"_02","w")
	 c.write(p[:int(len(p)/2):])
	 d.write(p[int(len(p)/2)::])
	 os.remove("files/"+k)
