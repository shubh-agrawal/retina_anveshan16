#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <SPI.h>
#include <Mirf.h>
#include <nRF24L01.h>
#include <MirfHardwareSpiDriver.h>

Adafruit_BNO055 bno = Adafruit_BNO055();


void setup(void)
{
  Serial.begin(9600);
  Serial.println("Orientation Sensor Raw Data Test"); Serial.println("");

  /* Initialise the sensor */
  if (!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while (1);
  }

  delay(1000);
  Mirf.cePin = 7;
  Mirf.csnPin = 8;
  Mirf.spi = &MirfHardwareSpi;
  Mirf.init();
  byte payload[8];
  Mirf.payload = sizeof(payload);
  Mirf.channel = 10;
  Mirf.config();
  Mirf.setTADDR((byte *)"host2");  
  bno.setExtCrystalUse(true);

  Serial.println("Calibration status values: 0=uncalibrated, 3=fully calibrated");
}


void loop(void)
{
  long sender[]={0,0,0};
  imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);

  /* Display the floating point data */
//  Serial.print("X: ");
//  Serial.print(euler.x());
//  Serial.print(" Y: ");
//  Serial.print(euler.y());
//  Serial.print(" Z: ");
//  Serial.print(euler.z());
//  Serial.print("\t\t");

  /*
  // Quaternion data
  imu::Quaternion quat = bno.getQuat();
  Serial.print("qW: ");
  Serial.print(quat.w(), 4);
  Serial.print(" qX: ");
  Serial.print(quat.y(), 4);
  Serial.print(" qY: ");
  Serial.print(quat.x(), 4);
  Serial.print(" qZ: ");
  Serial.print(quat.z(), 4);
  Serial.print("\t\t");
  */

  /* Display calibration status for each sensor. */
  uint8_t system, gyro, accel, mag = 0;

  sender[0]=11*100000+euler.x()*100.0;
  sender[1]=12*100000+(euler.y()+180)*100.0;
  sender[2]=13*100000+(euler.z()+180)*100.0;
  
  Serial.print("X: ");
  Serial.print(sender[0]);
  Serial.print(" Y: ");
  Serial.print(sender[1]);
  Serial.print(" Z: ");
  Serial.print(sender[2]);
  Serial.print("\t\t");
  
  long temp0 = sender[0];
  long temp1 = sender[1];
  long temp2 = sender[2];
  Mirf.send((byte *)&temp0);
  while (Mirf.isSending()) {}
  delay(5);
  Mirf.send((byte *)&temp1);
  while (Mirf.isSending()) {}
  delay(5);
  Mirf.send((byte *)&temp2);
  while (Mirf.isSending()) {}
  delay(5);
  Serial.println("Finished sending");

}
