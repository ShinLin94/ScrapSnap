#include <SPI.h>
#include <ArduCAM.h>
#include "memorysaver.h"

#define CS_PIN 10

ArduCAM myCAM(OV2640, CS_PIN);

void setup() {
  Serial.begin(115200);
  SPI.begin();

  myCAM.initCAM();
  delay(1000);

  Serial.println("Ready. Type 'snap' to take a picture.");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "snap") {
      captureImage();
    }
  }
}

void captureImage() {
  Serial.println("CAPTURE_START");

  myCAM.flush_fifo();
  myCAM.clear_fifo_flag();
  myCAM.start_capture();

  // wait until capture is done
  while (!myCAM.get_bit(ARDUCHIP_TRIG, CAP_DONE_MASK));

  uint32_t length = myCAM.read_fifo_length();

  if (length >= 0x7FFFFF) {
    Serial.println("ERROR: Image too large");
    return;
  }

  myCAM.CS_LOW();
  myCAM.set_fifo_burst();

  // send raw JPEG bytes
  for (uint32_t i = 0; i < length; i++) {
    uint8_t b = SPI.transfer(0x00);
    Serial.write(b);
  }

  myCAM.CS_HIGH();

  Serial.println("\nCAPTURE_END");
}