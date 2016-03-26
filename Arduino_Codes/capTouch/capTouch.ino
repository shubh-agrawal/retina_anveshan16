
int interruptPin=2;
int signalValue=0;
int activenessCount=0;
int gesture_flag=0;
unsigned long t1=0, t_keep=0;
unsigned long time_gap_threshold=2000;

void execute_gesture(int count)
{
  Serial.print("Gesture number:  ");Serial.println(count);
}

void capTouch()
{
    if (activenessCount==0)
     {
       t1=millis();
       activenessCount++;
       gesture_flag=1;
     }
     
    if (activenessCount!=0)
    {
      t_keep=millis();
      if ( (t_keep - t1)<time_gap_threshold)
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
        //Serial.println(activenessCount);
}

void setup() 
{

  pinMode(interruptPin, INPUT);
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(interruptPin), capTouch, RISING);
}

void loop() 
{
  t_keep=millis();
  if ( ((t_keep - t1) > time_gap_threshold) && gesture_flag == 1)
 {
   execute_gesture(activenessCount-1);
   activenessCount=0;
   gesture_flag=0;
        
 } 
//Serial.println(digitalRead(interruptPin));
//delay(50);
}
