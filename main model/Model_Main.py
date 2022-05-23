#Created by Ricky Huang
'''Main function and animation production'''
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

def getAnimation(Xaxis, Yaxis, MatrixY, size, flag):
    '''Plot all time frames' heatmaps in one ANIMATION'''
    fr = len(MatrixY)
    fig,ax = plt.subplots(figsize = (6,6))
    def animate(i):
        ax.clear()
        ax.axis('off')
        if flag == 1: #contour plot
            ax.contourf(Xspace, Yspace, MatrixY[i], cmap='hot')
        if flag == 2: #seaborn heatmap
            sns.heatmap(MatrixY[i], cmap='hot', ax=ax, cbar=False)
        ax.set_title('T = %03d'%(i)) 

        
    ani =  matplotlib.animation.FuncAnimation(fig,animate,frames=fr,
                                              interval=300,blit=False)
    #ani.save('(7x3).gif',  writer='pillow', fps=10)
    ani.show()
    


def MatrixPlot(Xspace, Yspace, MatrixY, size, flag):
    '''Plot all time frames' heatmaps in STATIC plots'''
    N = len(MatrixY)

    fig, axes = plt.subplots(int(N/5), 5, figsize = [20,20])
    if flag == 1 :#contour plot
        for i in range(N):
            ax = axes[int(i/5),(i%5)]
            ax.axis('off')
            if (i > 0):
                ax.title.set_text('T = {}'.format(i-1))
            else:
                ax.title.set_text('Pre-normalized')

            #add colorbar
            divider = make_axes_locatable(ax)
            cax = divider.append_axes('right', size='5%', pad=0.05)

            im = ax.contourf(Xspace, Yspace, MatrixY[i],  cmap='hot')
            fig.colorbar(im, cax=cax, orientation='vertical')
            
    if flag == 2 :#seaborn heatmap plot
        i = 0
        for ax in axes.flat:
            ax.axis('off')
            if (i > 0):
                ax.title.set_text('T = {}'.format(i-1))
            else:
                ax.title.set_text('Pre-normalized')
            sns.heatmap(MatrixY[i],ax=ax, cmap='hot', cbar=True)
            i += 1
    plt.suptitle("Normalizaiton heatmaps in {}-neuron grid".format(size), fontsize=14)  



'''run this function to see animation'''
def main():
    #T = 30
    #t_off = 5
    #macro neuron per row = 10
    #micro neuron per row = 3
    x = np.random.rand()-0.5 #random from [-0.5, 0.5)
    y = np.random.rand()-0.5 #random from [-0.5, 0.5)
    theta = np.random.rand()*np.pi #random from [0, pi)
    
    '''might take a while (1min)'''
    Xaxis, Yaxis, MatrixY, Y, Xinit = run(10, 30, 10, 
                           micro=3, radius=4, 
                           stim_x=x, stim_y=y, stim_theta=theta,
                           gamma=1, sigma=1, exp=2,)
    getAnimation(Xaxis, Yaxis, MatrixY, 2)
    #MatrixPlot(Xaxis, Yaxis, MatrixY, 2)
    print(len(Y[0]))
    print(len(Xinit))
    print(np.where(Xinit == max(Xinit)))
    print(np.where(Y[0] == max(Y[0])))
    print(max(Xinit))
    print(max(Y[0]))
    
main()
