import numpy as np

class FSHalftoning:
    def __init__(self, w=0, h=0):
        self.w = w
        self.h = h
        
    def process(self, v, compression):
        w = self.w
        h = self.h

        c = compression / (np.sum(v)/(w*h))

        ret = np.zeros(w*h)
        ret = c*v.copy()

        for i in range(0,h):
            for j in range(0,w):
                oldPixel = ret[i*w + j]

                newPixel = 0
                if oldPixel >= 0.5:
                    newPixel = 1

                ret[i*w + j] = newPixel
                quantError = float(oldPixel - newPixel)

                if j+1 < w:
                    ret[i*w + j+1] += quantError * 7. / 16.

                if j-1 >= 0 and i + 1 < h:
                    ret[(i+1)*w + j-1] += quantError * 3. / 16.

                if i + 1 < h:
                    ret[(i+1)*w + j] += quantError * 5. / 16.

                if i+1 < h and j+1 < w :
                    ret[(i+1)*w + j+1] += quantError * 1. / 16.

        return ret