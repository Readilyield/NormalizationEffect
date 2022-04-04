#Created by Ricky Huang
'''Main function to find viable radii'''
'''Files needed in the same folder:
    InitializationTimeMd.py
    NeuronGrid.py
    ModelUtil.py'''
from InitializationTimeMd import run
import matplotlib as plt
import matplotlib.animation
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.axes_grid1 import make_axes_locatable
import seaborn as sns

def testRadius(n, flag = 0, k = 0):
    
    if (flag == 1): 
        r = np.linspace(1.+k,0.05,num=20+int(-1*k/0.05), endpoint=True)
    else:
        r = np.linspace(1.,0.05,num=20, endpoint=True)
    Yarray = []
    Xarray = []
    x = np.random.rand()-0.5 #random from [-0.5, 0.5)
    y = np.random.rand()-0.5 #random from [-0.5, 0.5)
    theta = np.random.rand()*np.pi #random from [0, pi)
    for i in range(len(r)):
        
        Xaxis, Yaxis, MatrixY, Y, Xinit = run(n, 20, 10, 
                           micro = 3, radius=r[i], 
                           stim_x=x, stim_y=y, stim_theta=theta,
                           gamma = 1, sigma = 1, exp = 2,)
        assert(len(Y[0])==len(Xinit))
        Xarray.append(np.where(Xinit == max(Xinit))[0][0])
        Yarray.append(np.where(Y[0] == max(Y[0]))[0][0])
        if(Xarray[i]==Yarray[i]):
            #print('best r: ',r[i])
            #print('max ind: ',Xarray[i])
            return r[i]
        
    #print('no suitable radius')
    return 0
 
def histRadius(n, m = 3):
    radii = []
    flag = 0; k = 0
    for i in range(30):
        radii.append(testRadius(n, flag, k))
        if (radii[-1] < 0.5):
            flag = 1
            if (k > 0.2): k -= 0.1
        else:
            flag = 0;
            
    print('mean for n = {0}: {1}'.format(n,np.mean(radii)))
    return radii, np.mean(radii), np.std(radii), n*n*m*m

def getRadiusData(start,end,m = 3):
    N = end-start+1
    radiiData = [0]*N
    meanData = [0]*N
    stdData = [0]*N
    size = [0]*N
    for i in range(N):
        radiiData[i], meanData[i], stdData[i], size[i] = histRadius(i+start)
        assert(i+start <= end)
    return radiiData, meanData, stdData, size
            

#radiiData, meanData, stdData, size = getRadiusData(3,8,m = 3)

# plt.hist(radii)
# text = 'Viable radii for {}-neuron Neuron grid'.format()
# plt.title(text)
