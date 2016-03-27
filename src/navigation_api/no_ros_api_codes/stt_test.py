# Drawback of using funtion readline() is that it always waits for newline charachter
# Documentation is available at http://pyserial.readthedocs.io/en/latest/shortintro.html

import serial,time
ser=serial.Serial('/dev/ttyUSB0',baudrate=9600,timeout=None)
s=''
data=""

while s!='#':
	s=ser.read(1)
	data=data+s


print data
ser.close()


# This works in accordance with AMR voice app since it eol is #. readline() can recognize only \n or \r or \r\n even after changing eol
# hence it was necessary to use read() that reads number of bytes stated within it and uses it as timeout. timeout none specifies
# it will always wait for atleast one byte forever. read(10) means it will wait for 10 bytes and timeout will be executed other the 
# the time specified in timeout parameter will be waiting time

