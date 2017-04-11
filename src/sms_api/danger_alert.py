#!/usr/bin/python
# It will send a message without GPS if no message from gpsLocation topic is received. If any GPS message is sought, it will try to send it with the text message attached 

import rospy
from std_msgs.msg import String
from time import sleep
import urllib2
import cookielib
from getpass import getpass
import sys, re

username = "9933988118"
passwd = "blackhole"
comm_message = "(Danger Alert) at GPS ->"
message = "(Danger Alert) at GPS ->"
current_gps_location=(-1,-1)
number = "9933988118"

message = "+".join(message.split(' '))

def send_sms():
  url = 'http://site24.way2sms.com/Login1.action?'
  data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')]
  try:
      usock = opener.open(url, data)
  except IOError:
      print "Error while logging in."
      sys.exit(1)
 
  jession_id = str(cj).split('~')[1].split(' ')[0]
  send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
  send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+message+'&msgLen=136'
  opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
 
  try:
      sms_sent_page = opener.open(send_sms_url,send_sms_data)
  except IOError:
      print "Error while sending message"
      sys.exit(1)

  print "SMS has been sent."


def string_parse(gps_str):
	lat=re.findall('(.*?)%',gps_str)	
	lng=re.findall('%(.*?)@',gps_str)
	current_location_tuple = (float(lat[0]),float(lng[0]))
	return current_location_tuple

def gpscallback(gps_data):
	global current_gps_location
	global comm_message
	global message
	current_gps_location=string_parse(gps_data.data)
	message = comm_message + str(current_gps_location)
	message = "+".join(message.split(' '))

rospy.init_node('danger_alert', anonymous=True)
rospy.Subscriber("gpsLocation", String, gpscallback)

sleep(2)
#send_sms()

