# --------------------------------------------------------------------------------------------------
# Title: Grav Codes
# Author: Edson Alonso Falla Luza
# Description: Source codes 
# Collaboratores: Rodrigo Bijani
# --------------------------------------------------------------------------------------------------

# -------- Import Python internal libraries ---------
import numpy as np
from scipy.spatial.distance import mahalanobis
import Graph.graphs
# -------- L1 Norm (sum norm) ---------

def l1dist(x_coord,y_coord):
    '''
    This function takes two vectors, x_coord and y_coord, and returns a matrix were the element in the ij position is the distance (considering the sum norm, ou l1 norm) betwen the point (x_coord[i],y_coord[i]) and (x_coord[j],y_coord[j]).
    
    Inputs:
    x_coord - numpy array 
    y_coord - numpy array
    
    Output:
    dl1 - numpy array - Matrix of distances
    '''
    
    #Stablishing the error condition
    tamx = np.shape(x_coord)[0]           
    tamy = np.shape(x_coord)[0]
    if tamx != tamy:
        raise ValueError("All inputs must have same length!")
        
    #Calculating and savingn the distances
    #tam = ( math.factorial(tamx) )/( 2*(math.factorial(tamx-2)) ) #2 choises over 'tamx'(or 'tamy') posibilities 
    distl1_matrix = np.zeros((tamx,tamy))
                                    
    for i in range(tamx):
        for j in range(tamx):
            distl1_matrix[i][j] = abs(x_coord[i] - x_coord[j]) + abs(y_coord[i] - y_coord[j])                                      
            
    return distl1_matrix
    

# -------- L2 Norm (euclidians norm) ---------

def l2dist(x_coord,y_coord):
    '''
    This function takes two vectors, x_coord and y_coord, and returns a matrix were the element in the ij position is the distance (considering the euclidian norm, ou l2 norm) betwen the point (x_coord[i],y_coord[i]) and (x_coord[j],y_coord[j]).
    
    Inputs:
    x_coord - numpy array 
    y_coord - numpy array
    
    Output:
    dl1 - numpy array - Matrix of distances
    '''
    
    #Stablishing the error condition
    tamx = np.shape(x_coord)[0]           
    tamy = np.shape(x_coord)[0]
    if tamx != tamy:
        raise ValueError("All inputs must have same length!")
        
    #Calculating and savingn the distances
    #tam = ( math.factorial(tamx) )/( 2*(math.factorial(tamx-2)) ) #2 choises over 'tamx'(or 'tamy') posibilities
    distl2_matrix = np.zeros((tamx,tamy))
                                    
    for i in range(tamx):
        for j in range(tamx):
            distl2_matrix[i][j] = ( (x_coord[i] - x_coord[j])**2 + (y_coord[i] - y_coord[j])**2 )**(1/2)                                     
            
    return distl2_matrix


#-----------Importing the getgraph function----------



# -------- Graph L2 Distance Function ---------

class distgraphl2( ):
    
    def calculate( self , M):
        '''
        This function recives a matrix, in with the colum i means the coordinates of a point in the i axis, creates a graph as well as its MST and returns a value (float) of the square of the sum of the weight of all knots to the average of the weights (phi) as the average itself (dmG).

        Inputs:
        M - array like (m,n)

        Output:

        phi = float
        dmG = float
        '''

        #creates a graph and its MST:
        self.G,self.TSG = Graph.graphs.getgraph(M)
        # get the weights of the undirected Graph:
        dm1 = []
        for (u, v, wt) in self.TSG.edges.data('weight'):
            dm1.append(wt)

        # computing the mean of the MST:
        self.dmG = np.mean( np.array(dm1) )

        # compute the variance of the distances of the MST:
        self.phi = 0.0
        for i in range( len(dm1) ):
            self.phi += (dm1[i] - self.dmG)**2

        self.phi = np.sqrt( self.phi )

        return self.phi#,self.dmG

# -------- Graph L1 Distance Function ---------

class distgraphl1:

    def calculate(self, M):
        '''
           This function recives a matrix, in with the colum i means the coordinates of a point in the i axis, creates a graph as well as its MST and returns a value (float) of the sum of the weight of all knots to the average of the weights (phi) as the average itself (dmG).

        Inputs:

        M - array like (m,n)

        Output:

        phi = float
        dmG = float
        '''
        #creates a graph and its MST:
        self.G,self.TSG = Graph.graphs.getgraph(M)

        # get the weights of the undirected Graph:
        dm1 = []
        for (u, v, wt) in self.TSG.edges.data('weight'):
            dm1.append(wt)

        # computing the mean of the MST:
        self.dmG = np.mean( np.array(dm1) )

        # compute the variance of the distances of the MST:
        self.phi = 0.0
        for i in range( len(dm1) ):
            self.phi += abs(dm1[i] - self.dmG)
        return self.phi#,self.dmG

# -------- Graph Mahalanobis Distance Function ---------

class distgraphmaha:

    def calculate( self, M ):
        '''
        This function recives a matrix, in with the colum i means the coordinates of a point in the i axis, creates a graph as well as its MST and returns the mahalanobis distances of the vertices in the MST as well as the as the average itself (dmG).
    .

        Inputs:

        M - array like (m,n)

        m - float - mahalanobis distance
        dmG - float
        '''
        #Separates the entries of the M matrix:
        x = M[:,0]
        x = np.array(x)

        y = M[:,1]
        y = np.array(y)

        #creates a graph and its MST:
        self.G,self.TSG = Graph.graphs.getgraph(M)

        # get the weights of the undirected Graph:
        dm1 = []
        u   = []
        v   = []
        for (i, j, wt) in self.TSG.edges.data('weight'):
            u.append(x[i])
            v.append(y[j])
            dm1.append(wt)

        # computing the mean of the MST:
        self.dmG = np.mean( np.array(dm1) )
        
        N = np.c_[ u,v ]
        C = np.cov( N )

        if np.linalg.det( C ) < 1e-100:
            np.fill_diagonal( C, 1e10)
        
        invC = np.linalg.inv( C )

        self.m = abs( mahalanobis( u,v,invC ) - self.dmG )
        
        return self.m #, self.dmG

class DistFactory:
    
    def getdist( self, dist ):
        if dist == 'L1':
            return distgraphl1( )
        
        if dist == 'L2':
            return distgraphl2( )
        
        if dist == 'Maha':
            return distgraphmaha( )
        
def getDistance( chamada, M ):
    return DistFactory( ).getdist( chamada ).calculate( M )