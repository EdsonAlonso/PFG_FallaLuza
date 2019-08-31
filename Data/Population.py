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

        nind = len( existing )
        nfontes = len( existing[ 0 ] )
        temp = { }
        fontes = [ ]
        for i in range( nind ):
            for k in range( nfontes ):
                s1 = sphere( existing[ i ][ k,0 ], existing[ i ][ k,1 ], existing[ i ][ k,2 ] )
                temp[ s1 ] = np.array( s1.params )
            fontes.append( temp )
            temp = { }
        return fontes


    def Gera( self, minbounds, maxbounds, nfontes = 100, nind = 500 ):

        self.minbounds = minbounds
        self.maxbounds = maxbounds
        self.nfontes = nfontes
        self.nind = nind
        self.npar = len(self.minbounds)

        self.fontes = [ ]
        self.__fontes__ = { }
        self.temp = np.zeros( ( self.nind, self.nfontes, self.npar ) )

        for k in range( nind ):
            self.mass = sortbetween(self.minbounds[ 2 ], self.maxbounds[ 2 ])
            for i in range( nfontes ):
                x = sortbetween( self.minbounds[ 0 ] , self.maxbounds[ 0 ] )
                z = sortbetween( self.minbounds[ 1 ], self.maxbounds[ 1 ] )
                s1 = sphere(x, z, self.mass)
                for j in range( self.npar ):
                    self.temp[ k,i,j ] = s1.params[ j ]
                self.__fontes__[ s1 ] = self.temp[ k ][ i ]
            self.fontes.append(  self.__fontes__  )
            self.__fontes__ = { }


    def Gz( self, xobs, zobs, fontes = None):

        if fontes == None:
            fontes = self.fontes

        self.gz = [ ]
        self.__gz__ = 0
        for i, ind in enumerate( fontes ):
            for esfera in ind:
                self.__gz__ += esfera.Gz( xobs, zobs )
            self.gz.append( self.__gz__ )
            self.__gz__ = 0

        return self.gz

    def asDict( self ):
        return self.fontes

    def asArray( self ):
        return self.temp
