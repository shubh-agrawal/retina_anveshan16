python-nrf24
============

python-lib for interfacing with nRF24L01 modules
This is a port of the tinkerer.eu lib.

Introduction
------------
The library is to be used with python2.

Requirements
------------
 * For SPI communication py-spidev: https://github.com/doceme/py-spidev.git
 * For GPIO WiringPi2-Python: https://github.com/Gadgetoid/WiringPi2-Python.git

Wiring
------

	   nRF24L01              RaspberryPi
	+-+-+                    (header)      wiringpi-pins
	|8|7|	1: GND      ->   6              -
	+-+-+	2: 3.3V     ->   1              -
	|6|5|	3: CE       ->   13             2
	+-+-+	4: CSN      ->   15             3
	|4|3|	5: SCKL     ->   23            14
	+-+-+	6: MOSI     ->   19            12
	|2|1|	7: MISO     ->   21            13
	+-+-+	8: IRQ      ->   not used      not used

Example
-------
For a sender:

	from nrf24 import Nrf24
	nrf = Nrf24(cePin=2,csnPin=3,channel=10,payload=8)
	nrf.config()
	nrf.setRADDR("host1")
	nrf.setTADDR("host2")
  
	if not nrf.isSending():
		nrf.send(map(ord,"Helloooo"))
		
For a receiver:

	from nrf24 import Nrf24
	nrf = Nrf24(cePin=2,csnPin=3,channel=10,payload=8)
	nrf.config()
	nrf.setRADDR("host2")
	nrf.setTADDR("host1")
  
	while True:
		if nrf.dataReady():
			print nrf.getData()
			break

	
  
Notes on Testing 
--------------------
Note that RX and TX addresses must match
	
Note that communication channels must match:
 * python-nrf24: Set the channel parameter of the constructor
 * arduino-mirf24: Set the channel in the example code 

Note that payload size must match:
 * python-nrf24: Set the payload parameter of the constructor
 * arduino-mirf24: Adjust the payload in the example code

Mirf24 ping_server example adjustments

	byte payload[8];
  	Mirf.payload = sizeof(payload);
  	Mirf.channel = 10;
  
Just an example :)





