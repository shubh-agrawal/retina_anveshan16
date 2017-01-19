#!/usr/bin/env python
import rospy 
from navigation_api.msg import navigation_msg
from nrf24 import Nrf24

nrf = Nrf24(cePin=2,csnPin=3,channel=10,payload=8)
nrf.config()
nrf.setTADDR("host2")
targetheading = -1;


def callback(data):
    rospy.logininfo( "Target Heading : " + str(data.target_heading) )
    targetheading = int(data.target_heading*100)

def listener();
    rospy.init_node('nrfsender')
    rospy.Subscriber("navigation_api_data", navigation_msg, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
    if not nrf.isSending():
        nrf.send(map(ord,targetheading))
