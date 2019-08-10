import numpy as np
import random
from abc import ABC,abstractmethod
import pandas as pd
from modules.auxiliar import sigmoide


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
        prob = sigmoide( params[ 0 ] )
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

        self.p = params[ 0 ]
        final = len( self.p )

        npar = np.size( self.p,1 )
        npop = np.size( self.p,0 )

        if npop%2 != 0:
            npop = npop - 1
            final = len( self.p ) - 1

        nfilhos = int( npop/2 )

        pais = self.p[ 0:nfilhos, : ]
        maes = self.p[ nfilhos:final, : ]

        self.filhos = ( pesomae*maes + pesopai*pais )/( pesomae + pesopai )

        return self.filhos

class _MutacaoOperator( _OperatorInterface ):

    def run( self, *params ):
        """
        :param params: (p, probmut, minp, maxp)
        :return: p: população mutada
        """
        self.p,probmut,minp,maxp = params

        npar = np.size( self.p,1 )
        npop = np.size( self.p,0 )

        for i in range( npop ):
            rand = random.random( )
            if probmut <= rand:
                ipar = random.randint( 0,npar-1 )
                a = minp[ ipar ]
                b = maxp[ ipar ]

                self.p[ i,ipar ] = self.p[ i,ipar ]*random.uniform( a,b )/( b-a )

        return self.p

class _ElitismoOperator( _OperatorInterface ):

    def run( self, *params ):
        """
        :param params: (pop,fitp,filhos,fitf)
        :return: pop1,fit1
        """
        p,fitp,filhos,fitf = params

        ini = len(p) - len(filhos)
        self.pop1 = np.copy(p)
        self.fit1 = np.copy(fitp)

        df = pd.DataFrame(fitp)
        x = df.sort_values(0, ascending=True)
        piores = x.index[len(x) - len(filhos):]

        for index, pos in enumerate(piores):
            self.pop1[pos] = filhos[index]
            self.fit1[pos] = fitf[index]

        return self.pop1, self.fit1




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