import numpy as np

class SaltPepperNoise(object):
    def __init__(self, w, h, salt, pepper):
        self.w = w
        self.h = h
        self.salt = salt
        self.pepper = pepper
        
    def process(self, f):
        salt = self.salt
        pepper = self.pepper
        w = self.w
        h = self.h
        
        ret = np.zeros(w*h)
        for i in range(1,w*h):
            a = np.random.rand(1)[0]
            if a <= salt:
                ret[i] = 1
            else:
                a = np.random.rand(1)[0]
                if a <= pepper:
                    ret[i] = 0
                else:
                    ret[i] = f[i]
            
        return ret