# -------- Import Python internal libraries ---------
import numpy as np
import networkx as nx
import Graph.graphs_distances
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
    x = M[:,0]
    x = np.array(x)
    
    y = M[:,1]
    y = np.array(y)   
    #creates the graph and the MST:
    G = nx.Graph()
    for i in range(len(x)):
        G.add_node(i ,pos=(x[i],y[i]))
        for j in range(len(x)):
            G.add_edge(i, j, weight=Graph.graphs_distances.l2dist(x, y)[i][j])

    TSG = nx.minimum_spanning_tree( G )

    return G,TSG
