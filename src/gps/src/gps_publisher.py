#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
#from geometry_msgs.msg import Twist

import serial
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) 

port          = serial.Serial("/dev/ttyUSB0", baudrate=9600)
RX            = 15
extFlag       = 0
rawstring     = ""
flag          = 0	
coord         = "ee"
desiredstring = ""
lati          = " "
longi         = " "
pub = rospy.Publisher('gpsLocation', String, queue_size=100)

def pubdata():
    global lati
    global longi
    global pub
    coord = lati + '%' + longi + '@'

    rospy.loginfo("Latitude : " + lati + "Longtitude : " + longi + " |" )
    pub.publish(coord)

def getGPSdata():
    global extFlag
    global desiredstring
    global lati
    global longi
    if extFlag is 1:
        extFlag       = 0
        dictgps       = desiredstring.split(',')
        lati          = (dictgps[2])
        longi         = (dictgps[4])
        desiredstring = ""
        pubdata()
        

def serialCallback():
    global rawstring
    global flag
    global extFlag
    global desiredstring
    global RX
    global port
    rcv = port.read(1)
    if rcv is not "$":
    	rawstring += rcv
    if (rawstring == 'GPGGA') or (flag is 1):
       flag           = 1
       desiredstring += rcv
       if rcv is "$":
           extFlag = 1
           flag    = 0
           getGPSdata()
           rawstring = ""
           desiredstring=""
    if rcv is "$":
	rawstring   = ""
 
if __name__ == '__main__':
    
    try:
        rospy.init_node('gps')
        rate = rospy.Rate(100)
        while not rospy.is_shutdown():
            serialCallback()
	    #getGPSdata()
            #pubdata()
            #pub.publish(coord)
            rate.sleep()    
    except rospy.ROSInterruptException:
        GPIO.cleanup()
        pass
