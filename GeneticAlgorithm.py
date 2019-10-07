from Data.Population import *
from Genetic.Operators import *
import numpy as np
from Data.Functionals import theta


class GeneticAlgorithm( ):

    def __init__( self, fitfunction, fit_param, min_bounds, max_bounds, pmut, nfontes, nind, nobs ):
        self.fit_function  = fitfunction
        self.winner = None
        self.min_bounds = min_bounds
        self.max_bounds = max_bounds
        self.pmut = pmut
        self.fit_params = fit_param
        self.nfontes = nfontes
        self.nind = nind
        self.xobs = np.linspace( min_bounds[ 0 ], max_bounds[ 0 ] , nobs )
        self.zobs = np.zeros( len( self.xobs ) )
        self.bests_theta = [ ]

    def Initialize( self ):
        self.pop = Fontes( )
        self.pop.Gera( self.min_bounds, self.max_bounds, self.nfontes, self.nind )
        self.fontes = self.pop.asArray( )
        self.fontes_gz = self.pop.Gz( self.xobs, self.zobs )

    def FirstFit( self ):
        self.fit = self.fit_function(self.fit_params[ 0], self.fontes_gz, self.fit_params[ 1 ], \
                                     self.fontes, self.fit_params[ 2 ])
        self.iwinner = np.argmin( self.fit )
        self.winner = self.fontes[ self.iwinner ]
        self.melhor = self.fit[ self.iwinner ]

    def start( self, ngera ):
        self.ngera = int( ngera )
        self.Initialize( )
        self.FirstFit( )

        c = 0
        for i in range( self.ngera ):
            c += 1

            print( f'Geração { i }' )
            # Etapa 03: Selecao dos pais (roleta viciada)

            pais = operator( 'Roleta', np.array( self.fit ) )

            # Etapa 04: Definicao da subpopulacao para o cruzamento:

            popcruz = [ ]

            for pai in pais:
                popcruz.append( self.fontes[ pai ] )

            # Etapa 05: Cruzamento para criacao dos filhos:
            filhos = operator( 'Cruzamento', popcruz )

            # Etapa 06: Aplicacao de mutacao em alguns individuos da populacao de filhos:

            filhos = operator( 'Mutacao', filhos, self.pmut, self.min_bounds, self.max_bounds )
            self.fontes_gz = self.pop.Gz( self.xobs, self.zobs, self.pop.Gera_from_Existing( filhos ) )

            # Etapa 07: Calculo das aptidoes dos filhos:

            fit_filhos = self.fit_function(self.fit_params[ 0 ], self.fontes_gz, self.fit_params[ 1 ], \
                                     filhos, self.fit_params[ 2 ])

            # Etapa 08: Elitismo para colocar os filhos na populacao original:
            self.fontes, self.fit = operator( 'Elitismo', self.fontes, self.fit, filhos, fit_filhos )
            
            novotheta = theta( self.fit_params[ 1 ], self.fontes )

            self.bests_theta.append( novotheta[ np.argmin( self.fit ) ] )

            if self.fit[ np.argmin( self.fit ) ] < self.melhor:
                c = 0
                print( self.fit[ np.argmin( self.fit ) ] )
                self.melhor = self.fit[ np.argmin( self.fit ) ]

            if c >= 10000:
                break

        print( f'Melhor: { self.fit[ np.argmin( self.fit ) ] }' )

        # Etapa 09: convergencia:

        self.iwinner = np.argmin( self.fit )
        self.winner = self.fontes[ self.iwinner ]
