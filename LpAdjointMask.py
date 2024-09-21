import numpy as np

from Laplacian import Laplacian
from L2ParabolicInpainting import L2ParabolicInpainting

class LpAdjointMask(object):
  NAME = "LpADJ"
  def __init__(self, w=0, h=0):
    self.w = w
    self.h = h
      
  def setHalftoneMethod(self, halftoneMethod):
    self.halftoneMethod = halftoneMethod
    
  def setAlpha(self, alpha):
    self.alpha = alpha

  def setP(self, p):
    self.p = p
      
  def create(self, f, compression):
    w = self.w
    h = self.h
    p = self.p
    
    LF = Laplacian(w,h)
    lapF = LF.assemble().process(f)

    IM = L2ParabolicInpainting(w,h)
    IM.setAlpha(self.alpha)
    IM.setPrevious(self.alpha*lapF)
    IM.assemble(0*np.ones(w*h), np.zeros(w*h))
    v0 = IM.process()

    IM = L2ParabolicInpainting(w,h)
    IM.setAlpha(self.alpha)
    if p > 1:
      IM.setPrevious( -np.power(abs(v0), p-2)*v0)
    elif p == 1:
      IM.setPrevious( -np.sign(v0))
    IM.assemble(0*np.ones(w*h), np.zeros(w*h))
    w0 = IM.process()

    criterion = -v0*w0

    self.mask = self.halftoneMethod.process(criterion, compression)
    return self.mask, f
