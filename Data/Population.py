import random
from Models import sphere
import numpy as np

class Fontes:

    def __init__( self ):
        self.fontes = [ ]

    def Gera( self, minbounds, maxbounds, nfontes = 100 ):

        self.minbounds = minbounds
        self.maxbounds = maxbounds
        npar = len(self.minbounds) + 1

        self.fontes = np.zeros( ( nfontes, npar ) )

        for i in range( nfontes ):
            x = random.uniform( self.minbounds[ 0 ], self.maxbounds[ 0 ] )
            z = random.uniform( self.minbounds[ 1 ], self.maxbounds[ 1 ] )
            s1 = sphere(x, z, 1e6)
            for j in range( npar ):
                self.fontes[ i,j ] = s1.params[ j ]

        return self.fontes