# --------------------------------------------------------------------------------------------------
# Title: Grav Codes
# Author: Edson Alonso Falla Luza
# Description: Source codes 
# Collaboratores: Rodrigo Bijani
# --------------------------------------------------------------------------------------------------

# -------- Import Python internal libraries ---------
import math
import numpy as np
import random


def my_atan(x, y):
    '''
    Return the more stable output for arctan calculation by correcting the
    value of the angle in arctan2, in order to fix the sign of the tangent.
    '''
    arctan = np.arctan2(x, y)
    arctan[x == 0] = 0
    arctan[(x > 0) & (y < 0)] -= np.pi
    arctan[(x < 0) & (y < 0)] += np.pi
    return arctan


def my_log(x):
    '''
    Return the value 0 for log(0), once the limits applying in the formula
    tend to 0.
    '''

    log = np.log(x)
    log[x == 0] = 0
    return log

def sortbetween( min, max ):
    t = random.random( )
    return ( 1 - t )*min + t*max

def sigmoide(x):
    a = 1.0
    sig = 1.0 - ( 1.0 / ( 1.0 + np.exp( -a * x ) ) )
    return sig

def normalize( x ):
    a = max( x )
    b = min( x )

    return 1 - ( ( x - a )/( b - a ) )

def sec(angle):
    '''function that computes the secant of a specific angle in radians
       input: a float representing the angle, in radians.'''
    
    sec = (1.0/math.cos(angle))
    return sec

def cossec(angle):
    ''' function that computes the cosecant of a specific angle in radians
        input: a float representing the angle, in radians.'''
    cossec = (1.0/math.sin(angle))
    return cossec

def cotg(angle):
    '''function that computes the cosecant of a specific angle in radians
       input: a float representing the angle, in radians.'''
    
    cotg = math.cos(angle)/math.sin(angle)
    return cotg

# calculo do perfil para o caso de linhas de massa
def linemasses(p1, p2, npts):
    ''' Funcao que cria uma linha de npts massas pontuais regularmente espacadas a partir dos pontos p1 e p2
    Inputs: p1 - lista com o par ordenado inicial (x1,z1)
            p2 - lista com o par ordenado final (x2,z2)
            npts - inteiro que define o numero total de fontes entre p1 e p2
    Output: xp,zp = coordenadas das massas pontuais '''
    
    # Defines points coordinates
    x1, y1 = p1
    x2, y2 = p2
    
    # Calculate the distances
    maxdist = np.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2 )
    distances = np.linspace(0.0, maxdist, npts)
    
    # Angle of profile line
    angle = np.arctan2(y2 - y1, x2 - x1)
    xp = x1 + distances * np.cos(angle)
    yp = y1 + distances * np.sin(angle)    
    
    # Return the final output
    return xp, yp
