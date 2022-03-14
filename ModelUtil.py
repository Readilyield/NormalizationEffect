#Created by Ricky Huang
'''Util functions for Time Model algorithm'''
import numpy as np
from NrnResponse import *
from NSclasses import *

'''this function might need some updates
    to deal with boundary neurons'''
def CircularRFwt(target, neurons):
    #target: input neuron to generate weights w.r.t others
    #neurons: the list of all other neurons in the same pool as the target
    N = len(neurons)
    r = min(target.grid.xylim)/2 
    '''radius = quarter of box side length'''
    tar_x, tar_y = target.x, target.y
    weight = np.zeros(N)
    #neuron i in the list has weight i
    count = 0
    for i in range(N):
        n_x, n_y = neurons[i].x, neurons[i].y
        dist = np.sqrt((tar_x-n_x)**2+(tar_y-n_y)**2)
        if dist > r:
            weight[i] = 0
        else:
            count = count + 1
            weight[i] = 1 - dist/r
            
    if count == 0:
        count = count + 1
    #return weight/count this part needs debugging
    return weight

def WtResponse(response, weight):
    '''returns the weighted sum of summation field'''
    assert(len(response) == len(weight))
    #response from neuron i is assigned with weight i
    return sum(weight*response)

def GetRes(nodes, neurons, stimu, Grid, micro = 1):
    '''Obtain input response for all neurons'''
    res = np.zeros(nodes**2*(micro**2))
    for i in range(len(res)):
        res[i] = NrnResponse(neurons[i], stimu, Grid)
    return res

def WeightRes(nodes, neurons, responses, micro = 1):
    '''Obtain weighted-sum response for all neurons
    Extract weights for each neuron: weight
    Compute weighted sum: res'''
    #responses = all responses from input/last step
    
    res = np.zeros(nodes**2*(micro**2))
    for i in range(len(res)):
        target = neurons[i]
        rest_neurons = np.delete(neurons,i)
        rest_res = np.delete(responses,i)
        weight = CircularRFwt(target, rest_neurons)
        res[i] = WtResponse(rest_res, weight)
    return res

def NormalizeRes(nodes, neurons, responses, z, micro = 1):
    '''Normalization step1:
    Extract single neuron response: i_tar
    Extract pooled neurons weighted responses: i_pool'''
    #responses = all responses from input/last step
    #z = weighted-sum responses for all neurons

    res = np.zeros(nodes**2*(micro**2))
    for i in range(len(res)):
        i_pool = z[i]
        i_tar = responses[i]
        res[i] = NormalizedR(i_tar, i_pool)
    return res

def NormalizedR(ini, ini_m, gamma = 1, sigma = 0, exp = 1):
    '''Normalization step2:
    Normalize single neuron's response'''
    #ini = target neuron's response
    #ini_m = other neurons' responses (weighted sum)
    nom = ini**exp
    denom = sigma**exp + ini_m**exp + nom
    return gamma* (nom/denom)

def ToMatrix(nodes,arr, micro = 1):
    '''Reshape an array of responses into matrix'''
    res = np.reshape(arr, (nodes*micro, nodes*micro))

    return res

def getGlobalAxis(Xspace, Yspace):
    '''Reconstruct the [-1,1]x[-1,1] global grid'''
    hx = Xspace[1]-Xspace[0]
    Xleft = np.arange(-1, Xspace[0], hx)
    Xright = np.arange(Xspace[-1], 1, hx)
    #global X axis
    GX = np.hstack([Xleft[:-1], Xspace, Xright[1:]])
    
    Xleft_ind = len(Xleft)-1
    Xright_ind = len(Xleft)+len(Xspace)-1-1
    
    hy = Yspace[1]-Yspace[0]
    Yleft = np.arange(-1, Yspace[0], hy)
    Yright = np.arange(Yspace[-1], 1, hy)
    #global Y axis
    GY = np.hstack([Yleft[:-1], Yspace, Yright[1:]])
    
    Yleft_ind = len(Yleft)-1
    Yright_ind = len(Yleft)+len(Yspace)-1-1
    
    return [Xleft_ind, Xright_ind], [Yleft_ind, Yright_ind], GX, GY