#!/usr/bin/env python
import rospy
import subprocess
import espeak
from navigation_api.msg import navigation_msg
from geometry_msgs.msg import Quaternion
touchCode=0
prevtouchCode=0
currMenuNumber=10

def touchCallback(data):
#    print "data rec"    
    touchCode= data.w
    global currMenuNumber
    global prevtouchCode

    if touchCode == 1 and prevtouchCode != 1:
        currMenuNumber=currMenuNumber-1

    if touchCode == 2 and prevtouchCode != 2:
        currMenuNumber=currMenuNumber+1

    prevtouchCode = touchCode
    rospy.loginfo("touchcode  " + str(touchCode) + " | curr menu no : " +  str(currMenuNumber))
    touchCode = touchCode - 1
    if touchCode > 0:
        executecommand(touchCode)
    

def executecommand(touch):
    if touch == 2:
       # startlevelone()
        print "Level ONE"
        espeak.synth("LEVEL ONE")
    elif touch == 3:
       # startleveltwo()
        print "Level TWO"
        espeak.synth("LEVEL TWO")
    elif touch == 4:
       # startlevelthree()
        print "Level THREE"
        espeak.synth("LEVEL THREE")
    elif touch == 1:
        print "Level ONE"
        espeak.synth("LEVEL ONE")
#        rospy.loginfo("Retina Squared : Level One")
    
def endprocess(prolist,index):
    p = subprocess.Popen('ps aux | grep python', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        pid = line.split(' ')
        str1 = prolist[int(index)]
        if str1 in pid:
            print pid[6]
            cmd = "kill -9 " + str(pid[6])
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def listener():
    
    rospy.init_node('ui', anonymous=True)
    rospy.Subscriber("stickData", Quaternion, touchCallback)
    startlevelzero()
    rospy.spin()
    
   

def startlevelzero():
    p1 = subprocess.Popen('rosrun nrfcomm totalnrfcomm.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p2 = subprocess.Popen('rosrun gps gps_publisher.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p3 = subprocess.Popen('rosrun localization kalmanLocalization.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p4 = subprocess.Popen('rosrun webdoda webserver.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    

def startlevelone():
    p1 = subprocess.Popen('rosrun navigation_api navigation_stt_tts_en.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p2 = subprocess.Popen('rosrun navigation_api headingcorrection.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def startleveltwo():
    p1 = subprocess.Popen('python /home/pi/doda_ws/src/sms_api/danger_alert.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def endlevelone():
    p1 = subprocess.Popen('rosnode kill /navigation_api_data', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def startlevelthree():
    p1 = subprocess.Popen('python /home/pi/doda_ws/src/sms_api/send_custom_sms.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
 



if __name__ == '__main__':
   
    listener()
   




