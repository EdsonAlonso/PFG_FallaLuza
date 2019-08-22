import random
from Models import sphere
import numpy as np

class Fontes:

    def __init__( self ):
        self.fontes = [ ]

    @staticmethod
    def Gera_from_Existing( existing ):
        """

        :param existing: matrix as [ [x,z,mass] ]
        :return: population of spheres with the same properties
        """

        npop = len( existing )
        fontes = { }
        for i in range( npop ):
            for j in range( len( existing[ 0 ]) ):
                s1 = sphere( existing[ i ][j,0], existing[ i ][j,1], existing[ i ][j,2] )
                fontes[ s1 ] = s1.params
        return fontes

    def Gera( self, minbounds, maxbounds, nfontes = 100 ):

        self.mass = np.random.normal( 100, 1e7 )
        self.minbounds = minbounds
        self.maxbounds = maxbounds
        npar = len(self.minbounds) + 1

        self.fontes = { }
        self.temp = np.zeros( ( nfontes, npar ) )

        for i in range( nfontes ):
            x = ( 1 - random.random( ) )* self.minbounds[ 0 ] + random.random( )*self.maxbounds[ 0 ]
            z = ( 1 - random.random( ) ) * self.minbounds[ 1 ] + random.random( ) * self.maxbounds[ 1 ]
            s1 = sphere(x, z, self.mass)
            for j in range( npar ):
                self.temp[ i,j ] = s1.params[ j ]
            self.fontes[ s1 ] = self.temp[ i ]


    def Gz( self, xobs, zobs ):
        self.gz = 0
        for fonte in self.fontes:
            self.gz += fonte.gz( xobs, zobs )

        return self.gz

    def asDict( self ):
        return self.fontes

    def asArray( self ):
        return self.temp
