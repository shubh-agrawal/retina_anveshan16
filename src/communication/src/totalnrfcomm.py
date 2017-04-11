#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Point32
from nrf24 import Nrf24
import random 

nrf = Nrf24(cePin=2,csnPin=3,channel=10,payload=8)
nrf.config()
nrf.setRADDR("host2")
raw_data = [-1,-1,-1,-1,-1,-1,-1,-1]

bx = -1
by = -1
bz = -1
bw = -1
sx = -1
sy = -1
sz = -1
sw = -1
rx = -0.0
ry = -0.0
rz = -0.0
step_length = -0.0

bpub = rospy.Publisher('boxAngles', Quaternion, queue_size=100)
spub = rospy.Publisher('stickData', Quaternion, queue_size=100)
rpub = rospy.Publisher('rightlegAngles', Point32, queue_size=100)
temp_length=0.0
prev_step_length=0.0
if __name__ == '__main__':
    try:
        rospy.init_node('nrfall')
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            if nrf.dataReady():
                raw_data = nrf.getData()
            value = raw_data[0] + 256*raw_data[1] + 256*256*raw_data[2] + 256*256*256*raw_data[3]            
            decoded = (value%100000)/100.0
            index = value/100000
            if index is 11:
		rx=decoded
            elif index is 12:
                ry = decoded-180
            elif index is 13:
                rz = decoded - 180
            elif index is 14:
		step_length=decoded
            elif index is 21:
                bx = decoded  
	    elif index is 22:
                by = decoded-180
            elif index is 23:
		bz = decoded-180
            elif index is 24:
                bw= decoded
            elif index is 31:
                sx = decoded
            elif index is 34:
                sw = decoded  
	    
	    if abs(step_length-prev_step_length) >= 0.1:
            	prev_step_length = step_length
            else:
                step_length = 0

            rospy.loginfo(" stick x : " + str(sx) + " | stick y :" + str(sy) + " | stick z " + str(sz) + " | stick w : " + str(sw))
            rospy.loginfo(" box x : " + str(rx) + " | box y :" + str(ry) + " | box z " + str(rz) + " | box w : " + str(bw))
            rospy.loginfo(" right x : " + str(rx) + " | right y : " + str(ry) + " | right z : " + str(rz) + " | step_length : " + str(step_length))
            sdata = Quaternion(sx,sy,sz,sw)
	    bdata = Quaternion(rx,ry,rz,bw)
            rdata  = Point32(rx,ry,step_length)
            bpub.publish(bdata)
	    rpub.publish(rdata)
            spub.publish(sdata)
            rate.sleep()

    except rospy.ROSInterruptException:
        pass



