/**
 * Pro Micro 5V / BlueSMiRF Test
 *
 * Pro Micro has 2 Serial adapters. One on the USB port (Serial), another on 
 * pin 11 (RX) and 12 (TX) (known as Serial1).
 *
 * This program will transmit data received on Serial to Serial1 and Serial1 
 * to Serial. This can be useful when a bluetooth adapter must be hooked up to 
 * an usb port.
 *
 * Pins
 *    VCC to VCC (3.3-6V)
 *    GND to GND 
 *    TX-O to RX-I 
 *    RX-I to TX-O 
 * 
 * LEDs
 *    Orange: USB receive, Bluetooth transmit
 *    Green:  Bluetooth receive, USB transmit
 *
 * $Id$
 */

void setup() {
  Serial.begin(115200); //  USB
  Serial1.begin(115200); // BlueSMiRF
}

void loop() {
  if (Serial.available())
    Serial1.write(Serial.read());
  
  if (Serial1.available())
    Serial.write(Serial1.read());
}
