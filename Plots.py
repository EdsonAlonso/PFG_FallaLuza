import matplotlib.pyplot as plt
import numpy as np

def plotRect( rect , Gz, xobs, zlim, fill = False ):

    models = rect

    plt.subplot(211)
    Gz_model = 0
    for gz in Gz:
        Gz_model += gz

    plt.plot(xobs, Gz_model,'b' )
    plt.xlim(min(xobs), max(xobs))
    plt.grid()

    plt.subplot(212)
    for model in models:
        plt.plot([model.params[0], model.params[0], model.params[1], model.params[1], model.params[0]], \
                 [model.params[2], model.params[3], model.params[3], model.params[2], model.params[2]], "-b")

        if fill == True:
            plt.fill_between([model.params[0], model.params[0], model.params[1], model.params[1], model.params[0]], \
                             [model.params[2], model.params[3], model.params[3], model.params[2], model.params[2]], alpha = 0.3, facecolor = 'blue')

    plt.grid()
    plt.ylim(0 , 1000 )
    plt.xlim(min(xobs), max(xobs))
    plt.gca().invert_yaxis()
    plt.show()
