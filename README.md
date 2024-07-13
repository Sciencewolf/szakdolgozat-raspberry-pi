# Szakdolgozat Raspberry Pi(Hardware) part

## Getting Started

```shell
git clone https://github.com/Sciencewolf/szakdolgozat-raspberry-pi.git
```

```shell
cd szakdolgozat-raspberry-pi
docker build -t webapp .
```

- Wait to install all dependencies

```shell
docker run -it -p 8080:8080 webapp
```

> Visit ```http://<raspberry_pi_ip_address>:8080/```

## RGB LED and AHT20 wiring

> [!NOTE]
> Hardware used in breadboard

> - Raspberry Pi 4 model B
> - Breadboard
> - Adafruit T-Cobbler
> - 3x Resistor 330R
> - 1x RGB LED 
> - 1x Adafruit AHT20 Temperature and Humidity Sensor
> - 8x Male-Male Wire

<img src="sketches/rgb-led-aht20-temp-hum-sensor-wiring_image.png" alt="wiring" />
