import numpy as np
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


class _BaseModel_( ABC ):

    _gravConst = 6.674e-11

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
        num = ( self.mass*( self.__zobs__ - self.z ) )
        den = ( ( self.__xobs__ - self.x )**2 + ( self.__zobs__ - self.z)**2 )
        self.__gz__ =  -( _BaseModel_._gravConst*( num/den ) )
        return self.__gz__

    def plotGz( self ):
        plt.figure( figsize = ( 10,10 ), facecolor='w' )
        plt.plot( self.__xobs__,self.__gz__ )
        plt.grid( )
        plt.show( )

    def plotModel( self ):
        plt.figure( figsize=(10,10), facecolor='w' )
        plt.scatter( self.x, self.z, s = 50, c = 'b' )
        plt.xlim( min( self.__xobs__), max( self.__xobs__ ) )
        plt.ylim( -0.5, self.z + 5.0 )
        plt.gca( ).invert_yaxis( )
        plt.grid( )
        plt.show( )


class rect( _BaseModel_ ):

    def __init__( self, x, z, vertical_length, horizontal_length, rho ):
        self.x = x
        self.z = z
        self.vertical_length = vertical_length
        self.horizontal_length = horizontal_length
        self.rho = rho

    def Gz( self , xobs, yobs ):
        self.__xobs__ = xobs
        self.__yobs__ = yobs
        gz1 = ( _BaseModel_._gravConst*self.rho*self.horizontal_length )
        den1 = ( np.sqrt( ( self.__xobs__ - self.x )**2 + ( self.__yobs__ - self.z )**2 ) )
        gz2 = ( 1/den1 )
        den2 = ( np.sqrt( ( self.__xobs__ - self.x )**2 + ( self.__yobs__ - self.vertical_length )**2 ) )
        gz3 = ( 1/den2 )
        self.gz = gz1*( gz2 - gz3 )

        return self.gz

    def plotGz( self ):
        plt.figure( figsize = ( 10,10 ), facecolor='w' )
        plt.plot( self.__xobs__,self.gz )
        plt.grid( )
        plt.show( )

    def plotModel( self ):
        pass

    def addnoise( self ):
        noise = np.random.normal( 0, 0.0002, len( self.gz ) )

        self.gz_noised = self.gz + noise

        return self.gz_noised

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
