import numpy as np
import random
from abc import ABC,abstractmethod
import pandas as pd
from modules.auxiliar import sortbetween, normalize
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
        prob = normalize( fit )
        self.pai = [ ]
        for i in range( len( prob ) ):
            r = random.random( )
            if prob[ i ] >= r:
                self.pai.append( i )
        if len( self.pai ) == 1:
            if 0 in self.pai and 1 not in self.pai:
                self.pai.append( 1 )
            elif 1 in self.pai and 0 not in self.pai:
                self.pai.append( 0 )
            else:
                self.pai.append( 0 )
        elif len( self.pai ) == 0:
            self.pai.append( random.randint( 0, 500 ) )
            self.pai.append( random.randint( 0, 500 ) )

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

        self.p = params[ 0 ][ : ]

        final = len( self.p )

        npop = len( self.p )

        if npop%2 != 0:
            npop = npop - 1
            final = len( self.p ) - 1

        nfilhos = int( npop/2 )

        __pais =  self.p[ 0:nfilhos ]
        __maes =  self.p[ nfilhos:final ]
        num = 0
        den = pesomae + pesopai
        for i in range( len( __pais ) ):
            num = ( pesopai*__pais[ i ] + pesomae*__maes[ i ] )
            self.filhos.append( num / den )
            num = 0

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

        self.temp = pop[ : ]

        for index,ind in enumerate( self.temp ):
            rand = random.random( )
            if probmut > rand:
                ipar = random.randint(0, npar - 1)
                a = minp[ ipar ]
                b = maxp[ ipar ]
                if ipar != 2:
                    for fonte in ind:
                        factor = (sortbetween(a, b) / (b - a))
                        fonte[ ipar ] = fonte[ ipar ]*factor
                elif ipar == 2:
                    factor = (sortbetween(a, b) / (b - a))
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