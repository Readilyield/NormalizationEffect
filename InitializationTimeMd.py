#Created by Ricky Huang
'''Initialization for the Time Model algorithm
   With Neuron grid set up'''
import numpy as np
from NrnResponse import *
from NSclasses import *
from ModelUtil import *
from NeuronGrid import *


def MicroInitialization(nodes, micro = 1):
    '''Initializes Neuron grid'''
    assert(nodes >= 4)
    
    Grid = Mygrid(1, 1, 50, 50)

    neurons, h = getNeuronGrid(nodes, micro = 3, flag = 0)
    
    #Xgrid and Ygrid within [-1, 1]x[-1, 1] 
    Xspace = np.linspace(-1+0.5-h, 1-0.5+h, 
                         num=nodes*micro, endpoint=True)
    Yspace = np.linspace(-1+0.5-h, 1-0.5+h, 
                         num=nodes*micro, endpoint=True)
    
    return Xspace, Yspace, neurons, Grid

'''Normalization Time Model ver.1.2'''
def TimeModelwithMicro(number, total, time_off, micro = 1):
    T = total 
    nodes = number
    Sti = MyPtStm(0, 0, np.pi/2) #initial point stimulus
    S_t = []
    T_on = 0; T_off = time_off
    for i in range(T):
        if (i < T_off):
            S_t.append(Sti)
        else:
            S_t.append(0)
    #initialization here
    Xspace, Yspace, neurons, Grid = MicroInitialization(nodes, 
                                                    micro = 3)
    X = []
    Y = []

    if S_t[0] != 0:
        X.append(GetRes(nodes, neurons, S_t[0], Grid, micro))
        z = WeightRes(nodes, neurons, X[0], micro)
    else:
        X.append(np.zeros(nodes**2*(micro**2))) #new
        z = 0
    Y.append(NormalizeRes(nodes, neurons, X[0], z, micro))
    for i in range(1,T):
        if S_t[i] != 0:
            X.append(GetRes(nodes, neurons, S_t[i], Grid, micro))
            z =  WeightRes(nodes, neurons, X[i]+Y[i-1], micro) #update
        else:
            X.append(np.zeros(nodes**2*(micro**2))) #new
            z = WeightRes(nodes, neurons, Y[i-1], micro)
        #update
        Y.append(NormalizeRes(nodes, neurons, Y[i-1]+X[i], z, micro)) 
        
    
    return Xspace, Yspace, Y

'''Runs Simulation for T = t_total steps'''
def run(n, t_total, t_off):
    Xspace, Yspace, Y = TimeModelwithMicro(n, t_total, t_off, micro = 3)
    Xind, Yind, GbX, GbY = getGlobalAxis(Xspace, Yspace)
    Xleft = Xind[0]; Xright = Xind[1];
    Yleft = Yind[0]; Yright = Yind[1];
    N = len(Y)
    MatrixY = []
    
    for i in range(N):
        container = np.zeros((len(GbX),len(GbY)))
        container[Xleft:Xright+1, Yleft:Yright+1] = ToMatrix(n,Y[i], micro = 3)
        MatrixY.append(container)
    return GbX, GbY, MatrixY, Y