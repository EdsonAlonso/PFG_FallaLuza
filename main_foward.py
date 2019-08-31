from Genetic.Operators import operator
import numpy as np
from Data.Population import Fontes
import matplotlib.pyplot as plt
from Models import rect, sphere
from modules.auxiliar import sigmoide

def alp(x, y):
    fun = -(x * y) ** (0.5) * np.sin(x) * np.sin(y)
    return fun

def phi( x,y ):
    return ( np.linalg.norm( x - y ) )**2


if __name__ == "__main__":
    xobs = np.linspace( 0,10,300 )
    zobs = np.zeros( len( xobs ) )
    xmin, xmax = 2.0, 8.0
    ymin, ymax = 0.5, 10.0
    min_bounds = [xmin, ymin]
    max_bounds = [xmax, ymax]
    npop = 20
    pmut = 0.1
    ngera = int( 500 )
    npar = len( min_bounds )
    conv = [ ]
    best = [ ]

    model = rect( 4.5, 3.0, 5.0 , 4.0 , 3e8)
    model_gz = model.gz( xobs, zobs )

    fit = [ ]
    pop = Fontes( )
    pop.Gera( min_bounds, max_bounds, nfontes = npop , nind = 4)
    fontes = pop.asArray( )
    gz = pop.Gz( xobs, zobs )

    for index,ind in enumerate(pop.fontes):
        plt.figure()
        plt.title(f'Individuo {index}')
        plt.subplot(211)
        plt.plot(xobs, gz[index])
        plt.grid( )

        plt.subplot(212)
        for fonte in ind:
            plt.scatter( fonte.params[0], fonte.params[1], c = 'black' )
        plt.xlim(min(xobs), max(xobs) )
        plt.gca().invert_yaxis()
        plt.grid( )
        #plt.savefig('Imagegm'+str(index)+'.png')
    plt.show( )
