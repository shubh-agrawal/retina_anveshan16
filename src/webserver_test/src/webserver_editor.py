#!/usr/bin/env python
import rospy,re

from std_msgs.msg import String
lat=" "
long=" "
def string_parse(gps_str):
    global lat
    global lng
    lat=re.findall('(.*?)%',gps_str)
    lng=re.findall('%(.*?)@',gps_str)
    current_location_tuple = (float(lat[0]),float(lng[0]))
    return current_location_tuple

def callback(data):
    parsed=string_parse(data.data)
    print("Logging Data")
    f=open('/var/www/index.html')
    lines = f.readlines()
    f.close()
    r=open('/var/www/index.html','w')
    r.writelines([item for item in lines[:-1]])
    r.close()
    w=open('/var/www/index.html','a')
    w.write(str(parsed)+'<br>')
    w.write('\n</body></html>')
    w.close()

def initializer():
    rospy.init_node('webedit')
    rospy.Subscriber("gpsLocation", String, callback)
    rospy.spin()

if __name__ == '__main__':
    f=open('/var/www/index.html','w')
    f.write('<html><body><h1>Anveshan Data logging test</h1>\n')
    f.write('</body></html>')
    f.close()
    initializer()
