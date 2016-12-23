#!/usr/bin/env python
import rospy
import RPi.GPIO as GPIO
from navigation_api.msg import navigation_msg
from geometry_msgs.msg import Quaternion
from nrf24 import Nrf24

buzzerPin = 12
global targetheading = -1
global currentheading = -1

def targetcallback(data):
    rospy.logininfo( "Target Heading : " + str(data.target_heading) + " | " )
    targetheading = int(data.target_heading*100)

def currentcallback(data):
    rospy.logininfo( "Current Heading : " + str(data.x) + " | " )
    currentheading = int(data.x)

def listener():
    rospy.init_node('headingcorrection')
    rospy.Subscriber("navigation_api_data", navigation_msg, targetcallback)
    rospy.Subscriber('stickAngles', Quaternion, currentcallback)
    rospy.spin()

def initBuzzer():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buzzerPin, GPIO.OUT)


def correctHeading():
    if abs(currentheading - targetheading < 10):
        GPIO.output(buzzerPin, GPIO.HIGH)
    else:
        GPIO.output(buzzerPin, GPIO.LOW)



if __name__ == '__main__':
    initBuzzer()

    try:
        listener()
        rate = rospy.Rate(100)
        while not rospy.is_shutdown():
            correctHeading()
            rate.sleep()

    except rospy.ROSInterruptException:
        GPIO.cleanup()
        pass
