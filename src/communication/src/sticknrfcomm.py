#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Quaternion
from nrf24 import Nrf24
 
# stick == 3 

nrf = Nrf24(cePin=2,csnPin=3,channel=10,payload=8)
nrf.config()
nrf.setRADDR("host2")
x = -1
y = -1
z = -1
w = -1
raw_data = [-1,-1,-1,-1,-1,-1,-1,-1]
pub = rospy.Publisher('stickAngles', Quaternion, queue_size=100)

if __name__ == '__main__':

    try:
        rospy.init_node('nrfbnostick')
        rate = rospy.Rate(100)
        while not rospy.is_shutdown():
            if nrf.dataReady():
                raw_data = nrf.getData()
            value = raw_data[0] + 256*raw_data[1] + 256*256*raw_data[2] + 256*256*256*raw_data[3]            
            decoded = (value%100000)/100.0
            index = value/100000    
            if   index is 31:
                x = decoded
            elif index is 32:
                y = decoded - 180
            elif index is 33:
                z = decoded - 180 
            elif index is 34:
                w = decoded  

            rospy.loginfo(" stick x : " + str(x) + " | stick y : " + str(y) + " | stick z : " + str(z) + " | touch : " + str(w))
            data = Quaternion(x,y,z,w)
            pub.publish(data)
            rate.sleep()

    except rospy.ROSInterruptException:
        pass

