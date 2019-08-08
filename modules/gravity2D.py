# --------------------------------------------------------------------------------------------------
# Title: Grav Codes
# Author: Edson Alonso Falla Luza
# Description: Source codes 
# Collaboratores: Rodrigo Bijani
# --------------------------------------------------------------------------------------------------

# -------- Import Python internal libraries ---------
import numpy as np
from modules.auxiliar import cotg,sec,cossec

def g_sphere(x, z, sphere1, component='z'):
    '''    
    This function calculates all components of gravity attraction produced by a solid point mass and returns the one associated to the required one.
    This is a Python implementation for the subroutine presented in Blakely (1995). On this function, there are received the value of the initial
    and final observation points (X and Y) and the properties of the sphere.
       
    Inputs:
    x - numpy array - observations in x directions (meters)
    y - numpy array - observations in y directions (meters)
    component - string - the required component to be calculated
    sphere1 - list - elements of the sphere: [x_center(meters), z_center(meters), mass(kg)]
    
    Output:
    g - numpy array - the required component for the gravity in mGal. Size of gz is the same as x and z observations    
    '''
    
    # Stablishing some conditions
    if x.shape != z.shape:
        raise ValueError("All inputs must have same shape!")
    
    # Definition for some constants
    G = 6.673e-11 # SI
    si2mGal = 100000.0
    
    
    # building a "transposed" list for correct usage of enumerate loop:
 
    sphere=[]
    for i in range( len(sphere1[0]) ): # sphere1[0] contains of all masses considered.
        sphere.append([ sphere1[0][i], sphere1[1][i], sphere1[2][i] ])

    # Setting the initial value for gravity:
    g = 0.
    gg = 0.0
    xs = np.zeros( len(sphere) )
    zs = np.zeros( len(sphere) )
    ms = np.zeros(len(sphere) )
    # loop for all point masses in list sphere
    for i,j in enumerate(sphere):
        #print (i,j)
        xs[i] = j[0]
        zs[i] = j[1]
        ms[i] = j[2]
    
        # Setting position-vector: 
        dx = xs[i] - x
        dz = zs[i] - z
    
        # properties of the sphere:
        mass = ms[i]
     
        # Compute the distance
        r = np.sqrt(dx**2 + dz**2)
    
        if component=='z':
            # Compute the vertical component 
            g = mass * dz / (r**3)
            g *= G*si2mGal
        elif component =='x':
            # Compute the vertical component 
            g = mass * dx / (r**3)
            g *= G*si2mGal
        
        gg += g
        # Return the final outpu
    return gg
###########################################################################################################################

def volfont(raio,rho):
    '''
    This function calculates the volume and mass of a sphere, given the radius and the density of itself.
    It also returns the radius and the density if the user wants to save them in a list or a tuple. 
    
    Inputs:
    
    raio - float (given in metters)
    rho - float (given in Km/m^3)
    '''
    V = (4.0/3.0) * np.pi * raio**3 * rho
    massa = V * rho
    return raio,rho,V,massa

########################################################################################################################

def g_rod(x,z,rod,component='z'):
    '''
    This function calculates the vertical component of gravity attraction produced by a thin rod with particular inclination and cross section
    (Telford, 1981)
    Inputs: x,z = arrays with cartesian coordinates in meters;
    rod: list with the following elements in this specific order: rod[x_rod, z_rod, L, alpha, rho, A ]:
    x_rod      = horizontal distance from origin (meters)
    z_rod      = vertical distance from origin (meters)
    L         = length of the thin rod (meters) (never zero!)
    alpha     = inclination of the rod (degrees)
    rho       = density of the rod (kg/m3)
    A         = cross section of the rod in (m2)
    component = the gravitational component to be computed (only z component is available yet) 
    
    Output:
    g - numpy array - the required component for the gravity in mGal. Size of gz is the same as x and z observations    
    '''

    # Stablishing some conditions
    if x.shape != z.shape:
        raise ValueError("All inputs must have same shape!")
        
    if component !='z':
        raise ValueError("Only z component is available yet!")
    
    # Definition for some constants
    G = 6.673e-11 # SI
    si2mGal = 100000.0 # convert to mGal
    degree2rad = np.pi/180.0 # convert from degrees to radians

    # get variables from list rod:
    x_rod = rod[0]
    z_rod = rod[1]
    L     = rod[2]
    alpha = (np.pi/2) + rod[3]*degree2rad # set alpha to radians in here
    rho   = rod[4]
    A     = rod[5]
    
    # Setting position-vector: 
    dx = x - x_rod
    dz = z - z_rod
    dummy = 1e-4 # pay attention to this number!
    
    # Verify the division by zero during calculations (for position-vector):
    for i in range(np.size(dx,0)):
        if dx[i] == 0.0:
            dx[i]+= dummy
        if dz[i]==0.0:
            dz[i]+=dummy
            
    # Verify the division by zero during calculations (for alpha):
    if alpha in [0.0, np.pi]:
        aplha+=1e-3 # pay attention to this value
        print('WARNING: CRITICAL INCLINATION. MAY NOT TRUST IN OUTCOMES!')
    
    # set the size of output array:
    g = np.zeros( np.size(x) )
    
    # calculation of gravitation by parts:
    # first part of equation:
    term0 = ( G*rho*A / ( dx*np.sin(alpha) ) )
    
    term11 = ( dx + dz*(cotg(alpha)) ) 
    term12 = ( (dz**2) * ((cossec(alpha))**2) + 2.0*dx*dz *cotg(alpha) + (dx**2) )

    term1 = term11 / (term12)**(0.5)

    term21 = ( dx + dz*cotg(alpha) + L*np.cos(alpha) )
    term22 = ( ( ( L + dz*cossec(alpha) )**2) + (dx**2) + 2.0*dx*( L*np.cos(alpha) + dz*cotg(alpha) ) )
    
    term2 = term21/ (term22)**(0.5)
    
    
    g = term0 * ( term1 - term2 )
    
    return g*si2mGal


###################################################################################

def g_prism(x,z,prism):
    
    '''
    This function calculates the vertical component of gravity attraction produced by a prism 
    
    (Telford, 1981)
    Inputs: x,z = arrays with cartesian coordinates in meters;
    rod: list with the following elements in this specific order: prism[x_prism, h1_prism, L, A, rho ]:
    x_prism      = horizontal distance from origin (meters)
    h1_prism      = vertical distance from origin to top (meters)
    L         = length of the thin prism (meters) (never zero!)
    rho       = density of the prism (kg/m3)
    A         = cross section of the prism (m2)
    component = the gravitational component to be computed (only z component is available yet) 
    
    Output:
    g - numpy array - the required component for the gravity in mGal. Size of gz is the same as x and z observations    
    '''

    #saving the inputs of prism:
    x_prism  = prism[0]
    h1_prism = prism[1]
    L_prism  = prism[2]
    h2_prism  = abs(L_prism - h1_prism)
    A        = prism[3]
    rho      = prism[4]
    
    #seting the variables to make the calclation?
    dx = abs(x - x_prism)
    dy = np.zeros(len(x))
    h1 = abs(z - h1_prism)
    h2 = abs(z - h2_prism)
    
    #setting some constans:
    G = 6.673e-11
    si2mGal = 100000.0
    
    #making the comptation of g
    term0 = (G*rho*A)
    
    term11 = ( dx**2 + dy**2 + h1**2)
    term1 = 1/(term11**(0.5))
    
    term21 = ( dx**2 + dy**2 + h2**2)
    term2 = 1/(term21**(0.5))

    g = term0 * (term1 - term2)
    
    return g*si2mGal


########################################################################################################################

def g_finit_sheet(x,z,sheet):
    '''
    This function calculates the vertical gravitational attraction gz of a dipping thin sheet with an inclination (alpha) equal (90+dipping angle) with horizontal plan and has 
    finite length (l) and thickness (T)
    
    Inputs: x,z = arrays with cartesian coordinates in meters;
    sheet: list with the following elements in this specific order: rod[x_sheet, z_sheet, rho, alpha, l, T ]:
    x_sheet      = horizontal distance from origin (meters)
    z_sheet      = vertical distance from origin (meters)
    rho       = density of the sheet (kg/m3)
    alpha     = inclination of the sheet (degrees)
    l         = length of the thin sheet (meters)
    T         = thickness of the sheet (meters)
    
    Output:
    g - numpy array - the required component for the gravity in mGal. Size of gz is the same as x and z observations    
    '''

    # Stablishing some conditions
    if x.shape != z.shape:
        raise ValueError("All inputs must have same shape!")
        
    # Definition for some constants
    G = 6.673e-11 # SI
    si2mGal = 100000.0 # convert to mGal
    degree2rad = np.pi/180.0 # convert from degrees to radians
    rad2degree = 180.0/np.pi
    # get variables from list rod:
    x_sheet = sheet[0]
    z_sheet = sheet[1]
    rho     = sheet[2]
    alpha = (np.pi/2.0) + sheet[3]*degree2rad # set alpha to radians in here
    l   = sheet[4]
    T     = sheet[5]
    
    # Setting position-vector: 
    dx = (x - x_sheet) #+ 10e-3 # dummy to avoid nans
    dz = (z - z_sheet) #+ 10e-3
    
    # set the size of output array:
    g = np.zeros( np.size(x) )
    
    # calculation of gravitation by parts:
    # first part of equation:
    r1 = (dx**2 + dz**2 )**(1/2)
    r2 = ( ( dx + l*np.cos(alpha) )**2 + ( dz +l*np.sin(alpha) )**2 )**(1/2)
    theta12 =  np.arccos( (r1**2 + r2**2 - l**2) / (2*r1*r2) ) 

    term1 = (2*G*rho*T)
    term2 = ( np.sin(alpha)*np.log(r2/r1) - theta12*np.cos(alpha) ) 
    g = term1*term2
    
    return g*si2mGal

########################################################################################################################

def g_semifin_sheet(x,z,sheet):
    '''
    This function calculates the vertical gravitational attraction gz of a horizontal semi-infinite thin sheet with thickness (T)
    
    Inputs: x,z = arrays with cartesian coordinates in meters;
    sheet: list with the following elements in this specific order: rod[x_sheet, z_sheet, rho, T ]:
    x_sheet      = horizontal distance from origin (meters)
    z_sheet      = vertical distance from origin (meters)
    rho       = density of the sheet (kg/m3)
    T         = thickness of the sheet (meters)
    
    Output:
    g - numpy array - the required component for the gravity in mGal. Size of gz is the same as x and z observations    
    '''

    # Stablishing some conditions
    if x.shape != z.shape:
        raise ValueError("All inputs must have same shape!")
        
    # Definition for some constants
    G = 6.673e-11 # SI
    si2mGal = 100000.0 # convert to mGal
    degree2rad = np.pi/180.0 # convert from degrees to radians
    rad2degree = 180.0/np.pi
    # get variables from list rod:
    x_sheet = sheet[0]
    z_sheet = sheet[1]
    rho     = sheet[2]
    T     = sheet[3]
    
    # Setting position-vector: 
    dx = x - x_sheet
    dz = z - z_sheet
    
    # set the size of output array:
    g = np.zeros( np.size(x) )
    
    # calculation of gravitation by parts:
    # first part of equation:
    
    term1 = (2*G*rho*T)
    term2 =( (np.pi/2) - np.arctan(dx/dz) )
    
    g = term1*term2
    
    return g*si2mGal

