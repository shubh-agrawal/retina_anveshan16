#include <SPI.h>
#include <Mirf.h>
#include <nRF24L01.h>
#include <MirfHardwareSpiDriver.h>

float t1=239.35,t2=321.34, t3=231.23,t4=22.27;
long sender[]={0,0,0,0};
void setup(){
  Serial.begin(9600);
  /*
   * Setup pins / SPI.
   */
 
  /* To change CE / CSN Pins:
   * 
   * Mirf.csnPin = 9;
   * Mirf.cePin = 7;
   */
  /*
 
  */
  Mirf.cePin = 7;
  Mirf.csnPin = 8;
  Mirf.spi = &MirfHardwareSpi;
  Mirf.init();
  byte payload[8];
  /*
   * Configure reciving address.
   */
 
 
  /*
   * Set the payload length to sizeof(unsigned long) the
   * return type of millis().
   *
   * NB: payload on client and server must be the same.
   */
 
  Mirf.payload = sizeof(payload);
 
  /*
   * Write channel and payload config then power up reciver.
   */
 
  /*
   * To change channel:
   * 
 
   *
   * NB: Make sure channel is legal in your area.
   */
 
  Mirf.channel = 10;
  Mirf.config();
 
  Serial.println("Beginning ... "); 
}


void loop(){
 
  sender[0]=7*100000;
  sender[1]=4*100000+t1*100.0;
  sender[2]=5*100000+t2*100.0;
  sender[3]=6*100000+t3*100.0;
  unsigned long time=700000;
  Mirf.setTADDR((byte *)"host2");

    long temp0=sender[0];
    long temp1=sender[1];
    long temp2=sender[2];
    long temp3=sender[3];
    Mirf.send((byte *)&temp0);
     delay(25);
    Mirf.send((byte *)&temp1);
     delay(25);
    Mirf.send((byte *)&temp2);
     delay(25);
    Mirf.send((byte *)&temp3);
    delay(25);
  
  while(Mirf.isSending()){
  }
  Serial.println("Finished sending");
 
  while(!Mirf.dataReady()){
    //Serial.println("Waiting");
//    if ( ( millis() - time )>1000 ) {
//      Serial.println("Timeout on response from server!");
      return;
//    }
  }
 
}
