

from nrf24 import Nrf24
nrf = Nrf24(cePin=2,csnPin=3,channel=10,payload=8)
nrf.config()
nrf.setRADDR("host2")

while True:
    if nrf.dataReady():
        print nrf.getData()
