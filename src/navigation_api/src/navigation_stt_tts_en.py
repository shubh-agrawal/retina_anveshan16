#!/usr/bin/env python

# Installed espeak TTS that is meant excuslively for python 
# For installing : sudo apt-get install espeak python-espeak
# Needs only two line of code to make it work
# from espeak import espeak
# espeak.synth("String to be TTS converted")
# for chnging property of voice refer to http://espeak.sourceforge.net/voices.html


import rospy
from std_msgs.msg import String
from navigation_api.msg import navigation_msg

import re
import urllib
import urllib2
import xml.etree.ElementTree as ET
import math

import serial,time
ser=serial.Serial('/dev/ttyUSB0',baudrate=9600,timeout=None)

from espeak import espeak

api_key="AIzaSyB68uuzp_wq_Fjs-bVW8NMXUklRNIxGiks"
website_comm="https://maps.googleapis.com/maps/api/directions/xml?"

user_set_origin=""
user_set_destination=""
mode=""             # This is user set mode
primary_data_dict={}
confirmed_data=""   # This data is user confirmed that can be used by other functions#

current_gps_location=(-1,-1)

def stt_serial_input(str_output):
	"A custom function for stt newline character #. Taken advantage of reading one byte"
	print str_output
	input_str=''
	inchar=''

	while inchar!='#':
		inchar=ser.read(1)
		input_str=input_str+inchar

	input_str=input_str.replace('#','')
	input_str=input_str.replace('*','')

	print "Speech Recognised : ",input_str
	return input_str

def ask_for_user_data():
	"function asks for user data and would return a list of it"
	global user_set_origin
	global user_set_destination
	global mode

	user_set_origin=""
	user_set_destination=""
	mode=""

	user_defined_data_dict={}

	while len(user_set_origin)<=1:
		espeak.synth("Enter the origin, or beginning point. ")
		user_set_origin=stt_serial_input("Enter the origin or beginning point:")
		if len(user_set_origin)<=1:
			print "This field cannot be left blank"
			espeak.synth("This field cannot be left blank, ")
		else:
			user_defined_data_dict['USER_SET_ORIGIN']=user_set_origin
			break

	while len(user_set_destination)<=1:	
		espeak.synth("Enter the destination or the end point. ")
		user_set_destination=stt_serial_input("Enter the destination or the end point:")	
		if len(user_set_destination)<=1:
			print "This field cannot be left blank"
			espeak.synth("This field cannot be left blank, ")
		else:
			user_defined_data_dict['USER_SET_DESTINATION']=user_set_destination
			break

	#For generalized more of transports only. Now default is walking.
	'''while 1:	
		espeak.synth("Enter the mode of transport, Available options are driving, bicycling, walking. ")
		mode=stt_serial_input("Enter the mode of transport. Available options driving, bicycling, walking:")
		if len(mode)<=1:
			mode="driving"
			print "mode of transports defaults to driving"
			espeak.synth("mode of transports defaults to driving. ")
			user_defined_data_dict['USER_SET_MODE']=mode
			break
		elif mode=='driving' or mode=='bicycling' or mode=='walking':
			print "Succesfully fetched mode:",mode
			espeak.synth("Succesfully fetched mode, "+mode)
			user_defined_data_dict['USER_SET_MODE']=mode
			break
		else:
			print "Something went wrong. Enter data once again"
			espeak.synth("Something went wrong. Enter data once again")
			continue
	'''
	user_defined_data_dict['USER_SET_MODE']='walking'
	return user_defined_data_dict


def call_google_api(user_dict):
	"This function would simply give raw_data as output that can be used by various function dependiing upon user input"
	data=""	
	origin_api=user_dict['USER_SET_ORIGIN']
	destination_api=user_dict['USER_SET_DESTINATION']
	mode_api=user_dict['USER_SET_MODE']

	url=website_comm+urllib.urlencode({'origin':origin_api,'destination':destination_api,'mode':mode_api,'region':'in','key':api_key})
	handle=urllib2.urlopen(url)

	for line in handle:
		line=line.strip()
		data=data+line

	return data


def get_primary_data(raw_data):
	"Function must give origin,destination and their co-ordinates as understood by api ( used for confirmation of data)"
	"Also it would give total distance and time required to reach destination"
	global confirmed_data
	tree=ET.fromstring(raw_data)

	primary_data_dict['start_address_api_set']=tree.find('.//leg/start_address').text
	primary_data_dict['end_address_api_set']=tree.find('.//leg/end_address').text
	primary_data_dict['start_gps_api_set']=(float(tree.find('.//leg/start_location/lat').text),float(tree.find('.//leg/start_location/lng').text))
	primary_data_dict['end_gps_api_set']=(float(tree.find('.//leg/end_location/lat').text),float(tree.find('.//leg/end_location/lng').text))
	primary_data_dict['total_distance']=long(tree.find('.//leg/distance/value').text)
	primary_data_dict['total_duration']=tree.find('.//leg/duration/text').text

	print "Please confirm the following details and proceed"
	#espeak.synth("Please confirm the following details and proceed")

	print "Start address :",primary_data_dict['start_address_api_set']
	#espeak.synth("Start address is ")
	#time.sleep(2)
	#espeak.synth(primary_data_dict['start_address_api_set'])

	print "End address :",primary_data_dict['end_address_api_set']
	#espeak.synth("End address is ")
	#time.sleep(2)
	#espeak.synth(primary_data_dict['end_address_api_set'])
	
	print "Total time of travel is ",primary_data_dict['total_duration']
	
	print "Total distance to destination :",primary_data_dict['total_distance']

	time.sleep(1)
	espeak.synth(" Confirm for the data with Y or N.")
	
	confirm_tag=stt_serial_input("Confirm for the above printed data with Y (if yes) or N (if no).")
	if confirm_tag=='Y' or confirm_tag=='y' or confirm_tag=='' or confirm_tag=='yes':
		confirmed_data=raw_data
		return primary_data_dict
	
	else:
		get_primary_data(call_google_api(ask_for_user_data()))


def bearing_calculator(A,B): # A=(lat,lng) , B=(lat,lng) two orderes tuple
	"gives bearing angle when looking from A towards B"
	
	X=(math.cos(B[0]))*(math.sin(B[1]-A[1]))
	Y=(math.cos(A[0]))*(math.sin(B[0]))-(math.sin(A[0]))*(math.cos(B[0]))*(math.cos(B[1]-A[1]))
	
	beta=(math.atan2(-X,Y)*180/math.pi)
	
	if beta>=0:
		return beta
	else:
		return beta+360

def get_bearing_set(gps_data_list):#link for calculation :http://www.igismap.com/formula-to-find-bearing-or-heading-angle-between-two-points-latitude-longitude/
	"This function would take in raw data and will give list of bearing angles that must be followed to reach target waypoint(steps)"
	#lat_lng_lst=[]
	bearing_data_lst=[]
	
	for index,element in enumerate(gps_data_list):
		if element==gps_data_list[0]:
			bearing_data_lst.append(bearing_calculator(primary_data_dict['start_gps_api_set'],element))
		else:
			bearing_data_lst.append(bearing_calculator(gps_data_list[index-1],element))

	print bearing_data_lst
	return bearing_data_lst

def get_steps_navigation(raw_data):     #must be given confirmed_data variable only
	"This function would give steps and waythrough points and will output a list of lat & long : Exclusively for Anveshan project"
	lat_lng_lst=[]                       #contains target waypoints. No start point
	navigation_dict={}           		# Contains lists required for navigation like (lat,lng), bearing, instructions 
	tree=ET.fromstring(raw_data)
	#lat_long_tree_lst=tree.findall('.//step')

	lat_lst=tree.findall('.//step/end_location/lat')
	lng_lst=tree.findall('.//step/end_location/lng')
		
	for x in range(0,len(lat_lst)):
		lat_lng_lst.append((float(lat_lst[x].text),float(lng_lst[x].text)))

	print lat_lng_lst
	
	navigation_dict['target_lat_lng_list']=lat_lng_lst
	navigation_dict['target_bearing_angle_list']=get_bearing_set(lat_lng_lst)
	
	return navigation_dict

def string_parse(gps_str):
	lat=re.findall('(.*?)%',gps_str)	
	lng=re.findall('%(.*?)@',gps_str)
	current_location_tuple = (float(lat[0]),float(lng[0]))
	return current_location_tuple

def gpscallback(gps_data):
	global current_gps_location
	current_gps_location=string_parse(gps_data.data)  
	rospy.loginfo("Current GPS Location: %s",current_gps_location)
	publisher()
	#print current_gps_location

def listener():
	rospy.init_node('navigation_api_stt', anonymous=True)
	rospy.Subscriber("gpsLocation", String, gpscallback)
	rospy.spin()

#get_primary_data(call_google_api(ask_for_user_data()))
#get_steps_navigation(confirmed_data)

def publisher():
	nav_msg = navigation_msg()
	nav_msg.target_heading =  navigation_dict['target_bearing_angle_list'][0]
	nav_msg.start_point  = primary_data_dict['start_address_api_set']
	nav_msg.destination = primary_data_dict['end_address_api_set']
	pub.publish(nav_msg)
	 
pub=rospy.Publisher('navigation_api_data', navigation_msg, queue_size=100)
rospy.init_node('navigation_api_stt', anonymous = True)

if __name__ == '__main__':
	get_primary_data(call_google_api(ask_for_user_data()))
	navigation_dict = get_steps_navigation(confirmed_data)
	listener()
	
