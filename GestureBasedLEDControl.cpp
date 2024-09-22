const int led1 = 2;
const int led2 = 3;
const int led3 = 4;

void setup() {
  Serial.begin(9600);  // Start serial communication
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char data = Serial.read();  // Read data from the serial port

    // Turn on LEDs based on the number of fingers detected
    if (data == '1') {
      digitalWrite(led1, HIGH);
      digitalWrite(led2, LOW);
      digitalWrite(led3, LOW);
    } else if (data == '2') {
      digitalWrite(led1, HIGH);
      digitalWrite(led2, HIGH);
      digitalWrite(led3, LOW);
    } else if (data == '3') {
      digitalWrite(led1, HIGH);
      digitalWrite(led2, HIGH);
      digitalWrite(led3, HIGH);
    }
  }
}
