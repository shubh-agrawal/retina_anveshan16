#include <avr/io.h>
#include <avr/wdt.h>
#include <avr/interrupt.h>  /* for sei() */
#include <util/delay.h>     /* for _delay_ms() */
//#include <Wire.h>
//#include <Adafruit_Sensor.h>
//#include <Adafruit_BNO055.h>
//#include <utility/imumaths.h>
#include <SPI.h>
#include <Mirf.h>
#include <nRF24L01.h>
#include <MirfHardwareSpiDriver.h>

#define F_CPU 16000000

// SONAR MACROS
#define BUZZER         8
#define THRESHBUZZ     25
#define ECHO1          3
#define TRIG1          4
#define BUTTON1        A2
#define BUTTON2        A3
#define BUTTON3        A4
#define BUTTON4        A5

#define TICKS_PER_MS           15984 // instructions per millisecond (depends on MCU clock, 12MHz current)
#define MAX_RESP_TIME_MS       40    // timeout - max time to wait for low voltage drop (higher value increases measuring distance at the price of slower sampling)
#define DELAY_BETWEEN_TESTS_US 200   // echo cancelling time between sampling

#define SONAR_DELAY     20
#define DIST_LIMIT      500
#define NUM_OF_READINGS 5
// SONAR MACROS END

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


int           count               = 0;
int           gesture             = 0;
unsigned long previousTime        = 0;
unsigned long currentTime         = 0;

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
ISR(TIMER1_OVF_vect)
{
    if (up1)
    {       // voltage rise was detected previously
    timerCounter1++;
    // count the number of overflows
    // Don't wait too long for the sonar end response, stop if time for measuring the distance exceeded limits
    uint32_t ticks1 = timerCounter1 * 65535 + TCNT1;
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
ISR(INT1_vect)
{
     if (running1)
     { //accept interrupts only when sonar was started
     if (up1 == 0)
     { // voltage rise, start time measurement
        up1 = 1;
        timerCounter1 = 0;
        TCNT1 = 0; // reset timer counter
     }
     else
     {        // voltage drop, stop time measurement
        up1 = 0;
        // convert from time to distance(millimeters): d = [ time_s * 340m/s ] / 2 = time_us/58
        result1 = (timerCounter1 * 65535 + TCNT1)/940;
        running1 = 0;
     }
     }
}

void enableSonar(int num)
{
     if(num == 1)
     {
     // turn on interrupts for INT4, connect Echo to INT4
     EIMSK |= (1 << INT1);       // Turns on INT4
     EICRA |= (1 << ISC10);      // enable interrupt on any(rising/droping) edge
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

void tim1_Init()
{
  TCCR1A = 0;
  TCCR1B = 0;

  TCCR1B |= (1<<CS10); // select internal clock with no prescaling
  TCNT1 = 0; // reset counter to zero
  TIMSK1 = 1<<TOIE1; // enable timer interrupt
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


/***********************************************************************************/
/* NRF */

void nrfloop(int gesture)
{
  
  long sender[] = {0, 0, 0};
  sender[0] = 34 * 100000 + (gesture) * 100  ;
  sender[1]=  31 * 100000 + (dist[0]) * 100.0;
  long temp0 = sender[0];
  long temp1 = sender[1];
  Mirf.cePin = 9;
  Mirf.csnPin = 10;
  Mirf.spi = &MirfHardwareSpi;
  Mirf.init();
  byte payload[8];
  Mirf.payload = sizeof(payload);
  Mirf.channel = 10;
  Mirf.config();
  Mirf.setTADDR((byte *)"host2");

  /*
   * If a packet has been recived.
   *
   * isSending also restores listening mode when it
   * transitions from true to false.
   */
  /*
     * Send the data back to the client.
     */
  Mirf.send((byte *)&temp0);
  
  while (Mirf.isSending()) {}
  delay(5);
//  Serial.println("timmieeh");
  Mirf.send((byte *)&temp1);
  while (Mirf.isSending()) {}
  delay(5);
    /*
     * Wait untill sending has finished
     *
     * NB: isSending returns the chip to receving after returning true.
     */

    Serial.println("  Gesture and Obstacle distance sent.");
  }



/***********************************************************************************/
/* BNO */

/***********************************************************************************/
/* TOUCH */

int detectGestureold()
{
int ges=9;
//int button[] = {0,0,0,0}
//int button[0] = digitalRead(A0);
//int button[1] = digitalRead(A1);
//int button[2] = digitalRead(A2);
//int button[3] = digitalRead(A3);
if (digitalRead(BUTTON1) == 0)
{ ges = 4; }
else if (digitalRead(BUTTON2) == 0)
{ ges = 3; }
else if (digitalRead(BUTTON3) == 0)
{ ges = 2; }
else if (digitalRead(BUTTON4) == 0)
{ ges = 1; }
else
{ ges = 8; }

return ges;
}

int detectGesture()
{
int ges=9;
//int button[] = {0,0,0,0}
//int button[0] = digitalRead(A0);
//int button[1] = digitalRead(A1);
//int button[2] = digitalRead(A2);
//int button[3] = digitalRead(A3);
if (analogRead(BUTTON1) >= 500)
{
  ges = 1; }
else if (analogRead(BUTTON2) >= 500)
{ ges = 2; }
else if (analogRead(BUTTON4) >= 600)
 {ges = 4;}
else if (analogRead(BUTTON3) >= 600)
 {ges = 3;}
else
{ ges = 8; }

return ges;
}


/***********************************************************************************/
/* BUZZER*/
void buzzerfun()
{
if (dist[0] < THRESHBUZZ )
  {
  digitalWrite(BUZZER,HIGH);
  Serial.print("  B HIGH :");
  }
  else
  {digitalWrite(BUZZER,LOW);
  Serial.print("  B HIGH :");}
}
/***********************************************************************************/
/* BUZZER*/



/***********************************************************************************/
/* TOUCH */

void pinInit()
{
  pinMode(ECHO1,INPUT );
  pinMode(TRIG1,OUTPUT);
  pinMode(BUZZER,OUTPUT);
  
  pinMode(BUTTON1   , INPUT_PULLUP);
  pinMode(BUTTON2   , INPUT_PULLUP);
  pinMode(BUTTON3   , INPUT_PULLUP);
  pinMode(BUTTON4   , INPUT_PULLUP);

  
}




void Init()
{
  Serial.begin(9600);
//  Serial.println("Orientation Sensor Raw Data Test"); Serial.println("");
  pinInit();
  noInterrupts();
  tim1_Init();
  interrupts(); // enable all(global) interrupts

  enableSonar(1);
  initializeSonar();
  previousTime = millis();
  currentTime  = previousTime;

}                                                                                                                                                                                                                                                                                                                                                                                                                                                          

void _print()
{
   Serial.print("  SONAR-1 :"); Serial.print(dist[0]); Serial.print(" cm ");
   Serial.print("  GESTURE :"); Serial.println(gesture);
}

void setup()
{
  Init();
}

void loop()
{

  handleObstacle(1);  // SONAR
  gesture = detectGestureold();    // Captouch
  buzzerfun();
  _print();           // print SONAR
  nrfloop(gesture);          // nrf

}










//  pinMode(A4   , INPUT_PULLUP);
//  pinMode(A5   , INPUT_PULLUP);

//  pinMode(BUTTON1   , OUTPUT);
//  pinMode(BUTTON2   , OUTPUT);
//  pinMode(BUTTON3   , OUTPUT);
//  pinMode(BUTTON4   , OUTPUT);
//
//  digitalWrite(BUTTON1   , LOW);
//  digitalWrite(BUTTON2   , LOW);
//  digitalWrite(BUTTON3   , LOW);
//  digitalWrite(BUTTON4   , LOW);
//  Serial.print("  GESTURE2 :"); Serial.print(analogRead(A2));
//  Serial.print("  GESTURE3 :"); Serial.print(analogRead(A3));
//  Serial.print("  GESTURE4 :"); Serial.print(analogRead(A4));
//  Serial.print("  GESTURE5 :"); Serial.println(analogRead(A5));

//  Serial.print("  GESTURE2 :"); Serial.print(digitalRead(A2));
//  Serial.print("  GESTURE3 :"); Serial.print(digitalRead(A3));
//  Serial.print("  GESTURE4 :"); Serial.print(digitalRead(A4));
//  Serial.print("  GESTURE5 :"); Serial.println(digitalRead(A5));



