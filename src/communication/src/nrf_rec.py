#!/usr/bin/env python
import rospy
from std_msgs.msg import String	
#from geometry_msgs.msg import Twist
from nrf24 import Nrf24


nrf = Nrf24(cePin=2,csnPin=3,channel=10,payload=8)
nrf.config()
nrf.setRADDR("host2")

pub = rospy.Publisher('raw_nrf_data', String, queue_size=100)

if __name__ == '__main__':

    try:
        rospy.init_node('nrf_rec')
        rate = rospy.Rate(100)
        while not rospy.is_shutdown():
            if nrf.dataReady():
                raw_data = nrf.getData()
            value = raw_data[0] + 256*raw_data[1] + 256*256*raw_data[2] + 256*256*256*raw_data[3]            
            decoded = (value%100000)/100.0
            index = value/100000    

            print index
#            rospy.loginfo("raw data received:"+str(raw_data[0]))
            pub.publish(str(raw_data[0]))
            rate.sleep()

    except rospy.ROSInterruptException:
        pass

