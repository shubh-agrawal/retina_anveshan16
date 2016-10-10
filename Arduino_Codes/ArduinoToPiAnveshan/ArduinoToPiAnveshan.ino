#include <avr/io.h>
#include <avr/wdt.h>
#include <avr/interrupt.h>  /* for sei() */
#include <util/delay.h>     /* for _delay_ms() */
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <SPI.h>
#include <Mirf.h>
#include <nRF24L01.h>
#include <MirfHardwareSpiDriver.h>

#define F_CPU 16000000

#define BUZZER_PIN   13
#define BUZZER_LIMIT 30
#define ECHO1        3
#define TRIG1        6

#define TICKS_PER_MS           15984 // instructions per millisecond (depends on MCU clock, 12MHz current)
#define MAX_RESP_TIME_MS       40    // timeout - max time to wait for low voltage drop (higher value increases measuring distance at the price of slower sampling)
#define DELAY_BETWEEN_TESTS_US 200   // echo cancelling time between sampling

#define THRESHOLD       10
#define SONAR_DELAY     20
#define DIST_LIMIT      500
#define NUM_OF_READINGS 5

#define MAXTIME     5   // multiply with precision to get actual time 
#define BUZZER_TIME 100 // microseconds // 0.1 sec

volatile long          result1                    = 0;
volatile unsigned char up1                        = 0;
volatile unsigned char running1                   = 0;
volatile uint32_t      timerCounter1              = 0;
volatile uint32_t      max_ticks                  = (uint32_t)MAX_RESP_TIME_MS * TICKS_PER_MS;
volatile int           distCnt[2]                 = {0};
volatile int           distData1[NUM_OF_READINGS] = {0};
volatile int           distData2[NUM_OF_READINGS] = {0};
volatile int           distSum1                   = 0;
volatile int           distSum2                   = 0;
volatile int           dist[2]                    = {1000, 1000};
volatile int           dataCnt                    = 0;
volatile unsigned long t1                         = 0;
volatile unsigned long t_keep                     = 0;
volatile int           activenessCount            = 0;

bool          buzzerFlag          = LOW;
bool          buzzInitFlag        = LOW;
int           interruptPin        = 2;
int           signalValue         = 0;
int           gesture_flag        = 0;
int           count               = 0;
int           gestureNumber       = 0;
float         targetHeading       = -1;
int           rawHeading          = -1;
unsigned long time_gap_threshold  = 2000;
unsigned long previousTime        = 0;
unsigned long currentTime         = 0;

Adafruit_BNO055 bno = Adafruit_BNO055();

void setPin(int pin)
{
  digitalWrite(pin, HIGH);
}

void resetPin(int pin)
{
  digitalWrite(pin, LOW);
}

/***********************************************************************************/
/* SONAR INTERRUPT HANDLERS */

// Timer overflow interrupt for Sonar
ISR(TIMER3_OVF_vect)
{
    if (up1)
    {       // voltage rise was detected previously
    timerCounter1++; // count the number of overflows
    // Don't wait too long for the sonar end response, stop if time for measuring the distance exceeded limits
    uint32_t ticks1 = timerCounter1 * 65535 + TCNT3;
        if (ticks1 > max_ticks)
      {
          // timeout
          up1 = 0;          // stop counting timer values
          running1 = 0; // ultrasound scan done
          result1 = 1000; // show that measurement failed with a timeout (could return max distance here if needed)
      }
    }
}

// Echo Interrupt Handler for Left Sonar
ISR(INT5_vect)
{
     if (running1)
     { //accept interrupts only when sonar was started
     if (up1 == 0)
     { // voltage rise, start time measurement
        up1 = 1;
        timerCounter1 = 0;
        TCNT3 = 0; // reset timer counter
     }
     else
     {        // voltage drop, stop time measurement
        up1 = 0;
        // convert from time to distance(millimeters): d = [ time_s * 340m/s ] / 2 = time_us/58
        result1 = (timerCounter1 * 65535 + TCNT3)/940;
        running1 = 0;
     }
     }
}

void enableSonar(int num)
{
     if(num == 1)
     {
     // turn on interrupts for INT4, connect Echo to INT4
     EIMSK |= (1 << INT5);       // Turns on INT4
     EICRB |= (1 << ISC50);      // enable interrupt on any(rising/droping) edge
     }
}

void sonar(int num)
{
     if(num == 1)
     {
     resetPin(TRIG1);
     delayMicroseconds(1);
     setPin(TRIG1);
     delayMicroseconds(10);
     resetPin(TRIG1);
     delayMicroseconds(1);
     running1 = 1;
     }
}

void handleObstacle(int cnt)
{
    while(cnt--)
    {
      if(running1 == 0)
      {
        distData1[distCnt[0]] = result1;
        distCnt[0]++;

        if(distCnt[0] == NUM_OF_READINGS)
          distCnt[0] = 0;
        int n;
        distSum1 = 0;
        for(n=0; n<NUM_OF_READINGS; n++)
        {
          distSum1 += distData1[n];
        }

        dist[0] = distSum1/NUM_OF_READINGS;

        if(dist[0] > DIST_LIMIT && dist[0] != 1000)
          dist[0] = DIST_LIMIT;

        sonar(1); // launch measurement
        delay(SONAR_DELAY);
      }
    }
}

void tim3_Init()
{
  TCCR3A = 0;
  TCCR3B = 0;

  TCCR3B |= (1<<CS30); // select internal clock with no prescaling
  TCNT3 = 0; // reset counter to zero
  TIMSK3 = 1<<TOIE3; // enable timer interrupt
}

void initializeSonar()
{
  int m;

  for(m=0; m<NUM_OF_READINGS; m++)
  {
     distData1[m] = 1000;
  }
}

/***********************************************************************************/
/* SONAR INTERRUPT HANDLERS */


/***********************************************************************************/
/* CAP TOUCH */

void execute_gesture(int count)
{
  Serial.print("Gesture number:  "); Serial.println(count);
}

void enableTouch(int num)
{
  if (num == 1)
  {
    // turn on interrupts for INT4, connect Echo to INT4
    EIMSK |= (1 << INT4);               // Turns on INT4
    EICRB |= (1 << ISC40)|(1 << ISC41); // enable interrupt on rising edge
  }
}

ISR(INT4_vect)
{
  if (activenessCount == 0)
  {
    t1 = millis();
    activenessCount++;
    gesture_flag = 1;
  }

  if (activenessCount != 0)
  {
    t_keep = millis();
    if ( (t_keep - t1) < time_gap_threshold)
    {
      activenessCount++;
      t1 = t_keep;
    }
    //      else
    //      {
    //        execute_gesture(activenessCount-2);
    //        activenessCount=0;
    //
    //      }
  }
  Serial.println(activenessCount);
}

void timeCondition()
{
  t_keep = millis();

  if ( ((t_keep - t1) > time_gap_threshold) && gesture_flag == 1)
  {
    gestureNumber = 1;
    activenessCount = 0;
    gesture_flag = 0;

  }
  else
  {
    gestureNumber = 0;
  }

}

/***********************************************************************************/
/* CAP TOUCH */


/***********************************************************************************/
/* BNO */

void BNOsendinit()
{
  /* Initialise the sensor */
  if (!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while (1);
  }

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

void BNOinit()
{
  /* Initialise the sensor */
  if (!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while (1);
  }

  Mirf.cePin = 7;
  Mirf.csnPin = 8;
  Mirf.spi = &MirfHardwareSpi;
  Mirf.init();
  byte payload[8];
  Mirf.payload = sizeof(payload);
  Mirf.channel = 10;
  Mirf.config();
//  Mirf.setTADDR((byte *)"host2");
  bno.setExtCrystalUse(true);

  Serial.println("Calibration status values: 0=uncalibrated, 3=fully calibrated");
}

void BNOnrfloop()
{
  Serial.println("timmieeh");
  long sender[] = {0, 0, 0};
  sender[0] = 34 * 100000 + (gestureNumber) * 100;
  long temp0 = sender[0];
  Mirf.setRADDR((byte *)"host2");
  byte data[Mirf.payload];
  
  /*
   * If a packet has been recived.
   *
   * isSending also restores listening mode when it 
   * transitions from true to false.
   */
   
  if(!Mirf.isSending() && Mirf.dataReady()){
    Serial.println("Got Heading");
    
    /*
     * Get load the packet into the buffer.
     */
     
    Mirf.getData(data);

    rawHeading = (int)(data);
    /*
     * Set the send address.
     */
     
     
    Mirf.setTADDR((byte *)"host2");
    
    /*
     * Send the data back to the client.
     */
     
    Mirf.send((byte *)&temp0);
    
    /*
     * Wait untill sending has finished
     *
     * NB: isSending returns the chip to receving after returning true.
     */
      
    Serial.println("Gesture sent.");
  }

}

/***********************************************************************************/
/* BNO */




/***********************************************************************************/
/* BUZZER */
void buzzerCondition()
{
  if ( dist[0] < BUZZER_LIMIT )
  {
    buzzInitFlag = HIGH;
  }
  else
    buzzInitFlag = LOW;

  currentTime = millis();
  if (currentTime - previousTime > BUZZER_TIME)
  {
  previousTime = currentTime;
  timerIsr();
  }
}

void startBuzzer()
{
  digitalWrite(BUZZER_PIN, HIGH);
}

void stopBuzzer()
{
  digitalWrite(BUZZER_PIN, LOW);
}

void timerIsr()
{
  if ( buzzInitFlag == HIGH )
  {
     
    if ( buzzerFlag == HIGH && count > MAXTIME )
    {
      Serial.print("  SONAR-1 :"); Serial.print(dist[0]); Serial.print(" cm ");
      Serial.println(" buzzer on ");
      startBuzzer();
      buzzerFlag = LOW;
      count = 0;
    }
    else if ( buzzerFlag == LOW  && count > MAXTIME )
    {
      Serial.print("  SONAR-1 :"); Serial.print(dist[0]); Serial.print(" cm ");
      Serial.println(" buzzer off ");
      stopBuzzer();
      buzzerFlag = HIGH;
      count = 0;
    }
    else
    {
      count += 1;
    }

  }
  else if ( buzzInitFlag == LOW )
  {
    stopBuzzer();
    count = 0;
  }
}

/***********************************************************************************/
/* BUZZER */

void pinInit()
{
  pinMode(ECHO1,        INPUT);
  pinMode(TRIG1,        OUTPUT);
  pinMode(BUZZER_PIN,   OUTPUT);
  pinMode(interruptPin, INPUT);
}




void Init()
{
  Serial.begin(9600);
  Serial.println("Orientation Sensor Raw Data Test"); Serial.println("");
  pinInit();
  noInterrupts();
  tim3_Init();
  interrupts(); // enable all(global) interrupts

  enableSonar(1);
  enableTouch(1);
  initializeSonar();
    
  BNOinit();
  previousTime = millis();
  currentTime  = previousTime;

 
  
}

void _print()
{
   Serial.print("  SONAR-1 :"); Serial.print(dist[0]); Serial.println(" cm ");
//   Serial.println(digitalRead(interruptPin));
}

void setup()
{
  Init();
} 
 
void loop()
{ 
  handleObstacle(1);  // SONAR
  timeCondition();    // Captouch
  
//  _print();           // print SONAR
  BNOnrfloop();
  buzzerCondition();
}

