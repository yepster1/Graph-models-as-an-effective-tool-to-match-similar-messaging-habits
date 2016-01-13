import plotly.plotly as py
import plotly.graph_objs as go
import os
import numpy as np
numbers = [10,5,4,3,2,1]
files = os.listdir("data/top-10")
print files
N = 147
ys = []
traces = []
for k in numbers:
	data = open("data/relative coorolation.txt")
	random_y0 = []
	random_x = []
	for a in data:
		b = a.split(" - ")
		random_y0.append(float(b[1])*100)
		random_x.append(int(b[0]))
	#ys.append[random_y0]
	random_x.sort()
	trace = go.Scatter(x = random_x,y = random_y0,mode = 'lines',name = str(k))
	traces.append(trace)

data = [traces[0]]

py.iplot(data, filename='line-mode')