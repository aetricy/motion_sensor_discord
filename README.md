# Motion Sensor Discord Bot Project

This project is an IoT application that uses NodeMCU and a motion sensor to detect motion and send notifications to the user through a Discord bot. It also allows the user to control the motion sensor through Discord.

## Features

- Motion detection using NodeMCU and a HC-SR04 Ultrasonic Distance sensor.
- Sending notifications to a specified Discord channel when motion is detected.
- Controlling the motion sensor through a Discord bot.

## Requirements

To use this project, you will need the following components:

- NodeMCU ESP8266.
- HC-SR04 Ultrasonic Distance sensor.
- Breadboard and jumper wires.
- USB cable for programming the NodeMCU.
- Discord bot token (obtained from the Discord Developer Portal).

## Connections

To connect the motion sensor to NodeMCU, make the following connections:

- Sensor VCC pin -> NodeMCU 3.3V pin.
- Sensor GND pin -> NodeMCU GND pin.
- Sensor TRIG pin -> NodeMCU D1 (GPIO 5) pin.
- Sensor ECHO pin -> NodeMCU D2 (GPIO 4) pin.

For more details and a connection diagram, refer to the [connections.md](./connections.md) file.

## Setup

1. Program the NodeMCU using a suitable Arduino IDE or NodeMCU programming software. You can use `client/nodemcu/nodemcu.ino` to upload the code.
2. Replace "WIFI_SSID" with your Wi-Fi network name (SSID) and "WIFI_PASSWORD" with your Wi-Fi password in `client/nodemcu/nodemcu.ino`.
3. Create a Discord bot and obtain its token in [Discord Portal](https://discord.com/developers/docs/intro). Add the token by filling in the appropriate field in `server/discord_bot.py`.
4. Install the required Python packages by running the following command in the project directory:
- python = 3.8.10
- discord.py = 2.3.1
- beautifulsoup4 = 4.12.2
- requests = 2.22.0

To install python packages


```bash
  chmod +x start.sh
  sudo ./start.sh
```


## Documentation

[discord.py Documentation](https://discordpy.readthedocs.io/en/stable/)

[Nodemcu ESP8266 Documentation](https://tttapa.github.io/ESP8266/Chap10%20-%20Simple%20Web%20Server.html)

