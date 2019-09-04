from Genetic.Operators import operator
import numpy as np
from Data.Population import Fontes
import matplotlib.pyplot as plt
from Models import rect, sphere
from modules.auxiliar import sigmoide, softmax

def alp(x, y):
    fun = -(x * y) ** (0.5) * np.sin(x) * np.sin(y)
    return fun

def phi( x,y ):
    return ( np.linalg.norm( x - y ) )**2


if __name__ == "__main__":
    xobs = np.linspace( -10,10,300 )
    zobs = np.zeros( len( xobs ) )
    xmin, xmax = -0.5, 0.5
    ymin, ymax =  2.0, 6.0
    min_bounds = [xmin, ymin, 5e4]
    max_bounds = [xmax, ymax, 5e4]
    npop = 500
    pmut = 0.1
    ngera = int( 500 )
    npar = len( min_bounds )

    model = rect( -0.5,0.5,2.0,6.0,5e5 )
    model_gz = model.Gz( xobs, zobs )
    model_gz_noised = model.addnoise( )

    massbounds = [ 1e4,1e7 ]
    pop = Fontes( )
    pop.Gera( min_bounds, max_bounds, nfontes = npop , nind = 1)
    fontes = pop.asArray( )
    gz = pop.Gz( xobs, zobs )


    plt.figure()
    plt.subplot(211)
    plt.plot(xobs, model_gz, label = str( ( phi( model_gz, gz ) ) ) )
    plt.plot( xobs, gz[0])
    plt.grid( )
    plt.xlim(-10,10)
    plt.legend( )

    plt.subplot(212)
    plt.plot( [ model.params[ 0 ], model.params[ 0 ], model.params[ 1 ], model.params[ 1 ], model.params[ 0 ] ],\
              [ model.params[ 2 ],model.params[ 3 ], model.params[ 3 ], model.params[ 2 ],model.params[ 2 ] ],".-" )
    for key in pop.fontes[ 0 ]:
        plt.scatter( key.params[ 0 ], key.params[ 1 ] )
    plt.grid( )
    plt.ylim( 0,10 )
    plt.gca( ).invert_yaxis( )
    plt.xlim( -10,10 )
    # plt.show( )

    plt.figure()
    plt.plot(xobs, softmax(xobs))
    plt.show()

