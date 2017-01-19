#!/usr/bin/env python
import rospy
import RPi.GPIO as GPIO
from navigation_api.msg import navigation_msg
from geometry_msgs.msg import Quaternion
from nrf24 import Nrf24

buzzerPin = 19
targetheading = -1
currentheading = -1


def targetcallback(data):
    global targetheading
    rospy.loginfo( "Target Heading : " + str(data.target_heading) + " | " )
    targetheading = data.target_heading

def currentcallback(data):
    rospy.loginfo( "Current Heading : " + str(data.x) + " | "  + "Target Heading" + str(targetheading))
    currentheading = int(data.x)
    correctHeading(currentheading,targetheading)

def listener():
    rospy.init_node('headingcorrection')
    rospy.Subscriber("navigation_api_data", navigation_msg, targetcallback)

def subs():
    rospy.Subscriber('boxAngles', Quaternion, currentcallback)
    rospy.spin()    

def initBuzzer():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzerPin, GPIO.OUT)


def correctHeading(currentheading,targetheading):
    if abs(currentheading - targetheading < 50) and targetheading > 0:
        GPIO.output(buzzerPin, GPIO.HIGH)
	rospy.loginfo("buzzer on")
    else :
	rospy.loginfo("buzzer off")
        GPIO.output(buzzerPin, GPIO.LOW)



if __name__ == '__main__':
    initBuzzer()
    listener()
    try:
        rate = rospy.Rate(100)
      	subs()
        rate.sleep()

    except rospy.ROSInterruptException:
        GPIO.cleanup()
        pass
