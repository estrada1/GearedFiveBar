# -*- coding: utf-8 -*-
"""
Created Sept. 19 2015
@author: markcutkosky
Example of solving for a Jansen-like linkage using circcirc() and 
other utilities. The approach is similar to CircCirc4Bar.py, but 
longer, so you might like to review that example first.
This Jansen-lite example is from a 2011 report by Amanda Ghassaei
at Pomona College, who wanted to design a Jansen-like linkage
but with fewer links and joints:
http://www.robotee.com/LR/51018_THEO-JANSEN-Details.pdf
This linkage also has more symmetry than the Jansen linkage
and re-uses some link lengths, which simplifies the solution some.
The original Jansen linkage would be solved in the same way, 
but with a couple more uses of circcirc() for additional joints.
"""

# Use numpy and matplotlib for Matlab-like stuff
import numpy as np
from matplotlib.pyplot import *   #Lazy syntax...
import os

#Maybe combine these into a single file LinksUtilities.py ?
# Import some handy utility functions
from ArcPoints import arcpoints
from CircCirc import circcirc
from CouplerPoint import coupler


# Set the range of angles that we want the crank
# to rotate through, and specify how many steps. 
thetastart = 1.4
thetaend = 1.4+1.95*np.pi  # rotates clockwise in this case
numsteps = 50

# Set up for plotting stuff
#figure()   #if you want it to start a new figure
clf()
grid(True)
axes().set_aspect('equal', 'datalim')  #square and limited by data

#Link lengths from Fig. 5.4.3 of the report
linka = 26.
linke = 56.
linkd = 77.
linkf = 75.
link1 = 53.           #Ground link
alpha1 = 0.085        #Angle given for ground link
gammad = -(np.pi-2.97)   #Angle given for rigid triangle

#First fixed joint (for crank) is at (0, 0)
fp1 = np.array([0.0,0.0])
#Get coordinates of the second fixed joint
fp2 = -link1*np.array([np.cos(alpha1),np.sin(alpha1)])
plot((fp2[0],0.0),(fp2[1],0.0),color='k')     #plot the ground link


#Compute crank arc from thetastart to thetaend
crankpoints = arcpoints(fp1,linka,thetastart,thetaend,numsteps)
plot(crankpoints[:,0],crankpoints[:,1],color = 'g',linewidth=0.5)


#For each crank position, compute joint3 and joint4,
#i.e., the upper and lower intersections of links 'e' and 'd'
#In this linkage they are mirror images of each other.
#joints4 = 1st solution (LHS if traveling to fp2)
#joints3 = 2nd solution (RHS if traveling to fp2)
joints3 = np.zeros((numsteps,2),float)
joints4 = np.zeros((numsteps,2),float)
for i in range(0,numsteps):   
    intersects = circcirc(crankpoints[i,:],linke,fp2,linkd)
    joints4[i,:] = intersects[0,:]
    joints3[i,:] = intersects[1,:]

plot(joints3[:,0],joints3[:,1],color = 'g',linewidth=0.5)
plot(joints4[:,0],joints4[:,1],color = 'g',linewidth=0.5)


#Now we can get joints5. The rigid triangles with linkd
#create a bent link for which the coupler is joint5.
#In fact, because fp2 is fixed, it traces an arc like
#joint3, but phase-shifted by (pi-2.97)
joints5 = np.zeros((numsteps,2),float)
for i in range(0,numsteps): 
    joints5[i,:] = coupler(joints3[i,:],fp2,linkd,gammad)
    
plot(joints5[:,0],joints5[:,1],color = 'g',linewidth=0.5)


#Finally we get the foot location, again using circcirc().
#Going from joint5 to joint4, we want the intersection on RHS
foots = np.zeros((numsteps,2),float)
for i in range(0,numsteps):   
    intersections = circcirc(joints5[i,:],linkf,joints4[i,:],linkf)
    foots[i,:] = intersections[1,:]

# Plot foot locations, with big dot at start
# Note that it's quite fast at top of step.
plot(foots[:,0],foots[:,1],'.')
plot(foots[0,0],foots[0,1],'o')


#Now, for comparison, we can trace the initial configuration
#as drawn in fig 5.4.3 in the report.
#This requires setting thetastart to about 80deg = 1.4 radians
plot((0.0,crankpoints[0,0]),(0.0,crankpoints[0,1]),color='b')
plot((crankpoints[0,0],joints3[0,0]),(crankpoints[0,1],joints3[0,1]),color='b')
plot((joints3[0,0],fp2[0]),(joints3[0,1],fp2[1]),color='b')
plot((fp2[0],joints5[0,0]),(fp2[1],joints5[0,1]),color='b')
plot((joints5[0,0],foots[0,0]),(joints5[0,1],foots[0,1]),color='b')
plot((foots[0,0],joints4[0,0]),(foots[0,1],joints4[0,1]),color='b')
plot((joints4[0,0],fp2[0]),(joints4[0,1],fp2[1]),color='b')



# Save plot in PDF
show()
savefig('Jansen-lite.pdf')

# Open file for writing joint and coupler points data
# in format that Excel, Matlab, Numpy, etc. can read.
# If we are not sure where we are writing:
#print("Data written: " + os.getcwd() + "/Jansen-lite-points.txt\n")   
Table = np.column_stack((joints3,joints4,joints5,foots))
f_handle = file('Jansen-lite-points.txt', 'w')
headerstring = "joint3(x,y),  joint4(x,y),     joint5(x,y),    foot(x,y)"
np.savetxt(f_handle,Table,header=headerstring,delimiter='\t',newline='\n',fmt='%4.2f')
f_handle.close()

