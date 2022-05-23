#Created by Ricky Huang
'''Util functions for Time Model algorithm'''
import numpy as np
from NrnResponse import *
from NSclasses import *

'''this function might need some updates
    to deal with boundary neurons'''
def CircularRFwt(target, neurons, radius = 0.5):
    #target: input neuron to generate weights w.r.t others
    #neurons: the list of all other neurons in the same pool as the target
    N = len(neurons)
    r = min(target.grid.xylim)*radius 
    tar_x, tar_y, tar_th = target.x, target.y, target.theta
    weight = np.zeros(N)
    #neuron i in the list has weight i
    #count = 0
    for i in range(N):
        n_x, n_y, n_th = neurons[i].out
        
        dist = np.sqrt((tar_x-n_x)**2+(tar_y-n_y)**2+
                        (tar_th-n_th)**2)
        if dist > r:
            weight[i] = 0
        else:
            #count = count + 1
            weight[i] = 1 - dist/r
            
    #if count == 0:
        #count = count + 1
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

def WeightRes(weights, nodes, neurons, responses, micro = 1):
    '''Obtain weighted-sum response for all neurons
    Extract weights for each neuron: weight
    Compute weighted sum: res'''
    #responses = all responses from input/last step
    
    res = np.zeros(nodes**2*(micro**2))
    for i in range(len(res)):
        target = neurons[i]
        rest_neurons = np.delete(neurons,i)
        rest_res = np.delete(responses,i)
        #weight = CircularRFwt(target, rest_neurons) 
        #!!! store the weight somewhere else
        res[i] = WtResponse(rest_res, weights[i])
    return res

def NormalizeRes(nodes, neurons, responses, z, micro = 1, **kwargs):
    '''Normalization step1:
    Extract single neuron response: i_tar
    Extract pooled neurons weighted responses: i_pool'''
    #responses = all responses from input/last step
    #z = weighted-sum responses for all neurons

    res = np.zeros(nodes**2*(micro**2))
    for i in range(len(res)):
        i_pool = z[i]
        i_tar = responses[i]
        res[i] = NormalizedR(i_tar, i_pool, **kwargs)
    return res

def NormalizedR(ini, ini_m, gamma = 1, sigma = 1, exp = 2):
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

def visualizeGridRF9x9(neurgrid):
    '''Visualizes every neuron's spatial RF'''
    'Nick\'s version, modified by Ricky'
    neur_grid_curves = [neurgrid[ii].PosCurve() for ii in range(81)]

    fig = plt.figure(figsize=(10., 10.))
    grid = ImageGrid(fig, 111,  # similar to subplot(111)
                     nrows_ncols=(9, 9),  # creates 2x2 grid of axes
                     axes_pad=0.2,  # pad between axes in inch.
                     share_all=True)

    for ax, im in zip(grid, neur_grid_curves):
        # Iterating over the grid returns the Axes.
        ax.imshow(im, extent = [-1, 1, -1, 1], aspect='auto')

    plt.show()
    
def visualizeGridWt9x9(neurgrid):
    '''Visualizes every neuron's connective weight in the grid'''
    'Nick\'s version, modified by Ricky'
    neur_grid_curves = [CircularRFwt(neuron,neurgrid,radius=1).reshape(9,9) 
                        for neuron in neurgrid]
    # counts = [CircularRFwt(neuron, neur_grid, radius=1)[1] 
    #           for neuron in neur_grid]
    fig = plt.figure(figsize=(10., 10.))
    grid = ImageGrid(fig, 111,  # similar to subplot(111)
                     nrows_ncols=(9, 9),  # creates nxn grid of axes
                     axes_pad=0.2,  # pad between axes in inch.
                     share_all=True,
                     cbar_location="right",
                     cbar_mode="edge",
                     cbar_size="5%",
                     cbar_pad=0.3)

    for ax, data in zip(grid, neur_grid_curves):
        # Iterating over the grid returns the Axes.
        im = ax.imshow(data)

        ax.cax.colorbar(im)
    plt.show()
    
def visualizeSingleWt9x9(neurgrid):
    '''Visualizes a single neurons's connective weight in the grid'''
    'Nick\'s version, modified by Ricky'
    r = 4
    neur_grid_curves = [CircularRFwt(neuron,neurgrid,radius=r).reshape(9,9) 
                        for neuron in neurgrid]
    # counts = [CircularRFwt(neuron, neur_grid, radius=1)[1] 
    #           for neuron in neur_grid]
    fig = plt.figure(figsize=(8., 8.))
    grid = ImageGrid(fig, 111,  # similar to subplot(111)
                     nrows_ncols=(1, 1),  # creates nxn grid of axes
                     cbar_location="right",
                     cbar_mode="edge",
                     cbar_size="5%",
                     cbar_pad=0.3)
    #print(neur_grid_curves[0])
    for ax, data in zip(grid, [neur_grid_curves[0]]):
        # Iterating over the grid returns the Axes.
        im = ax.imshow(data)
        ax.cax.colorbar(im)
        
    ax.set_title('Single neuron circular weights, r = {}'.format(r))
    plt.show()
    
