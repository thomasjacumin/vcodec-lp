import numpy as np

from GaussianSmoothing import GaussianSmoothing
from Laplacian import Laplacian

class H1Mask(object):
    NAME = "H1"
    def __init__(self, w=0, h=0):
        self.w = w
        self.h = h
        
    def setHalftoneMethod(self, halftoneMethod):
        self.halftoneMethod = halftoneMethod
        
    def create(self, f, compression):
        w = self.w
        h = self.h

        smoothF = GaussianSmoothing(w,h).assemble(1.0,f).process()
        
        laplacianFilter = Laplacian(w, h)
        lap = laplacianFilter.assemble().process(smoothF)

        lap = np.abs(lap)
        lapMax = np.amax(lap)
        lap = lap/lapMax
        
        self.mask = self.halftoneMethod.process(lap,compression)
        return self.mask, f
