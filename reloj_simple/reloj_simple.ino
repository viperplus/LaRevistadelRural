#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>

#define HARDWARE_TYPE MD_MAX72XX::PAROLA_HW
#define MAX_DEVICES 4
#define CS_PIN 5

MD_Parola matrix = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

// Hora manual (ajustar)
int hora = 12;
int minuto = 30;

// Animaciones
const char* animaciones[] = {
  "HOLA",
  "ESP32",
  "LED MATRIX",
  "RELOJ DIGITAL"
};
int numAnim = 4;
int animActual = 0;

// Control de tiempo
unsigned long anteriorMillis = 0;
const long intervalo = 1000;
bool mostrarPuntos = true;

// Modo actual
enum Modo { RELOJ, ANIMACION };
Modo modoActual = RELOJ;
unsigned long ultimoCambioModo = 0;
const unsigned long duracionAnim = 4000;

void setup() {
  Serial.begin(115200);
  matrix.begin();
  matrix.setIntensity(15);
  matrix.displayClear();
  
  Serial.println("Matrix LED 4x8x8 - ESP32");
  Serial.println("Envia 'h' para modo reloj");
  Serial.println("Envia 'a' para animaciones");
  Serial.println("Envia '+' hora / '-' bajar hora");
  Serial.println("Envia 'd' subir minuto / 'u' bajar minuto");
}

void loop() {
  matrix.displayAnimate();
  
  // Control manual por serial
  if (Serial.available()) {
    char c = Serial.read();
    switch(c) {
      case 'h': case 'H':
        modoActual = RELOJ;
        ultimoCambioModo = millis();
        Serial.println("Modo: RELOJ");
        break;
      case 'a': case 'A':
        modoActual = ANIMACION;
        ultimoCambioModo = millis();
        matrix.displayScroll(animaciones[animActual], PA_LEFT, PA_SCROLL_LEFT, 50);
        Serial.println("Modo: ANIMACION");
        break;
      case '+':
        hora = (hora + 1) % 24;
        Serial.print("Hora: "); Serial.println(hora);
        break;
      case '-':
        hora = (hora - 1 + 24) % 24;
        Serial.print("Hora: "); Serial.println(hora);
        break;
      case 'd': case 'D':
        minuto = (minuto + 1) % 60;
        Serial.print("Minuto: "); Serial.println(minuto);
        break;
      case 'u': case 'U':
        minuto = (minuto - 1 + 60) % 60;
        Serial.print("Minuto: "); Serial.println(minuto);
        break;
    }
  }
  
  switch(modoActual) {
    case RELOJ:
      mostrarReloj();
      break;
      
    case ANIMACION:
      mostrarAnimacion();
      break;
  }
}

void mostrarReloj() {
  unsigned long actualMillis = millis();
  
  // Actualizar tiempo cada segundo
  if (actualMillis - anteriorMillis >= intervalo) {
    anteriorMillis = actualMillis;
    mostrarPuntos = !mostrarPuntos;
    
    minuto++;
    if (minuto >= 60) {
      minuto = 0;
      hora = (hora + 1) % 24;
    }
  }
  
  // Dibujar reloj
  char buffer[6];
  if (mostrarPuntos) {
    sprintf(buffer, "%02d:%02d", hora, minuto);
  } else {
    sprintf(buffer, "%02d %02d", hora, minuto);
  }
  
  matrix.displayClear();
  matrix.displayText(buffer, PA_CENTER, 0, 0, PA_PRINT);
}

void mostrarAnimacion() {
  unsigned long actualMillis = millis();
  
  if (!matrix.displayAnimate()) {
    animActual = (animActual + 1) % numAnim;
    
    // Si terminamos todas las animaciones, volver al reloj
    if (animActual == 0) {
      modoActual = RELOJ;
      ultimoCambioModo = actualMillis;
      Serial.println("Volviendo al reloj...");
    } else {
      matrix.displayScroll(animaciones[animActual], PA_LEFT, PA_SCROLL_LEFT, 50);
    }
  }
}
