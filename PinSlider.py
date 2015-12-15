#Simple Python program for pin-slider mechanism
#Feb 17, 2014 -MRC

# Use numpy and matplotlib for Matlab-like stuff
from numpy import *
from matplotlib.pyplot import *
import os

#See Week 7 2014 class notes for definitions.
#R2 is the length in the input (crank) link
#(px,py) are the coordinates of the pin in the slot

R2 = 2.0
px, py = 5.0, 2.0


#Add provisions for a coupler location
#(Modify this to suit your design.)
gammac = pi*(-10.0/180) #radians (note the '.0' to force floating point)
R5 = 9.0

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

#Draw the fixed ground link
X1 = 0
Y1 = 0
X4 = px
Y4 = 0
plot([X4,X1],[Y4,Y1], color = 'b')
plot([X4,X4],[py,Y4],color = 'b')

grid(True)
axes().set_aspect('equal', 'datalim')  #square and limited by data


################################
#Main loop for each crank angle
#numpy counts from zero, not one
for i in range(0,numsteps):

    cosq2 = cos(theta2s[i])
    sinq2 = sin(theta2s[i])
    
    loopy = py - R2*sinq2
    loopx = px - R2*cosq2
    q3 = arctan2(loopy,loopx)

    
    #Compute locations of joints 2,3
    X2 = R2 * cosq2
    Y2 = R2 * sinq2
#   X3 = X2+R3*cosq3
#   Y3 = Y2+R3*sinq3
    
    #Now plot the linkage... 
    #plot every 2nd step to make less messy 
    if i%2==0:
        plot([X1,X2],[Y1,Y2],color = 'g') 
        plot([X2,px],[Y2,py],color = 'r')
  #     plot([X3,X4],[Y3,Y4],color = 'b')
    
    #Coupler location 
    xca1[i] = R2*cos(theta2s[i])+R5*cos(q3+gammac)
    yca1[i] = R2*sin(theta2s[i])+R5*sin(q3+gammac)
    
    #Plot Coupler
    plot(xca1[i],yca1[i],'*')
    if i%2==0:
        plot([px,xca1[i]],[py,yca1[i]],color='r')

    
#end for i loop


#Open file for writing the coupler points as X Y values with
#tab delimiter for easy import into Matlab or Excel
print("Data written: " + os.getcwd() + "/PinSliderPoints.txt\n")   #Make sure we are in the right directory...
Table = column_stack((xca1,yca1))
f_handle = file('PinSliderPoints.txt', 'w')
savetxt(f_handle,Table,delimiter='\t',newline='\n',fmt='%4.2f')
f_handle.close()

show()
savefig('PinSliderPoints.pdf')




