#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

import serial
import re

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=None)
pub = rospy.Publisher('gpsLocation', String, queue_size=100)

        
def serialCallback_pub():
    global port
    input_str = ''
    inchar = ''
    
    try:
        while port.inWaiting() == 0: 
            pass
    except:
        pass
    
    try:
        input_str = port.readline()
    
    except serial.serialutil.SerialException:
        pass                  
    lati = re.findall('GPGGA,.*?,([0.0-9.0]+),', input_str)
    longi = re.findall('GPGGA,.*?N,([0.0-9.0]+),E', input_str)

    if len(lati) != 0 or len(longi) != 0:
        latitude = int(float(lati[0])/100) + (float(lati[0]) - (int(float(lati[0])/100.00))*100)/60.0
	longitude = int(float(longi[0])/100) + (float(longi[0]) - (int(float(longi[0])/100.00))*100)/60.0
 
        latitude_s = format(latitude, '.8f')
        longitude_s = format(longitude, '.8f')
        coord = latitude_s + '%' + longitude_s + '@'
        rospy.loginfo("Latitude : " + latitude_s + "Longtitude : " + longitude_s + " |" )
        pub.publish(coord)

if __name__ == '__main__':
    
    try:
        rospy.init_node('gps')
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            serialCallback_pub()
            rate.sleep()    
    except rospy.ROSInterruptException:
        GPIO.cleanup()
        pass
