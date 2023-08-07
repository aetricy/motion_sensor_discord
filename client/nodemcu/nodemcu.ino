//Library
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

#include "secrets.h"

//Pin Define
#define trigger D1
#define echo D2
#define alarmLed D3
#define toggleLed 2


unsigned long firstTime, timer, lastTime = 0;
long distance, temp = 0;
const long delayTime = 500;

int alarm = 0;
bool work = false;



ESP8266WebServer server(255);

void setup() {
  Serial.begin(115200);
  delay(100);


  // WiFi Connection
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  IPAddress ip(192, 168, 1, 254);
  IPAddress gateway(192, 168, 1, 1);
  IPAddress subnet(255, 255, 255, 0);
  WiFi.config(ip, gateway, subnet);
  delay(3000);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }
  Serial.println(WiFi.localIP());

  //HTTP Setup
  server.on("/", handle_OnConnect);
  server.on("/reset", handle_reset);
  server.on("/toggle", handle_toggle);
  server.on("/status", handle_status);

  server.onNotFound(handle_NotFound);
  server.begin();

  // Pin Configs
  pinMode(alarmLed, OUTPUT);
  pinMode(toggleLed, OUTPUT);
  pinMode(echo, INPUT);
  pinMode(trigger, OUTPUT);
  digitalWrite(alarmLed, LOW);
  digitalWrite(toggleLed, LOW);
}
void handle_NotFound() {
  server.send(200, "text/plain", "Not Found");
}

void handle_OnConnect() {
  server.send(200, "text/html", SendHTML(distance, alarm));
}

void handle_reset() {
  server.sendHeader("Location", "/");
  alarm = 0;
  server.send(303);
}
void handle_status() {
  server.send(200, "text/xml", SendXML(distance, alarm, work));
}

void handle_toggle() {
  server.sendHeader("Location", "/");

  if (work) {
    alarm = 0;
    distance = 0;
    work = false;
  } else {
    alarm = 0;
    distance = 0;
    work = true;
  }
  server.send(303);
}

void loop() {

  // Server Setup
  server.handleClient();

  if (work) {
    digitalWrite(toggleLed, HIGH);
    firstTime = millis();
    if (firstTime - lastTime >= delayTime) {

      digitalWrite(trigger, LOW);
      delayMicroseconds(2);
      digitalWrite(trigger, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigger, LOW);
      timer = pulseIn(echo, HIGH);
      distance = (timer / 2) / 29.1;

      if (distance < temp - 40 && alarm == 0) {
        alarm = 1;

      } else {
        temp = distance;
      }
      if (alarm == 1) {
        digitalWrite(alarmLed, HIGH);
      } else digitalWrite(alarmLed, LOW);


      lastTime = millis();
    }
  } else {
    digitalWrite(toggleLed, LOW);
    digitalWrite(alarmLed, LOW);
  }
}

String SendHTML(long value, int alarm) {
  String ptr = "<!DOCTYPE html>\n";
  ptr += "<head><meta http-equiv='refresh' content='30'><meta charset='UTF-8'><meta http-equiv='X-UA-Compatible' content='IE=edge'><meta http-equiv='refresh' content=2; URL='/' /><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>MEASUREMENT</title>";
  ptr += "</head><body><h1>Movement Sensor</h1>";
  ptr += "<p>Distance: ";
  ptr += int(value);
  ptr += " cm</p><p class='alarm'>Alarm: ";
  ptr += alarm;
  ptr += "</p><a href='/reset'>Alarm Reset</a><a>    </a><a href='/toggle'>TOGGLE</a></body>";

  return ptr;
}
String SendXML(long distance, long alarm, bool work) {
  String ptr = "<?xml version='1.0' encoding='utf-8'?><stats><ds>";
  ptr += distance;
  ptr += "</ds><al>";
  ptr += alarm;
  ptr += "</al><wk>";
  if (work) {
    ptr += "1";
  } else {
    ptr += "0";
  }
  ptr += "</wk></stats>";

  return ptr;
}
