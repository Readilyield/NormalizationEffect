#Created by Ricky Huang
from TuningCurves import *

#Grid class that contains the neuron receptive field
class Mygrid:
    def __init__(self, xlim, ylim, tnum, xnum):
        self.xylim = [xlim, ylim]
        self.tnum = tnum
        self.xnum = xnum
    
    def info(self):
        txt = "Grid size: [{0}, {1}] x [{2}, {3}]".format(-1*self.xylim[0],
                            self.xylim[0], -1*self.xylim[1], self.xylim[1])
        print(txt, end="\n")
        txt2 = "Orient nodes num: {0}, Pos nodes num : {1} x {1}".format(
                self.tnum, self.xnum)
        print(txt2, end="\n")
    
    def out(self):
        return [self.xylim, self.tnum, self.xnum]



'''My neuron class with preferred 2D position and 1D orientation in radian'''
#neuron class
class MyNrn:
    def __init__(self, x, y, Xind, Yind, theta, Mygrid):
        self.x = x
        self.y = y
        self.Xind = Xind
        self.Yind = Yind
        self.theta = theta
        self.grid = Mygrid
    
    def info(self):
        print("Preferred pos: (" + self.x, self.y, 
            + "), Preferred orient: " + self.theta)
    
    def out(self):
        return [self.x, self.y, self.theta]
    
    def OrientCurve(self):
        A = np.linspace(0, np.pi, self.grid.tnum, endpoint = True)
        return OrientTuningCurve(self.theta, A)

    def PosCurve(self):
        [xlim, ylim] = self.grid.xylim
        X = np.linspace(-1*xlim, xlim, self.grid.xnum, endpoint = True)
        Y = np.linspace(-1*ylim, ylim, self.grid.xnum, endpoint = True)
        return PosTuningCurve(self.x, self.y, X, Y)
    
    def __repr__(self):
        return f'object of class MyNrn:\nx={self.x}\ny={self.y}\ntheta={self.theta}\ngrid={self.grid}'
        

#Point Stimulus class (vector)
class MyPtStm:
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
    
    def info(self):
        print("Stimulus pos: (" + self.x, self.y, 
            + "), Stimulus orient: " + self.theta)
    
    def out(self):
        return [self.x, self.y, self.theta]
