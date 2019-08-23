import networkx as nx

if __name__ == '__main__':
    G = nx.DiGraph( )
    x = [0.0,1.0]
    y = [1.0,2.0]

    G.add_node( ( x[ 0 ],y[ 0 ] ) )
    G.add_node( ( x[ 1 ],y[ 1 ] ) )

    G.add_edge( (0,1),(1,2), weight = 0.9)
    print( f' Nodes: {G.nodes}' )
    print( f' Edges: {G.edges.data( )}' )