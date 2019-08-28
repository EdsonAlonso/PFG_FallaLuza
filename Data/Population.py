from Models import sphere
import numpy as np
from modules.auxiliar import sortbetween

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

    def Gera( self, minbounds, maxbounds, nfontes = 100, nind = 500 ):

        self.minbounds = minbounds
        self.maxbounds = maxbounds
        self.nfontes = nfontes
        self.nind = nind
        self.npar = len(self.minbounds) + 1

        self.fontes = [ ]
        self.__fontes__ = { }
        self.temp = np.zeros( ( self.nfontes, self.npar, self.nind ) )

        for k in range( nind ):
            self.mass = sortbetween(1e1, 1e8)
            for i in range( nfontes ):
                x = sortbetween( self.minbounds[ 0 ] , self.maxbounds[ 0 ] )
                z = sortbetween( self.minbounds[ 1 ], self.maxbounds[ 1 ] )
                s1 = sphere(x, z, self.mass)
                for j in range( self.npar ):
                    self.temp[ i,j,k ] = s1.params[ j ]
                self.__fontes__[ s1 ] = self.temp[ i ]
            self.fontes.append(  self.__fontes__  )
            self.__fontes__ = { }

    def Gz( self, xobs, zobs ):
        self.gz = np.empty( self.nind )
        self.__gz__ = 0
        for i, ind in enumerate( self.fontes ):
            for esfera in ind:
                self.__gz__ += esfera.gz( xobs, zobs )
                print( self.__gz__)
            self.gz[ i ] = self.__gz__
            self.__gz__ = 0

        return self.gz

    def asDict( self ):
        return self.fontes

    def asArray( self ):
        return self.temp
