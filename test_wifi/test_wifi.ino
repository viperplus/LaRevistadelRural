#include <WiFi.h>

const char* ssid = "SAVV-G";
const char* password = "D854A41095d854a41095..";

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("Escaneando redes...");
  WiFi.mode(WIFI_STA);
  int n = WiFi.scanNetworks();
  Serial.println("Redes encontradas:");
  for (int i = 0; i < n; i++) {
    Serial.print("  ");
    Serial.print(WiFi.SSID(i));
    Serial.print(" (");
    Serial.print(WiFi.RSSI(i));
    Serial.print(" dBm)");
    if (WiFi.encryptionType(i) == WIFI_AUTH_OPEN) Serial.print(" [ABIERTA]");
    Serial.println();
  }

  Serial.println();
  Serial.print("Conectando a: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  int intentos = 0;
  while (WiFi.status() != WL_CONNECTED && intentos < 20) {
    delay(500);
    Serial.print("Status: ");
    Serial.println(WiFi.status());
    intentos++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("CONECTADO!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.print("FALLO. Status final: ");
    Serial.println(WiFi.status());
  }
}

void loop() {}
