# -*- coding: utf-8 -*-
"""
Created Tue Sep  8 17:58:02 2015 
@author: markcutkosky
Utility functions useful for solving linkages. Used in examples:
 CircCirc4Bar.py, Klann-ish.py, Jansen-lite.py, Geared5Bar.py
Contents:
* arcpoints(): Compute points in an arc.
* coupler(): Given 2 points and an angle and distance, compute the third point.
* circcirc(): Compute intersection of two circles.
* grashof(): Check if 4-bar linkage satisfies Grashof criterion (continuous rotation)

Functions all use Numpy and Matplotlib for Matlab-like syntax so
they are easy to translate to Matlab. Points are 2 element arrays (x,y).
Trajectories are Nx2 arrays with points in each row.
"""

import numpy as np

#########################
# Compute points for a circular arc
# given center, radius, start angle, end angle, numsteps
# cpoint is a 2 element array [x,y].
# Output is Nx2 array of [x,y] points as rows.
def arcpoints(cpoint,radius,thetastart,thetaend,numsteps):
    thetas = np.linspace(thetastart,thetaend,numsteps)
    plotpts = np.zeros((numsteps,2),float)          #array for the output
    
    for i in range(0,numsteps):
        plotpts[i,0] = cpoint[0] + radius*np.cos(thetas[i])
        plotpts[i,1] = cpoint[1] + radius*np.sin(thetas[i])

    return plotpts

#########################
#Given two points, travel from point1 to point2, then rotate
#(anticlockwise) by theta, and proceed a distance r to
#a third point. Return coords of that point.

#Useful for plotting coupler points or end
#points of bent links. 
#point1, point2 and cpoint are 2-element arrays
def coupler(point1,point2,r,theta):
      delta = point2-point1
      phi = np.arctan2(delta[1],delta[0])
      psi = phi+theta
      rx = r*np.cos(psi)
      ry = r*np.sin(psi)
      cpoint = point2+np.array([rx,ry])
      return cpoint

#########################

# Adapted from circirc.m in the Matlab Mapping Toolbox
# https://lost-contact.mit.edu/afs/cs.stanford.edu/package/matlab-r2009b/matlab/r2009b/toolbox/map/map/circcirc.m      

# Given two circles centered at point1 and point2, with radii
# r1 and r2, respectively, what are the two intersections?
# Useful for linkage problems with two known joint locations
# and two link lengths -- find the third joint.

# point1, point2 are 2-element arrays. circpoints is an
# array of two points, corresponding to the two solutions.
# The first solution will be the one that is on the left 
# when traveling from point1 to point2.

import numpy as np

def circcirc(point1,r1,point2,r2):
    if(r1 < 0 or r2 < 0):
        print('\n\t circirc: radii must be positive')
        
    delta = point2 - point1
    r12sq = np.dot(delta,delta)
    r12 = np.sqrt(r12sq)
    if(r12 > r1+r2 or r1 > r2+r12 or r2 > r1+r12):
        print('\n\t circirc: circles do not intersect!')
        
    r1sq = r1*r1
    r2sq = r2*r2

    phi = np.arctan2(delta[1],delta[0])
    alpha1 = np.arccos((r12sq+r1sq-r2sq)/(2*r1*r12))
    theta1 = phi+alpha1
    theta2 = phi-alpha1
    
    c1 = point1 + r1*np.array([np.cos(theta1),np.sin(theta1)])
    c2 = point1 + r1*np.array([np.cos(theta2),np.sin(theta2)])

    #Create 2x2 array for output points
    circpoints = np.row_stack((c1,c2))
    # first point:   circpoints[0,:]
    # second point:  circpoints[1,:]
    
    return circpoints

#########################

def grashof(link1,link2,link3,link4):
    # if (longest+shortest <= sum(other two)) then isgrashof = True
    linkarray = np.sort([link1,link2,link3,link4])
    isgrashof = True
    if (linkarray[0]+linkarray[3] > linkarray[1]+linkarray[2]):
        isgrashof = False

    return isgrashof
