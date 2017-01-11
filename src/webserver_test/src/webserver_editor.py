#!/usr/bin/env python
import rospy,re
from navigation_api.msg import navigation_msg
from std_msgs.msg import String
from geometry_msgs.msg import Quaternion
import urllib2

lat=" "
long=" "
query_list = []


def string_parse(gps_str):
    global lat
    global lng
    lat=re.findall('(.*?)%',gps_str)
    lng=re.findall('%(.*?)@',gps_str)
    current_location_tuple = (float(lat[0]),float(lng[0]))
    return current_location_tuple

def target_callback(data):
    global query_list
    parsed = string_parse(data.variable)
    query_list.extend(["targetlat",parsed[0],"targetlong",parsed[1]])
    send_query(query_list)

def coord_callback(data):
    global query_list
    parsed=string_parse(data.data)
    query_list.extend(["currentlat",parsed[0],"currentlong",parsed[1]])
    send_query(query_list)

def status_callback(data):
    global query_list
    status = str(data.w)
    query_list.extend(["status",status])
    send_query(query_list)


def send_query(qlist):
    if len(qlist) is 10:
        extlist = [" ", " ", " ", " ", " "]
        rospy.loginfo("Element 1 :" + str(qlist[0]) + "Element 2 :" + str(qlist[1]) + "Element 3 :" + str(qlist[2]) + "Element 4 :" + str(qlist[3]) + "Element 5 :" + str(qlist[4]) + " | ")
        for i in range 0,(len(qlist) - 1) :
            if qlist[i] is "currentlat":
                extlist[0] = qlist[i+1]
            elif qlist[i] is "currentlong":
                extlist[1] = qlist[i+1]
            elif qlist[i] is "status":
                extlist[2] = qlist[i+1]
            elif qlist[i] is "targetlat":
                extlist[3] = qlist[i+1]
            elif qlist[i] is "targetlong":
                extlist[4] = qlist[i+1]
        if len(extlist) is 5:
            query = "http://shubhagrawal.in/doda.php?user_cur_lat=" + str(extlist[0]) + "&user_cur_long=" + str(extlist[1])+ "&gesture=" + str(extlist[2]) + "&user_tar_lat=" + str(extlist[3]) + "&user_tar_long=" + str(extlist[4])
            response = urllib2.urlopen(query)
            del qlist[:]
            del extlist[:]
        else:
            rospy.loginfo("parsing error")
    else:
        rospy.loginfo("Collecting data ........")



def initializer():
    rospy.init_node('webedit')
    rospy.Subscriber("gpsLocation", String, coord_callback)
    rospy.Subscriber('stickAngles', Quaternion, status_callback)
    rospy.Subscriber("navigation_api_data",navigation_msg,target_callback)
    rospy.spin()

if __name__ == '__main__':

    initializer()
