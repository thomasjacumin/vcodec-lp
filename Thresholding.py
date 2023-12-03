import numpy as np

class Thresholding:
	def __init__(self, w=0, h=0):
		self.w = w
		self.h = h
        
	def process(self, v, compression):
		w = self.w
		h = self.h

		imgWithIndex = np.zeros(w*h, dtype=(float,2))

		for i in range(0,h*w):
			imgWithIndex[i,0] = v[i]
			imgWithIndex[i,1] = i

		imgWithIndex = imgWithIndex.tolist()
		imgWithIndex.sort(key=lambda tup: -tup[0])

		mask = np.zeros(w*h)
		for i in range(0,int(compression*w*h)):
			index = int(imgWithIndex[i][1])
			mask[index] = 1
                
		return mask