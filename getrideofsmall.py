import os
files = os.listdir("People")
for k in files:
	if(os.stat('People/'+k).st_size<1048576):
		os.remove("People/"+k)

