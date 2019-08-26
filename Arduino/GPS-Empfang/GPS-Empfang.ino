#include <LiquidCrystal.h>
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


int delaye = 1000;
long lat = 557080;   //55.7080
long lon = 424452;   //42.4452
long hig = 10000000; //1000.0000
long v_lat = 0.0;
long v_lon = 0.0;
long v_hig = 0.0;
long v_lat_min =    -162 * (delaye / 1000.0);  // -0.02 * (delaye / 1000.0)
long v_lat_max =     162 * (delaye / 1000.0);  //  0.02 * (delaye / 1000.0)
long v_lon_min =    -262 * (delaye / 1000.0);  // -0.02 * (delaye / 1000.0)
long v_lon_max =     262 * (delaye / 1000.0);  //  0.02 * (delaye / 1000.0)
long v_hig_min = -100000 * (delaye / 1000.0);  //-11.00 * (delaye / 1000.0)
long v_hig_max =       0 * (delaye / 1000.0);  //  0.00 * (delaye / 1000.0)
int i = 0;


void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  delay(1000);
  lcd.begin(16, 2);
  lcd.clear();
}

void loop() {
  i++;
  long randLat = random(  -162 * (delaye / 1000.0),   162 * (delaye / 1000.0) + 1);    //random(  -20,   21) /  10.0
  long randLon = random(  -262 * (delaye / 1000.0),   262 * (delaye / 1000.0) + 1);    //random(  -20,   21) /  10.0
  long randHig = random(-108100, -88099);  //random(-1081, -880) / 100.0
  v_lat += randLat;
  v_lon += randLon;
  v_hig += randHig * (delaye / 1000.0);
  v_lat = constrain(v_lat, v_lat_min, v_lat_max);
  v_lon = constrain(v_lon, v_lon_min, v_lon_max);
  v_hig = constrain(v_hig, v_hig_min, v_hig_max);
  lat += v_lat;
  lon += v_lon;
  hig += v_hig + random(-10000, 10001);
  if (hig <= 100000) {  //hig <= 10.0
    hig = 10000000;     //hig = 1000.0
    v_lat = 0.0;
    v_lon = 0.0;
    v_hig = 0.0;
  }
  //Serial.println(String(randLat) + "\n" + String(randLon));
  if (i >= 1000.0 / delaye) {
    lcd.clear();
    lcd.print(v_lat);
    lcd.setCursor(0, 1);
    lcd.print(v_lon);
    i = 0;
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.print("51 " + String(lat) + ", 7 " + String(lon) + ", " + String(hig));//51 55.7080, 7 42.4452
  }
  delay(delaye);
  digitalWrite(LED_BUILTIN, LOW);
  /*Serial.print("51 54.7080, 7 43.4452");//51 54.7080, 7 43.4452
  delay(delaye);
  Serial.print("51 53.7080, 7 44.4452");//51 53.7080, 7 44.4452
  delay(delaye);
  Serial.print("51 52.7080, 7 45.4452");//51 52.7080, 7 45.4452
  delay(delaye);
  Serial.print("51 51.7080, 7 46.4452");//51 51.7080, 7 46.4452
  delay(delaye);
  Serial.print("51 52.7080, 7 45.4452");//51 52.7080, 7 45.4452
  delay(delaye);
  Serial.print("51 53.7080, 7 44.4452");//51 53.7080, 7 44.4452
  delay(delaye);
  Serial.print("51 54.7080, 7 43.4452");//51 54.7080, 7 43.4452
  delay(delaye);*/
}
