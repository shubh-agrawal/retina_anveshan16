#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Quaternion
 
touchCode=0
currMenuNumber=10

def caller(menuNo):
	if menuNo==0:
		espeak.speak("One. Start Navigation Doda")
	elif menuNo==1:
		espeak.speak("Two. Stop Navigation Doda")
	elif menuNo==2:
		espeak.speak("Three. Tell me where I am Doda")
	elif menuNo==3:
		espeak.speak("Four. Send SOS Doda")
 	elif menuNo==4:
		espeak.speak("Five. Send custom SMS Doda")

def touchCallback(data):
    touchCode=data.w 
    if touchCode == 1 and in_loop==0:
    	currMenuNumber=currMenuNumber-1
    if touchCode == 2 and in_loop==0:
	currMenuNumber=currMenuNumber+1
    speaker(currMenuNumber)
	
   
	
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("stickAngles", Quaternion, touchCallback)
    rospy.spin()

if __name__ == '__main__':
    listener()
