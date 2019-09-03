import numpy as np
import random
from abc import ABC,abstractmethod
import pandas as pd
from modules.auxiliar import sigmoide, sortbetween
from Data.Functionals import somadict,dictTimesConstant


def operator( name, *params ):
    return OperatorFactory( ).getOperator( name ).run( *params )

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
        fit = params[ 0 ][ : ]
        prob = sigmoide( fit )
        self.pai = [ ]

        for i in range( len( prob ) ):
            r = random.random( )
            if prob[ i ] >= r:
                self.pai.append( i )

        return np.array( self.pai )

class _CruzamentoOperator( _OperatorInterface ):

    def run(self, *params):
        """
        :param params: array contendo a população de candidatos a cruzamento
        :return: filhos: array contendo os filhos
        """

        pesopai = random.random( )
        pesomae = random.random( )

        self.filhos = [ ]

        self.p = np.copy( params[ 0 ] )

        final = len( self.p )

        npop = len( self.p )

        if npop%2 != 0:
            npop = npop - 1
            final = len( self.p ) - 1

        nfilhos = int( npop/2 )

        pais =  self.p[ 0:nfilhos ]
        maes =  self.p[ nfilhos:final ]
        num = [ ]
        for i in range( len( pais ) ):
            pais[ i ] = dictTimesConstant( pais[ i ], pesopai )
            maes[ i ] = dictTimesConstant( maes[ i ], pesomae )
            num = somadict( pais[ i ], maes[ i ] )
            self.filhos.append( num/ (pesopai + pesomae) )
            num = [ ]

        return self.filhos


class _MutacaoOperator( _OperatorInterface ):

    def run( self, *params ):
        """
        :param params: (filhos, probmut, minp, maxp)
        :return: p: população mutada
        """
        pop,probmut,minp,maxp = params

        npar = len( pop[ 0 ][ 0 ] )

        nind = len( pop )

        self.temp = np.copy( pop )

        for index,ind in enumerate( self.temp ):
            rand = random.random( )
            if probmut > rand:
                ipar = random.randint(0, npar - 1)
                a = minp[ ipar ]
                b = maxp[ ipar ]
                factor = ( sortbetween( a, b )/( b - a ) )
                for fonte in ind:
                    fonte[ ipar ] = fonte[ ipar ]*factor

        return self.temp

class _ElitismoOperator( _OperatorInterface ):

    def run( self, *params ):
        """
        :param params: (pop,fitp,filhos,fitf)
        :return: pop1,fit1
        """
        pop,fitpop,filhos,fitf = params

        ini = len( pop ) - len( filhos )

        df = pd.DataFrame( fitpop )
        x = df.sort_values(0, ascending=True)
        piores = x.index[ ini: ]

        self.pop = pop[ : ]
        self.fitpop = fitpop[ : ]
        for index, pos in enumerate(piores):
            self.pop[ pos ] = filhos[ index ]
            self.fitpop[ pos ] = fitf[ index ]

        return self.pop, self.fitpop




class OperatorFactory:
    @staticmethod
    def getOperator( name ):
        if name == 'Roleta':
            return _RoletaOperator( )
        if name == 'Cruzamento':
            return _CruzamentoOperator( )
        if name == 'Mutacao':
            return _MutacaoOperator( )
        if name == 'Elitismo':
            return _ElitismoOperator( )