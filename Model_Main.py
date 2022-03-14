#Created by Ricky Huang
'''Main function and animation production'''
'''Files needed in the same folder:
    InitializationTimeMd.py
    NeuronGrid.py
    ModelUtil.py'''
from InitializationTimeMd import *
import matplotlib.animation
from matplotlib.animation import FuncAnimation, PillowWriter 

def getAnimation(Xspace, Yspace, MatrixY):

    fr = len(MatrixY)
    fig,ax = plt.subplots(figsize = (6,6))
    def animate(i):
        ax.clear()
        ax.contourf(Xspace, Yspace, MatrixY[i], cmap='hot')
        ax.set_title('T = %03d'%(i)) 

        
    ani =  matplotlib.animation.FuncAnimation(fig,animate,frames=fr,
                                              interval=200,blit=False)

    #ani.save('testtt.gif',  writer='pillow', fps=10)
    plt.show()

'''run this function to see animation'''
def main():
    #T = 30
    #t_off = 5
    #macro neuron per row = 10
    #micro neuron per row = 3
    '''might take a while (1-2min)'''
    GbX, GbY, MatrixY, Y = run(10, 30, 5)
    getAnimation(GbX, GbY, MatrixY)

main()
