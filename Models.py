import numpy as np
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


class _BaseModel_( ABC ):

    _gravConst = 6.674e-2

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
        self.__gz__ =  -( _BaseModel_._gravConst*( num/den ) )
        return self.__gz__

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
        self.rho = rho
        self.params = [ self.x1, self.x2, self.z1, self.z2, self.rho ]

    def theta( self, x, z ):
        return np.arctan( z/x )

    def Gz( self , xobs, yobs ):
        self.__xobs__ = xobs
        self.__yobs__ = yobs

        dx1 = self.x1 - self.__xobs__
        dx2 = self.x2 - self.__xobs__
        dz1 = self.z1 - self.__yobs__
        dz2 = self.z2 - self.__yobs__

        gz0 = ( 2*_BaseModel_._gravConst*self.rho )

        theta4 = ( self.theta( dz2, dx1 ) )
        theta3 = ( self.theta( dz2, dx2 ) )
        gz1 = ( dz2 )*( theta4 - theta3 )

        theta2 = ( self.theta( dz1, dx2 ) )
        theta1 = ( self.theta( dz1, dx1 ) )
        gz2 = ( dz1 )*( theta2 - theta1 )

        ln1num = ( ( dx1 )**2 + ( dz2 )**2 )
        ln1den = ( ( dx1 )**2 + ( dz1 )**2 )

        gz3 = ( dx1 )*( np.log( ln1num/ln1den ) )

        ln2num = ( ( dx2 )**2 + ( dz1 )**2 )
        ln2den = ( ( dx2 )**2 + ( dz2 )**2 )

        gz4 = ( dx2 )*( np.log( ln2num/ln2den ) )

        self.gz = gz0*( gz1 + gz2 - 0.5*( gz3 + gz4 ) )

        return self.gz + abs( min( self.gz ) )

    def plotGz( self ):
        plt.figure( figsize = ( 10,10 ), facecolor='w' )
        plt.plot( self.__xobs__,self.gz )
        plt.grid( )
        plt.show( )

    def plotModel( self ):
        pass

    def addnoise( self ):
        noise = np.random.normal( 0, 0.0001, len( self.gz ) )

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
