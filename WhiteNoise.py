import numpy as np

class WhiteNoise(object):
    def __init__(self, w, h, deviation):
        self.w = w
        self.h = h
        self.data = np.random.normal(loc=0.0, scale=deviation, size=w*h)
        
    def process(self, f):
        return np.clip(f + self.data, 0, 1)
        