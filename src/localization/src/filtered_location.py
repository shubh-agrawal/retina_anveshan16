#!/usr/bin/env python
# license removed for brevity
import rospy
import utm, math
from std_msgs.msg import String
from geometry_msgs.msg import Point32
from geometry_msgs.msg import Quaternion

#Set some home position here
truth_latitude = 22.31901420
truth_longitude = 87.29969989
heading = 0.0
gps_flag = 1  #Mentions if gps data is available or not
step_length = 0.0
prev_step_length = 0.0

def headingCallback(heading_data):
	global heading	
	heading = heading_data.x

def angleCallback(angle_data):
	global step_length, prev_step_length
	step_length = angle_data.z
	
def gpsCallback(gps_data):
	global gps_flag, truth_latitude, truth_longitude
	gps_flag = 1
	sep1 = (gps_data.data).find('%')
	sep2 = (gps_data.data).find('@')
	truth_latitude	= float((gps_data.data)[0:sep1])
	truth_longitude = float((gps_data.data)[sep1+1:sep2])


def loop():
	rospy.Subscriber("gpsLocation", String, gpsCallback)
	rospy.Subscriber("rightlegAngles", Point32, angleCallback)
	rospy.Subscriber("boxAngles", Quaternion, headingCallback)
	

if __name__ == '__main__':
	try:
		global gps_flag, step_length, prev_step_length	
		rospy.init_node('filtered_location')
		pub = rospy.Publisher('filteredGpsLocation', String, queue_size=100)		
		loop()
		rate = rospy.Rate(1)
		utm_crdnts = utm.from_latlon(truth_latitude, truth_longitude)
		utm_zone = utm_crdnts[2]
		utm_zone_name = utm_crdnts[3]
		updated_easting = utm_crdnts[0]
		updated_northing = utm_crdnts[1]

		while not rospy.is_shutdown():

			if gps_flag == 0:
				if step_length != prev_step_length:
					prev_step_length = step_length
				else:
					step_length = 0.0
				updated_easting = updated_easting + 0.01*step_length*math.sin(heading) # 0.01 for convertion to metres
				updated_northing = updated_northing + 0.01*step_length*math.cos(heading)
				(filtered_latitude, filtered_longitude) = utm.to_latlon(updated_easting, updated_northing, utm_zone, utm_zone_name)
				print "Updated GPS: ", (filtered_latitude, filtered_longitude)
				print "step: ", step_length		
				coord = format(filtered_latitude, '.8f') + '%' + format(filtered_longitude, '.8f') + '@'
				pub.publish(coord)

			else:
				utm_crdnts = utm.from_latlon(truth_latitude, truth_longitude)
				utm_zone = utm_crdnts[2]
				utm_zone_name = utm_crdnts[3]
				updated_easting = utm_crdnts[0]
				updated_northing = utm_crdnts[1]				
				coord = format(truth_latitude, '.8f') + '%' + format(truth_longitude, '.8f') + '@'
				print "Normal GPS: ", (truth_latitude, truth_longitude)
				pub.publish(coord)
				gps_flag = 0			
			#pub.publish(coord)	
			rate.sleep()
        except rospy.ROSInterruptException:
	        pass
