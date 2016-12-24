#!/usr/bin/python
# It will send a message without GPS if no message from gpsLocation topic is received. If any GPS message is sought, it will try to send it with the text message attached 

import rospy
from std_msgs.msg import String
from time import sleep
import urllib2
import cookielib
from getpass import getpass
import sys, re

import serial,time
ser=serial.Serial('/dev/ttyUSB0',baudrate=9600,timeout=None)
from espeak import espeak

username = "9933988118"
passwd = "blackhole"
current_gps_location=(-1,-1)
number = "9933988118"

def stt_serial_input(str_output):
	"A custom function for stt newline character #. Taken advantage of reading one byte"
	print str_output
	espeak.synth(str_output)
	input_str=''
	inchar=''

	while inchar!='#':
		inchar=ser.read(1)
		input_str=input_str+inchar

	input_str=input_str.replace('#','')
	input_str=input_str.replace('*','')

	print "Speech Recognised : ",input_str
	return input_str

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

message = stt_serial_input("Say, your,  message")
message = "+".join(message.split(' '))
send_sms()

