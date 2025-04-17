# Szakdolgozat Raspberry Pi(Hardware) part

> [!IMPORTANT]
>  - First Hatching started at 2025-02-21 18:07:59 
>  - Hatching ended at 2025-03-15 15:30:16
>  - Result: 0 kikelés

> [!IMPORTANT]
>  - Second Hatching started at 2025-03-24 17:46:28
>  - Hatching ended at 2025-04-15 10:55:33
>  - Result: 0 kikelés, 2 viszont fejlődött

> [!IMPORTANT]
> LED Color Code

- Lid open: red
- Heating element on: green
- Cooler on: white
- DC motor on: yellow
- Raspi on: cold white
- Other: -

# Preparing

<img src="sketches/images/hw_sys_image.png" />

# Hardware Wiring

## All Hardware

<img src="sketches/images/overall-wiring_image.png" alt="all hardware wiring image"/>

## Hardware with Relay

<img src="sketches/images/all_hw_with_relay_image.png" alt="all hw with relay" />

## AHT20 wiring

> [!NOTE]
> Required hardware

- Raspberry Pi 4 model B
- Breadboard
- Adafruit T-Cobbler
- 1x Adafruit AHT20 Temperature and Humidity Sensor
- 4x Male-Male Wire

<img src="sketches/images/aht20-temp-hum-sensor-wiring_image.png" alt="AHT20 wiring" />

## Limit Switch wiring

> [!NOTE]
> Required hardware

- Raspberry Pi 4 model B
- 1x V-156-1C25 Limit Switch
- 2x Male-Female Wire

<img src="sketches/images/limit-switch-wiring_image.png" alt="V-156-1C25 Limit Switch wiring" />

## Fan with Relay wiring

> [!NOTE]
> Required hardware

- Raspberry Pi 4 model B
- Breadboard
- Adafruit T-Cobbler (or, connect directly to ras-pi)
- 1x 5V Fan
- 1x Relay (4 relay module)
- 6x Male-Male wire

<img src="sketches/images/relay-and-fan-wiring_image.png" alt="Fan with Relay wiring" />

## Heating Element with Relay wiring

> [!NOTE]
> Required hardware

- Raspberry Pi 4 model B
- Breadboard
- Adafruit T-Cobbler (or, connect directly to ras-pi)
- 1x Heating Element (12V, 110℃)
- 1x 12V Adapter (12V*2A)
- 1x Relay (4 relay module)
- 4x Male-Male Wire

<img src="sketches/images/heating-element-and-relay-wiring_image.png" alt="Heating Element with Relay wiring" />

## DC Engine wiring

> [!NOTE]
> Required hardware

- Raspberry Pi 4 model B
- Breadboard
- Adafruit T-Cobbler (or, connect directly to ras-pi)
- 1x DC Engine (12V, 75RPM)
- 1x 12V Adapter (12V*1A)
- 1x L298N Dual H-Bridge Motor Driver
- 8x Wire

<img src="sketches/images/dc-engine-wiring_image.png" alt="DC Engine wiring" />

## LED Panel wiring

> [!NOTE]
> Required hardware

- Raspberry Pi 4 model B
- Breadboard
- Adafruit T-Cobbler (or, connect directly to ras-pi)
- 5 LED (Red, Green, White, Yellow, Cold White)
- 7x Wire

<img src="sketches/images/led-panel-wiring_image.png" alt="LED Panel wiring" />