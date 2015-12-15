# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 17:58:02 2015

@author: markcutkosky
"""

import numpy as np

# Compute points for a circular arc
# given center, radius, start angle, end angle, numsteps
# cpoint is a 2 element array [x,y].
# Output is an Nx2 array of [x,y] points as rows.
def arcpoints(cpoint,radius,thetastart,thetaend,numsteps):
    thetas = np.linspace(thetastart,thetaend,numsteps)
    plotpts = np.zeros((numsteps,2),float)          #array for the output
    
    for i in range(0,numsteps):
        plotpts[i,0] = cpoint[0] + radius*np.cos(thetas[i])
        plotpts[i,1] = cpoint[1] + radius*np.sin(thetas[i])

    return plotpts
#########################