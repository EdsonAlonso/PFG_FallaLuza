# --------------------------------------------------------------------------------------------------
# Title: Grav-Mag Codes
# Author: Rodrigo Bijani and Edson Fallaluza
# Description: Source codes for plotting images.
# --------------------------------------------------------------------------------------------------

# Import Python libraries:
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pylab as py
from itertools import product, combinations

######################################################################################################
def draw_rectangle(prism, style='-k', linewidth=1, fill=None, alpha=1., label=None):
    """
    Plot a rectangle in a ax plotbox.

    Parameters:

    * area : list = [x1, x2, y1, y2]
        Borders of the rectangle
    * style : str
        String with the color and line style (as in matplotlib.pyplot.plot)
    * linewidth : float
        Line width
    * fill : str
        A color string used to fill the square. If None, the square is not
        filled
    * alpha : float
        Transparency of the fill (1 >= alpha >= 0). 0 is transparent and 1 is
        opaque
    * label : str
        label associated with the square.
    * xy2ne : True or False
        If True, will exchange the x and y axis so that the x coordinates of
        the polygon are north. Use this when drawing on a map viewed from
        above. If the y-axis of the plot is supposed to be z (depth), then use
        ``xy2ne=False``.

    Returns:

    * axes : ``matplitlib.axes``
        The axes element of the plot

    """
    xo, zo   = prism[0], prism[1]
    L = prism[2]
    A = prism[4]
    t = np.sqrt(A)
    # coordenadas finais do prism:
    x1 = xo + t # consideracao: tampa do prisma quadrada! (A = t**2) 
    z1 = zo 
    
    # coordenadas com a thickness da sheet:
    x2 = x1
    z2 = zo + L

    x3 = xo 
    z3 = zo + L # z positivo para baixo!

    xs = [xo, x1, x2, x3, xo]
    zs = [zo, z1, z2, z3, zo]    
    
    # x1, x2, y1, y2 = area
   # if xy2ne:
   #     x1, x2, y1, y2 = y1, y2, x1, x2
   # xs = [x1, x1, x2, x2, x1]
   # ys = [y1, y2, y2, y1, y1]
    return xs,zs


def draw_prism(ax,dike):
    
    """
    Plot a 3D view of the input dike in a ax plotbox.

    Parameters:

    * ax : box plot where figure goes
    
    * dike[size=0,6]: list with the corners and the dike and the density at last position.    
      dike[x1,x2,y1,y2,z1,z2,density] # all in SI
    
    Returns:
    * ax : ``matplitlib.axes``
        The axes element of the plot

    """
    # vertices of a prism
    x1, x2 = dike[0:2]
    y1, y2 = dike[2:4]
    z1, z2 = dike[4:6]
    
    v = np.array([[x1, y1, z1], [x1, y2, z1], [x2, y2, z1],  [x2, y1, z1], 
              [x1, y1, z2], [x1, y2, z2], [x2, y2, z2],  [x2, y1, z2]])
    
    # use scatter plot for plotting the vertices of the prism:
    #ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])

    # generate list of sides of our prism
    verts = [[v[0],v[1],v[2],v[3]], [v[0],v[1],v[5],v[4]], [v[1],v[2],v[6],v[5]],
         [v[2],v[3],v[7],v[6]], [v[3],v[0],v[4],v[7]], [v[4],v[5],v[6],v[7]]]

    # plot sides
    pc = Poly3DCollection(verts, alpha=0.3, linewidths=0.5, edgecolors='k')
    pc.set_facecolor('red')
    ax.add_collection3d( pc )

    # ------------ ALL THE ABOVE SHOULD BE PLACED IMMEDIATELY AFTER THE CALLING OF THE FUNCTION----------#
    #change size projection
    #x_scale=1.
    #y_scale=1.
    #z_scale=1.
    #scale=np.diag([x_scale, y_scale, z_scale, 1.0])
    #scale=scale*(1.0/scale.max())
    #scale[3,3]=1.0
    #def short_proj():
    #    return np.dot(Axes3D.get_proj(ax), scale)
    #ax.get_proj=short_proj

    # ----- labels (all these should be used outside of the function!)
    #ax.set_xlabel('Label here', labelpad=20 ,fontsize=14)
    #ax.set_ylabel('Label here', labelpad=20 ,fontsize=14)
    #ax.set_zlim(-1000,40000)
    #ax.set_zlabel('Depth (m)',labelpad=20 ,fontsize=14, rotation = 90)

    #visualization angle
    #ax.view_init(30, 10)
    #ax.invert_zaxis()
    #plt.tight_layout(True)
    return ax
   
######################################################################################################
def draw_finite_sheet(sheet,draw = True):
    '''This function recieves a list 'sheet' = [x_ini, z_ini, dens, dip, length, thickness] representating a rectangle and returns the coordinates of its vertices
    
    Inputs - 
    sheet -> list like [x_ini, z_ini, dens, dip, length, thickness]

    Outputs - 
    
    xs -> list meaning the x coordinates of the rectangle vertices
    ys -> list meaning the y coordinates of the rectangle vertices
    '''
    
    xo, zo   = sheet[0], sheet[1]
    d, alpha = sheet[4], (np.pi/2) + np.pi*sheet[3]/180 
    beta     = np.pi - alpha
    t = sheet[5]
    # coordendas finais da thin sheet:
    x1 = xo + d * np.cos(beta)
    z1 = zo + d * np.sin(beta)

    gamma = (np.pi/2.0) - beta
    # coordenadas com a thickness da sheet:
    x3 = xo + t * np.cos(gamma)
    z3 = zo - t * np.sin(gamma)

    x2 = x3 + d * np.cos(beta)
    z2 = z3 + d * np.sin(beta) # z positivo para baixo!

    xs = [xo, x1, x2, x3, xo]
    zs = [zo, z1, z2, z3, zo]
    
    if draw == True:
        plt.figure(figsize = (10,10),facecolor = 'w')
        plt.plot(xs,zs,'r')
        plt.fill(xs,zs, color='r', alpha=0.4)
        plt.xlim(xo-2 , x1 + 2)
        plt.ylim(0 , z1 + 2)
        plt.grid()
        plt.gca().invert_yaxis()
        plt.show()
    return xs,zs

######################################################################################################
def draw_infinite_sheet(sheet,xmax,draw = True):
    '''This function recieves a list 'sheet' = [x_ini, z_ini, dens, thickness] representating a infinite rectangle and returns the coordinates of its vertices and the
    xmax meanig the maximum value for the x coordinate observation
    
    Inputs - 
    sheet -> list like [x_ini, z_ini, dens, thickness]
    xmax -> float 
    
    Outputs - 
    xs -> list meaning the x coordinates of the infinite rectangle vertices
    ys -> list meaning the y coordinates of the infinite rectangle vertices
    '''
    
    xo, zo   = sheet[0], sheet[1]
    t = sheet[3]
    # coordendas finais da thin sheet:
    x1 = xmax 
    z1 = zo
    
    # coordenadas com a thickness da sheet:
    x2 = x1
    z2 = zo - t

    x3 = xo
    z3 = zo - t # z positivo para baixo!

    xs = [xo, x1, x2, x3, xo]
    zs = [zo, z1, z2, z3, zo]
    
    if draw == True:
        plt.figure(figsize = (10,10),facecolor = 'w')
        plt.plot(xs,zs,'r')
        plt.fill(xs,zs, color='r', alpha=0.4)
        plt.xlim(xo-2 , xmax)
        plt.ylim(0 , z1 + 2)
        plt.grid()
        plt.gca().invert_yaxis()
        plt.show()
    return xs,zs