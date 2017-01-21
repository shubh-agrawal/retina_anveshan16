#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Point32
from nrf24 import Nrf24
import random 
# right == 1 

nrf = Nrf24(cePin=2,csnPin=3,channel=10,payload=8)
nrf.config()
nrf.setRADDR("host2")
x = -0.0
y = -0.0
z = -0.0
step_length = -0.0
raw_data = [0,-1,-1,-1,-1,-1,-1,-1]
pub = rospy.Publisher('rightlegAngles', Point32, queue_size=100)

if __name__ == '__main__':

    try:
        rospy.init_node('nrfbnoright')
        rate = rospy.Rate(100)
        while not rospy.is_shutdown():
            if nrf.dataReady():
                raw_data = nrf.getData()
            value = raw_data[0] + 256*raw_data[1] + 256*256*raw_data[2] + 256*256*256*raw_data[3]            
            decoded = (value%100000)/100.0
            index = value/100000    
            if index is 11:
                x = decoded
            elif index is 12:
                y = decoded - 180
            elif index is 13:
                z = decoded - 180  
            elif index is 14:
                step_length = decoded
	    #step_length = random.randint(70,80) 
            rospy.loginfo(" right x : " + str(x) + " | right y : " + str(y) + " | step_length : " + str(step_length))
            data = Point32(x,y,step_length)
            pub.publish(data)
            rate.sleep()

    except rospy.ROSInterruptException:
        GPIO.cleanup()
        pass

