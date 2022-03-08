#Created by Ricky Huang
'''Uniform-grid set up
   n x n neuron spatial receptive field in a uniform grid'''
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from NrnResponse import *
from NSclasses import *
from mpl_toolkits.axes_grid1 import ImageGrid

def PlotUniformGrid(num, neurons):
    #Plot receptive fields of neurons in a uniform grid set-up
    assert(len(neurons) == num**2)
    neuron_im = [0]*(num**2)
    
    for i in range(num):
        for j in range(num):
            neuron_im[i+j*num] = neurons[i+j*num].PosCurve()
            
    fig = plt.figure(figsize=(10, 10))
    plt.title('Uniform-grid Spatial R-Fields for {} neurons'.format(num**2), 
              fontsize = 16)
    plt.axis('off')
    
    grid = ImageGrid(fig, 111,  # similar to subplot(111)
             nrows_ncols=(num, num),  # creates grid of axes
             axes_pad=0.3,  # pad between axes in inch.
             share_all = True,
             )
    for ax, im in zip(grid, neuron_im):
        # Iterating over the grid returns the Axes.
        ax.imshow(im, extent = [-1, 1, -1, 1], aspect='auto')

    plt.show()

def GetUniformGrid(nodes, flag = 0):
    assert(nodes >= 5)
    
    Grid = Mygrid(1, 1, 50, 50)
    Tar = MyNrn(0, 0, np.pi/2, Grid)
    Stimu = MyPtStm(0.1, -0.1, np.pi/2-0.1) #slight offset from target
    #Xgrid and Ygrid within [-1, 1]x[-1, 1] 
    
    '''cell distance = 1/(nodes-1)'''
    '''cellRF center boundary [-0.5, 0.5]'''
    Xspace = np.linspace(-1+0.5, 1-0.5, num=nodes, endpoint=True)
    Yspace = np.linspace(-1+0.5, 1-0.5, num=nodes, endpoint=True)
    
    #Xspace = np.delete(Xspace, np.where(abs(Xspace-Tar.x) < 0.2))
    #Yspace = np.delete(Yspace, np.where(abs(Yspace-Tar.y) < 0.2))
    
    Neurons = [0]*(nodes**2)
    Res = [0]*(nodes**2)
    
    for i in range(nodes):
        for j in range(nodes):
            x = Xspace[i]
            y = Yspace[j]
            Neurons[i+j*nodes] = MyNrn(x, y, 
                                             (i+j*nodes)*np.pi/(nodes**2), Grid)
            Res[i+j*nodes] = NrnResponse(Neurons[i+j*nodes], Stimu, Grid)
            
    ini =  NrnResponse(Tar, Stimu, Grid)
    ini_m = sum(Res)
    
    if (flag == 1):
        PlotUniformGrid(nodes, Neurons)
    else:
        print(ini, ini_m)
        return ini, ini_m
