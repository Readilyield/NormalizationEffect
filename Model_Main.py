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

def getAnimation(Xspace, Yspace, MatrixY, flag):
    '''Plot all time frames' heatmaps in one ANIMATION'''
    fr = len(MatrixY)
    fig,ax = plt.subplots(figsize = (6,6))
    def animate(i):
        ax.clear()
        ax.axis('off')
#         p?db.set_trace()
        if flag == 1: #contour plot
            ax.contourf(Xspace, Yspace, MatrixY[i], cmap='hot')
        if flag == 2: #seaborn heatmap
            sns.heatmap(MatrixY[i], cmap='hot', ax=ax, cbar=False)
        ax.set_title('T = %03d'%(i)) 

        
    ani =  matplotlib.animation.FuncAnimation(fig,animate,frames=fr,
                                              interval=200,blit=False)

    #ani.save('test.gif',  writer='pillow', fps=10)
    plt.show()

def MatrixPlot(Xspace, Yspace, MatrixY, flag):
    '''Plot all time frames' heatmaps in STATIC plots'''
    N = len(MatrixY)

    fig, axes = plt.subplots(int(N/5), 5, figsize = [20,20])
    if flag == 1 :#contour plot
        for i in range(N):
            ax = axes[int(i/5),(i%5)]
            ax.axis('off')
            ax.title.set_text('T = {}'.format(i+1))

            #add colorbar
            divider = make_axes_locatable(ax)
            cax = divider.append_axes('right', size='5%', pad=0.05)

            im = ax.contourf(Xspace, Yspace, MatrixY[i],  cmap='hot')
            fig.colorbar(im, cax=cax, orientation='vertical')
            
    if flag == 2 :#seaborn heatmap plot
        i = 0
        for ax in axes.flat:
            ax.axis('off')
            ax.title.set_text('T = {}'.format(i+1))
            sns.heatmap(MatrixY[i],ax=ax, cmap='hot', cbar=True)
            i += 1
            



'''run this function to see animation'''
def main():
    #T = 30
    #t_off = 5
    #macro neuron per row = 10
    #micro neuron per row = 3
    '''might take a while (1min)'''
    GbX, GbY, MatrixY, Y = run(10, 30, 5)
    getAnimation(GbX, GbY, MatrixY, 2)
    #MatrixPlot(GbX, GbY, MatrixY, 2)

main()
