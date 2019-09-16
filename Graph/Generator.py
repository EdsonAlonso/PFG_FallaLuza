import networkx as nx

class Graph:

    def __init__( self ):
        self.graph = nx.Graph( )
        self.MST = None

    def createnodes( self, population ):
        self.__init__( )
        """

        :param population: array as [x,y]
               x: array
               y: array
        :return: G = Directed Graph where nodes are [x,y]

        """
        [ self.graph.add_node( ( population[ i,0 ], population[ i, 1 ] ) )\
          for i in range( population.shape[ 0 ] )  ]

        return self.graph

    def calculateMST( self ):

        for node in self.graph.nodes:
            self.graph.add_edge( *node )

        self.MST = nx.minimum_spanning_tree( self.graph )

        return nx.minimum_spanning_tree( self.graph )
