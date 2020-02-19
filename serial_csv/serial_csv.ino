// instrumentation amp vars
int in_pin = A1;
int v_amp = 0;

// keep track of time
int freq = 60;
unsigned int count = 0;

// buffer for formatted csv output
// <count(5)>,<voltage(4)>
char* output = "00000,0000";

void setup() {
  pinMode(in_pin, INPUT);
  Serial.begin(115200);
  delay(2000);
  Serial.println("START");
}

void loop() {
  count++;
  v_amp = analogRead(in_pin);

  sprintf(output, "%05i,%04i", count, v_amp);
  Serial.println(output);
  
  delay(1000 / freq);
}
