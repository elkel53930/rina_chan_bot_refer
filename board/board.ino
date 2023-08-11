#include <Adafruit_NeoPixel.h>

#define INDICATOR (13)
#define PIN (6)
#define NUM_OF_LED (200)
#define DATA_LEN (29)
#define BUF_SIZE (NUM_OF_LED*3+1)

#define R (10)
#define G (0)
#define B (4)

Adafruit_NeoPixel pixels(NUM_OF_LED, PIN, NEO_GRB + NEO_KHZ800);

/*
  0x80 : 先頭ビットが1のデータはコマンド。0x80は0/1データ送信。
  0x00~0x7F : 0のビットは消灯、1のビットは点灯。1byteあたり7個分の情報量で、LED200個分のデータを送るので合計29byte
*/

#define CMD_DISPLAY (0x80)

unsigned char rgb_buf[BUF_SIZE] = {0};
int index = 0;

void set_color(int index, unsigned char r, unsigned char g, unsigned char b) {
  rgb_buf[index*3] = r;
  rgb_buf[index*3+1] = g;
  rgb_buf[index*3+2] = b;
}

void fill_with(unsigned char r, unsigned char g, unsigned char b)
{
  for(int i = 0 ; i != NUM_OF_LED ; i++)
  {
    set_color(i, r, g, b);
  }
}

void show() {
  pixels.clear();

  digitalWrite(INDICATOR, HIGH);

  for(int i = 0 ; i != NUM_OF_LED ; i++){
    pixels.setPixelColor(i, pixels.Color(
      rgb_buf[i*3],
      rgb_buf[i*3+1],
      rgb_buf[i*3+2]
    ));
  }
  pixels.show();
  
  digitalWrite(INDICATOR, LOW);
}

/**** COMMANDS ****/

void process_display() {
  for(int i = 0; i != DATA_LEN; i++)
  {
    while(Serial.available() == 0);
    unsigned char c = Serial.read();
    for(int j = 0; j != 7; j++)
    {
      if (c & (1 << j)) {
        set_color(i*7+j, R, G, B);
      }
      else{
        set_color(i*7+j, 0, 0, 0);
      }
    }
  }
  show();
}

/**** SETUP ***/

void setup() {
    int i;
    randomSeed(analogRead(0));
    fill_with(0, 0, 0);
    pixels.begin();
    for(i = 0 ; i != NUM_OF_LED ; i++){
      fill_with(0, 0, 0);
      set_color(i, R, G, B);
      show();
      delay(5);
    }
    fill_with(0, 0, 0);
    show();

    pinMode(PIN, OUTPUT);

    pinMode(INDICATOR, OUTPUT);

    Serial.begin(38400);
}

/**** LOOP ***/

void loop() {
  char buf[4] = {0};
  int i = 0;
  bool flag = true;

  while(flag)
  {
    if(Serial.available() > 0)
    {
      unsigned char c = Serial.read();
      switch(c)
      {
      case CMD_DISPLAY:
        process_display();
        break;
      default:
        break;
      }
    }
  }
}
