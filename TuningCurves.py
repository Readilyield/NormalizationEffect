#Created by Ricky Huang
#Low-level functions for generating Gaussian field and tuning curves
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def FindNearest(array, value):
    ind = (np.abs(array - value)).argmin()
    return ind

def UseMax(arrSmall, arrBig):
    assert(len(arrSmall) <= len(arrBig))
    for i in range(len(arrSmall)):
        if (arrSmall[i] > arrBig[i]):
            arrBig[i] = arrSmall[i]
    return arrBig

'''1D gaussian pdf that has wraparound property'''
def GaussPDFwrap(start, end, mu, sigma, Xspace):
    delX = Xspace[1]-Xspace[0]
    n = (end-start)/delX
    Y = np.zeros(len(Xspace))
    left = mu-3*sigma
    right = mu+3*sigma
    head = start
    tail = end
    
    Y = stats.norm.pdf(Xspace, mu, sigma)
    
    if(left < 0):
        #left wrap-around
        head = end+left
        ind_head = FindNearest(Xspace, head)
        siz = len(Y[ind_head:])
        x1 = np.arange(left, start+delX, delX)[:siz]
        #use the larger pdf value for left tail (on the right side of graph)
        Y[ind_head:] = UseMax(Y[ind_head:], stats.norm.pdf(x1, mu, sigma))
        
    if(right > end):
        #right wrap-around
        tail = right-end
        ind_tail = FindNearest(Xspace, tail)
        siz = len(Y[:ind_tail])
        x1 = np.arange(end, right+delX, delX)[:siz]
        #use the larger pdf value for right tail (on the left side of graph)
        Y[:ind_tail] = UseMax(Y[:ind_tail], stats.norm.pdf(x1, mu, sigma))
        
    return Y

'''2D gaussian graph'''
def GaussPDFin2D(mu, Sigma, pos):
    #cited from https://stackoverflow.com/a/55737551
    n = mu.shape[0]
    Sigma_det = np.linalg.det(Sigma)
    Sigma_inv = np.linalg.inv(Sigma)
    N = np.sqrt((2*np.pi)**n * Sigma_det)

    fac = np.einsum('...k,kl,...l->...', pos-mu, Sigma_inv, pos-mu)

    return np.exp(-fac / 2) / N

'''-----Tuning curve functions-----'''
'''1D and 2D Gaussian Tuning curves'''
'''Change Sigma (var) HERE'''
def OrientTuningCurve(theta, X):
    #generates tuning curve w.r.t. to the given theta (preferred orientation)
    #num = number of nodes in the interval [0, pi]
    assert(0 <= theta and theta <= np.pi)
    [mu, var] = theta, 0.5
    return GaussPDFwrap(0, np.pi, mu, var, X)

def PosTuningCurve(x, y, X, Y):
    #generates tuning curve w.r.t. to the given center (x, y)
    #num = number of nodes in the interval [-10,10] x [-10,10]
    assert(X[0] <= x and x <= X[-1])
    assert(Y[0] <= y and y <= Y[-1])
    mu = np.array([x, y])
    Sigma = np.array([[5 , 0.], [0.,  5]])
    X, Y = np.meshgrid(X, Y)
    pos = np.empty(X.shape + (2,))
    pos[:, :, 0] = X
    pos[:, :, 1] = Y
    Res = GaussPDFin2D(mu, Sigma, pos)
    return Res