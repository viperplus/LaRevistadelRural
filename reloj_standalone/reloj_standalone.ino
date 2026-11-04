#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>
#include <WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

// WiFi - solo se conecta al inicio
const char* ssid = "SAVV-G";
const char* password = "D854A41095d854a41095..";

// Matrix
#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 4
#define CS_PIN 5

MD_Parola matrix = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

// NTP
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", -10800, 0);

// Reloj interno
int hora = 0;
int minuto = 0;
int segundo = 0;
unsigned long anteriorMillis = 0;
bool mostrarPuntos = true;

// Sincronización periódica (cada 6 horas para evitar drift)
unsigned long ultimoSync = 0;
const unsigned long intervaloSync = 6 * 60 * 60 * 1000UL; // 6 horas

// Animación
const char* mensajes[] = {
  "HOLA MUNDO",
  "ESP32",
  "LED MATRIX",
  "ANIMACION"
};
int numMensajes = 4;
int msgActual = 0;
bool modoReloj = true;
unsigned long tiempoAnimacion = 0;
const unsigned long duracionReloj = 30000; // 30 segundos en reloj

void setup() {
  Serial.begin(115200);
  
  matrix.begin();
  matrix.setIntensity(2);
  matrix.displayClear();
  
  // Fase 1: Conectar WiFi y obtener hora
  matrix.displayText("WIFI...", PA_CENTER, 0, 0, PA_PRINT);
  WiFi.begin(ssid, password);
  
  int intentos = 0;
  while (WiFi.status() != WL_CONNECTED && intentos < 20) {
    delay(500);
    Serial.print(".");
    intentos++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    timeClient.begin();
    timeClient.update();
    hora = timeClient.getHours();
    minuto = timeClient.getMinutes();
    segundo = timeClient.getSeconds();
    ultimoSync = millis();
    
    Serial.print("Hora: ");
    Serial.print(hora);
    Serial.print(":");
    Serial.println(minuto);
    
    matrix.displayText("OK!", PA_CENTER, 0, 0, PA_PRINT);
    delay(1000);
  } else {
    Serial.println("Sin WiFi - hora 00:00");
    hora = 0;
    minuto = 0;
    matrix.displayText("ERR", PA_CENTER, 0, 0, PA_PRINT);
    delay(1000);
  }
  
  // Fase 2: Desconectar WiFi
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
  Serial.println("WiFi apagado - modo standalone");
  
  anteriorMillis = millis();
  tiempoAnimacion = millis();
}

void loop() {
  matrix.displayAnimate();
  
  // Actualizar reloj interno cada segundo
  unsigned long actualMillis = millis();
  if (actualMillis - anteriorMillis >= 1000) {
    anteriorMillis = actualMillis;
    mostrarPuntos = !mostrarPuntos;
    
    segundo++;
    if (segundo >= 60) {
      segundo = 0;
      minuto++;
      if (minuto >= 60) {
        minuto = 0;
        hora = (hora + 1) % 24;
      }
    }
  }
  
  // Re-sincronizar cada 6 horas (opcional)
  if (actualMillis - ultimoSync >= intervaloSync) {
    resyncTime();
  }
  
  // Modo reloj o animación
  if (modoReloj) {
    mostrarReloj();
    
    if (actualMillis - tiempoAnimacion > duracionReloj) {
      modoReloj = false;
      tiempoAnimacion = actualMillis;
      msgActual = 0;
      matrix.displayScroll(mensajes[msgActual], PA_LEFT, PA_SCROLL_LEFT, 50);
    }
  } else {
    if (!matrix.displayAnimate()) {
      msgActual++;
      if (msgActual >= numMensajes) {
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
  char buffer[6];
  if (mostrarPuntos) {
    sprintf(buffer, "%02d:%02d", hora, minuto);
  } else {
    sprintf(buffer, "%02d %02d", hora, minuto);
  }
  
  if (!matrix.displayAnimate()) {
    matrix.displayClear();
    matrix.displayText(buffer, PA_CENTER, 0, 0, PA_PRINT);
  }
}

void resyncTime() {
  Serial.println("Re-sincronizando hora...");
  
  // Reconectar brevemente
  WiFi.begin(ssid, password);
  int intentos = 0;
  
  while (WiFi.status() != WL_CONNECTED && intentos < 10) {
    delay(500);
    intentos++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    timeClient.update();
    hora = timeClient.getHours();
    minuto = timeClient.getMinutes();
    segundo = timeClient.getSeconds();
    Serial.println("Hora actualizada");
  }
  
  // Desconectar de nuevo
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
  ultimoSync = millis();
}
