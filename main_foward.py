import numpy as np
from Models import rect
from Plots import plotRect

def alp(x, y):
    fun = -(x * y) ** (0.5) * np.sin(x) * np.sin(y)
    return fun

def phi( x,y ):
    return ( np.linalg.norm( x - y ) )**2


if __name__ == "__main__":
    xobs = np.linspace( -1000,1000,300 )
    zobs = np.zeros( len( xobs ) )
    xmin, xmax = -0.5, 0.5
    ymin, ymax =  2.0, 6.0
    min_bounds = [xmin, ymin, 5e4]
    max_bounds = [xmax, ymax, 5e4]
    npop = 500
    pmut = 0.1
    ngera = int( 500 )
    npar = len( min_bounds )

    model = rect( -100,100,200,800,2 )
    model_gz = model.Gz( xobs, zobs )

    plotRect(model, model_gz, xobs, [0,1000], fill = False)