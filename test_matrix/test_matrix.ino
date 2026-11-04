#include <SPI.h>

#define CS_PIN 5

void max7219_send(byte reg, byte data, int device) {
  digitalWrite(CS_PIN, LOW);
  for (int i = 0; i < 4; i++) {
    SPI.transfer((i == device) ? reg : 0x00);
    SPI.transfer((i == device) ? data : 0x00);
  }
  digitalWrite(CS_PIN, HIGH);
}

void setup() {
  pinMode(CS_PIN, OUTPUT);
  digitalWrite(CS_PIN, HIGH);
  SPI.begin();
  SPI.setFrequency(10000000);
  SPI.setDataMode(SPI_MODE0);

  for (int i = 0; i < 4; i++) {
    max7219_send(0x0F, 0x00, i);
    max7219_send(0x0B, 0x07, i);
    max7219_send(0x0A, 0x0F, i);
    max7219_send(0x0C, 0x01, i);
    max7219_send(0x09, 0x00, i);
    for (int row = 1; row <= 8; row++) {
      max7219_send(row, 0xFF, i);
    }
  }
}

void loop() {
}
