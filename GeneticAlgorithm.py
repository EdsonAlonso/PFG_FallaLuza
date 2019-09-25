from Data.Population import *
from Data.Functionals import phi
from Genetic.Operators import *

xobs = np.linspace(-1000,1000)
zobs = np.zeros((len(xobs)))
class GeneticAlgorithm( ):

    def __init__( self, Fontes, fit, modelfunction, min_bounds, max_bounds, pmut ):
        self.fit  = fit
        self.fontes = Fontes
        self.pop = None
        self.winner = None
        self.min_bounds = min_bounds
        self.max_bounds = max_bounds
        self.pmut = pmut
        self.model_gz = modelfunction


    def Initialize( self ):
        self.pop = Fontes( )
        self.__fontes__ = self.pop.Gera_from_Existing( self.fontes )
        self.iwinner = np.argmin( self.fit )
        self.winner = self.fontes[ self.iwinner ]
        self.melhor = self.fit[ self.iwinner ]

    def start( self, ngera ):
        self.ngera = int( ngera )
        self.Initialize( )
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
            gz_fonts = self.pop.Gz( xobs, zobs, self.pop.Gera_from_Existing( filhos ) )

            # Etapa 07: Calculo das aptidoes dos filhos:

            fit_filhos = phi( self.model_gz, gz_fonts )

            # Etapa 08: Elitismo para colocar os filhos na populacao original:
            self.fontes, self.fit = operator( 'Elitismo', self.fontes, self.fit, filhos, fit_filhos )

            print( self.fontes[ np.argmin( self.fit ) ] )

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


