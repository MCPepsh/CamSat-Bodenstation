#include <LiquidCrystal.h>
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

char x_input[14];
char y_input[14];
int i_x = 0;
int i_y = 0;
int pin = LED_BUILTIN;

byte z1[] = {
  '>',
  '>',
  '>',
  '>',
  '>',
  '>',
  'T',
  'E',
  'A',
  'M',
  '<',
  '<',
  '<',
  '<',
  '<',
  '<'
};
byte z2[] = {
  '>',
  '>',
  '>',
  '>',
  '>',
  'C',
  'A',
  'M',
  'S',
  'A',
  'T',
  '<',
  '<',
  '<',
  '<',
  '<'
};

void setup() {
  lcd.begin(16, 2);
  lcd.clear();
  //lcd.cursor();
  Serial.begin(115200);
  pinMode(pin, OUTPUT);

  for (int i = 0; i < 16; i++) {
    lcd.setCursor(i, 0);
    lcd.write(z1[i]);
    lcd.setCursor(15 - i, 1);
    lcd.write(z2[15 - i]);
    delay(64);
  }
}

void loop() {
  if (Serial.available()) {
    delay(100);
    lcd.clear();
    memset(x_input, '\0', sizeof(x_input));
    memset(y_input, '\0', sizeof(y_input));
    i_x = 0;
    i_y = 0;
    if (Serial.read() == 'x') {
      char temp;
      while (Serial.available() > 0 && temp != 'y') {
        temp = Serial.read();
        x_input[i_x] = temp;
        i_x++;
      }
      while (Serial.available() > 0 && temp != 'x') {
        temp = Serial.read();
        y_input[i_y] = temp;
        i_y++;
      }
    }
    float x = atof(x_input);
    float y = atof(y_input);
    lcd.setCursor(0, 0);
    lcd.print("x:" + String(x));
    lcd.setCursor(0, 1);
    lcd.print("y:" + String(y));
    //lcd.setCursor(0, 0);
    if (x > 0.0) {
      for (int i = 0; i < int(x); i++) {
        lcd.setCursor(8 + i, 0);
        lcd.write(byte(0));
      }
    } else if (x < 0.0) {
      for (int i = 0; i < int(x); i--) {
        lcd.setCursor(7 + i, 0);
        lcd.write(byte(1));
      }
    }
    if (y > 0.0) {
      for (int i = 0; i < int(y); i++) {
        lcd.setCursor(8 + i, 1);
        lcd.write(byte(2));
      }
    } else if (y < 0.0) {
      for (int i = 0; i < int(y); i--) {
        lcd.setCursor(7 + i, 1);
        lcd.write(byte(3));
      }
    }
    /*if (x > 0.0 || x < 0.0) {
      digitalWrite(pin, HIGH);
      //lcd.clear();
      //lcd.setCursor(0, 0);
      //lcd.print("8");
      //lcd.setCursor(0, 1);
      //lcd.print("8");
      } else {
      digitalWrite(pin, LOW);
      //lcd.clear();
      }*/
  }
}
