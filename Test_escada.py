from Models import rect
from Plots import plotRect
import numpy as np

xobs = np.linspace( -1000, 1000, 300 )
zobs = np.zeros( len( xobs ) )
rec1 = rect( -300, -100, 50, 150, 2 )
rec2 = rect( -200, 0, 150, 250, 2 )
rec3 = rect( -100, 100, 250, 350, 2 )
rec4 = rect( 0, 200, 350, 450, 2 )
rec5 = rect( 100, 300, 450, 550, 2 )
gz1 = rec1.Gz( xobs, zobs )
gz2 = rec2.Gz( xobs, zobs )
gz3 = rec3.Gz( xobs, zobs )
gz4 = rec4.Gz( xobs, zobs )
gz5 = rec5.Gz( xobs, zobs )

if __name__ == '__main__':
    plotRect( [ rec1, rec2, rec3, rec4, rec5 ], [ gz1, gz2, gz3, gz4, gz5 ], xobs, 1000, True)
