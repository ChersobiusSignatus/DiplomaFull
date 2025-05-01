
#include <Wire.h>
#include <DHT.h>
#include <BH1750.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <LowPower.h>

#define DHTPIN 5
#define DHTTYPE DHT11
#define SOIL_SENSOR_POWER 7
#define SOIL_SENSOR_PIN A2
#define MQ9_A0 A0

DHT dht(DHTPIN, DHTTYPE);
BH1750 lightMeter(0x5C);
SoftwareSerial BTSerial(10, 11); 

void setup() {
    Serial.begin(9600);
    BTSerial.begin(9600);
    Serial.println("Starting...");
    BTSerial.println("Bluetooth ready!");

    Wire.begin();
    dht.begin();
    lightMeter.begin();

    pinMode(SOIL_SENSOR_POWER, OUTPUT);
    digitalWrite(SOIL_SENSOR_POWER, LOW);
}

void loop() {
    Serial.println("Reading sensors...");
    BTSerial.println("Reading sensors...");
    
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    int soilMoisture = readSoilMoisture();
    float lux = lightMeter.readLightLevel();
    int gasLevel = analogRead(MQ9_A0);
    
    if (isnan(temperature) || isnan(humidity)) {
        Serial.println("DHT11 reading failed!");
        BTSerial.println("{\"error\": \"DHT11 sensor failure\"}");
    } else {        
        StaticJsonDocument<200> doc;
        doc["temperature"]["value"] = temperature;
        doc["temperature"]["unit"] = "°C";

        doc["humidity"]["value"] = humidity;
        doc["humidity"]["unit"] = "%";

        doc["soilMoisture"]["value"] = soilMoisture;
        doc["soilMoisture"]["unit"] = "raw";

        doc["light"]["value"] = lux;
        doc["light"]["unit"] = "lux";

        doc["gas"]["value"] = gasLevel;
        doc["gas"]["unit"] = "analog";
        
        String jsonString;
        serializeJson(doc, jsonString);
        BTSerial.println(jsonString);
    }

    Serial.println("Data collected. Entering sleep mode for 24 hours...");
    BTSerial.println("Data collected. Entering sleep mode for 24 hours...");
    Serial.println("---------------------------");
    
    for (int i = 0; i < 10800; i++) {
        LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
    }
}

int readSoilMoisture() {
    digitalWrite(SOIL_SENSOR_POWER, HIGH);
    delay(10);
    int value = analogRead(SOIL_SENSOR_PIN);
    digitalWrite(SOIL_SENSOR_POWER, LOW);
    return value;
}
