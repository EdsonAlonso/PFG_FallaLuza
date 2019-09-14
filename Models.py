import numpy as np
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from modules.auxiliar import my_atan, my_log


class _BaseModel_( ABC ):

    _gravConst = 6.674e-11
    _si2mGal = 100000.0

    @abstractmethod
    def Gz( self ):
        pass

    @abstractmethod
    def plotGz( self ):
        pass

    @abstractmethod
    def plotModel( self ):
        pass

class sphere( _BaseModel_ ):

    def __init__( self, x, z, mass ):
        self.x = x
        self.z = z
        self.mass = mass
        self.params = [ self.x, self.z, self.mass ]

    def Gz( self, x_obs, z_obs ):
        self.__xobs__ = x_obs
        self.__zobs__ = z_obs
        num = ( self.mass*( self.__zobs__ - self.z ) ) # MASSA * (Zobs - Z)
        den = ( ( self.__xobs__ - self.x )**2 + ( self.__zobs__ - self.z)**2 )**(3/2) # (Xobs-X)**2 + (Zobs- Z)**2
        self.gz =  -( _BaseModel_._gravConst*( num/den ) )

        return self.gz*_BaseModel_._si2mGal

    def plotGz( self ):
        plt.figure( figsize = ( 10,10 ), facecolor='w' )
        plt.plot( self.__xobs__,self.__gz__ )
        plt.grid( )
        plt.show( )

    def plotModel( self ):
        p1 = plt.figure( figsize=(10,10), facecolor='w' )
        plt.scatter( self.x, self.z, s = 50, c = 'b' )
        plt.xlim( min( self.__xobs__), max( self.__xobs__ ) )
        plt.ylim( -0.5, self.z + 5.0 )
        plt.gca( ).invert_yaxis( )
        plt.grid( )
        plt.show( )

class rect( _BaseModel_ ):

    def __init__( self, x1, x2, z1, z2, rho ):
        self.x1 = x1
        self.x2 = x2
        self.z1 = z1
        self.z2 = z2
        self.rho = rho*1000.
        self.params = [ self.x1, self.x2, self.z1, self.z2, self.rho ]


    def Gz( self , xobs, zobs ):
        self.__xobs__ = xobs
        self.__zobs__ = zobs
        yobs = self.__xobs__*0

        dx = [ self.x2 - self.__xobs__, self.x1 - self.__xobs__ ]
        dy = [  600 - yobs , -600 - yobs ]
        dz = [ self.z2 - self.__zobs__, self.z1 - self.__zobs__ ]

        self.gz = np.zeros_like( xobs )

        for k in range( 2 ):
            for j in range( 2 ):
                for i in range( 2 ):
                    r = np.sqrt( dx[ i ]**2 + dy[ j ]**2 + dz[ k ]**2 )
                    result = -( dx[ i ]*my_log( dy[ j ] + r )\
                                + dy[ j ]*my_log( dx[ i ] + r )\
                                - dz[ k ]*my_atan( dx[ i ]*dy[ j ], dz[ k ]*r ) )
                    self.gz += ( (-1)**( i+j+k ) )*result*self.rho

        self.gz *= _BaseModel_._gravConst*_BaseModel_._si2mGal

        return self.gz

    def plotGz( self ):
        plt.figure( figsize = ( 10,10 ), facecolor='w' )
        plt.plot( self.__xobs__,self.gz )
        plt.grid( )
        plt.show( )

    def plotModel( self ):
        pass

    def addnoise( self ):
        noise = np.random.normal( 0, 0.05, len( self.gz ) )

        self.gz = self.gz + noise

        return  self.gz


class semiFiniteSheet( _BaseModel_ ):

    def __init__( self, x, z, rho, thickness ):
        self.x = x
        self.z = z
        self.rho = rho
        self.thickness = thickness

    def Gz( self, xobs, yobs ):
        self.__xobs__ = xobs
        self.__yobs__ = yobs

        gz1 = ( 2*_BaseModel_._gravConst*self.rho*self.thickness )
        gz2 = ( np.pi/2 )
        gz3 = ( np.arctan( ( self.__xobs__ - self.x )/( self.__yobs__ - self.z ) ) )

        self.__gz__ = gz1*( gz2 - gz3 )

        return self.__gz__

    def plotGz( self ):
        plt.figure( figsize = ( 10,10 ), facecolor='w' )
        plt.plot( self.__xobs__,self.__gz__ )
        plt.grid( )
        plt.show( )

    def plotModel( self ):
        pass
