/**
 * KP_promicro.ino
 * Example
 * 
 */

const int BAUDRATE = 115200;  // bits/sec
const int BURST_DELAY = 50;   // ms between flashes

// runs once on power up
void setup() {
  Serial.begin(BAUDRATE);
  Serial1.begin(BAUDRATE); // begin Bluetooth connection (RX1 and TX0)
  RXBurst();
  TXBurst();
}

// runs continuously
void loop() {
  if (Serial1.available()) {
    RXBurst();
    int input = Serial1.read();
    if (input == 'h') {
      TXBurst();
    }
    Serial.println("hello");
  }
  if (Serial.available()) {
    RXBurst();
    TXBurst();
    Serial.print(Serial.read());
  }
}

// makes RX (yellow) LED blink three times
void RXBurst() {
  int RXLED = 17;
  digitalWrite(RXLED, LOW);
  delay(BURST_DELAY);
  digitalWrite(RXLED, HIGH);
  delay(BURST_DELAY);
  digitalWrite(RXLED, LOW);
  delay(BURST_DELAY);
  digitalWrite(RXLED, HIGH);
  delay(BURST_DELAY);
  digitalWrite(RXLED, LOW);
  delay(BURST_DELAY);
  digitalWrite(RXLED, HIGH);
  delay(BURST_DELAY);
}

// makes TX (green) LED blink three times
void TXBurst() {
  TXLED1;
  delay(BURST_DELAY);
  TXLED0;
  delay(BURST_DELAY);
  TXLED1;
  delay(BURST_DELAY);
  TXLED0;
  delay(BURST_DELAY);
  TXLED1;
  delay(BURST_DELAY);
  TXLED0;
  delay(BURST_DELAY);
}
