# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 14:09:47 2015
@author: markcutkosky
"""
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