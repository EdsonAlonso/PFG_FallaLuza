from Data.Population import *
from Data.Functionals import phi
from Models import rect
from Genetic.Operators import *
import matplotlib.pyplot as plt
from time import time


#Etapa 00: Definições Iniciais:

xobs = np.linspace(-1000, 1000, 500)
zobs = np.zeros(len(xobs))
model = rect( -100,100,300,900,2 )
model_gz = model.Gz(xobs, zobs)
model_gz_noised = model.addnoise()
xmin, xmax = -1000.0, 1000.0
ymin, ymax = 200, 800.0
min_bounds = [xmin, ymin, 1e6]
max_bounds = [xmax, ymax, 1e10]
nfontes = 40
nind = 500
pmut = 0.1
ngera = int( 1e5 )

t1 = time( )

#Etapa 01: Inicialização da População:

pop = Fontes( )
pop.Gera( min_bounds, max_bounds, nfontes, nind )
fontes = pop.asArray( )
gz_fonts = pop.Gz( xobs, zobs )


#Etapa 02: Avaliação da População Inicial:
fit = phi( model_gz_noised, gz_fonts )

iwinner = np.argmin( fit )
best =  fontes[ iwinner ]
melhor = fit[ np.argmin( fit ) ]

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
        self.__fontes__ = pop.Gera_from_Existing( self.fontes )
        self.iwinner = np.argmin( self.fit )
        self.winner = self.fontes[ self.iwinner ]
        self.melhor = self.fit[ np.argmin( self.fit ) ]

    def start( self, ngera ):
        self.ngera = int( ngera )
        self.Initialize( )
        c = 0
        for i in range(self.ngera):

            c += 1
            print(f'Geração {i}')
            # Etapa 03: Selecao dos pais (roleta viciada)

            pais = operator('Roleta', np.array(self.fit))

            # Etapa 04: Definicao da subpopulacao para o cruzamento:

            popcruz = []

            for pai in pais:
                popcruz.append(self.fontes[pai])

            # Etapa 05: Cruzamento para criacao dos filhos:
            filhos = operator('Cruzamento', popcruz)

            # Etapa 06: Aplicacao de mutacao em alguns individuos da populacao de filhos:

            filhos = operator('Mutacao', filhos, self.pmut, self.min_bounds, self.max_bounds)
            gz_fonts = pop.Gz(xobs, zobs, pop.Gera_from_Existing(filhos))

            # Etapa 07: Calculo das aptidoes dos filhos:

            fit_filhos = phi(self.model_gz, gz_fonts)

            # Etapa 08: Elitismo para colocar os filhos na populacao original:
            self.fontes, self.fit = operator('Elitismo', self.fontes, self.fit, filhos, fit_filhos)

            if fit[ np.argmin( fit ) ] < self.melhor:
                c = 0
                print(fit[np.argmin(fit)])
                self.melhor = fit[ np.argmin( fit ) ]

            if c >= 10000:
                break

        print(f'Melhor: {fit[np.argmin(fit)]}')
        print(f'Tempo Total {time() - t1}')
        
        # Etapa 09: convergencia:

        self.iwinner = np.argmin(fit)
        self.winner = fontes[iwinner]

if __name__ == '__main__':
    ga = GeneticAlgorithm( fontes, fit, model_gz, min_bounds, max_bounds, pmut)
    ga.start( 100 )
    print( ga.winner )

