from Genetic.Operators import *
import numpy as np
from Data.Population import *
import matplotlib.pyplot as plt


def operator(name, *params):
    return OperatorFactory().getOperator(name).run(*params)

def alp(x, y):
    fun = -(x * y) ** (0.5) * np.sin(x) * np.sin(y)
    return fun


if __name__ == "__main__":
    xobs = np.linspace( -10,10,300 )
    zobs = np.zeros( len( xobs ) )
    xmin, xmax = 0.0, 10.0
    ymin, ymax = 0.0, 10.0
    min_bounds = [xmin, ymin]
    max_bounds = [xmax, ymax]
    npop = 300
    pmut = 0.1
    ngera = int(100)
    npar = len(min_bounds)
    conv = []
    best = []

    fit = np.zeros((npop))

    pop = Fontes( )
    pop.Gera( min_bounds, max_bounds, nfontes= npop )
    fontes = pop.asArray( )
    gz = pop.Gz( xobs, zobs )

    for n in range(ngera):
        # Etapa 02: Avaliacao da funcao objetivo:
        fit = alp( fontes[:, 0], fontes[:, 1] )

        # Etapa 03: Selecao dos pais (roleta viciada)
        pais = operator('Roleta',fit)

        # Etapa 04: Definicao da subpopulacao para o cruzamento:
        pcruz = np.zeros((len(pais), npar))
        pcruz = fontes[pais, 0:2]

        # Etapa 05: Cruzamento para criacao dos filhos:
        filhos = operator('Cruzamento',pcruz)

        # Etapa 06: Aplicacao de mutacao em alguns individuos da populacao de filhos:
        filhos = operator('Mutacao',filhos, pmut, min_bounds, max_bounds)

        # Etapa 07: Calculo das aptidoes dos filhos:
        fit_filhos = np.zeros(len(filhos))
        fit_filhos = alp(filhos[:, 0], filhos[:, 1])

        # Etapa 08: Elitismo para colocar os filhos na populacao original:
        fontes, fit = operator('Elitismo',fontes[:,0:2], fit, filhos, fit_filhos)

    # Etapa 09: convergencia:
    iwinner = np.argmin(fit)
    best.append(fontes[iwinner, :])
    print(best)
