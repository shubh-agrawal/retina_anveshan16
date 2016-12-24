#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <SPI.h>
#include <Mirf.h>
#include <nRF24L01.h>
#include <MirfHardwareSpiDriver.h>
#define POSTHRES 0.3
#define NEGTHRES -0.3
#define LENGTH 80


/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (85)

Adafruit_BNO055 bno = Adafruit_BNO055(55);

long prevFive[5] = {0, 0, 0, 0, 0};
int readings[5] = {0, 0, 0, 0, 0};

long total = 0;
long average=0;
long noOfSteps=0;
float initAngle = 0;

bool posflag = 0;
bool negflag = 1;
long readIndex = 0;

/**************************************************************************/
/*
    Displays some basic information on this sensor from the unified
    sensor API sensor_t type (see Adafruit_Sensor for more information)
*/
/**************************************************************************/
void displaySensorDetails(void)
{
  sensor_t sensor;
  bno.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" xxx");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" xxx");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" xxx");
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}

/**************************************************************************/
/*
    Arduino setup function (automatically called at startup)
*/
/**************************************************************************/
void setup(void)
{
  Serial.begin(115200);
  Serial.println("Orientation Sensor Test"); Serial.println("");

  /* Initialise the sensor */
  if (!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while (1);
  }
  setCal();       // Set Calibration Values - Comment out to read calibration values
  delay(100);

  /* Display some basic information on this sensor */
  displaySensorDetails();
  Mirf.cePin = 9;
  Mirf.csnPin = 10;
  Mirf.spi = &MirfHardwareSpi;
  Mirf.init();
  byte payload[8];
  Mirf.payload = sizeof(payload);
  Mirf.channel = 10;
  Mirf.config();
  Mirf.setTADDR((byte *)"host2");
  bno.setExtCrystalUse(true);
  Serial.println("Calibration status values: 0=uncalibrated, 3=fully calibrated");

  sensors_event_t event;

  for (int i = 0; i < 5; i++)
  {
    bno.getEvent(&event);
    prevFive[i] = event.orientation.y;
  }
  initAngle = event.orientation.y;
}


long prevX = 0;
void loop(void)
{
  //total = total - readings[readIndex];
  long sender[4] = {0, 0, 0, 0};
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);
  //  getCalStat();                  // Uncomment to get calibration values
  //readings[readIndex] = event.orientation.x;
  //total = total + readings[readIndex];
  readIndex++;

  if (readIndex >= 5) {
    readIndex = 0;
  }

  //average = total / 5;

  prevFive[1] = prevFive[0];
  prevFive[2] = prevFive[1];
  prevFive[3] = prevFive[2];
  prevFive[4] = prevFive[3];
  prevFive[0] = event.orientation.y - prevX;

  if (negflag == 1 && posflag == 0 && prevFive[0] >= POSTHRES && prevFive[1] >= POSTHRES && prevFive[2] >= POSTHRES && prevFive[3] >= POSTHRES && prevFive[4] >= POSTHRES)
  {
    //Serial.println("NEGEDGE");
    posflag = 1;
    negflag = 0;
    sender[0] = 11 * 100000 + event.orientation.x * 100.0;
    sender[1] = 12 * 100000 + (event.orientation.y + 180) * 100.0;
    sender[2] = 13 * 100000 + (event.orientation.z + 180) * 100.0;
    sender[3] = 14 * 100000;
    /* Display the floating point data */
    /*Serial.print("X: ");
    Serial.print(average, 4);
    Serial.print("\tY: ");
    Serial.print(event.orientation.y, 4);
    Serial.print("\tZ: ");
    Serial.print(event.orientation.z, 4);
    Serial.println("");*/

    delay(BNO055_SAMPLERATE_DELAY_MS);
    long temp0 = sender[0];
    long temp1 = sender[1];
    long temp2 = sender[2];
    long temp3 = sender[3];
    Mirf.send((byte *)&temp0);
    while (Mirf.isSending()) {}
    delay(5);
    Mirf.send((byte *)&temp1);
    while (Mirf.isSending()) {}
    delay(5);
    Mirf.send((byte *)&temp2);
    while (Mirf.isSending()) {}
    delay(5);
    Mirf.send((byte *)&temp3);
    while (Mirf.isSending()) {}
    delay(5);
    //Serial.println("Finished sending");

  }

  else if (negflag == 0 && posflag == 1 && prevFive[0] <= NEGTHRES && prevFive[1] <= NEGTHRES && prevFive[2] <= NEGTHRES && prevFive[3] <= NEGTHRES && prevFive[4] <= NEGTHRES)
  {
    noOfSteps++;
    float extremeAngle = event.orientation.y - initAngle; 
    Serial.print("No of steps is \t");
    Serial.println(noOfSteps);
    //Serial.println("POSEDGE");
    posflag = 0;
    negflag = 1;
    sender[0] = 11 * 100000 + event.orientation.x * 100.0;
    sender[1] = 12 * 100000 + (event.orientation.y + 180) * 100.0;
    sender[2] = 13 * 100000 + (event.orientation.z + 180) * 100.0;
    sender[3] = 14 * 100000 + 2*LENGTH * sin(extremeAngle) * 100.0;  //sending in cms as length in cms
    
    Serial.print("step lenght is ");
    Serial.println(abs(2*LENGTH*sin(extremeAngle)));
    delay(BNO055_SAMPLERATE_DELAY_MS);
    long temp0 = sender[0];
    long temp1 = sender[1];
    long temp2 = sender[2];
    long temp3 = sender[3];
    Mirf.send((byte *)&temp0);
    while (Mirf.isSending()) {}
    delay(5);
    Mirf.send((byte *)&temp1);
    while (Mirf.isSending()) {}
    delay(5);
    Mirf.send((byte *)&temp2);
    while (Mirf.isSending()) {}
    delay(5);
    Mirf.send((byte *)&temp3);
    while (Mirf.isSending()) {}
    delay(5);
    //Serial.println("Finished sending");
  }
  else
  {
    sender[0] = 11 * 100000 + event.orientation.x * 100.0;
    sender[1] = 12 * 100000 + (event.orientation.y + 180) * 100.0;
    sender[2] = 13 * 100000 + (event.orientation.z + 180) * 100.0;
    sender[3] = 14 * 100000;
    /* Display the floating point data */
    /*Serial.print("X: ");
    Serial.print(average, 4);
    Serial.print("\tY: ");
    Serial.print(event.orientation.y, 4);
    Serial.print("\tZ: ");
    Serial.print(event.orientation.z, 4);
    Serial.println("");*/

    delay(BNO055_SAMPLERATE_DELAY_MS);
    long temp0 = sender[0];
    long temp1 = sender[1];
    long temp2 = sender[2];
    long temp3 = sender[3];
    Mirf.send((byte *)&temp0);
    while (Mirf.isSending()) {}
    delay(5);
    Mirf.send((byte *)&temp1);
    while (Mirf.isSending()) {}
    delay(5);
    Mirf.send((byte *)&temp2);
    while (Mirf.isSending()) {}
    delay(5);
    Mirf.send((byte *)&temp3);
    while (Mirf.isSending()) {}
    delay(5);
    //Serial.println("Finished sending");
  }

  prevX = event.orientation.y;


}
void setCal() {
  // DAVES MOD - Writes calibration data to sensor//
  byte calData;
  bno.setMode( bno.OPERATION_MODE_CONFIG );    // Put into CONFIG_Mode
  delay(25);

  calData = bno.setCalvalARL(232);

  calData = bno.setCalvalARM(3);

  calData = bno.setCalvalMRL(87);

  calData = bno.setCalvalMRM(3);

  calData = bno.setCalvalAOXL(231);

  calData = bno.setCalvalAOXM(255);

  calData = bno.setCalvalAOYL(253);

  calData = bno.setCalvalAOYM(255);

  calData = bno.setCalvalAOZL(5);

  calData = bno.setCalvalAOZM(0);

  calData = bno.setCalvalMOXL(14);

  calData = bno.setCalvalMOXM(1);

  calData = bno.setCalvalMOYL(127);

  calData = bno.setCalvalMOYM(0);

  calData = bno.setCalvalMOZL(173);

  calData = bno.setCalvalMOZM(1);

  calData = bno.setCalvalGOXL(155);

  calData = bno.setCalvalGOXM(255);

  calData = bno.setCalvalGOYL(255);

  calData = bno.setCalvalGOYM(255);

  calData = bno.setCalvalGOZL(254);

  calData = bno.setCalvalGOZM(255);

  bno.setMode( bno.OPERATION_MODE_NDOF );    // Put into NDOF Mode
  delay(25);
}


