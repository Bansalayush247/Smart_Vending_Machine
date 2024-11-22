#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <SPI.h>
#include <MFRC522.h>

// WiFi credentials
const char* ssid = "Your SSID";
const char* password = "Your Password";

// Server URL
const char* serverUrl = "http://192.168.152.115:5000/rfid"; // Replace with your Raspberry Pi's IP and port

// RFID Reader pins
constexpr uint8_t RST_PIN = D3;  // Configurable, see typical pin layout above
constexpr uint8_t SS_PIN = D4;   // Configurable, see typical pin layout above

MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the MFRC522 class
MFRC522::MIFARE_Key key;

void setup() {
    Serial.begin(9600);

    // Initialize SPI and MFRC522
    SPI.begin();
    rfid.PCD_Init();
    Serial.println("RFID reader initialized");

    // Connect to WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to WiFi");
}

void loop() {
  if(!rfid.PICC_IsNewCardPresent()) return;
    // Check for new RFID cards
    if ( rfid.PICC_ReadCardSerial()) {
        // Read RFID tag
        String tag = "";
        for (byte i = 0; i < rfid.uid.size; i++) {
            tag += String(rfid.uid.uidByte[i], HEX); // Convert to hexadecimal
        }
        tag.toUpperCase(); // Optional: make tag uppercase
        Serial.printf("RFID Tag: %s\n", tag.c_str());

        // Send the RFID data to the server
        sendRFIDData(tag);

        // Halt the card and stop encryption
        rfid.PICC_HaltA();
        rfid.PCD_StopCrypto1();
    }

    delay(1000); // Slight delay to prevent rapid polling
}

void sendRFIDData(const String& tag) {
    if (WiFi.status() == WL_CONNECTED) {
        WiFiClient client;
        HTTPClient http;

        // Initialize HTTP client with the server URL
        http.begin(client, serverUrl);

        // Set the content type to JSON
        http.addHeader("Content-Type", "application/json");

        // Create JSON payload
        String payload = "{\"rfid\":\"" + tag + "\"}";

        // Send HTTP POST request
        int httpResponseCode = http.POST(payload);

        // Check the response
        if (httpResponseCode > 0) {
            Serial.printf("HTTP Response Code: %d\n", httpResponseCode);
            String response = http.getString();
            Serial.printf("Response: %s\n", response.c_str());
        } else {
            Serial.printf("Error in sending POST request: %s\n", http.errorToString(httpResponseCode).c_str());
        }

        // Close connection
        http.end();
    } else {
        Serial.println("WiFi not connected");
    }
}
