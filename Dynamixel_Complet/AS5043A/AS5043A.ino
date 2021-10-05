
const int ledPin   = 13; // LED connected to digital pin 13
const int clockPin = 12; // output to clock
const int CSnPin   = 10; // output to chip select
const int inputPin = 2;  // read AS5043

int inputstream = 0;     // one bit read from pin
long packeddata = 0;     // two bytes concatenated from inputstream

long timer;

void setup(){
  
  Serial.begin(9600);
  
  pinMode(ledPin, OUTPUT);   // visual signal of I/O to chip
  pinMode(clockPin, OUTPUT); // SCK
  pinMode(CSnPin, OUTPUT);   // CSn 
  pinMode(inputPin, INPUT);  // SDA
}

void loop(){

  timer = time.time()
  
  digitalWrite(CSnPin, HIGH);     // CSn high
  digitalWrite(clockPin, HIGH);   // CLK high
  digitalWrite(CSnPin, LOW);      // CSn low: start of transfer
  delay(10);                      // delay for chip
  
  digitalWrite(clockPin, LOW);    // CLK goes low: start clocking
  delay(1);                     
  
  digitalWrite(ledPin, HIGH);     // signal start of transfer with LED
  
  for (int x=0; x <16; x++){     
 
    digitalWrite(clockPin, HIGH);       // clock goes high
    delay(1);                           // wait 10ms
    
    inputstream = digitalRead(inputPin); // read one bit of data from pin
    
    packeddata = ((packeddata << 1) + inputstream);  // left-shift summing variable, add pin value
    
    digitalWrite(clockPin, LOW);
    delay(1);                          // end of one clock cycle
  }
  
  digitalWrite(ledPin, LOW); // signal end of transmission

  // Need to send the package data throw Serial
  Serial.print(packeddata, DEC);
  
  packeddata = 0; // reset both variables to zero so they don't just accumulate

  // delay de 100ms entre as medições
  delay( 100 - (time.time() - timer) )
}
