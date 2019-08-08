from Genetic.Operators import *
import numpy as np

def operator(name, *params):
    return OperatorFactory().getOperator(name).run(*params)

def pop_inicial(parmin, parmax, npop):
    """
    parmin: lista com o limite inferior de todos os parametros do problema:
    parmax:lista com o limite superior de todos os parametros do problema:
    npop: numero inteiro indicando o numero total de individuos na populacao:
    """
    # numero total de parametros do problema:
    npar = len(parmin)
    pop = np.zeros((npop, npar))

    for i in range(npar):
        for j in range(npop):
            pop[j, i] = random.uniform(parmin[i], parmax[i])

    return pop


def alp(x, y):
    fun = -(x * y) ** (0.5) * np.sin(x) * np.sin(y)
    return fun


if __name__ == "__main__":
    xmin, xmax = 0.0, 10.0
    ymin, ymax = 0.0, 10.0
    min_bounds = [xmin, ymin]
    max_bounds = [xmax, ymax]
    npop = 300
    pmut = 0.1
    ngera = int(2e4)
    npar = len(min_bounds)
    conv = []
    best = []

    fit = np.zeros((npop))

    pop = pop_inicial(min_bounds,max_bounds,npop)

    for n in range(ngera):
        # Etapa 02: Avaliacao da funcao objetivo:
        fit = alp(pop[:, 0], pop[:, 1])

        # Etapa 03: Selecao dos pais (roleta viciada)
        pais = operator('Roleta',fit)

        # Etapa 04: Definicao da subpopulacao para o cruzamento:
        pcruz = np.zeros((len(pais), npar))
        pcruz = pop[pais, :]

        # Etapa 05: Cruzamento para criacao dos filhos:
        filhos = operator('Cruzamento',pcruz)

        # Etapa 06: Aplicacao de mutacao em alguns individuos da populacao de filhos:
        filhos = operator('Mutacao',filhos, pmut, min_bounds, max_bounds)

        # Etapa 07: Calculo das aptidoes dos filhos:
        fit_filhos = np.zeros(len(filhos))
        fit_filhos = alp(filhos[:, 0], filhos[:, 1])

        # Etapa 08: Elitismo para colocar os filhos na populacao original:
        pop, fit = operator('Elitismo',pop, fit, filhos, fit_filhos)

    # Etapa 09: convergencia:
    iwinner = np.argmin(fit)
    best.append(pop[iwinner, :])
    print(best)
