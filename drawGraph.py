import matplotlib.pyplot as plt
import os
files = os.listdir("character/percentAmount/")
plt.ylabel('some numbers')
mins = 1.0
fig,ax = plt.subplots()
for k in files:
	target = open("character/percentAmount/"+k,"r")
	vals = []
	for k in target:
		r = k.split(" - ")
		if (float(r[0]) < mins):
			mins = float(r[0])
		vals.append(float(r[0]))
	ax.plot(vals,label=str(k))
plt.axis([0, 150, mins - 0.1,1.1])


plt.show()
