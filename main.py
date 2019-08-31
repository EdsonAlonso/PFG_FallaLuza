from Genetic.Operators import operator
import numpy as np
from Data.Population import Fontes
import matplotlib.pyplot as plt
from Models import rect, sphere
from modules.auxiliar import sigmoide

def alp(x, y):
    fun = -(x * y) ** (0.5) * np.sin(x) * np.sin(y)
    return fun

def phi( x,y ):
    return ( np.linalg.norm( x - y ) )**2


if __name__ == "__main__":
    xobs = np.linspace( 0,10,300 )
    zobs = np.zeros( len( xobs ) )
    xmin, xmax = 2.0, 8.0
    ymin, ymax = 0.5, 10.0
    min_bounds = [xmin, ymin]
    max_bounds = [xmax, ymax]
    npop = 20
    pmut = 0.1
    ngera = int( 500 )
    npar = len( min_bounds )
    conv = [ ]
    best = [ ]

    model = rect( 4.5, 3.0, 5.0 , 4.0 , 3e8)
    model_gz = model.gz( xobs, zobs )

    fit = [ ]
    pop = Fontes( )
    pop.Gera( min_bounds, max_bounds, nfontes = npop , nind = 4)
    fontes = pop.asArray( )
    gz = pop.Gz( xobs, zobs )

    for index,ind in enumerate(pop.fontes):
        plt.figure()
        plt.title(f'Individuo {index}')
        plt.subplot(211)
        plt.plot(xobs, gz[index])
        plt.grid( )

        plt.subplot(212)
        for fonte in ind:
            plt.scatter( fonte.params[0], fonte.params[1], c = 'black' )
        plt.xlim(min(xobs), max(xobs) )
        plt.gca().invert_yaxis()
        plt.grid( )
        #plt.savefig('Imagegm'+str(index)+'.png')
    plt.show( )

    #
    # plt.figure()
    # for n in range(ngera):
    #
    #     # Etapa 03: Selecao dos pais (roleta viciada)
    #
    #     pais = operator( 'Roleta', np.array( fit ) )
    #
    #     # Etapa 04: Definicao da subpopulacao para o cruzamento:
    #     pcruz = [ ]
    #     for pai in pais:
    #         pcruz.append(np.array( fontes[ pai ][ :, 0:3 ] ) )
    #
    #     # Etapa 05: Cruzamento para criacao dos filhos:
    #     filhos = operator( 'Cruzamento', pcruz )
    #
    #     # Etapa 06: Aplicacao de mutacao em alguns individuos da populacao de filhos:
    #     filhos = operator( 'Mutacao', filhos, pmut, min_bounds, max_bounds )
    #
    #     pop = Fontes( )
    #     filhos_novos = pop.Gera_from_Existing( filhos )
    #
    #
    #     div = len( filhos )
    #     gz_filhos = [ ]
    #     liminf = 0
    #     limsup = 0
    #     for i in range( int( div ) ):
    #         liminf += 300 * i
    #         limsup += 300
    #         gz_temp = 0
    #         for index, filho in enumerate( filhos_novos ):
    #             if liminf <= index < limsup:
    #                 gz_temp += filho.gz( xobs, zobs )
    #
    #         gz_filhos.append( gz_temp )
    #
    #         liminf = 0
    #
    #     # Etapa 07: Calculo das aptidoes dos filhos:
    #     fit_filhos = [ ]
    #
    #     for k in range( int( div ) ):
    #         fit_filhos.append( phi( model_gz, gz_filhos[ k ] ) )
    #
    #     # Etapa 08: Elitismo para colocar os filhos na populacao original:
    #     fontes, fit = operator( 'Elitismo', fontes, fit, filhos, fit_filhos )
    #
    # # Etapa 09: convergencia:
    # iwinner = np.argmin( fit )
    # best.append( fontes[ iwinner ][ : ] )
    #
    # melhor =  pop.Gera_from_Existing( best )
    #
    # gz_melhor = 0
    #
    # for bolinha in melhor:
    #     gz_melhor += bolinha.gz( xobs, zobs )
    #
    #
    # plt.subplot( 211 )
    # plt.plot( xobs,model_gz,'r', label = 'Sinal Observado' )
    # plt.plot( xobs, gz_melhor, label = 'Sinal Invertido' )
    # plt.legend( )
    #
    # plt.subplot( 212 )
    # plt.scatter( best[ 0 ][ :,0 ],best[ 0 ][ :,1 ] )
    # plt.xlim( min(xobs)-1, max( xobs ) +1)
    # plt.show( )
    #
    #
