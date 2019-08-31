from Data.Population import *
from Data.Functionals import phi
from Models import rect
from Genetic.Operators import *

#Etapa 00: Definições Iniciais:

xobs = np.linspace(0, 10, 300)
zobs = np.zeros(len(xobs))
model = rect(4.5, 3.0, 5.0, 4.0, 3e8)
model_gz = model.Gz(xobs, zobs)
model_gz_noised = model.addnoise()
xobs = np.linspace(0, 10, 300)
zobs = np.zeros(len(xobs))
xmin, xmax = 0.0, 10.0
ymin, ymax = 0.5, 10.0
min_bounds = [xmin, ymin, 1e5]
max_bounds = [xmax, ymax, 1e9]
npop = 50
nind = 500
pmut = 0.1
ngera = 500


#Etapa 01: Inicialização da População:

pop = Fontes( )
pop.Gera( min_bounds, max_bounds, npop, nind )
fontes = pop.fontes

#Etapa 02: Avaliação da População Inicial:
fit = phi( model_gz_noised, pop.Gz( xobs, zobs ) )

for i in range( ngera ):

    print(f'Geração {i}')
    # Etapa 03: Selecao dos pais (roleta viciada)

    pais = operator( 'Roleta', np.array( fit ) )


    # Etapa 04: Definicao da subpopulacao para o cruzamento:

    popcruz = [ ]
    for pai in pais:
        popcruz.append( fontes[ pai ]  )

    # Etapa 05: Cruzamento para criacao dos filhos:
    filhos = operator( 'Cruzamento', popcruz )


    # Etapa 06: Aplicacao de mutacao em alguns individuos da populacao de filhos:

    filhos = operator( 'Mutacao', filhos, pmut, min_bounds, max_bounds )
    filhos = pop.Gera_from_Existing( filhos )


    # Etapa 07: Calculo das aptidoes dos filhos:

    fit_filhos = phi( model_gz_noised, pop.Gz( xobs, zobs , fontes = filhos ) )


    # Etapa 08: Elitismo para colocar os filhos na populacao original:
    fontes, fit = operator( 'Elitismo', fontes, fit, filhos, fit_filhos )


# Etapa 09: convergencia:

iwinner = np.argmin( fit )
best = fontes[ iwinner ]

gz_melhor = 0
for esfera in best:
    gz_melhor += esfera.Gz( xobs, zobs)
    

import matplotlib.pyplot as plt

plt.figure()
plt.subplot(211)
plt.plot(xobs, gz_melhor , label = 'Gz bolinhas')
plt.plot(xobs, model_gz_noised, label = 'Gz observado + ruído')
plt.grid( )
plt.legend( )
plt.subplot(212)
for fonte in best:
    plt.scatter( fonte.params[0], fonte.params[1], c = 'black' )
plt.xlim(min(xobs), max(xobs) )
plt.gca().invert_yaxis()
plt.grid( )
#plt.savefig('Imagegm'+str(index)+'.png')
plt.show( )