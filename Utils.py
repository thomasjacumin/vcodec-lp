import numpy as np
from PIL import Image
import colorsys
import math

from WhiteNoise import WhiteNoise
from SaltPepperNoise import SaltPepperNoise

class Utils(object):
    @staticmethod
    def openGrayscaleImage(inputPathname):
        f = np.asarray(Image.open(inputPathname).convert('L'))
        w = np.size(f,1)
        h = np.size(f,0)
        return f.flatten() / 255, w, h

    @staticmethod
    def saveGrayscaleImage(data,w, h, inputPathname):
        Image.fromarray(np.uint8(255*data.reshape([h,w]))).save(inputPathname)

    @staticmethod
    def applyWhiteNoise(f, w, h, deviation, seed=None):
        if seed != None:
            np.random.seed(0)
        whiteNoise = WhiteNoise(w, h, deviation)
        return whiteNoise.process(f)

    @staticmethod
    def applySPNoise(f, w, h, s, p, seed=None):
        if seed != None:
            np.random.seed(0)
        whiteNoise = SaltPepperNoise(w, h, salt=s, pepper=p)
        return whiteNoise.process(f)

    @staticmethod
    def MSE(u,v,w,h):
        tmp = np.power(u-v, 2)
        return np.sum(tmp) / (w*h)
    
    @staticmethod
    def PSNR(u,v,w,h):
        tmp = 1 / Utils.MSE(u,v,w,h)
        return 10*np.log10(tmp)
    
    @staticmethod
    def L2Error(u,v,w,h):
        tmp = np.power(u-v, 2)
        return np.sqrt(np.sum(tmp))
    
    @staticmethod
    def L1Error(u,v,w,h):
        tmp = np.abs(u-v)
        return np.sum(tmp)
