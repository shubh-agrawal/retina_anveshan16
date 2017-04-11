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
Qgps = 1e-5 #gps variance

# allocate space for arrays
xhatX=np.zeros(sz)      # a posteri estimate of x
PX=np.zeros(sz)         # a posteri error estimate
xhatminusX= np.zeros(sz)# a priori estimate of x
PminusX=np.zeros(sz)    # a priori error estimate
KX=np.zeros(sz)         # gain or blending factor

xhatY=np.zeros(sz)      # a posteri estimate of y
PY=np.zeros(sz)         # a posteri error estimate
xhatminusY=np.zeros(sz) # a priori estimate of y
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

R = 0.1**2 # imu measurement variance
Rgps = 0.1**6 #gps measurement variance

# intial guesses 
xhatX[0] = 0.0
xhatY[0] = 0.0
PX[0] = 1.0
PY[0] = 1.0

gpspub=rospy.Publisher("kalmanGPS",String, queue_size=100)
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

       	   	        # time update Y
			xhatminusY[0] = XhatprevY
			PminusY[0] = PprevY+Q

			# measurement update X
			KX[0] = PminusX[0]/( PminusX[0]+R)
			xhatX[0] = xhatminusX[0]+KX[0]*(rightLegData.z*0.01*math.cos(heading))
			PX[0] = (1-KX[0])*PminusX[0]
			XhatprevX=xhatX[0]
			PprevX=PminusX[0]

			# measurement update Y
			KY[0] = PminusY[0]/( PminusY[0]+R )
			xhatY[0] = xhatminusY[0]+KY[0]*(rightLegData.z*0.01*math.sin(heading))
			PY[0] = (1-KY[0])*PminusY[0]
			XhatprevY=xhatY[0]
			PprevY=PminusY[0]
			print xhatX[0]
			print xhatY[0]

			(filtered_latitude, filtered_longitude) = utm.to_latlon(xhatY[0], xhatX[0], utm_zone, utm_zone_name)

			print "xhat | "+ str(filtered_latitude)
			print "yhat | "+ str(filtered_longitude)
		        pubstr=str(filtered_latitude)+"%"+str(filtered_longitude)+"@"
			gpspub.publish(pubstr)
		        

		prevStep=rightLegData.z
		  

def gpsCallback(gps_msg):
		global XhatprevX, XhatprevY, PprevX, PprevY, Qgps
		global xhatminusX, xhatminusY, PminusX, PminusY, PX, PY, xhatX, xhatY, KX, KY
		global utm_coord, utm_zone, utm_zone_name

		#measurement update X
		xhatminusX[0] = XhatprevX
		PminusX[0] = PprevX + Qgps
	
		#measurement update Y
		xhatminusY[0] = XhatprevY
		PminusY[0] = PprevY + Qgps

		gps_data=gps_msg.data
		sep1 = gps_data.find('%')
		sep2 = gps_data.find('@')
		lati_local = gps_data[0:sep1]
		longi_local = gps_data[sep1+1:sep2]
		utm_coord = utm.from_latlon(float(lati_local), float(longi_local))
		utm_zone = utm_coord[2]
		utm_zone_name = utm_coord[3]

		# measurement update X
		KX[0] = PminusX[0]/( PminusX[0]+Rgps)
		xhatX[0] = xhatminusX[0]+KX[0]*(utm_coord[1] - xhatminusX[0])
		PX[0] = (1-KX[0])*PminusX[0]
		XhatprevX=xhatX[0]
		PprevX=PminusX[0]
         	
 	        #measurement update Y
		KY[0] = PminusY[0]/( PminusY[0]+Rgps )
		xhatY[0] = xhatminusY[0]+KY[0]*(utm_coord[0] - xhatminusY[0])
		PY[0] = (1-KY[0])*PminusY[0]
		XhatprevY=xhatY[0]
		PprevY=PminusY[0]
                print "gpsvalX | "+ str(xhatX[0])
                print "gpsvalY | "+ str(xhatY[0])

	

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
