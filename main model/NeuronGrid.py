#Created by Ricky Huang
'''Creates Micro+Macro combined Neuron Grid'''
import numpy as np
from NrnResponse import *
from NSclasses import *
import matplotlib.pyplot as plt
import seaborn as sns

'''Creates nxn Macro grid'''
def getMacroGrid(nodes):
    #generate a MacroGrid for nxn spatial preferences
    assert(nodes >= 3)
    
    Grid = Mygrid(1, 1, 50, 50)
    #Xgrid and Ygrid within [-1, 1]x[-1, 1] 
    Xspace = np.linspace(-1+0.5, 1-0.5, num=nodes, endpoint=True)
    Yspace = np.linspace(-1+0.5, 1-0.5, num=nodes, endpoint=True)
    h = Xspace[1] - Xspace[0]
    
    MacroNeurons = [0]*(nodes**2)
    for i in range(nodes):
        for j in range(nodes):
            x = Xspace[i]
            y = Yspace[j]
            MacroNeurons[i+j*nodes] = MyNrn(x, y, 
                                             4*np.pi/9, Grid)
    #orientation preference defined based on mid index in 3x3 micro grid
    return MacroNeurons, Grid, h


'''Creates 3x3 Micro grid'''
def getMicroGrid(Neuron, h, Grid, micro = 3):
    #for a neuron in the MacroGrid
    #generate 8 surrounding MicroGrid neurons
    #return a 3x3 matrix
    MicroNeurons = [([0]*micro) for i in range(micro)] #fix 3x3
    diff = h/micro
    x, y, the = Neuron.out()
    for i in range(micro):
        for j in range(micro):
            MicroNeurons[j][i] = MyNrn(x+(j-1)*diff, y+(1-i)*diff, 
                                (j+i*micro)*np.pi/(micro**2), Grid)
            
    temp = MicroNeurons[1][1]
    temp_x, temp_y, temp_the = temp.out()
    assert(x == temp_x and y == temp_y and the == temp_the)
    return MicroNeurons

def MicroGridPlot(neurons):
    num = len(neurons)
    X = np.linspace(neurons[0].x -0.5, neurons[-1].x +0.5, 
                         num=50, endpoint=True)
    Y = np.linspace(neurons[0].y +0.5, neurons[-1].y -0.5, 
                         num=50, endpoint=True)
    Z = np.zeros((50, 50))
    
    x = [0]*num
    y = [0]*num
    for i in range(num):
        x[i] = neurons[i].x
        y[i] = neurons[i].y
    
    return x, y

'''Finds the index in array such that array[index] is closest to value'''
def FindNearest(array, value):
    ind = (np.abs(array - value)).argmin()
    return ind

'''Creates the Neuron Grid'''
def getNeuronGrid(nodes, micro = 3, flag=0):
    """
    Nick's version, modified by Ricky
    """
    assert(nodes >= 3)
    assert(micro%2 == 1)
    
    allNeurons = []
    Grid = Mygrid(1, 1, 50, 50)
    #Xgrid and Ygrid within [-1, 1]x[-1, 1] 
    Xspace = np.linspace(-1+0.5, 1-0.5, num=nodes, endpoint=True)
    Yspace = np.linspace(-1+0.5, 1-0.5, num=nodes, endpoint=True)
    
    #XspaceAll = np.linspace(-1+0.5, 1-0.5, num=nodes*micro, endpoint=True)
    hx = (Xspace[1] - Xspace[0])/micro
    Xglobal = np.arange(-1, 1+hx, hx)
    
    
    #YspaceAll = np.linspace(-1+0.5, 1-0.5, num=nodes*micro, endpoint=True)
    hy = (Yspace[1] - Yspace[0])/micro
    Yglobal = np.arange(-1, 1+hy, hy)
    
    orientations = np.linspace(0, np.pi, micro**2)
    
    allNeurons = []
    for i in range(nodes):
        for micro_i in range(micro):
            for j in range(nodes):
                for micro_j in range(micro):
                    micro_n = micro*(micro_i) + micro_j
                    # i will end up as the row dimension, which is actually y
                    # j will end up as the col dimension, which is actually x
                    x = Xspace[j]
                    y = Yspace[i]
                    
                    Xnode = Xglobal[FindNearest(Xglobal, x - hx*(micro-1)/2)]
                    Xind = int(np.where(Xglobal == Xnode)[0][0]+micro_j)
                    
                    Ynode = Yglobal[FindNearest(Yglobal, y - hy*(micro-1)/2)]
                    Yind = int(np.where(Yglobal == Ynode)[0][0]+micro_i)
                    
                    neuron = MyNrn(x, y, Xind, Yind, orientations[micro_n], Grid)
                    allNeurons.append(neuron)
                    
    Axis = [Xglobal, Yglobal]
    return allNeurons, Axis

def checkNeuronGrid():
    '''Created by Nick'''
    neur_grid, _, = getNeuronGrid(3, micro=3, flag = 100)
    resps = []
    for ii in range(len(neur_grid)):
        resps.append(neur_grid[ii].x)
    sns.heatmap(np.array(resps).reshape(9,9))
    plt.title('x location')
    plt.show()

    resps = []
    for ii in range(len(neur_grid)):
        resps.append(neur_grid[ii].y)
    sns.heatmap(np.array(resps).reshape(9,9))
    plt.title('y location')
    plt.show()

    resps = []
    for ii in range(len(neur_grid)):
        resps.append(neur_grid[ii].theta)
    sns.heatmap(np.array(resps).reshape(9,9))
    plt.title('theta')
    plt.show()

    resps = []
    for ii in range(len(neur_grid)):
    #     print(MacroNeurons[ii])
        resp = NrnResponse(neur_grid[ii],  MyPtStm(0,0, np.pi/2), neur_grid[ii].grid)
        resps.append(resp)
    sns.heatmap(np.array(resps).reshape(9,9))
    plt.title('response to point stimulus')
    plt.show()

def visualizeNeuronGrid():
    '''Created by Nick'''
    neur_grid, _, = getNeuronGrid(3, micro=3, flag = 100)
    from mpl_toolkits.axes_grid1 import ImageGrid
    neur_grid_curves = [neur_grid[ii].PosCurve() for ii in range(81)]

    fig = plt.figure(figsize=(10., 10.))
    grid = ImageGrid(fig, 111,  # similar to subplot(111)
                    nrows_ncols=(9, 9),  # creates 2x2 grid of axes
                    axes_pad=0.01,  # pad between axes in inch.
                    )

    for ax, im in zip(grid, neur_grid_curves):
        # Iterating over the grid returns the Axes.
        ax.imshow(im)

    plt.show()

#visualizeNeuronGrid()

'''!!!This is an old version with many bugs'''
# def getNeuronGrid(nodes, micro = 3, flag = 0):
#     #nodes = number of neurons in the MacroGrid
    
#     MacroNeurons, Grid, h = getMacroGrid(nodes)
#     allNeurons = [0] * (nodes**2 * micro**2)
    
    
#     MatrixNeuron = getMicroGrid(MacroNeurons[0], h, Grid, micro = 3)
#     for j in range(1,nodes):
#         temp = getMicroGrid(MacroNeurons[j], h, Grid)
#         MatrixNeuron = np.vstack((temp, MatrixNeuron))
    
#     for i in range(1,nodes):
#         temp_col = getMicroGrid(MacroNeurons[i*nodes], h, Grid)
#         for j in range(1,nodes):
#             temp = getMicroGrid(MacroNeurons[j+i*nodes], h, Grid)
#             temp_col = np.vstack((temp, temp_col))
#         MatrixNeuron = np.hstack((MatrixNeuron, temp_col))
    
#     allNeurons = np.reshape(MatrixNeuron, (1, nodes**2 * micro**2))[0]
    
#     '''Plots the neuron grid'''
#     if (flag == 100): #plot micro-grid neuron centers
#         allNeurons = np.flip(allNeurons)
#         fig, axes = plt.subplots(nodes,nodes,figsize = [9,8])
        
#         for i in range(nodes):
#             for j in range(nodes):
#                 ax = axes[i,j]
#                 r = i*micro
#                 c = j*nodes*micro**2
#                 temp1 = allNeurons[r+c:r+c+micro]
#                 temp1 = np.transpose(temp1)
#                 temp2 = allNeurons[r+c+nodes*micro:r+c+nodes*micro+micro]
#                 temp2 = np.transpose(temp2)
#                 temp3 = allNeurons[r+c+nodes*micro*2:r+c+nodes*micro*2+micro]
#                 temp3 = np.transpose(temp3)
#                 temp = np.hstack((temp1, temp2, temp3))
#                 x, y = MicroGridPlot(temp)
#                 ax.set_xlim(-1, 1)
#                 ax.set_ylim(-1, 1)
#                 cl = ['b']*micro**2
#                 cl[micro+1] = 'r'
#                 ax.scatter(x, y, color =cl, alpha=0.5)
#         fig.tight_layout()
#         title = '{2}x{3} MicroGrid in {0}x{1} MacroGrid'
#         st = fig.suptitle(title.format(nodes, nodes, micro, micro), 
#                           fontsize = 16)
#         st.set_y(0.95)
#         fig.subplots_adjust(top=0.9)
#         allNeurons = np.flip(allNeurons)
#         plt.show()

#     if (flag == 0):    
#         return allNeurons, h/3

#getNeuronGrid(3, flag = 100)