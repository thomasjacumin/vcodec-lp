import numpy as np
from scipy import sparse
from scipy.sparse.linalg.dsolve import linsolve

from L2ParabolicInpainting import L2ParabolicInpainting

class GaussianSmoothing(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        
    def assemble(self, sigma, f):
        w = self.w
        h = self.h
        dt = sigma**2 / 2        
        
        self.gaussianSmoothing = L2ParabolicInpainting(w,h)
        self.gaussianSmoothing.setAlpha(dt)
        self.gaussianSmoothing.setPrevious(f)
        self.gaussianSmoothing.assemble(0, np.zeros(w*h))

        return self
        
    def process(self):
        return self.gaussianSmoothing.process()
        
