#!/usr/bin/env python
import rospy

import numpy as np
import matplotlib.pyplot as plt
from geometry_msgs.msg import Point32


# intial parameters

sz = (1,) # size of array
truth_latitude=23
truth_longitude=87

Q = 1e-5 # process variance

# allocate space for arrays
xhat=np.zeros(sz)      # a posteri estimate of x
P=np.zeros(sz)         # a posteri error estimate
xhatminus=np.zeros(sz) # a priori estimate of x
Pminus=np.zeros(sz)    # a priori error estimate
K=np.zeros(sz)         # gain or blending factor
PhatprevX=0
XhatprevX=0
PhatprevY=0
XhatprevY=0

R = 0.1**2 # estimate of measurement variance, change to see effect

# intial guesses
xhat[0] = 0.0
P[0] = 1.0


def angleCallback(angle_data):
	# time update
	xhatminus[0] = xhatprevX
    Pminus[0] = PminusprevX+Q

    # measurement update
    K[0] = Pminus[0]/( Pminus[0]+R )
    xhat[k] = xhatminus[0]+K[0]*(angle_data.x-xhatminus[0])
    P[k] = (1-K[0])*Pminus[0]
    xhatprev=xhat[0]
    Pminusprev=Pminus[0]

    # time update
	xhatminus[0] = xhatprevY
    Pminus[0] = PminusprevY+Q

    # measurement update
    K[0] = Pminus[0]/( Pminus[0]+R )
    xhat[k] = xhatminus[0]+K[0]*(angle_data.x-xhatminus[0])
    P[k] = (1-K[0])*Pminus[0]
    xhatprev=xhat[0]
    Pminusprev=Pminus[0]

def gpsCallback(gps_data):
	sep1 = gps_data.find('%')
	sep2 = gps_data.find('@')
	truth_latitude	= gps_data[0:sep1]
	truth_longitude = gps_data[sep1+1:sep2]

def loop():
	rospy.Subscriber("gpsLocation", String, gpsCallback)
	rospy.Subscriber("leftlegAngles", Point32, angleCallback)

if __name__ == '__main__':
    try:
        loop()
    except rospy.ROSInterruptException:
        pass