#include <SimpleFOC.h>
#include "SimpleFOCDrivers.h"
#include "encoders/as5048a/MagneticSensorAS5048A.h"

// magnetic sensor instance - SPI
MagneticSensorAS5048A sensor(10);

// BLDC motor & driver instance
BLDCMotor motor = BLDCMotor(11);
BLDCDriver3PWM driver = BLDCDriver3PWM(5, 9, 6, 8);

const int LED_PIN = 13;
const int VOLTAGE = 8;

struct CTX{
    bool is_initialized;
    float initial_angle;
    float target_angle;
}ctx;


void(* resetFunc) (void) = 0; //declare reset function @ address 0


void init_actuator() {
  if (ctx.is_initialized) {
      return;
  }
  // init sensor
  sensor.init();
  motor.linkSensor(&sensor);
  ctx.initial_angle = sensor.getSensorAngle();
  // init driver
  driver.voltage_power_supply = VOLTAGE;
  driver.voltage_limit = VOLTAGE;
  driver.init();
  motor.linkDriver(&driver);

  // init motor
  motor.controller = MotionControlType::angle;
  motor.voltage_limit = VOLTAGE;
  motor.velocity_limit = 20;

//  motor.P_angle.P = 10;
//  motor.P_angle.I = 0;
//  motor.P_angle.D = 3;

  motor.init();

  motor.initFOC();

  ctx.is_initialized = true;
}

unsigned char read() {
    while(Serial.available() == 0);
    return Serial.read();
}

void process_command(unsigned char cmd) {
    unsigned char upper;
    unsigned char lower;
    switch(cmd)
    {
    case 0x80: // init
        init_actuator();
        Serial.println("end");
        break;

    case 0x81: // stop
        motor.voltage_limit = 0;
        Serial.println("end");
        break;

    case 0x89: // reset
        resetFunc();
        break;

    case 0x90: // Set velocity limit
        motor.velocity_limit = read();
        break;

    case 0x91: // Set target position
        upper = read();
        lower = read();
        ctx.target_angle = (((float)upper * 128.0 + (float)lower - 8192.0) * 2.0 * PI / 16384.0)*10;

        break;

    case 0x92: // Set current limit
        motor.current_limit = (float)read() / 10.0;
        break;

    case 0x93: // Set zero point
        upper = read();
        lower = read();
        ctx.initial_angle = -(((float)upper * 128.0 + (float)lower - 8192.0) * 2.0 * PI / 16384.0)*10;
        break;

    case 0x94: // Get angle
        Serial.print("i:");
        Serial.print(ctx.initial_angle);
        Serial.print(" t:");
        Serial.print(ctx.target_angle);
        Serial.print(" a:");
        Serial.println(sensor.getSensorAngle());
        break;
    }
}

void setup() {
  Serial.begin(38400);

  pinMode( LED_PIN, OUTPUT );

  ctx.is_initialized = false;
  ctx.initial_angle = 0.0;
  ctx.target_angle = 0.0;
}

void loop() {

    if (Serial.available() != 0) {
        unsigned char data = Serial.read();
        if (data & 0x80) {
            // if head bit is 1, it is a command
            process_command(data);
        }
    }

    if (ctx.is_initialized) {
        // Motion control function
        motor.move(ctx.initial_angle + ctx.target_angle);
        // main FOC algorithm function
        motor.loopFOC();
        digitalWrite( LED_PIN, HIGH );
    }
    else {
      digitalWrite( LED_PIN, LOW );
    }
}
