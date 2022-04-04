#Created by Ricky Huang
'''Initialization for the Time Model algorithm
   With Neuron grid set up'''
import numpy as np
from NrnResponse import *
from NSclasses import *
from ModelUtil import *
from NeuronGrid import getNeuronGrid


def MicroInitialization(nodes, micro = 1):
    '''Initializes Neuron grid'''
    assert(nodes >= 3)
    
    Grid = Mygrid(1, 1, 50, 50)

    neurons, Axis = getNeuronGrid(nodes, micro = 3, flag = 0)
    
    return neurons, Axis, Grid

'''Iteration in time model ver.1.2.3'''
def TimeModelwithMicro(number, total, time_off, 
                       micro = 3, radius= 1, 
                       stim_x= 0, stim_y= 0, stim_theta= np.pi/2,
                       gamma = 1, sigma = 1, exp = 2,
                      ):
    T = total 
    nodes = number
    
    S_ti = []
    #for i in range(time_off):
    #    S_ti.append(MyPtStm(-0.5+i/time_off, -0.5-i/time_off, np.pi/4))
        
        
    Sti = MyPtStm(stim_x, stim_y, stim_theta) #initial point stimulus
    
    S_t = []
    T_on = 0; T_off = time_off
    for i in range(T):
        if (i < T_off):
            #S_t.append(S_ti[i])
            S_t.append(Sti)
        else:
            S_t.append(0)
    #initialization here
    neurons, Axis, Grid = MicroInitialization(nodes, micro)
    X = []
    Y = []

    weights = []
    #calculate the weights for each neuron
    for i in range(len(neurons)):
        target = neurons[i]
        rest_neurons = np.delete(neurons,i)
        weight = CircularRFwt(target, rest_neurons, radius)
        weights.append(weight)
    
    if S_t[0] != 0:
        X.append(GetRes(nodes, neurons, S_t[0], Grid, micro))
        #print('len:X[0],',len(X[0]))
        z = WeightRes(weights, nodes, neurons, X[0], micro)
        #print('len:z,',len(z))
    else:
        X.append(np.zeros(nodes**2*(micro**2))) #new
        z = 0
    Y.append(NormalizeRes(nodes, neurons, X[0], z, micro, 
                          gamma=gamma, sigma=sigma, exp=exp))
    #print('len:Y[0],',len(Y[0]))
    #check(neurons, Y[0], number, micro)
    
    
    
    for i in range(1,T):
        if S_t[i] != 0:
            X.append(GetRes(nodes, neurons, S_t[i], Grid, micro))
            z =  WeightRes(weights, nodes, neurons, X[i]+Y[i-1], micro) #update
        else:
            X.append(np.zeros(nodes**2*(micro**2))) #new
            z = WeightRes(weights, nodes, neurons, Y[i-1], micro)
        Y.append(NormalizeRes(nodes, neurons, Y[i-1]+X[i], z, micro,
                              gamma=gamma, sigma=sigma, exp=exp)) #update
        
    
    return neurons, Axis, Y, X

'''Runs Simulation for T = t_total steps'''
def run(n, t_total, t_off, micro, **kwargs):
    neurons, Axis, Y, X = TimeModelwithMicro(n, t_total, t_off, **kwargs)
    Xglobal, Yglobal = Axis[0], Axis[1]
    
    N = len(Y)
    MatrixY = []
    #first frame is the un-normalized response
    Xtmp = ToMatrix(n,X[0],micro)
    Ntmp = ToMatrix(n,neurons,micro)
    container = np.zeros((len(Xglobal),len(Yglobal)))
        
    for j in range(n*micro):
        for k in range(n*micro):
            container[Ntmp[j,k].Xind,Ntmp[j,k].Yind] = Xtmp[j,k]
    MatrixY.append(container)
    
    for i in range(N):
        container = np.zeros((len(Xglobal),len(Yglobal)))
        Ytmp = ToMatrix(n,Y[i],micro)
        assert(Ntmp.shape == Ytmp.shape)
        
        for j in range(n*micro):
            for k in range(n*micro):
                container[Ntmp[j,k].Xind,Ntmp[j,k].Yind] = Ytmp[j,k]

        MatrixY.append(container)
    return Xglobal, Yglobal, MatrixY, Y, X[0]

#neur_grid, _, = getNeuronGrid(3, micro=3)
#visualizeGridRF9x9(neur_grid)
#visualizeGridWt9x9(neur_grid)
#visualizeSingleWt9x9(neur_grid)