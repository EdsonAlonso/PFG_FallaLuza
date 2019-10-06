# -------- Import Python internal libraries ---------
import numpy as np
import networkx as nx
from scipy.spatial import distance_matrix
import matplotlib.pyplot as plt
# -------- Creating a Graph and its MST ---------

def getgraph(M):
    '''
    This function recives a matrix, in with the colum i means the coordinates of a point in the i axis, and returns a graph where each knot is a point with the coordinates taken from matrix M and its MST.
    Inputs:
    M - matrix like (n,m)
    
    Output:
    
    G - Graph
    TSG - MST of G
    '''
    #Creates x and y arrays
    X = M[ :,0:2 ]
    
    Weight = distance_matrix( X,X )
    
    G = nx.from_numpy_matrix( Weight )
    
    TSG = nx.minimum_spanning_tree( G )

    return TSG




    