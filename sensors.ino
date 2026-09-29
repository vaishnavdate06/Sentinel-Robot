#include <DHT.h>

#define DHT_PIN       4
#define DHT_TYPE      DHT22

#define IR_PIN        27
#define MQ2_PIN       34

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
  Serial.begin(115200);

  pinMode(IR_PIN, INPUT);


  dht.begin();

  delay(2000);

  Serial.println("ESP32 Sensor Monitoring Started");
}

void loop() {

  // -------------------------
  // DHT22
  // -------------------------
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // -------------------------
  // IR Sensor
  // -------------------------
  int irValue = digitalRead(IR_PIN);

  // Change this if your IR module works opposite
  bool objectDetected = (irValue == LOW);

  // -------------------------
  // MQ-2
  // -------------------------
  int mq2Value = analogRead(MQ2_PIN);

  // -------------------------
  // Metal Detector
  // -------------------------

  // Change HIGH/LOW according to your module

  // -------------------------
  // Serial Output
  // -------------------------

  Serial.println("---------------");

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");

  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  Serial.print("IR Sensor: ");
  if (objectDetected)
    Serial.println("OBJECT DETECTED");
  else
    Serial.println("CLEAR");

  Serial.print("MQ-2 Raw Value: ");
  Serial.println(mq2Value);


  // -------------------------
  // JSON FORMAT
  // Useful for Raspberry Pi
  // -------------------------

  Serial.print("{");

  Serial.print("\"temperature\":");
  Serial.print(temperature);

  Serial.print(",\"humidity\":");
  Serial.print(humidity);

  Serial.print(",\"ir\":");
  Serial.print(objectDetected ? 1 : 0);

  Serial.print(",\"mq2\":");
  Serial.print(mq2Value);

  Serial.println("}");

  delay(2000);
}
