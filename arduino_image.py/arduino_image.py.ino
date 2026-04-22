#include <Wire.h>
#include <ArduCAM.h>
#include <SPI.h>
#include "memorysaver.h"

const int CS_PIN = 10;
ArduCAM myCAM(OV2640, CS_PIN);

void setup() {
  Serial.begin(115200);
  Wire.begin();
  SPI.begin();

  pinMode(CS_PIN, OUTPUT);
  digitalWrite(CS_PIN, HIGH);

  // Reset the CPLD
  myCAM.write_reg(0x07, 0x80);
  delay(100);
  myCAM.write_reg(0x07, 0x00);
  delay(100);

  // Verify SPI
  uint8_t temp;
  myCAM.write_reg(ARDUCHIP_TEST1, 0x55);
  temp = myCAM.read_reg(ARDUCHIP_TEST1);
  if (temp != 0x55) {
    Serial.println("SPI interface error — check wiring!");
    while (1);
  }
  // Serial.println("SPI interface OK");

  // Verify camera
  uint8_t vid, pid;
  myCAM.wrSensorReg8_8(0xff, 0x01);
  myCAM.rdSensorReg8_8(OV2640_CHIPID_HIGH, &vid);
  myCAM.rdSensorReg8_8(OV2640_CHIPID_LOW, &pid);
  if ((vid != 0x26) && (pid != 0x41 || pid != 0x42)) {
    Serial.println("Camera not detected — check I2C wiring!");
    while (1);
  }
  // Serial.println("Camera detected OK");

  myCAM.set_format(JPEG);
  myCAM.InitCAM();
  myCAM.OV2640_set_JPEG_size(OV2640_320x240);
  delay(1000);

  // Serial.println("Ready. Send 'c' to capture a photo.");
}

void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();

    if (cmd == 'c' || cmd == 'C') {
      captureAndSend();
    } else {
      // Serial.println("Unknown command. Send 'c' to capture.");
    }
  }
}

void captureAndSend() {
  Serial.println("CAPTURE_START");

  myCAM.flush_fifo();
  myCAM.clear_fifo_flag();
  myCAM.start_capture();

  // Wait for capture to complete
  while (!myCAM.get_bit(ARDUCHIP_TRIG, CAP_DONE_MASK));
  // Serial.println("Capture done!");

  // Read image size
  uint32_t imgSize = myCAM.read_fifo_length();
  // Serial.print("Image size: ");
  // Serial.print(imgSize);
  // Serial.println(" bytes");

  // Stream image over Serial
  myCAM.CS_LOW();
  myCAM.set_fifo_burst();

  for (uint32_t i = 0; i < imgSize; i++) {
    uint8_t data = SPI.transfer(0x00);
    Serial.write(data);
  }

  myCAM.CS_HIGH();
  Serial.println("CAPTURE_END");
}

// #include <SPI.h>
// #include <ArduCAM.h>
// #include <Wire.h>
// // #include "memorysaver.h"

// #define CS_PIN 7

// ArduCAM myCAM(OV2640, CS_PIN);
// uint8_t read_fifo_burst(ArduCAM myCAM);


// void setup() {
//   Serial.begin(115200);
//   SPI.begin();

//   Serial.println("Hello World :)");
//   myCAM.InitCAM();
//   delay(1000);
//   Serial.println("Ready. Type 'snap' to take a picture.");

// }

// void loop() {
//   if (Serial.available()) {
//     String cmd = Serial.readStringUntil('\n');
//     cmd.trim();

//     if (cmd == "snap") {
//       captureImage();
//     }
//   }
// }

// void captureImage() {
//   Serial.println("CAPTURE_START");

//   myCAM.flush_fifo();
//   myCAM.clear_fifo_flag();
//   myCAM.start_capture();

//   // wait until capture is done
//   while (!myCAM.get_bit(ARDUCHIP_TRIG, CAP_DONE_MASK));

//   uint32_t length = myCAM.read_fifo_length();

//   if (length >= 0x7FFFFF) {
//     Serial.println("ERROR: Image too large");
//     return;
//   }

//   myCAM.CS_LOW();
//   myCAM.set_fifo_burst();

//   // send raw JPEG bytes
//   for (uint32_t i = 0; i < length; i++) {
//     uint8_t b = SPI.transfer(0x00);
//     Serial.write(b);
//   }

//   myCAM.CS_HIGH();

//   Serial.println("\nCAPTURE_END");
// }