import numpy as np

class Laplacian(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        
    def assemble(self):
        return self
        
    def process(self, f):
      w = self.w
      h = self.h
      lap = np.zeros(w*h)

      for i in range(0,h):
        for j in range(0,w):
          if i >= 1 and i < h-1 and j >= 1 and j < w-1: # interior
            lap[i*w + j] = f[i*w + j-1]+f[i*w + j+1]+f[(i+1)*w + j]+f[(i-1)*w + j]-4*f[i*w + j]
          else: # boundary
            if i == 0 and j == 0: # top-left corner
              lap[i*w + j] = f[i*w + j+1]+f[(i+1)*w + j]-2*f[i*w + j]
            elif i == 0 and j == w-1: # top-right corner
              lap[i*w + j] = f[i*w + j-1]+f[(i+1)*w + j]-2*f[i*w + j]
            elif i == h-1 and j == 0: # bottom-left corner
              lap[i*w + j] = f[i*w + j+1]+f[(i-1)*w + j]-2*f[i*w + j]
            elif i == h-1 and j == w-1: # bottom-right corner
              lap[i*w + j] = f[i*w + j-1]+f[(i-1)*w + j]-2*f[i*w + j]
            else: # not a corner
              if i == 0: # top border
                lap[i*w + j] = f[i*w + j-1]+f[i*w + j+1]+f[(i+1)*w + j]-3*f[i*w + j]
              elif i == h-1: # bottom border
                lap[i*w + j] = f[i*w + j-1]+f[i*w + j+1]+f[(i-1)*w + j]-3*f[i*w + j]
              elif j == 0: #left border
                lap[i*w + j] = f[i*w + j+1]+f[(i+1)*w + j]+f[(i-1)*w + j]-3*f[i*w + j]
              else: # right border
                lap[i*w + j] = f[i*w + j-1]+f[(i+1)*w + j]+f[(i-1)*w + j]-3*f[i*w + j]

      return lap
