# 3Sept2013 Convert to Python from HalfAngleMethod.m
# Alternative 4bar linkage solution from M. Stanisic (kinematician
# at Notre Dame http://www.nd.edu/~stanisic/)
# Use this to check accuracy of your own program 
# if you do a 4-bar rocker-crank.

# This method uses tangent half-angle formulas to simplify catching
# the 2 inversions (see Wikipedia "tangent half angle")
# Assumes link 1 is aligned with X axis.
# See '4bar_assemblies_diagram.pdf'for notation

# Start with equations (9.29) - (9.31) per Stanisic.
# Vector loop is R2 + R3 = R1 + R4, where R1 is horizontal
# from left to right. All angles anticlockwise from horizontal.
# Theta2 is input crank angle.

# Use numpy and matplotlib for Matlab-like stuff
from numpy import *
from matplotlib.pyplot import *
import os

#Define link lengths and inversion
#(Alternatively one could read initial joint xy locations
#from a file and use those to get the link lengths)
R1 = 9.0
R2 = 3.0
R3 = 10.0
R4 = 6.0
inversion = True    # True if inverted solution

#Add provisions for a coupler location
#(Modify this to suit your design.)
gammac = pi*(40.0/180) #radians (note the '.0' to force floating point)
R5 = 7.0

#Define range of angles to plot and step size
theta2start = 0.0
theta2end = 2*pi
numsteps = 24   

#array of input crank angles
theta2s = linspace(theta2start,theta2end,numsteps)
xca1 = zeros(numsteps,float)          #arrays for the coupler outputs
yca1 = zeros(numsteps,float)

#Clear figure
clf()

#The fixed ground link
X1 = 0
Y1 = 0
X4 = R1
Y4 = 0
plot([X4,X1],[Y4,Y1], color = 'k')

grid(True)
axes().set_aspect('equal', 'datalim')  #square and limited by data


################################
#Main loop for each crank angle
#numpy counts from zero, not one
for i in range(0,numsteps):

    cosq2 = cos(theta2s[i])
    sinq2 = sin(theta2s[i])
    
    # Define some substitutions (9.29-9.31)
    A = 2*R4*(R1 - R2*cosq2)
    B = -2*R2*R4*sinq2
    C = R3**2 - R2**2 - R4**2 - R1**2 + 2*R2*R1*cosq2
    
    #Solve for the roots of half angle equation (9.35)    
    #In general
    u41 = (B + sqrt(A**2 + B**2 - C**2))/(A+C)
    q4 = 2*arctan(u41)
    
    #If inversion
    if inversion:
        u42 = (B - sqrt(A**2 + B**2 - C**2))/(A+C)
        q4 = 2*arctan(u42)
    
    #Solve for theta3 (9.37-9.39)
    #range = -PI to +PI
    cosq3 = (-R2*cosq2 + R4*cos(q4) + R1)/R3
    sinq3 = (-R2*sinq2 + R4*sin(q4))/R3
    q3 = arctan2(sinq3,cosq3)  #don't really need it for plotting
    
    #Compute locations of joints 2,3
    X2 = R2 * cosq2
    Y2 = R2 * sinq2
    X3 = X2+R3*cosq3
    Y3 = Y2+R3*sinq3
    
    #Now plot the linkage... 
    #plot every 2nd step to make less messy 
    if i%2==0:
        plot([X1,X2],[Y1,Y2],color = 'g') 
        plot([X2,X3],[Y2,Y3],color = 'r')
        plot([X3,X4],[Y3,Y4],color = 'b')
    
    #Coupler location 
    xca1[i] = R2*cos(theta2s[i])+R5*cos(q3+gammac)
    yca1[i] = R2*sin(theta2s[i])+R5*sin(q3+gammac)
    
    #Plot Coupler
    plot(xca1[i],yca1[i],'*')
#   Makes plot kinda messy, but can uncomment if debugging
#    if i%2==0:
#        plot([X2,xca1[i]],[Y2,yca1[i]],color='m')

    
#end for i loop


#Open file for writing the coupler points as X Y values with
#tab delimiter for easy import into Matlab or Excel
print("Data written: " + os.getcwd() + "/CouplerPoints.txt\n")   #Make sure we are in the right directory...
Table = column_stack((xca1,yca1))
f_handle = file('CouplerPoints.txt', 'w')
savetxt(f_handle,Table,delimiter='\t',newline='\n',fmt='%4.2f')
f_handle.close()

show()
savefig('CouplerPlot.pdf')




