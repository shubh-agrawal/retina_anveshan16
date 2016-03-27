#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def callback(data):
    print("badger badger badger")
    f=open('/var/www/index.html')
    lines=f.readlines()
    f.close()
    w=open('/var/www/index.html','w')
    w.writelines([item for item in lines[:-1]])
    w.close()
    w=open('/var/www/index.html','a')
    w.write(data.data)
    w.write('</body></html>')
    w.close()

def listener():
    rospy.init_node('webedit')
    rospy.Subscriber("gpsLocation", String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
