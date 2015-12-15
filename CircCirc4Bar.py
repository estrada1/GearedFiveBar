# -*- coding: utf-8 -*-
"""
Started Thu Aug 27 12:33:35 2015
@author: markcutkosky
Sometimes it's convenient to define a linkage with an initial
set of joint positions instead of link lengths.
Let's do that by reading a text file 'InitialJoints.txt'
with the four X,Y joint locations (one per row),
followed by the coupler point X,Y location.
Then we compute arrays of X,Y positions (one per row) 
for the various joints and coupler locations.
We plot them, and save them to a file 'CircCirc4BarPoints.txt'
"""

# Solution uses circcirc.py (adapted from circcirc.m in Matlab
# mapping toolbox) to solve a 4-bar linkage.

# Use numpy and matplotlib for Matlab-like stuff
import numpy as np
from matplotlib.pyplot import *  #Lazy...
import os

#load some handy utility functions:
from ArcPoints import arcpoints
from CircCirc import circcirc
from CouplerPoint import coupler

####################################################################    
#Make sure we are in the right directory...
# If necessary:
# os.chdir('/Volumes/ExTraSpace/Courses/MatlabPython/Python4BarExamples')
print("Reading from: " + os.getcwd() + "/InitialJoints.txt\n")

#Load initial configuration
pointsdata = np.loadtxt('InitialJoints.txt')
initjoints = pointsdata[0:4,:]
initcoupler = pointsdata[4,:]

#Specify angle (radians) we want to rotate through
thetastart = 0.
thetaend = 1.95*np.pi
#Specify number steps to take
numsteps = 20
    
#Get ready for plotting
clf()
grid(True)
axes().set_aspect('equal', 'datalim')  #square and limited by data

# Plot the initial configuration in blue, with black line to coupler
plot(initjoints[:,0],initjoints[:,1],'b')
plot((initjoints[1,0],initcoupler[0]),(initjoints[1,1],initcoupler[1]),'k')

#Find lengths of the links. l2 is length of link2 between
# joint12 and joint23, and so forth...
# numpy.linalg.norm() computes the norm of a matrix;
# in this case it's just the square root of the sum of squares :-)
d12 = initjoints[1,:]-initjoints[0,:]
l2 = np.linalg.norm(d12)
d23 = initjoints[2,:]-initjoints[1,:]
l3 = np.linalg.norm(d23)
d34 = initjoints[3,:]-initjoints[2,:]
l4 = np.linalg.norm(d34)
dc3 = initcoupler - initjoints[1,:]
lc = np.linalg.norm(dc3)

# Find the angle gammac between link3 and coupler
# Use arctan2(deltay,deltax) for unambiguous sign convention.
gamma1 = np.arctan2(d23[1],d23[0])
gamma2 = np.arctan2(dc3[1],dc3[0])
gammac = -gamma1+gamma2

# Use circcirc() to see which solution for joint34
# matches the one we've started with.
# This determines which 'assembly' we have.
# If neither solution matches, something went wrong...
# We use numpy.allclose() to check if negligible difference.
joint34 = circcirc(initjoints[1,:],l3,initjoints[3,:],l4)
if(np.allclose(joint34[0,:],initjoints[2,:])):
    assembly = 0
elif(np.allclose(joint34[1,:],initjoints[2,:])):
    assembly = 1
else:
    print('Hmmm, neither solution matches the input point...')

# Use Arcpoints() to get the positions of joint23,
# i.e., of the joint that connects links 2 and 3, where
# link2 is the input crank.
joints23 = arcpoints(initjoints[0,:],l2,thetastart,thetaend,numsteps)

# For each joint23 location, find the corresponding
# joint34 and coupler locations
joints34 = np.zeros((numsteps,2),float)
couplerpts = np.zeros((numsteps,2),float)
for i in range(0,numsteps):   
    intersects = circcirc(joints23[i,:],l3,initjoints[3,:],l4)
    joints34[i,:] = intersects[assembly,:]
    couplerpts[i,:] = coupler(joints34[i,:],joints23[i,:],lc,np.pi+gammac)


#Plot the various points - may want to modify this depending
# on what effects we are looking for.
# Currently plots a fat dot at start of angle range and a
# square at end of angle range.
# numpy.plot() works conveniently for lists of 'x' and 'y' values.
plot(joints23[:,0],joints23[:,1],color = 'g',linewidth=0.5)
plot(joints23[0,0],joints23[0,1],'o')
plot(joints23[numsteps-1,0],joints23[numsteps-1,1],'s')
plot(joints34[:,0],joints34[:,1],color = 'r',linewidth=0.5)
plot(couplerpts[:,0],couplerpts[:,1],color = 'k',linewidth=0.5)
plot(couplerpts[:,0],couplerpts[:,1],'*')
plot(couplerpts[0,0],couplerpts[0,1],'o')
plot(couplerpts[numsteps-1,0],couplerpts[numsteps-1,1],'s')
show()
#Save a PDF of the plot 
savefig('CircCirc4Bar.pdf')

# Open file for writing joint and coupler points data
# in format that Excel, Matlab, Numpy, etc. can read.
# If we are not sure where we are writing:
#print("Data written: " + os.getcwd() + "/CircCirc4BarPoints.txt\n")   
Table = np.column_stack((joints23,joints34,couplerpts))
f_handle = file('CircCirc4BarPoints.txt', 'w')
headerstring = "joint23(x,y), joint34(x,y),   coupler(x,y)"
np.savetxt(f_handle,Table,header=headerstring,delimiter='\t',newline='\n',fmt='%4.2f')
f_handle.close()

    