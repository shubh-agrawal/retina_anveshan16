from nrf24 import Nrf24
import time
nrf = Nrf24(cePin=2,csnPin=3,channel=10,payload=1)
nrf.config()
nrf.setTADDR("clie1")
while 1>0:
	if not nrf.isSending():
		nrf.send(map(ord,"a"))
		time.sleep(0.001)
		nrf.send(map(ord,"b"))
		time.sleep(0.001)
