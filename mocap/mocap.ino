#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#define BNO055_SAMPLERATE_DELAY_MS (20)

// Check I2C device address and correct line below (by default address is 0x29 or 0x28)
//                                   id, address
Adafruit_BNO055 bno = Adafruit_BNO055(-1, 0x28, &Wire);

unsigned long next_t = 0;

void setup(void)
{
  Serial.begin(115200);

  while (!Serial) delay(10);  // wait for serial port to open!

  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  delay(1000);
  bno.setExtCrystalUse(true);

  next_t = millis() + BNO055_SAMPLERATE_DELAY_MS;
}

void loop(void)
{
  union{
    struct{
      unsigned int start;
      unsigned int calib;
      int x;
      int y;
      int z;
    };
    unsigned char bin[sizeof(unsigned int)*5];
  } packet;

  uint8_t system, gyro, accel, mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);
  packet.calib = system * 64 + gyro * 16 + accel * 4 + mag;
  
  imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);

  packet.start = 0xFFFF;
  packet.x = euler.x();
  packet.y = euler.y();
  packet.z = euler.z();

  for( int i = 0 ; i != sizeof(packet) ; i++ ){
    Serial.write(packet.bin[i]);
  }

  while (millis() < next_t)
  {
    /* do nothing */
  }

  next_t += BNO055_SAMPLERATE_DELAY_MS;
}