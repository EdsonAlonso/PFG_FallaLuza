import numpy as np

def phi( gzmodel, gzcalc ):
    res = [ ]
    for gz in gzcalc:
        soma = 0
        for i in range( len( gz ) ):
            soma += ( gzmodel[ i ] - gz[ i ] )**2
        res.append( soma )
        soma = 0
    return  res

def somadict( dict1, dict2 ):
    soma = [ ]
    temp = [ ]

    for index1, key1 in enumerate( dict1 ):
        for index2, key2 in enumerate( dict2 ):
            temp.append( dict2[ key2 ] )

        soma.append( np.array( dict1[ key1 ] + temp[ index1 ] ) )
        temp = [ ]

    return np.array( soma )


def dictTimesConstant( dict, constant ):

    for key in dict:
        dict[ key ] = constant*dict[ key ]

    return dict
