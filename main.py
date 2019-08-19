from Genetic.Operators import operator
import numpy as np
from Data.Population import Fontes
import matplotlib.pyplot as plt
from Models import rect, sphere


def alp(x, y):
    fun = -(x * y) ** (0.5) * np.sin(x) * np.sin(y)
    return fun

def phi( x,y ):
    return ( np.linalg.norm( x - y ) )**2


if __name__ == "__main__":
    xobs = np.linspace( 0,10,300 )
    zobs = np.zeros( len( xobs ) )
    xmin, xmax = 3.0, 6.0
    ymin, ymax = 0.5, 10.0
    min_bounds = [xmin, ymin]
    max_bounds = [xmax, ymax]
    npop = 300
    pmut = 0.1
    ngera = int( 100 )
    npar = len( min_bounds )
    conv = [ ]
    best = [ ]
    
    model = rect( 4.5, 3.0, 5.0 , 4.0 , 3e8)
    model_gz = model.gz( xobs, zobs )

    fontes = [ ]
    fit = [ ]
    for j in range(20):
        pop = Fontes( )
        pop.Gera( min_bounds, max_bounds, nfontes = npop )
        fontes.append( pop.asArray( ))
        fit.append( phi( model_gz, pop.Gz( xobs,zobs ) ) )

    pais = operator( 'Roleta',np.array( fit ) )

    pcruz = [ ]
    for pai in pais:
        pcruz.append( np.array( fontes[ pai ][ :,0:3 ] ) )

    filhos = operator( 'Cruzamento', pcruz )

    filhos_mutados = operator( 'Mutacao', filhos, pmut, min_bounds, max_bounds )

    filhos_novos = pop.Gera_from_Existing( filhos_mutados )

    div = len( filhos_mutados )
    gz_filhos = [ ]
    liminf = 0
    limsup = 0
    for i in range( int( div ) ):
        liminf += 300*i
        limsup += 300
        gz_temp = 0
        for index, filho in enumerate(filhos_novos):
            if liminf <= index < limsup:
                 gz_temp += filho.gz( xobs, zobs )

        gz_filhos.append(  gz_temp )

        liminf = 0

    fit_filhos = [ ]
    for k in range( int( div ) ):
        fit_filhos.append( phi( model_gz, gz_filhos[ k ] ) )



    #
    # for n in range(ngera):
    #     # Etapa 02: Avaliacao da funcao objetivo:
    #     fit = alp( fontes[:, 0], fontes[:, 1] )
    #
    #     # Etapa 03: Selecao dos pais (roleta viciada)
    #     pais = operator('Roleta',fit)
    #
    #     # Etapa 04: Definicao da subpopulacao para o cruzamento:
    #     pcruz = np.zeros((len(pais), npar))
    #     pcruz = fontes[pais, 0:2]
    #
    #     # Etapa 05: Cruzamento para criacao dos filhos:
    #     filhos = operator('Cruzamento',pcruz)
    #
    #     # Etapa 06: Aplicacao de mutacao em alguns individuos da populacao de filhos:
    #     filhos = operator('Mutacao',filhos, pmut, min_bounds, max_bounds)
    #
    #     # Etapa 07: Calculo das aptidoes dos filhos:
    #     fit_filhos = np.zeros(len(filhos))
    #     fit_filhos = alp(filhos[:, 0], filhos[:, 1])
    #
    #     # Etapa 08: Elitismo para colocar os filhos na populacao original:
    #     fontes, fit = operator('Elitismo',fontes[:,0:2], fit, filhos, fit_filhos)
    #
    # # Etapa 09: convergencia:
    # iwinner = np.argmin(fit)
    # best.append(fontes[iwinner, :])
    # print(best)
