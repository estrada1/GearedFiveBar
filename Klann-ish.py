# -*- coding: utf-8 -*-
"""
Created Sept. 10 2015
@author: markcutkosky
Example of solving the Klann linkage from initial joint locations
in http://www.mekanizmalar.com/mechanicalspider.html 
This code should work for any Klann-ish 6-bar with same 
basic topology.

This script follows the general approach of CirCirc4Bar.py but is
a bit more complicated so it's probably easiest to review that
example first to see how it works.
The code treats the sequence of locations for each joint
as a matrix of N rows by 2 colums for the X,Y coordinates.
See 
http://bdml.stanford.edu/uploads/Main/ME112LinkageLinks/KlannNotation.png
for the joint and link numbering convention used.
"""

# Use numpy and matplotlib for Matlab-like stuff
import numpy as np
from matplotlib.pyplot import *   #Lazy syntax...
import os

# Import some handy utility functions
from ArcPoints import arcpoints
from CircCirc import circcirc
from CouplerPoint import coupler

# Read the initial joint locations from a file.
# First check if in right directory...
# If necessary enter something like this:
#os.chdir('./Google Drive/ActiveCourse/Python4BarExamples')
print("Reading from: " + os.getcwd() + "/InitialJointsKlann.txt\n")

# The first 3 rows are for the fixed points.
# The next 4 rows are moving joints, ending with the leg.
pointsdata = np.loadtxt('InitialJointsKlann.txt')
joint12 = pointsdata[0,:]
joint14 = pointsdata[1,:]
joint15 = pointsdata[2,:]
joint23 = pointsdata[3,:]
joint34 = pointsdata[4,:]
joint36 = pointsdata[5,:]
joint56 = pointsdata[6,:]
foot = pointsdata[7,:]

# Set the range of angles that we want the crank
# to rotate through, and specify how many steps. 
thetastart = 0.2
thetaend = -1.9*np.pi  # rotates clockwise in this case
numsteps = 30

# Set up for plotting
#figure()   #If you want to start a new figure
clf()
grid(True)
axes().set_aspect('equal', 'datalim')  #square and limited by data

# Plot fixed points as a triangle in black, initial links in blue
plot((joint12[0],joint14[0],joint15[0],joint12[0]),(joint12[1],joint14[1],joint15[1],joint12[1]),'k')
plot((joint12[0],joint23[0],joint34[0],joint14[0]),(joint12[1],joint23[1],joint34[1],joint14[1]),'b')
plot((joint23[0],joint34[0],joint36[0]),(joint23[1],joint34[1],joint36[1]),'b')
plot((joint15[0],joint56[0],joint36[0],foot[0]),(joint15[1],joint56[1],joint36[1],foot[1]),'b')


#Find lengths of the links. l2 is length of link2 between
# joint12 and joint23, and so forth...
# numpy.linalg.norm() computes the norm of a matrix;
# in this case it's just the square root of the sum of squares :-)
#See 
#http://bdml.stanford.edu/uploads/Main/ME112LinkageLinks/KlannNotation.png
#for joint and link numbering convention used.
d2 = joint23-joint12
l2 = np.linalg.norm(d2)
d3 = joint34-joint23
l3 = np.linalg.norm(d3)
d36 = joint36-joint34
c3 = np.linalg.norm(d36)
d4 = joint34-joint14
l4 = np.linalg.norm(d4)
d5 = joint56-joint15
l5 = np.linalg.norm(d5)
d35 = joint36-joint56
l6 = np.linalg.norm(d35)
d6 = foot-joint36
c5 = np.linalg.norm(d6)

# Find the angles gamma3 and gamma5 of the "bent links"
# Use arctan2(deltay,deltax) for unambiguous sign convention.
gamma1 = np.arctan2(d3[1],d3[0])
gamma2 = np.arctan2(d36[1],d36[0])
gamma3 = gamma2-gamma1

gamma1 = np.arctan2(d35[1],d35[0])
gamma2 = np.arctan2(d6[1],d6[0])
gamma5 = gamma2-gamma1


# Use circcirc() to solve for the initial location
# of joint34. One of the two solutions returned
# will match the actual initial position.
# This determines which "assembly" we have.
intersections = circcirc(joint23,l3,joint14,l4)
if(np.allclose(intersections[0],joint34)):
    assembly = 0
elif(np.allclose(intersections[1],joint34)):
    assembly = 1
else:
    print('Hmmm, neither solution matches the input point...')


# Use Arcpoints() to get all the positions of joint23,
# as input crank goes from thetastart to thetaend
joints23 = arcpoints(joint12,l2,thetastart,thetaend,numsteps)
# Plot them, with dot at start and square at end:
plot(joints23[:,0],joints23[:,1],color = 'g',linewidth=0.5)
plot(joints23[0,0],joints23[0,1],'o')
plot(joints23[numsteps-1,0],joints23[numsteps-1,1],'s')


# Compute all the locations of joint34 and joint36, treating
# joint36 as a coupler point
joints34 = np.zeros((numsteps,2),float)
joints36 = np.zeros((numsteps,2),float)
for i in range(0,numsteps):   
    intersections = circcirc(joints23[i,:],l3,joint14,l4)
    joints34[i,:] = intersections[assembly,:]
    joints36[i,:] = coupler(joints23[i,:],joints34[i,:],c3,gamma3)


# If desired, plot joint34 locations, with dot at start and square at end:
#plot(joints34[:,0],joints34[:,1],color = 'g',linewidth=0.5)
#plot(joints34[0,0],joints34[0,1],'o')
#plot(joints34[numsteps-1,0],joints34[numsteps-1,1],'s')   
    
# Plot joint36 locations, with dot at start and square at end:
plot(joints36[:,0],joints36[:,1],color = 'r',linewidth=0.5)
plot(joints36[0,0],joints36[0,1],'o')
plot(joints36[numsteps-1,0],joints36[numsteps-1,1],'s')   


#### Repeat the process above for the output of the mechanism
###  starting with locations of joint36 which we now know.

# Use circcirc() to solve for the initial location
# of joint56. One of the two solutions returned
# will match the actual initial position.
# This determines which "assembly" we have.
intersections = circcirc(joint36,l6,joint15,l5)
if(np.allclose(intersections[0],joint56)):
    assembly = 0
elif(np.allclose(intersections[1],joint56)):
    assembly = 1
else:
    print('Hmmm, neither solution matches the input point...')
    
    
# Compute all the locations of joint56 and foot
joints56 = np.zeros((numsteps,2),float)
foots = np.zeros((numsteps,2),float)
for i in range(0,numsteps):   
    intersections = circcirc(joints36[i,:],l6,joint15,l5)
    joints56[i,:] = intersections[assembly,:]
    foots[i,:] = coupler(joints56[i,:],joints36[i,:],c5,gamma5)


# Plot joint56 locations, with dot at start and square at end:
plot(joints56[:,0],joints56[:,1],color = 'g',linewidth=0.5)
plot(joints56[0,0],joints56[0,1],'o')
plot(joints56[numsteps-1,0],joints56[numsteps-1,1],'s')   
    
# Plot foot locations, with dot at start and square at end:
plot(foots[:,0],foots[:,1],'.')
plot(foots[0,0],foots[0,1],'o')
plot(foots[numsteps-1,0],foots[numsteps-1,1],'s')


# Save plot in PDF file
show()
savefig('KlannPlot.pdf')

# Open file for writing joint and coupler points data
# in format that Excel, Matlab, Numpy, etc. can read.
# If we are not sure where we are writing:
#print("Data written: " + os.getcwd() + "/KlannPlotPoints.txt\n")   
Table = np.column_stack((joints23,joints34,joints36,joints56,foots))
f_handle = file('KlannPlotPoints.txt', 'w')
headerstring = "joint23(x,y), joint34(x,y),  joint36(x,y),     joint56(x,y),   foot(x,y)"
np.savetxt(f_handle,Table,header=headerstring,delimiter='\t',newline='\n',fmt='%4.2f')
f_handle.close()

