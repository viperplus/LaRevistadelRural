#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>
#include <WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

// Configuración WiFi
const char* ssid = "TU_RED_WIFI";
const char* password = "TU_CONTRASENA";

// Configuración matrix
#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 4
#define CS_PIN 5

MD_Parola matrix = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

// NTP
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", -10800, 60000); // UTC-3 (Argentina)

// Variables de tiempo
unsigned long lastUpdate = 0;
int currentHour = 0;
int currentMinute = 0;
int currentSecond = 0;
bool showDots = true;

// Animación
uint8_t scrollSpeed = 50;
textEffect_t scrollEffect = PA_SCROLL_LEFT;
textPosition_t scrollAlign = PA_LEFT;
uint16_t scrollPause = 0;

// Mensajes animados
const char* mensajes[] = {
  "HOLA MUNDO",
  "ESP32 READY",
  "LED MATRIX",
  "ANIMACION"
};
int numMensajes = 4;
int msgActual = 0;
bool modoReloj = true;
unsigned long tiempoAnimacion = 0;
const unsigned long duracionAnimacion = 5000; // 5 segundos por mensaje

void setup() {
  Serial.begin(115200);
  
  // Iniciar matrix
  matrix.begin();
  matrix.setIntensity(2);
  matrix.displayClear();
  
  // Mostrar mensaje de inicio
  matrix.displayScroll("INICIANDO...", PA_LEFT, PA_SCROLL_LEFT, 50);
  
  // Conectar WiFi
  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");
  
  int intentos = 0;
  while (WiFi.status() != WL_CONNECTED && intentos < 20) {
    delay(500);
    Serial.print(".");
    intentos++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi conectado!");
    timeClient.begin();
    timeClient.update();
    matrix.displayScroll("CONECTADO!", PA_LEFT, PA_SCROLL_LEFT, 50);
  } else {
    Serial.println("\nError WiFi - Modo offline");
    matrix.displayScroll("SIN WIFI - MODO OFFLINE", PA_LEFT, PA_SCROLL_LEFT, 50);
  }
  
  delay(2000);
}

void loop() {
  matrix.displayAnimate();
  
  // Actualizar hora cada segundo
  if (millis() - lastUpdate >= 1000) {
    lastUpdate = millis();
    
    if (WiFi.status() == WL_CONNECTED) {
      timeClient.update();
      currentHour = timeClient.getHours();
      currentMinute = timeClient.getMinutes();
      currentSecond = timeClient.getSeconds();
    }
    
    showDots = !showDots; // Parpadeo de los dos puntos
  }
  
  // Cambiar entre modo reloj y animaciones
  if (modoReloj) {
    mostrarReloj();
    
    // Después de un tiempo, mostrar animación
    if (millis() - tiempoAnimacion > 30000) { // 30 segundos en modo reloj
      modoReloj = false;
      tiempoAnimacion = millis();
      matrix.displayScroll(mensajes[msgActual], PA_LEFT, PA_SCROLL_LEFT, 50);
    }
  } else {
    // Si terminó la animación, mostrar siguiente mensaje o volver al reloj
    if (!matrix.displayAnimate()) {
      msgActual = (msgActual + 1) % numMensajes;
      
      if (msgActual == 0) {
        // Volvió al inicio, volver al reloj
        modoReloj = true;
        tiempoAnimacion = millis();
        matrix.displayClear();
      } else {
        matrix.displayScroll(mensajes[msgActual], PA_LEFT, PA_SCROLL_LEFT, 50);
      }
    }
  }
}

void mostrarReloj() {
  char hora[6];
  
  // Formato HH:MM
  if (showDots) {
    sprintf(hora, "%02d:%02d", currentHour, currentMinute);
  } else {
    sprintf(hora, "%02d %02d", currentHour, currentMinute);
  }
  
  // Mostrar sin animación (display estático)
  if (!matrix.displayAnimate()) {
    matrix.displayClear();
    matrix.displayText(hora, PA_CENTER, 0, 0, PA_PRINT);
  }
}
