#!/usr/bin/env python
import rospy
from navigation_api.msg import navigation_msg
from geometry_msgs.msg import Quaternion
import math
import urllib
import urllib2
prev_coord = []


def targetcallback(data):
    #rospy.loginfo( "Target Heading : " + str(data.target_heading) + " | " )
    global prev_coord
    start_coord = [" " , " "]
    destination_coord = [" " , " "]
    current_coord = parse_coord(data.current_address)
    start_coord   = parse_coord(data.start_crdnts)
    destination_coord = parse_coord(data.target_crdnts)
    #start_coord = [" " , " "]
    #destination_coord = [" " ," "]
    #lati%longi@
    prev_coord = current_coord
    package = start_coord + current_coord + destination_coord
    distance = (prev_coord,current_coord) # in km
    if (distance > 0.01):
    	sendreq(package)
    package = []



def parse_coord(gps_str):
    lati  = gps_str.split("%")
    longi = lati[1].split("@")
    coord = [lati[0],longi[0]]
    return coord

def gps_distance(coord_0,coord_1):
    d2r = math.pi/180.0
    dlong = (coord_1[1] - coord_0[1]) * d2r
    dlat = (coord_1[0] - coord_0[0]) * d2r
    a = pow(math.sin(dlat/2.0), 2) + math.cos(coord_0[0]*d2r) * math.cos(coord_1[0]*d2r) * pow(math.sin(dlong/2.0), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6367 * c
    return distance

def sendreq(package):
    url = 'http://shubhagrawal.in/dodanew.php?'
    rq  = ""
    if (package[0] == " " or package[1] == " " or package[4] == " " or package[5] == " "):
        rq = url + 'user_cur_lat=' + package[2] + '&user_cur_long=' + package[3] + '&gesture=3&user_tar_lat=55.674983629&user_tar_long=23.423429'
    else:
        rq = url + 'user_cur_lat=' + package[2] + '&user_cur_long=' + package[3] + '&gesture=3' + '&user_tar_lat=' + package[4] + '&user_tar_long=' + package[5]
    req = urllib2.Request(rq)
    response = urllib2.urlopen(req)
    rq = ""


def listener():
    rospy.init_node('weblog')
    rospy.Subscriber("navigation_api_data", navigation_msg, targetcallback)


if __name__ == '__main__':
    listener()
    print "webdoda"
    try:
        rate = rospy.Rate(100)
        rate.sleep()

    except rospy.ROSInterruptException:
        pass
