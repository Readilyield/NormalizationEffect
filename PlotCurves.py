#Created by Ricky Huang
#Plot tuning curves for MyNrn class
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from NrnResponse import *
from NSclasses import *

def plot_2D(data_info,title,input_label,output_label,axis_bounds=None,xscale=None,yscale=None):

    plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.xticks(fontsize=12, rotation=0)
    plt.yticks(fontsize=12, rotation=0)

    for info_cache in data_info:
        plt.plot(info_cache[0][0],info_cache[0][1],
        info_cache[1],label=info_cache[2],linewidth=1.5,markersize=3)

    plt.title(title,fontsize=24)
    plt.xlabel(input_label,fontsize=20)
    plt.ylabel(output_label,fontsize=20)
    if not axis_bounds == None:
        plt.axis(axis_bounds)
    if not xscale == None:
        plt.xscale(xscale)
    if not yscale == None:
        plt.yscale(yscale)
    plt.legend(loc='best',fontsize=14)
    plt.show()
    
def PlotOrientCurve(Mynrn, sti = None):
    assert(0 <= sti <= np.pi)
    [start, end] = 0, np.pi 
    num = Mynrn.grid.tnum
    space = np.linspace(start, end, num, endpoint = True)
    
    Y = Mynrn.OrientCurve()
    
    datainfo = [[[space, Y],'r-','MyNrn']]
    if (sti != None):
        line = np.arange(0,max(Y), 1/(30*max(Y)))
        datainfo = [[[space, Y],'r-','MyNrn'], [[[sti]*len(line),line], 'o', 'Stimulus line']]
    tlt = 'Tuning curve at mu = {0:.2f}'.format(Mynrn.theta)
    plot_2D(datainfo,
            title=tlt,
            input_label='orientation in radian',
            output_label='response')

def PlotPosCurve(Mynrn, x = None, y = None):
    [xlim, ylim] = Mynrn.grid.xylim
    X = np.linspace(-1*xlim, xlim, Mynrn.grid.xnum, endpoint = True)
    Y = np.linspace(-1*ylim, ylim, Mynrn.grid.xnum, endpoint = True)
    X, Y = np.meshgrid(X, Y)
    Z = Mynrn.PosCurve()
    plt.figure(figsize=(8, 6))
    plt.contourf(X, Y, Z, cmap='Reds')
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    tlt = 'Tuning curve centered at [{0:.2f}, {1:.2f}]'.format(Mynrn.x, Mynrn.y)
    plt.title(tlt,fontsize=20)
    
    if ((x != None) and (y != None)):
        assert(-1*xlim <= x <= xlim)
        assert(-1*ylim <= y <= ylim)
        plt.plot(x,y, 'o', label ='Stimulus', markersize=10)
        plt.legend(loc='best')
    plt.xlim = ([-1*xlim, xlim])
    plt.ylim = ([-1*ylim, ylim])
    plt.colorbar()
    plt.show()


def test():
    Grid = Mygrid(10, 10, 50, 50)
    Myneuron = MyNrn(2.5, 2.5, np.pi/4, Grid)
    Mystimu = MyPtStm(3.5, 4.5, np.pi/2)
    PlotOrientCurve(Myneuron)
    PlotPosCurve(Myneuron)

#test()