import numpy as np
from scipy import sparse
from scipy.sparse.linalg.dsolve import linsolve

class H1Inpainting(object):
    NAME="H1"
    def __init__(self, w=0, h=0):
        self.w = w
        self.h = h
        
    def setSize(self, w, h):
        self.w = w
        self.h = h
        
    def assemble(self, f, mask):
        w = self.w
        h = self.h
        
        Av = []
        Ax = []
        Ay = []
        b = np.zeros(w*h)
        for i in range(0,h):
            #print(i/h*100)
            for j in range(0,w):
                if mask[i*w + j] >= 0.5:
                    b[i*w + j] = f[i*w + j]
                    #A[i*w + j, i*w + j] = 1
                    Av.append(1)
                    Ax.append(i*w + j)
                    Ay.append(i*w + j)
                else:
                    b[i*w + j] = 0

                    if i >= 1 and i <= h-2 and j >= 1 and j <= w-2: # not on the boundaries
                        #A[i*w + j, i*w + j] = -4
                        Av.append(-4)
                        Ax.append(i*w + j)
                        Ay.append(i*w + j)
                        #A[i*w + j, (i+1)*w + j] = 1
                        Av.append(1)
                        Ax.append(i*w + j)
                        Ay.append((i+1)*w + j)
                        #A[i*w + j, (i-1)*w + j] = 1
                        Av.append(1)
                        Ax.append(i*w + j)
                        Ay.append((i-1)*w + j)
                        #A[i*w + j, i*w + j+1] = 1
                        Av.append(1)
                        Ax.append(i*w + j)
                        Ay.append(i*w + j+1)
                        #A[i*w + j, i*w + j-1] = 1
                        Av.append(1)
                        Ax.append(i*w + j)
                        Ay.append(i*w + j-1)
                    else: # Neumann BC
                        if (i==0 and j==0) or (i==0 and j==w-1) or (i==h-1 and j==0) or (i==h-1 and j==w-1): # on a corner
                            #A[i*w + j, i*w + j] = -2
                            Av.append(-2)
                            Ax.append(i*w + j)
                            Ay.append(i*w + j)
                            if (i==0 and j == 0):
                                #A[i*w + j, (i+1)*w + j] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append((i+1)*w + j)
                                #A[i*w + j, i*w + j+1] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append(i*w + j+1)
                            elif (i==0 and j == w-1):
                                #A[i*w + j, (i+1)*w + j] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append((i+1)*w + j)
                                #A[i*w + j, i*w + j-1] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append(i*w + j-1)
                            elif (i==h-1 and j == 0):
                                #A[i*w + j, (i-1)*w + j] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append((i-1)*w + j)
                                #A[i*w + j, i*w + j+1] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append(i*w + j+1)
                            else:
                                #A[i*w + j, (i-1)*w + j] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append((i-1)*w + j)
                                #A[i*w + j, i*w + j-1] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append(i*w + j-1)
                        else: # not on a corner
                            if i == 0: # top
                                #A[i*w + j, i*w + j] = -3
                                Av.append(-3)
                                Ax.append(i*w + j)
                                Ay.append(i*w + j)
                                #A[i*w + j, (i+1)*w + j] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append((i+1)*w + j)
                                #A[i*w + j, i*w + j+1] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append(i*w + j+1)
                                #A[i*w + j, i*w + j-1] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append(i*w + j-1)
                            if i == h-1: # bottom
                                #A[i*w + j, i*w + j] = -3
                                Av.append(-3)
                                Ax.append(i*w + j)
                                Ay.append(i*w + j)
                                #A[i*w + j, (i-1)*w + j] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append((i-1)*w + j)
                                #A[i*w + j, i*w + j+1] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append(i*w + j+1)
                                #A[i*w + j, i*w + j-1] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append(i*w + j-1)
                            if j == 0: # left
                                #A[i*w + j, i*w + j] = -3
                                Av.append(-3)
                                Ax.append(i*w + j)
                                Ay.append(i*w + j)
                                #A[i*w + j, (i+1)*w + j] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append((i+1)*w + j)
                                #A[i*w + j, (i-1)*w + j] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append((i-1)*w + j)
                                #A[i*w + j, i*w + j+1] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append(i*w + j+1)
                            if j == w-1: # right
                                #A[i*w + j, i*w + j] = -3
                                Av.append(-3)
                                Ax.append(i*w + j)
                                Ay.append(i*w + j)
                                #A[i*w + j, (i+1)*w + j] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append((i+1)*w + j)
                                #A[i*w + j, (i-1)*w + j] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append((i-1)*w + j)
                                #A[i*w + j, i*w + j-1] = 1
                                Av.append(1)
                                Ax.append(i*w + j)
                                Ay.append(i*w + j-1)

        self.A = sparse.csc_matrix((Av, (Ax, Ay)), shape=[w*h,w*h])
        self.b = b
        
    def process(self):
        return linsolve.spsolve(self.A, self.b)