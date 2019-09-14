import matplotlib.pyplot as plt
import numpy as np

def plotRect( rect , Gz, xobs, zlim, fill = False ):

    model = rect

    plt.subplot(211)
    plt.plot(xobs, Gz)
    plt.xlim(min(xobs), max(xobs))
    plt.grid()

    plt.subplot(212)
    plt.plot([model.params[0], model.params[0], model.params[1], model.params[1], model.params[0]], \
             [model.params[2], model.params[3], model.params[3], model.params[2], model.params[2]], ".-")
    plt.grid()
    if fill == True:
        plt.fill_between([model.params[0], model.params[0], model.params[1], model.params[1], model.params[0]], \
                         [model.params[2], model.params[3], model.params[3], model.params[2], model.params[2]])

    plt.ylim(0 , 1000 )
    plt.xlim(min(xobs), max(xobs))
    plt.gca().invert_yaxis()
    plt.show()
