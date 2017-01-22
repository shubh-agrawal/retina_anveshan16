#!/usr/bin/env python
import rospy
import utm
import numpy as np
import matplotlib.pyplot as plt
from geometry_msgs.msg import Point32
from geometry_msgs.msg import Quaternion
from std_msgs.msg import String
import math
# intial parameters

sz = (1,) # size of array
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

utm_zone = 30
utm_zone_name = 'fa'
updated_easting = 20
updated_northing = 20
prevStep=0.0

PprevX=0
XhatprevX=0
PprevY=0
XhatprevY=0
heading=0

R = 0.1**2 # estimate of measurement variance, change to see effect

# intial guesses 
xhatX[0] = 0.0
xhatY[0] = 0.0
PX[0] = 1.0
PY[0] = 1.0

def headingCallback(heading_data):
    global heading
    heading=heading_data.x

def rightLegCallback(rightLegData):

    global XhatprevX, XhatprevY, PprevX, PprevY, Q
    global xhatminusX, xhatminusY, PminusX, PminusY, PX, PY, xhatX, xhatY, KX, KY
    global heading, utm_coord, utm_zone, utm_zone_name, prevStep
    if rightLegData.z != prevStep:
	    # time update X
	    xhatminusX[0] = XhatprevX
	    PminusX[0] = PprevX+Q

	    # measurement update X
	    KX[0] = PminusX[0]/( PminusX[0]+R)
	    xhatX[0] = xhatminusX[0]+KX[0]*(rightLegData.z*0.01*math.cos(heading))
	    PX[0] = (1-KX[0])*PminusX[0]
	    XhatprevX=xhatX[0]
	    PprevX=PminusX[0]

	    # time update Y
	    xhatminusY[0] = XhatprevY
	    PminusY[0] = PprevY+Q

	    # measurement update Y
	    KY[0] = PminusY[0]/( PminusY[0]+R )
	    xhatY[0] = xhatminusY[0]+KY[0]*(rightLegData.z*0.01*math.sin(heading))
	    PY[0] = (1-KY[0])*PminusY[0]
	    XhatprevY=xhatY[0]
	    PprevY=PminusY[0]
	    #print xhatX[0]
	    #print xhatY[0]

	    (filtered_latitude, filtered_longitude) = utm.to_latlon(xhatY[0], xhatX[0], utm_zone, utm_zone_name)

	    print "xhat | "+ str(filtered_latitude)
	    print "yhat | "+ str(filtered_longitude)

    prevStep=rightLegData.z
      

def gpsCallback(gps_msg):
	global XhatprevX, XhatprevY
	global utm_coord, utm_zone, utm_zone_name
        gps_data=gps_msg.data
	sep1 = gps_data.find('%')
	sep2 = gps_data.find('@')
	lati_local = gps_data[0:sep1]
	longi_local = gps_data[sep1+1:sep2]
	utm_coord = utm.from_latlon(float(lati_local), float(longi_local))
	utm_zone = utm_coord[2]
	utm_zone_name = utm_coord[3]
	XhatprevY  = utm_coord[0] #easting
	XhatprevX = utm_coord[1]  #northing
	

def loop():
	rospy.Subscriber("gpsLocation", String, gpsCallback)
	rospy.Subscriber("rightlegAngles", Point32, rightLegCallback)
	rospy.Subscriber("boxAngles", Quaternion, headingCallback)
	#print "x: " + str(xhatX[0]) + "y: " + str(xhatY[0])
	rospy.init_node('localizer', anonymous=True)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
           	
		rate.sleep()

if __name__ == '__main__':
    try:
        loop()
    except rospy.ROSInterruptException:
        pass
