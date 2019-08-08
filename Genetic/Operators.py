import numpy as np
import random
from abc import ABC,abstractmethod
import pandas as pd


class _OperatorInterface( ABC ):
    @abstractmethod
    def run( self, *params ):
        pass


class _RoletaOperator( _OperatorInterface ):

    def run(self , *params):
        """
        :param params: array contendo a função de ajuste aplicada à população
        :return: pai: array contendo os candidatos a pais
        """

        prob = sigmoid( params )
        pai = [ ]

        for i in range( len( prob ) ):
            r = random.random( )
            if prob[ i ] >= r:
                pai.append( i )

    return np.array( pai )

class _CruzamentoOperator( _OperatorInterface ):

    def run(self, *params):
        """
        :param params: array contendo a população de candidatos a cruzamento
        :return: filhos: array contendo os filhos
        """

        pesopai = random.random( )
        pesomae = random.random( )

        final = len( params )

        npar = np.size( p,1 )
        npop = np.size( p,0 )

        if npop%2 != 0:
            npop = npop - 1
            final = len( p ) - 1

        nfilhos = int( npop/2 )

        pais = p[ 0:nfilhos, : ]
        maes = p[ nfilhos:final, : ]

        filhos = ( pesomae*maes + pesopai*pais )/( pesomae + pesopai )

        return filhos

class _MutacaoOperator( _OperatorInterface ):

    def run( self, *params ):
        """
        :param params: (p, probmut, minp, maxp)
        :return: p: população mutada
        """
        p,probmut,minp,maxp = params

        npar = np.size( p,1 )
        npop = np.size( p,0 )

        for i in range( npop ):
            rand = random.random( )
            if probmut <= rand:
                ipar = random.randint( 0,npar-1 )
                a = minp[ ipar ]
                b = maxp[ ipar ]

                p[ i,ipar ] = p[ i,ipar ]*random.uniform( a,b )/( b-a )

        return p

class _Elitism( _OperatorInterface ):

    def run( self, *params ):
        """
        :param params: (p,fitp,filhos,fitf)
        :return: pop1,fit1
        """
        p,fitp,filhos,fitf = params

        ini = len( p ) - len( filhos )
        pop1 = np.copy( p )
        fit1 = np.copy( fitp )

        df = pd.DataFrame( fitp )
        x = df.sort_values( 0,ascending=True )
        piores = x.index[ len( x ) - len( filhos ), : ]

        for index, pos in enumerate( piores ):
            pop1[ pos ] = filhos[ index ]
            fit1[ pos ] = fitf[ index ]

        return pop1, fit1
    



class OperatorFactory:
    @staticmethod
    def getOperator( name ):
        if name == 'Roleta':
            return _RoletaOperator( )
        if name == 'Cruzamento':
            return _CruzamentoOperator( )
        if name == 'Mutacao':
            return _MutatacaoOperator( )
        if name == 'Elitismo':
            return _ElitismoOperator( )