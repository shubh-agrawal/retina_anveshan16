#!/usr/bin/env python
import rospy
import subprocess
from espeak import espeak
from navigation_api.msg import navigation_msg
from geometry_msgs.msg import Quaternion
touchCode=0
prevtouchCode=0
currMenuNumber=10
customsmsid = -1

def touchCallback(data):
#    print "data rec"    
    touchCode= data.w
    global currMenuNumber
    global prevtouchCode
    global customsmsid
    if touchCode == 1 and prevtouchCode != 1:
        currMenuNumber=currMenuNumber-1

    if touchCode == 2 and prevtouchCode != 2:
        currMenuNumber=currMenuNumber+1

    
#    rospy.loginfo("touchcode  " + str(touchCode) + " | curr menu no : " +  str(currMenuNumber))
    #touchCode = touchCode - 1
    if touchCode > 0:
        executecommand(touchCode,prevtouchCode)
    prevtouchCode = touchCode

def executecommand(touch,prevtouch):
    if touch == 2 and prevtouch != 2:
        print "Level ONE"
        espeak.synth("LEVEL ONE")
        startlevelone()
    elif touch == 3 and prevtouch != 3:
        print "Level TWO"
        espeak.synth("LEVEL TWO")
        startleveltwo()
    elif touch == 4 and prevtouch != 4:
        print "Level THREE"
        espeak.synth("LEVEL THREE")
        startlevelthree()
    elif touch == 1 and prevtouch != 1:
        print "Level ZERO"
        espeak.synth("LEVEL ZERO")
        stopcustom()
        
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
    
def stopcustom(pid):
    if (pid != -1):
        string = 'kill -9 ' + str(pid)
        p2 = subprocess.Popen(string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def startlevelzero():
    p1 = subprocess.Popen('rosrun nrfcomm totalnrfcomm.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p2 = subprocess.Popen('rosrun gps gps_publisher.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p3 = subprocess.Popen('rosrun localization kalmanLocalization.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p4 = subprocess.Popen('rosrun webdoda webserver.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    

def startlevelone():
    p1 = subprocess.Popen('roslaunch navigation_api navigation.launch', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p1.stdout.readlines():
        print line
    retval = p1.wait()
    #p2 = subprocess.Popen('rosrun navigation_api headingcorrection.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def startleveltwo():
    p1 = subprocess.Popen('python /home/pi/doda_ws/src/sms_api/danger_alert.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p1.stdout.readlines():
        print line
    retval = p1.wait()
#    subprocess.call("python /home/pi/doda_ws/src/sms_api/danger_alert.py", shell=True)

def endlevelone():
    p1 = subprocess.Popen('rosnode kill /navigation_api_data', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def startlevelthree():
    p1 = subprocess.Popen('python /home/pi/doda_ws/src/sms_api/send_custom_sms.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p1.stdout.readlines():
        print line
    retval = p1.wait() 



if __name__ == '__main__':
    espeak.synth(" RETINA SQUARED UI ")
    print " RETINA SQUARED UI"   
    listener()
   




