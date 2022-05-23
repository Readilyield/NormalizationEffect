#Created by Ricky Huang
#return neuron response w.r.t. point stimulus
import numpy as np
from NSclasses import *
from TuningCurves import *

#-----response fucntion-----
def NrnResponse(MyNrn, MyPtStm, grid):
    #returns the response of a neuron with preferred position and orientation
    #w.r.t. the stimulus position and orientation
    [x, y, theta] = MyNrn.out()
    [st_x, st_y, st_the] = MyPtStm.out()
    [[xlim, ylim],tnum, xnum] = grid.out()
    assert(0 <= theta and theta <= np.pi)
    assert(0 <= st_the and st_the <= np.pi)
    assert(-1*xlim <= x and x <= xlim)
    assert(-1*ylim <= y and y <= ylim)
    assert(-1*xlim-2 <= st_x and st_x <= xlim+2)
    assert(-1*ylim-2 <= st_y and st_y <= ylim+2)
    A = np.linspace(0, np.pi, tnum, endpoint = True)
    X = np.linspace(-1*xlim-2, xlim+2, xnum, endpoint = True)
    Y = np.linspace(-1*ylim-2, ylim+2, xnum, endpoint = True)
    st_x_ind = FindNearest(X, st_x)
    st_y_ind = FindNearest(Y, st_y)
    st_the_ind = FindNearest(A, st_the)
   
    Ro = OrientTuningCurve(theta, A)[st_the_ind]
    Rs = PosTuningCurve(x, y, X, Y)[st_x_ind, st_y_ind]
    return Ro * Rs #simple multiplication