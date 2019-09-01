void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()){
    digitalWrite(LED_BUILTIN, LOW);
    int in = Serial.parseInt();
    if(in > 0){
      for(int i = 0; i < in; i++){
        digitalWrite(LED_BUILTIN, HIGH);
        delay(100);
        digitalWrite(LED_BUILTIN, LOW);
        delay(100);
      }
    } else if (in < 0){
      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);
      digitalWrite(LED_BUILTIN, LOW);
      delay(500);
      for(int i = 0; i < -in; i++){
        digitalWrite(LED_BUILTIN, HIGH);
        delay(100);
        digitalWrite(LED_BUILTIN, LOW);
        delay(100);
      }
    } else{
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
}
