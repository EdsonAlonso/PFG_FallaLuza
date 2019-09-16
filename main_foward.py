import numpy as np
from Models import rect
from Plots import plotRect

if __name__ == "__main__":
    xobs = np.linspace( -1000,1000,300 )
    zobs = np.zeros( len( xobs ) )
    xmin, xmax = -0.5, 0.5
    ymin, ymax =  2.0, 6.0

    model = rect( -100,100,200,800,2 )
    model_gz = model.Gz( xobs, zobs )

    plotRect(model, model_gz, xobs, [0,1000], fill = False)