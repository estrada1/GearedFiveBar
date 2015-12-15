
# -*- coding: utf-8 -

import numpy as np

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
      