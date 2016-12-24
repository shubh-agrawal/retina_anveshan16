#!/usr/bin/env python
import rospy

import numpy as np
import matplotlib.pyplot as plt
from geometry_msgs.msg import Point32
from geometry_msgs.msg import Quaternion

# intial parameters

sz = (1,) # size of array
truth_latitude=23
truth_longitude=87

Q = 1e-5 # process variance

# allocate space for arrays
xhatX=np.zeros(sz)      # a posteri estimate of x
PX=np.zeros(sz)         # a posteri error estimate
xhatminusX= np.zeros(sz)# a priori estimate of x
PminusX=np.zeros(sz)    # a priori error estimate
KX=np.zeros(sz)         # gain or blending factor

xhatY=np.zeros(sz)      # a posteri estimate of x
PY=np.zeros(sz)         # a posteri error estimate
xhatminusY=np.zeros(sz) # a priori estimate of x
PminusY=np.zeros(sz)    # a priori error estimate
KY=np.zeros(sz)         # gain or blending factor

PprevX=0
XhatprevX=0
PprevY=0
XhatprevY=0
heading=0

R = 0.1**2 # estimate of measurement variance, change to see effect

# intial guesses 
xhat[0] = 0.0
P[0] = 1.0


def headingCallback(heading_data):
    heading=heading_data.x
    
def leftLegCallback(leftLegData):

    # time update X
    xhatminusX[0] = xhatprevX
    PminusX[0] = PprevX+Q

    # measurement update X
    KX[0] = PminusX[0]/( PminusX[0]+R )
    xhat[k] = xhatminusX[0]+KX[0]*(leftLegData.z*cos(heading))
    PX[0] = (1-KX[0])*PminusX[0]
    XhatprevX=xhatX[0]
    PprevX=PminusX[0]

    # time update Y
    xhatminusY[0] = xhatprevY
    PminusY[0] = PprevY+Q

    # measurement update Y
    KY[0] = PminusY[0]/( PminusY[0]+R )
    xhatY[k] = xhatminusY[0]+KY[0]*(leftLegData.z*sin(heading))
    PY[k] = (1-KY[0])*PminusY[0]
    XhatprevY=xhatY[0]
    PprevY=PminusY[0]

def gpsCallback(gps_data):
	sep1 = gps_data.find('%')
	sep2 = gps_data.find('@')
	xhatminusX[0] = gps_data[0:sep1]
	xhatminusY[0] = gps_data[sep1+1:sep2]

def loop():
	rospy.Subscriber("gpsLocation", String, gpsCallback)
	rospy.Subscriber("rightlegAngles", Point32, leftLegCallback)
	rospy.Subscriber("boxAngles", Quaternion, headingCallback)

if __name__ == '__main__':
    try:
        loop()
    except rospy.ROSInterruptException:
        pass
