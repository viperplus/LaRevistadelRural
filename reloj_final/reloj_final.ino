#include <SPI.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <time.h>

const char* ssid = "SAVV-G";
const char* password = "d854a41095D854A41095..";

#define CS_PIN 5

const byte font[39][5] = {
  {0x7E,0x81,0x81,0x81,0x7E},{0x00,0x82,0xFF,0x80,0x00},{0xC2,0xA1,0x91,0x89,0x86},
  {0x42,0x81,0x89,0x99,0x66},{0x30,0x28,0x24,0xFF,0x20},{0x4F,0x89,0x89,0x89,0x71},
  {0x7E,0x89,0x89,0x89,0x72},{0x01,0xE1,0x11,0x09,0x07},{0x76,0x89,0x89,0x89,0x76},
  {0x06,0x89,0x89,0x89,0x7E},{0x00,0x00,0x00,0x00,0x00},
  {0x7E,0x09,0x09,0x09,0x7E},{0x7F,0x89,0x89,0x89,0x76},{0x7E,0x81,0x81,0x81,0x42},
  {0x7F,0x81,0x81,0x81,0x7E},{0x7F,0x89,0x89,0x89,0x81},{0x7F,0x09,0x09,0x09,0x01},
  {0x7E,0x81,0x89,0x89,0x72},{0x7F,0x08,0x08,0x08,0x7F},{0x00,0x81,0xFF,0x81,0x00},
  {0x40,0x80,0x80,0x80,0x7F},{0x7F,0x08,0x14,0x22,0x41},{0x7F,0x80,0x80,0x80,0x80},
  {0x7F,0x02,0x04,0x02,0x7F},{0x7F,0x02,0x04,0x08,0x7F},{0x7E,0x81,0x81,0x81,0x7E},
  {0x7F,0x09,0x09,0x09,0x06},{0x7E,0x81,0xA1,0x41,0xBE},{0x7F,0x09,0x19,0x29,0x46},
  {0x46,0x89,0x89,0x89,0x72},{0x01,0x01,0x7F,0x01,0x01},{0x7F,0x80,0x80,0x80,0x7F},
  {0x1F,0x60,0x80,0x60,0x1F},{0x7F,0x40,0x20,0x40,0x7F},{0x63,0x14,0x08,0x14,0x63},
  {0x07,0x08,0x70,0x08,0x07},{0x61,0x51,0x49,0x45,0x43},
  {0x06,0x09,0x09,0x06,0x00}
};

byte pantalla[32];

int hora = 0, minuto = 0, segundo = 0;
float temperatura = 0;
unsigned long anteriorMillis = 0;
bool mostrarPuntos = true;

unsigned long ultimoSync = 0;
const unsigned long intervaloSync = 6UL * 60 * 60 * 1000;

enum Modo { RELOJ, TEMPERATURA, PACMAN };
Modo modoActual = RELOJ;
unsigned long ultimoCambioModo = 0;
unsigned long intervaloModo = 20000;

int animFrame = 0;
unsigned long ultimoFrame = 0;

struct tm timeinfo;

void max7219_send(byte reg, byte data, int device) {
  digitalWrite(CS_PIN, LOW);
  for (int i = 0; i < 4; i++) {
    SPI.transfer((i == device) ? reg : 0x00);
    SPI.transfer((i == device) ? data : 0x00);
  }
  digitalWrite(CS_PIN, HIGH);
}

void actualizarPantalla() {
  for (int dev = 0; dev < 4; dev++) {
    for (int row = 0; row < 8; row++) {
      byte colByte = 0;
      for (int bit = 0; bit < 8; bit++) {
        int pos = dev * 8 + (7 - bit);
        if (pantalla[pos] & (1 << row)) colByte |= (1 << bit);
      }
      max7219_send(row + 1, colByte, dev);
    }
  }
}

void limpiarPantalla() { memset(pantalla, 0, sizeof(pantalla)); }

void dibujarDigito(int x, int d) {
  if (d < 0 || d > 9) return;
  for (int i = 0; i < 5; i++)
    if (x + i >= 0 && x + i < 32) pantalla[x + i] = font[d][i];
}

void dibujarLetra(int x, char c) {
  int idx = -1;
  if (c >= '0' && c <= '9') idx = c - '0';
  else if (c >= 'A' && c <= 'Z') idx = c - 'A' + 11;
  else if (c >= 'a' && c <= 'z') idx = c - 'a' + 11;
  else if (c == ' ') idx = 10;
  else if (c == '.') { if (x >= 0 && x < 32) pantalla[x + 3] = 0x40; return; }
  else if (c == '-') { for (int i = 0; i < 5; i++) if (x+i>=0 && x+i<32) pantalla[x+i] = (i==2)?0x08:0x00; return; }
  if (idx >= 0) for (int i = 0; i < 5; i++)
    if (x+i>=0 && x+i<32) pantalla[x+i] = font[idx][i];
}

int dibujarString(int x, const char* s) {
  int startX = x;
  while (*s) { dibujarLetra(x, *s); x += 6; s++; }
  return x - startX;
}

void dibujarGrado(int x) {
  for (int i = 0; i < 3; i++)
    if (x + i >= 0 && x + i < 32) pantalla[x + i] = font[38][i];
}

void dibujarReloj() {
  int x = 2;
  dibujarDigito(x, hora / 10);    x += 6;
  dibujarDigito(x, hora % 10);    x += 6;
  if (mostrarPuntos) {
    if (x >= 0 && x < 32)   pantalla[x]   = 0x18;
    if (x+1 >= 0 && x+1 < 32) pantalla[x+1] = 0x18;
  }
  x += 3;
  dibujarDigito(x, minuto / 10);  x += 6;
  dibujarDigito(x, minuto % 10);

  int secBar = (int)((unsigned long)segundo * 31 / 59);
  for (int i = 0; i <= secBar && i < 32; i++)
    pantalla[i] |= 0x80;
}

void dibujarTemperatura(unsigned long t) {
  limpiarPantalla();

  float temp = temperatura;
  bool neg = temp < 0;
  if (neg) temp = -temp;

  int tempX10 = (int)(temp * 10 + 0.5);
  int parteEntera = tempX10 / 10;
  int parteDecimal = tempX10 % 10;

  int numDig = (parteEntera >= 10) ? 2 : 1;
  int totalW = numDig * 6 + 2 + 6 + 4 + 5;
  if (neg) totalW += 6;
  int startX = (32 - totalW) / 2;
  if (startX < 0) startX = 0;

  int x = startX;
  if (neg) { dibujarLetra(x, '-'); x += 6; }
  if (numDig == 2) { dibujarDigito(x, parteEntera / 10); x += 6; }
  dibujarDigito(x, parteEntera % 10); x += 6;
  if (x >= 0 && x < 32) pantalla[x] = 0x40;
  x += 2;
  dibujarDigito(x, parteDecimal); x += 6;
  dibujarGrado(x); x += 4;
  dibujarLetra(x, 'C');
}

const byte pmSpr[3][8] = {
  {0x3C,0x7E,0xFF,0xFF,0xFF,0xFF,0x7E,0x3C},
  {0x3C,0x7E,0xFF,0xFF,0xFF,0xE7,0x63,0x00},
  {0x3C,0x7E,0xFF,0xFF,0xC3,0x00,0x00,0x00}
};

const byte ghostSpr[8] = {0x7C,0xBE,0x77,0x3F,0x77,0xBF,0x7E,0x00};

int pmX = 0;
int pmDir = 1;
int pmBoca = 0;
int ghostPosX = 28;

void dibujarPacman(unsigned long t) {
  static unsigned long lastMove = 0;
  static unsigned long lastBoca = 0;

  if (t - lastBoca > 250) { lastBoca = t; pmBoca = (pmBoca + 1) % 3; }
  if (t - lastMove > 150) {
    lastMove = t;
    pmX += pmDir;
    if (pmX > 30) pmDir = -1;
    if (pmX < -2) pmDir = 1;
    ghostPosX -= 1;
    if (ghostPosX < -8) ghostPosX = 32;
  }

  limpiarPantalla();

  for (int i = 0; i < 32; i += 3) {
    bool covered = (i >= pmX && i < pmX + 8) || (i >= ghostPosX && i < ghostPosX + 8);
    if (!covered) pantalla[i] = 0x18;
  }

  for (int i = 0; i < 8; i++) {
    int x = pmX + i;
    if (x >= 0 && x < 32) pantalla[x] = pmSpr[pmBoca][i];
  }

  for (int i = 0; i < 8; i++) {
    int x = ghostPosX + i;
    if (x >= 0 && x < 32) pantalla[x] |= ghostSpr[i];
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(CS_PIN, OUTPUT);
  digitalWrite(CS_PIN, HIGH);
  SPI.begin();
  SPI.setFrequency(10000000);
  SPI.setDataMode(SPI_MODE0);

  for (int i = 0; i < 4; i++) {
    max7219_send(0x0F, 0x00, i);
    max7219_send(0x0B, 0x07, i);
    max7219_send(0x0A, 0x08, i);
    max7219_send(0x0C, 0x01, i);
    max7219_send(0x09, 0x00, i);
  }
  limpiarPantalla();
  actualizarPantalla();

  WiFi.begin(ssid, password);
  int intentos = 0;
  while (WiFi.status() != WL_CONNECTED && intentos < 30) { delay(500); intentos++; }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi OK");
    configTime(-10800, 0, "pool.ntp.org", "time.nist.gov");
    int retries = 0;
    while (!getLocalTime(&timeinfo) && retries < 20) { delay(500); retries++; }
    if (retries < 20) {
      hora = timeinfo.tm_hour;
      minuto = timeinfo.tm_min;
      segundo = timeinfo.tm_sec;
      Serial.printf("Hora NTP: %02d:%02d:%02d\n", hora, minuto, segundo);
    }

    HTTPClient http;
    http.begin("http://api.open-meteo.com/v1/forecast?latitude=-40.82&longitude=-63.00&current_weather=true");
    http.setTimeout(5000);
    int code = http.GET();
    if (code > 0) {
      String payload = http.getString();
      char resp[512];
      payload.toCharArray(resp, 512);
      char *pw = strstr(resp, "\"current_weather\":{");
      if (pw) {
        char *p = strstr(pw, "\"temperature\":");
        if (p) temperatura = atof(p + 14);
      }
      Serial.printf("Temp: %.1f\n", temperatura);
    }
    http.end();
  } else {
    Serial.println("Sin WiFi");
    hora = 12; minuto = 0;
  }

  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
  anteriorMillis = millis();
  ultimoCambioModo = millis();
}

void loop() {
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

  if (actualMillis - ultimoSync >= intervaloSync) resyncTime();

  if (actualMillis - ultimoCambioModo > intervaloModo) {
    modoActual = (Modo)((modoActual + 1) % 3);
    ultimoCambioModo = actualMillis;
    animFrame = 0;
  }

  limpiarPantalla();
  switch (modoActual) {
    case RELOJ:       dibujarReloj(); break;
    case TEMPERATURA: dibujarTemperatura(actualMillis); break;
    case PACMAN:      dibujarPacman(actualMillis); break;
  }
  actualizarPantalla();

  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'r') { modoActual = RELOJ; ultimoCambioModo = actualMillis; }
    if (c == 't') { modoActual = TEMPERATURA; ultimoCambioModo = actualMillis; }
    if (c == 'p') { modoActual = PACMAN; ultimoCambioModo = actualMillis; }
    if (c == 'h') { hora = (hora + 1) % 24; }
    if (c == 'm') { minuto = (minuto + 1) % 60; }
  }
}

void resyncTime() {
  WiFi.begin(ssid, password);
  int intentos = 0;
  while (WiFi.status() != WL_CONNECTED && intentos < 10) { delay(500); intentos++; }
  if (WiFi.status() == WL_CONNECTED) {
    configTime(-10800, 0, "pool.ntp.org", "time.nist.gov");
    int retries = 0;
    while (!getLocalTime(&timeinfo) && retries < 10) { delay(500); retries++; }
    if (retries < 10) {
      hora = timeinfo.tm_hour;
      minuto = timeinfo.tm_min;
      segundo = timeinfo.tm_sec;
    }

    HTTPClient http;
    http.begin("http://api.open-meteo.com/v1/forecast?latitude=-40.82&longitude=-63.00&current_weather=true");
    http.setTimeout(5000);
    if (http.GET() > 0) {
      String payload = http.getString();
      char resp[512];
      payload.toCharArray(resp, 512);
      char *pw = strstr(resp, "\"current_weather\":{");
      if (pw) {
        char *p = strstr(pw, "\"temperature\":");
        if (p) temperatura = atof(p + 14);
      }
    }
    http.end();
  }
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
  ultimoSync = millis();
}
